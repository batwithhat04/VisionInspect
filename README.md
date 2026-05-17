# VisionInspect – AI-Powered Seepage & Corrosion Detection

VisionInspect is a production-grade infrastructure inspection system designed to detect and quantify corrosion and seepage on structural assets using standard smartphones.

## 🚀 Key Features
- **Real-time Edge AI Detection (YOLOv8)**: Instant identification of damage regions.
- **Pixel-level Segmentation (U-Net)**: Precise mapping of damaged areas.
- **Severity Grading**: Automatic classification into Minor (<5%), Moderate (5–20%), and Critical (>20%) damage.
- **Offline Capabilities**: Full on-device inference using TensorFlow Lite with INT8 quantization.
- **GPS Auto-tagging**: Integrated location services for asset tracking.
- **Automated PDF Reports**: On-the-fly generation of detailed inspection logs with images and recommendations.

## 🏗️ Technical Architecture
### AI Pipeline
1. **CIE Lab Preprocessing**: Enhances rust (a* channel) and efflorescence (b* channel) detection.
2. **YOLOv8 Nano**: Detection of objects with high frame rate on mobile.
3. **U-Net + MobileNetV2**: Efficient pixel-wise mask prediction for quantifying surface area.
4. **Quantization (INT8/FP16)**: Drastic reduction in model size and latency for edge execution.

### Mobile Stack
- **Platform**: Android (Kotlin)
- **Framework**: CameraX for low-latency image stream.
- **Local Storage**: Room (SQLite) for offline history.
- **Design Pattern**: MVVM (Model-View-ViewModel) for clean, maintainable code.

## 📂 Project Structure
- `/brain`: Python scripts for model training (YOLOv8/U-Net) and TFLite conversion.
- `/mobile`: Android application source code implementing the AI pipeline.
- `/docs`: PDF templates and architecture diagrams.

## 🛠️ Setup Instructions
### Training Edge Models
1. Navigate to `/brain`.
2. Install dependencies: `pip install -r requirements.txt`. (Requires `ultralytics`, `tensorflow`, `segmentation-models`)
3. Train Detection: `python scripts/train_yolo.py`.
4. Train Segmentation: `python scripts/train_unet.py`.
5. Convert for Mobile: `python scripts/convert.py --quantization int8`.

### Installing the App
1. Open `/mobile` in **Android Studio**.
2. Place exported `.tflite` models in `app/src/main/assets`.
3. Build and Run on a mid-range Android device (6GB+ RAM).

## 📄 License
This project is for industrial infrastructure inspection and asset management.

## 📞 Support
Developed as an AI-first inspection tool for civil engineering.
