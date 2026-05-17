# VisionInspect - State of the Project

## 🏗️ Completed Infrastructure
1. **AI Brain (/brain)**:
   - CIE Lab Preprocessing Logic.
   - YOLOv8 Real-time Detection Training Script.
   - U-Net Segmentation Training Script with MobileNetV2 backbone.
   - INT8/FP16 TFLite Conversion & Quantization Suite.

2. **Android Application (/mobile)**:
   - **MVVM Architecture** structure.
   - **CameraX** implementation for real-time inference on the edge.
   - **TFLite Wrappers** for YOLO and U-Net models.
   - **SQLite/Room Persistence** for offline inspection history.
   - **GPS Auto-tagging** functionality.
   - **Automated PDF Report Generator** using iText7.
   - **UI Layout** with camera preview and live severity grading.

## 🛠️ Next Steps
- **Model Training**: Collect your dataset and run `python brain/scripts/train_yolo.py`.
- **Hardware Integration**: For Phase 2/3 (LiDAR & Drones), replace CameraX with the device's specific SDK in the `ui/camera` module.
- **Field Calibration**: Adjust the `a*` and `b*` thresholds in `ImagePreprocessor.kt` based on real-world lighting conditions in your specific environment.

## 📊 Deployment Target
- **Devices**: Mid-range Android smartphones (Min RAM: 6GB).
- **Inference Time**: Targeted under 1s for both detection + segmentation combined.
- **Deployment**: APK can be distributed via private MDM for inspector field testing.

Project is ready for **Phase 1: AI Model Training + Validation**.
