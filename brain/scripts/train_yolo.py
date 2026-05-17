import os
from ultralytics import YOLO

def train_vision_inspect_yolo(data_config_path="data/vision_inspect.yaml"):
    """
    Trains YOLOv8 nano model for Detection of Corrosion and Seepage.
    
    Why YOLOv8n?
    - Extremely low latency (40+ FPS) on mobile devices.
    - Small footprint (< 10MB).
    - Excellent balance between speed and precision.
    """
    model = YOLO("yolov8n.pt")  # Start with nano version for mobile
    
    # Train
    results = model.train(
        data=data_config_path,
        epochs=100,
        imgsz=640,
        batch=16,
        device="0",  # Use GPU if available
        name="vision_inspect_detection",
        # Data Augmentations
        degrees=15,  # Rotation
        brightness=0.2,
        hsv_s=0.5,
        hsv_v=0.4,
        scale=0.5,
        translate=0.1,
        fliplr=0.5,
        mosaic=1.0  # Crucial for small object detection like seepage patches
    )
    
    # Export to ONNX first
    model.export(format="onnx")
    
    return model

if __name__ == "__main__":
    # Note: Requires ultralytics package: pip install ultralytics
    # Requires a vision_inspect.yaml defining paths and classes ['Corrosion', 'Seepage']
    print("YOLOv8 Training script ready.")
    # train_vision_inspect_yolo()
