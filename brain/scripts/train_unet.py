import os
import tensorflow as tf
from tensorflow.keras import layers, models, optimizers

def build_unet_segmentation_model(input_shape=(224, 224, 3)):
    """
    Builds a U-Net model with MobileNetV2 encoder for edge-optimal performance.
    
    Why U-Net with MobileNetV2?
    1. U-Net's encoder-decoder structure is perfect for pixel masks.
    2. MobileNetV2 replaces standard convolutions with depthwise separable ones,
       drastically reducing trainable parameters and latency.
    """
    # Encoder
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=input_shape, include_top=False, weights='imagenet'
    )
    
    # Use the activations of these layers for skip connections
    # MobileNetV2 typical feature extraction layers:
    layer_names = [
        'block_1_expand_relu',   # 112x112
        'block_3_expand_relu',   # 56x56
        'block_6_expand_relu',   # 28x28
        'block_13_expand_relu',  # 14x14
        'block_16_project',      # 7x7
    ]
    base_model_outputs = [base_model.get_layer(name).output for name in layer_names]

    encoder = tf.keras.Model(inputs=base_model.input, outputs=base_model_outputs)
    encoder.trainable = False

    # Decoder / Upsampling helper
    def upsample(filters, size):
        result = tf.keras.Sequential([
            layers.Conv2DTranspose(filters, size, strides=2, padding='same', use_bias=False),
            layers.BatchNormalization(),
            layers.ReLU()
        ])
        return result

    up_stack = [
        upsample(512, 3),  # 7x7 -> 14x14
        upsample(256, 3),  # 14x14 -> 28x28
        upsample(128, 3),  # 28x28 -> 56x56
        upsample(64, 3),   # 56x56 -> 112x112
    ]

    inputs = layers.Input(shape=input_shape)
    
    # Downsampling
    skips = encoder(inputs)
    x = skips[-1]
    skips = reversed(skips[:-1])

    # Upsampling
    for up, skip in zip(up_stack, skips):
        x = up(x)
        concat = layers.Concatenate()
        x = concat([x, skip])

    # Final classifier layer
    # classes=2, activation='softmax' matching original standard
    last = layers.Conv2DTranspose(
        filters=2, kernel_size=3, strides=2,
        padding='same', activation='softmax' 
    ) # 112x112 -> 224x224
    
    x = last(x)

    model = tf.keras.Model(inputs=inputs, outputs=x)
    
    model.compile(
        optimizer=optimizers.Adam(learning_rate=1e-4),
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
        # Or binary cross entropy if the mask is generated differently, but standard for 2 classes:
        metrics=['accuracy']
    )
    
    return model

def train_segmentation(train_images, train_masks):
    """
    Trains U-Net on Damage/Rust masks.
    """
    model = build_unet_segmentation_model()
    
    # Simple setup for training loop demonstration
    # In practice, use tf.data.Dataset for high performance with data augmentation
    model.fit(
        x=train_images,
        y=train_masks,
        batch_size=32,
        epochs=100,
        validation_split=0.2,
        callbacks=[
            tf.keras.callbacks.EarlyStopping(patience=10),
            tf.keras.callbacks.ModelCheckpoint('brain/models/unet_damage.keras', save_best_only=True)
        ]
    )
    
    return model

if __name__ == "__main__":
    print("U-Net Training Script ready.")
    # build_unet_segmentation_model().summary()
