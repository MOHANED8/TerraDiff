import cv2
import numpy as np
from PIL import Image
import torch
import torchvision.transforms as T

# Optional: GeoTIFF support
try:
    import rasterio
    HAS_RASTERIO = True
except ImportError:
    HAS_RASTERIO = False


def read_image(path):
    """Read an image from path. Supports standard formats and GeoTIFF if rasterio is available."""
    ext = path.lower().split('.')[-1]
    if ext in ['tif', 'tiff'] and HAS_RASTERIO:
        with rasterio.open(path) as src:
            img = src.read([1,2,3])  # RGB bands
            img = np.transpose(img, (1,2,0))
            img = np.clip(img, 0, 255).astype(np.uint8)
        return img
    else:
        img = Image.open(path).convert('RGB')
        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)


def align_images_feature_based(img1, img2):
    """Align img2 to img1 using ORB feature matching and homography."""
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    orb = cv2.ORB_create(5000)
    kp1, des1 = orb.detectAndCompute(gray1, None)
    kp2, des2 = orb.detectAndCompute(gray2, None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)
    if len(matches) > 10:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
        M, mask = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, 5.0)
        h, w = img1.shape[:2]
        img2_aligned = cv2.warpPerspective(img2, M, (w, h))
        return img1, img2_aligned
    else:
        h, w = img1.shape[:2]
        img2_resized = cv2.resize(img2, (w, h))
        return img1, img2_resized


def detect_differences(img1, img2, threshold=30, min_area=500):
    """Classical difference detection using thresholded absolute difference and contour filtering."""
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(gray1, gray2)
    _, thresh = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
    kernel = np.ones((5,5), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.zeros_like(gray1)
    for cnt in contours:
        if cv2.contourArea(cnt) > min_area:
            cv2.drawContours(mask, [cnt], -1, 255, -1)
    return mask


def overlay_changes(img, mask, color=(0,0,255), alpha=0.5):
    """Overlay the binary mask on the image with a given color and transparency."""
    overlay = img.copy()
    overlay[mask==255] = color
    return cv2.addWeighted(overlay, alpha, img, 1-alpha, 0)

# --- Deep Learning Model ---
class SimpleUNet(torch.nn.Module):
    """A simple U-Net architecture for binary change detection."""
    def __init__(self, in_channels=6, out_channels=1):
        super().__init__()
        self.encoder = torch.nn.Sequential(
            torch.nn.Conv2d(in_channels, 16, 3, padding=1),
            torch.nn.ReLU(),
            torch.nn.Conv2d(16, 32, 3, padding=1),
            torch.nn.ReLU(),
        )
        self.decoder = torch.nn.Sequential(
            torch.nn.Conv2d(32, 16, 3, padding=1),
            torch.nn.ReLU(),
            torch.nn.Conv2d(16, out_channels, 1),
            torch.nn.Sigmoid(),
        )
    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x

def load_unet_model(weights_path=None, device='cpu'):
    """Load a simple U-Net model. If weights_path is None, returns an untrained model."""
    model = SimpleUNet()
    if weights_path:
        model.load_state_dict(torch.load(weights_path, map_location=device))
    model.eval()
    model.to(device)
    return model

def detect_differences_deep(img1, img2, model, device='cpu'):
    """Deep learning-based change detection using a PyTorch model."""
    transform = T.Compose([
        T.ToPILImage(),
        T.Resize((256, 256)),
        T.ToTensor(),
    ])
    t1 = transform(img1)
    t2 = transform(img2)
    inp = torch.cat([t1, t2], dim=0).unsqueeze(0).to(device)  # (1, 6, H, W)
    with torch.no_grad():
        out = model(inp)
        mask = (out.squeeze().cpu().numpy() > 0.5).astype(np.uint8) * 255
        mask = cv2.resize(mask, (img1.shape[1], img1.shape[0]))
    return mask 