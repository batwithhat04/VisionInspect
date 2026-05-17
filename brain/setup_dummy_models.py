import os
import shutil
import tensorflow as tf

BRAIN_DIR = os.path.dirname(os.path.abspath(__file__))
MOBILE_ASSETS_DIR = os.path.join(os.path.dirname(BRAIN_DIR), "mobile", "app", "src", "main", "assets")

def generate_dummy_yolo_tflite():
    print("Generating pure mock YOLO TFLite (Shape: 1x640x640x3 -> 1x6x8400)...")
    inputs = tf.keras.layers.Input(shape=(640, 640, 3))
    # Dummy operation to get the right shape
    x = tf.keras.layers.GlobalAveragePooling2D()(inputs)
    x = tf.keras.layers.Dense(6 * 8400)(x)
    outputs = tf.keras.layers.Reshape((6, 8400))(x)
    
    model = tf.keras.Model(inputs=inputs, outputs=outputs)
    
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()
    
    tflite_path = os.path.join(BRAIN_DIR, "yolov8.tflite")
    with open(tflite_path, "wb") as f:
        f.write(tflite_model)
    return tflite_path

def generate_dummy_unet_tflite():
    print("Generating pure mock U-Net TFLite (Shape: 1x224x224x3 -> 1x224x224x2)...")
    inputs = tf.keras.layers.Input(shape=(224, 224, 3))
    # Dummy operation: compress then decompress to the required shape
    x = tf.keras.layers.Conv2D(2, (1, 1), padding='same', activation='softmax')(inputs)
    
    model = tf.keras.Model(inputs=inputs, outputs=x)
    
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()
    
    tflite_path = os.path.join(BRAIN_DIR, "unet.tflite")
    with open(tflite_path, "wb") as f:
        f.write(tflite_model)
    return tflite_path

def main():
    yolo_tflite = generate_dummy_yolo_tflite()
    unet_tflite = generate_dummy_unet_tflite()
    
    os.makedirs(MOBILE_ASSETS_DIR, exist_ok=True)
    dest_yolo = os.path.join(MOBILE_ASSETS_DIR, "yolov8.tflite")
    dest_unet = os.path.join(MOBILE_ASSETS_DIR, "unet.tflite")
    
    shutil.copy(yolo_tflite, dest_yolo)
    shutil.copy(unet_tflite, dest_unet)
    
    print("\n" + "="*50)
    print("✅ SUCCESS! Mock models generated and deployed.")
    print(f"YOLO model copied to: {dest_yolo}")
    print(f"U-Net model copied to: {dest_unet}")
    print("You can now run Phase 2 without TensorFlow version conflicts!")
    print("="*50 + "\n")

if __name__ == "__main__":
    main()
