import tensorflow as tf
import os

def convert_h5_to_tflite(h5_model_path, tflite_output_path, quantization="int8", representative_dataset=None):
    """
    Converts a Keras .h5 model (U-Net) to TFLite with optional quantization.
    
    Quantization Options:
    - 'fp16': reduces size by ~2x, maintains accuracy well.
    - 'int8': reduces size by ~4x, significantly faster on mobile DSPs but 
      requires representative dataset for calibration.
    """
    model = tf.keras.models.load_model(h5_model_path)
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    
    # Enable transformations to optimize TFLite graph
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    
    if quantization == "fp16":
        converter.target_spec.supported_types = [tf.float16]
    elif quantization == "int8":
        if representative_dataset is None:
            raise ValueError("Representative dataset needed for INT8 quantization")
        converter.representative_dataset = representative_dataset
        # Force operations to be INT8 (for NPU compatibility)
        converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
        converter.inference_input_type = tf.uint8
        converter.inference_output_type = tf.uint8
    
    tflite_model = converter.convert()
    
    # Save model
    with open(tflite_output_path, 'wb') as f:
        f.write(tflite_model)
    
    print(f"Model successfully saved to: {tflite_output_path}")
    print(f"File size: {os.path.getsize(tflite_output_path) / (1024*1024):.2f} MB")

def convert_pt_to_tflite_yolo(onnx_path, output_tflite):
    """
    Note: For YOLOv8, the standard path is Exporting to ONNX then using onnx2tf 
    or using native Export from YOLOv8: model.export(format='tflite', int8=True)
    
    Example command (using ultralytics):
    yolo export model=yolov8n.pt format=tflite int8=True
    """
    print("For YOLOv8, use native ultralytics export:")
    print(f"yolo export model={onnx_path} format=tflite")

if __name__ == "__main__":
    print("TFLite Conversion Script ready.")
    # Example Conversion (commented for now)
    # convert_h5_to_tflite('brain/models/unet_damage.h5', 'brain/models/unet_damage_int8.tflite')
