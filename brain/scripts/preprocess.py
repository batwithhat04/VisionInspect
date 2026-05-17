import cv2
import numpy as np

def rgb_to_cielab_enhancement(image_path):
    """
    Converts RGB to CIE Lab and enhances channels for corrosion/seepage detection.
    
    Why CIE Lab?
    - Rust (corrosion) is highly distinctive in the 'a*' (green-red) channel.
    - Seepage/Efflorescence often affects the 'b*' (blue-yellow) channel.
    - Luminance 'L' is decoupled, making it more robust to lighting variations.
    """
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found")
        
    # Convert RGB to CIE Lab
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)
    l_channel, a_channel, b_channel = cv2.split(lab_image)
    
    # 1. Enhance 'a*' channel for Rust (Reddish tones)
    # Rust typically has high 'a*' values. We can apply CLAHE or simple scaling.
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    enhanced_a = clahe.apply(a_channel)
    
    # 2. Enhance 'b*' channel for Efflorescence (Yellowish/Salts)
    enhanced_b = clahe.apply(b_channel)
    
    # 3. Enhance 'L' channel for better contrast in dark corners
    enhanced_l = clahe.apply(l_channel)
    
    # Merge back
    enhanced_lab = cv2.merge([enhanced_l, enhanced_a, enhanced_b])
    
    # Convert back to BGR for inspection or YOLO training input
    enhanced_bgr = cv2.cvtColor(enhanced_lab, cv2.COLOR_Lab2BGR)
    
    return enhanced_bgr

if __name__ == "__main__":
    # Example usage
    # result = rgb_to_cielab_enhancement("test_rust.jpg")
    # cv2.imwrite("enhanced_rust.jpg", result)
    print("Preprocessing module ready.")
