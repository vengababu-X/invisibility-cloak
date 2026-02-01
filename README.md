<p align="center">
  <img src="assets/banner.gif" width="100%">
</p>

<h1 align="center">🧥 Universal Invisibility Cloak++</h1>

<p align="center">
  <b>A real-time adaptive computer vision system that makes ANY selected color invisible</b><br>
  <i>Built with OpenCV, NumPy, and optional ML segmentation</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/OpenCV-Computer%20Vision-green">
  <img src="https://img.shields.io/badge/Python-3.x-blue">
  <img src="https://img.shields.io/badge/Mode-Real--Time-orange">
</p>

---

## ✨ Project Preview (Animation)

<p align="center">
  <img src="assets/demo.gif" width="80%">
</p>

> The system dynamically removes the selected clothing color and replaces it with a reconstructed background in real time.

---

## 🚀 What Makes This Project Special

✔ Works with **any color**  
✔ No hard-coded HSV ranges  
✔ Handles **mixed fabrics & lighting changes**  
✔ Motion-aware background reconstruction  
✔ Multiple segmentation modes  
✔ Smooth edges with alpha blending  
✔ Runs on normal webcam (CPU only)

This is **not a YouTube trick**.  
This is an **adaptive vision system**.

---

## 🧠 System Architecture (Animated Flow)

<p align="center">
  <img src="assets/architecture.gif" width="85%">
</p>

---

## 🎛️ Supported Modes

| Mode | Description |
|----|----|
| HSV | Adaptive color detection (fast) |
| K-Means | Handles patterned / mixed fabrics |
| ML | Color-independent human segmentation |

Switch modes **live** while running.

---

## 🛠️ Tech Stack

- Python 3.x
- OpenCV
- NumPy
- MediaPipe (optional ML segmentation)

No GPU required.

---

## 📦 Installation

```bash
pip install opencv-python numpy mediapipe

▶️ How to Run
python invisibility_cloak.py

📂 Suggested Folder Structure
📁 invisibility-cloak
 ┣ 📁 assets
 ┃ ┣ banner.gif
 ┃ ┣ demo.gif
 ┃ ┣ architecture.gif
 ┃ ┣ background.gif
 ┃ ┗ motion.gif
 ┣ invisibility_cloak.py
 ┗ README.md
```
## 🧠 OpenCV Usage (Core of the Project)

This project is built **primarily on OpenCV**.  
All real-time vision, masking, blending, and motion detection are implemented using OpenCV APIs.

### Key OpenCV Functions Used
```
| Purpose | OpenCV API |
|------|-----------|
| Webcam capture | `cv2.VideoCapture` |
| Frame flipping | `cv2.flip` |
| Color space conversion | `cv2.cvtColor` |
| HSV masking | `cv2.inRange` |
| Morphological operations | `cv2.morphologyEx` |
| Noise removal | `cv2.GaussianBlur` |
| Motion detection | `cv2.absdiff`, `cv2.threshold` |
| Background blending | `cv2.addWeighted` (manual alpha blend) |
| K-Means clustering | `cv2.kmeans` |
| Real-time display | `cv2.imshow`, `cv2.waitKey` |
```
---

### Example: OpenCV-Based Masking & Blending

```python
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, lower, upper)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7))
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
mask = cv2.GaussianBlur(mask, (21,21), 0)

alpha = cv2.merge([mask/255]*3)
output = (alpha * background + (1 - alpha) * frame).astype(np.uint8)

---
```
### Optional one-line fix at the top (also recommended)

Replace this line near the top:

```markdown
Built with OpenCV, NumPy, and optional ML segmentation

Built primarily with OpenCV for real-time computer vision, with NumPy for math and optional ML-based segmentation

```
Thank you.
