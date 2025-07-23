# 🛰️ Satellite Image Change Detection

![App Banner](images/banner.png)

A professional, modern web application for comparing satellite images taken at different time intervals and detecting significant changes—such as new structures, natural events, or land use changes. The app features a beautiful, animated interface and provides clear, actionable visualizations of detected differences.

---

## ✨ Features

- **Upload** two satellite images (before/after) via drag-and-drop or file picker
- **Automatic alignment** and resizing for robust comparison
- **Change detection** using classical (OpenCV) or deep learning (U-Net) methods
- **Animated, modern UI** with dark/light mode, progress spinners, and smooth transitions
- **Side-by-side comparison slider** for intuitive before/after analysis
- **Results gallery** with download and batch download options
- **Threshold slider** for sensitivity adjustment
- **Accessible and responsive** on all devices
- **One-click data cleanup**
- **In-app help modal** and professional documentation

---

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **(Optional) For GeoTIFF support:**
   ```bash
   pip install rasterio
   ```
3. **(Optional) For deep learning:**
   - Place your trained U-Net weights as `unet_weights.pth` in the project root.
4. **Run the app:**
   ```bash
   python app.py
   ```
5. **Open your browser at:**
   [http://localhost:5000](http://localhost:5000)

---

## 🖼️ How It Works (Visual Guide)

### 1. Upload Images
![Upload Animation](images/upload.gif)
- Drag and drop or select two satellite images (same area, different times).

### 2. Adjust Sensitivity & Compare
![Threshold Animation](images/threshold.gif)
- Use the threshold slider to adjust detection sensitivity.
- Click **Compare**. Enjoy the animated progress bar and spinner.

### 3. View Results & Use the Slider
![Comparison Slider](images/slider.gif)
- Instantly see detected changes overlaid on your images.
- Use the before/after slider for intuitive comparison.

### 4. Explore the Gallery & Download
![Gallery Animation](images/gallery.gif)
- All results are saved in a gallery with timestamps.
- Download individual or all results with one click.

### 5. Clean Up
![Delete Animation](images/delete.gif)
- Use the **Delete All Data** button to clear uploads and results.

---

## 🧠 Method & Approach

- **Image Alignment:** Feature-based (ORB) alignment and automatic resizing
- **Classical Detection:** Thresholded absolute difference and contour filtering
- **Deep Learning:** U-Net model for semantic change detection (optional, user-provided weights)
- **Visualization:** Overlay of detected changes, animated comparison slider, and gallery

---

## 📚 Documentation & Help
- Click the **?** button in the app for a quick “How it works” guide.
- All interactive elements have tooltips and ARIA labels for accessibility.
- For advanced usage, see code comments and the `utils.py` file.

---

## 🛠️ Customization
- To use your own deep learning model, update `utils.py` and place weights at `unet_weights.pth`.
- To support more formats, extend `read_image` in `utils.py`.
- For advanced geospatial alignment, integrate with GDAL or rasterio.

---

## 📸 Screenshots

| Upload & Compare | Animated Slider | Results Gallery |
|------------------|----------------|-----------------|
| ![upload](images/upload.png) | ![slider](images/slider.png) | ![gallery](images/gallery.png) |

---

## 👩‍💻 Authors & Credits
- Designed and developed by [Your Name/Team]
- UI icons by [Icons8](https://icons8.com/)
- Animations by [LottieFiles](https://lottiefiles.com/) (if used)

---

## 📄 License
MIT License. See [LICENSE](LICENSE) for details.

---

> **Tip:** Replace the images and GIFs in the `images/` folder with your own screenshots and screen recordings for a fully branded, professional README! 