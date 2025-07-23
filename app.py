from flask import Flask, render_template, request, redirect, url_for, send_file, flash
import os
import cv2
import numpy as np
from utils import read_image, align_images_feature_based, detect_differences, overlay_changes, detect_differences_deep, load_unet_model
from werkzeug.utils import secure_filename
import uuid
import glob

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULTS_FOLDER'] = 'results'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB upload limit
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'tif', 'tiff', 'bmp'}
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULTS_FOLDER'], exist_ok=True)

# Load deep learning model once
MODEL_PATH = 'unet_weights.pth'  # Place your trained weights here
try:
    deep_model = load_unet_model(MODEL_PATH)
except Exception:
    deep_model = None

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/delete_all', methods=['POST'])
def delete_all():
    """Delete all files in uploads/ and results/ folders and clear gallery session."""
    for folder in [app.config['UPLOAD_FOLDER'], app.config['RESULTS_FOLDER']]:
        files = glob.glob(os.path.join(folder, '*'))
        for f in files:
            try:
                os.remove(f)
            except Exception:
                pass
    flash('All uploaded and result images have been deleted.')
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def index():
    """Main page: upload images, select method, view results gallery."""
    result_img_path = None
    error = None
    if request.method == 'POST':
        try:
            file1 = request.files.get('image1')
            file2 = request.files.get('image2')
            method = request.form.get('method', 'classical')
            if not (file1 and file2 and allowed_file(file1.filename) and allowed_file(file2.filename)):
                flash('Please upload valid image files (png, jpg, jpeg, tif, tiff, bmp).')
                return redirect(request.url)
            fname1 = secure_filename(file1.filename)
            fname2 = secure_filename(file2.filename)
            path1 = os.path.join(app.config['UPLOAD_FOLDER'], str(uuid.uuid4()) + '_' + fname1)
            path2 = os.path.join(app.config['UPLOAD_FOLDER'], str(uuid.uuid4()) + '_' + fname2)
            file1.save(path1)
            file2.save(path2)
            img1 = read_image(path1)
            img2 = read_image(path2)
            # Automatically resize images to match if needed
            if img1.shape != img2.shape:
                h, w = img1.shape[:2]
                img2 = cv2.resize(img2, (w, h))
            img1, img2 = align_images_feature_based(img1, img2)
            if method == 'deep':
                if deep_model is None:
                    flash('Deep learning model not available. Please provide weights at unet_weights.pth.')
                    return redirect(request.url)
                mask = detect_differences_deep(img1, img2, model=deep_model)
            else:
                mask = detect_differences(img1, img2)
            result = overlay_changes(img2, mask)
            result_id = str(uuid.uuid4())
            result_path = os.path.join(app.config['RESULTS_FOLDER'], f'result_{result_id}.png')
            cv2.imwrite(result_path, result)
            result_img_path = url_for('result_file', filename=f'result_{result_id}.png')
            # Clean up uploaded files after processing
            try:
                os.remove(path1)
                os.remove(path2)
            except Exception:
                pass
        except Exception as e:
            flash(f'An error occurred: {str(e)}')
            return redirect(request.url)
    # Persistent gallery: list all results in the results folder
    gallery_imgs = []
    for f in sorted(os.listdir(app.config['RESULTS_FOLDER'])):
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tif', '.tiff', '.bmp')):
            gallery_imgs.append(url_for('result_file', filename=f))
    return render_template('index.html', result_img=result_img_path, gallery_imgs=gallery_imgs)

@app.route('/results/<filename>')
def result_file(filename):
    """Serve result images from the results folder."""
    return send_file(os.path.join(app.config['RESULTS_FOLDER'], filename))

@app.route('/download/<filename>')
def download_file(filename):
    """Download a result image."""
    return send_file(os.path.join(app.config['RESULTS_FOLDER'], filename), as_attachment=True)

# For production deployment, use a WSGI server like Gunicorn or uWSGI and set debug=False
if __name__ == '__main__':
    app.run(debug=False) 