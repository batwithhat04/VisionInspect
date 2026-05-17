package com.visioninspect.utils

import android.graphics.*
import androidx.camera.core.ImageProxy
import java.io.ByteArrayOutputStream

/**
 * Utility class for common Image operations in VisionInspect.
 */
object ImageUtils {

    /**
     * Converts CameraX ImageProxy to Bitmap for AI inference.
     */
    fun imageProxyToBitmap(image: ImageProxy): Bitmap? {
        val planeProxy = image.planes[0]
        val buffer = planeProxy.buffer
        val bytes = ByteArray(buffer.remaining())
        buffer.get(bytes)
        
        val bitmap = BitmapFactory.decodeByteArray(bytes, 0, bytes.size) ?: return null
        
        // Rotate bitmap based on imageProxy orientation
        return if (image.imageInfo.rotationDegrees != 0) {
            val matrix = Matrix()
            matrix.postRotate(image.imageInfo.rotationDegrees.toFloat())
            Bitmap.createBitmap(bitmap, 0, 0, bitmap.width, bitmap.height, matrix, true)
        } else {
            bitmap
        }
    }

    /**
     * Resizes bitmap while maintaining aspect ratio or force-scaling to model input.
     */
    fun resizeForModel(bitmap: Bitmap, width: Int, height: Int): Bitmap {
        return Bitmap.createScaledBitmap(bitmap, width, height, true)
    }

    /**
     * Converts Bitmap to RGB FloatArray normalized [0, 1] for TFLite input.
     */
    fun bitmapToFloatArray(bitmap: Bitmap, width: Int, height: Int): FloatArray {
        val resized = resizeForModel(bitmap, width, height)
        val intValues = IntArray(width * height)
        resized.getPixels(intValues, 0, resized.width, 0, 0, resized.width, resized.height)
        
        val floatValues = FloatArray(width * height * 3)
        for (i in intValues.indices) {
            val val = intValues[i]
            floatValues[i * 3 + 0] = ((val shr 16) and 0xFF) / 255.0f
            floatValues[i * 3 + 1] = ((val shr 8) and 0xFF) / 255.0f
            floatValues[i * 3 + 2] = (val and 0xFF) / 255.0f
        }
        return floatValues
    }
}
