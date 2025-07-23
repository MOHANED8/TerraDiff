# 🛰️ TerraDiff: Satellite Image Change Detection

<p align="center">
  <img width="1464" height="728" alt="Image" src="https://github.com/user-attachments/assets/a88661fb-4528-4e85-b68e-15b65fd34942" alt="App Banner" width="80%" />
</p>

**TerraDiff** is a cutting-edge web application for detecting and visualizing changes in satellite imagery over time. Effortlessly monitor structural, environmental, and geographical transformations with precision and style.

---

## ✨ Key Features

- 🚀 **Effortless Upload:** Drag & drop or select two satellite images (before/after) for instant analysis.
- 🧠 **Smart Alignment:** Automatic image alignment and resizing for robust, accurate comparison.
- 🔍 **Change Detection:** Choose between classical (OpenCV) or deep learning (U-Net) methods.
- 🎨 **Modern UI:** Beautiful, animated interface with dark/light mode, progress spinners, and smooth transitions.
- 🖼️ **Intuitive Comparison:** Side-by-side slider for seamless before/after analysis.
- 🗂️ **Results Gallery:** All results saved with timestamps; download individually or in batch.
- 🎚️ **Threshold Control:** Fine-tune detection sensitivity with an interactive slider.
- 📱 **Responsive & Accessible:** Works perfectly on all devices, with ARIA labels and tooltips.
- 🧹 **One-Click Cleanup:** Instantly clear uploads and results.
- 🆘 **In-App Help:** Built-in help modal and comprehensive documentation.

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

## 🖼️ Visual Workflow

### 1. Upload Images
<p align="center"><img src="images/upload.gif" alt="Upload Animation" width="60%"></p>
*Drag and drop or select two satellite images (same area, different times).*

### 2. Adjust Sensitivity & Compare
<p align="center"><img src="images/threshold.gif" alt="Threshold Animation" width="60%"></p>
*Use the threshold slider to adjust detection sensitivity. Click **Compare** and watch the magic happen!*

### 3. View Results & Use the Slider
<p align="center"><img src="images/slider.gif" alt="Comparison Slider" width="60%"></p>
*Instantly see detected changes overlaid on your images. Use the before/after slider for intuitive comparison.*

### 4. Explore the Gallery & Download
<p align="center"><img src="images/gallery.gif" alt="Gallery Animation" width="60%"></p>
*All results are saved in a gallery with timestamps. Download individual or all results with one click.*

### 5. Clean Up
<p align="center"><img src="images/delete.gif" alt="Delete Animation" width="60%"></p>
*Use the **Delete All Data** button to clear uploads and results.*

---

## 🧠 How It Works

- **Image Alignment:** Feature-based (ORB) alignment and automatic resizing.
- **Classical Detection:** Thresholded absolute difference and contour filtering.
- **Deep Learning:** U-Net model for semantic change detection (optional, user-provided weights).
- **Visualization:** Overlay of detected changes, animated comparison slider, and gallery.

---

## 📚 Documentation & Help

- Click the **?** button in the app for a quick “How it works” guide.
- All interactive elements have tooltips and ARIA labels for accessibility.
- For advanced usage, see code comments and the `utils.py` file.

---

## 🛠️ Customization

- **Custom Models:** Update `utils.py` and place your weights at `unet_weights.pth`.
- **Format Support:** Extend `read_image` in `utils.py` for more formats.
- **Advanced Alignment:** Integrate with GDAL or rasterio for geospatial alignment.

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

> **Pro Tip:** Replace the images and GIFs in the `images/` folder with your own screenshots and screen recordings for a fully branded, professional README!

---

**Suggestions for further improvement:**
- Add a live demo link or video walkthrough.
- Include badges (build, license, stars, etc.) at the top.
- Add a FAQ or Troubleshooting section if your users might need it.
- Use more icons/emojis for visual appeal (but keep it professional). 
