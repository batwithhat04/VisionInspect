package com.visioninspect.utils

import android.content.Context
import com.itextpdf.kernel.pdf.PdfDocument
import com.itextpdf.kernel.pdf.PdfWriter
import com.itextpdf.layout.Document
import com.itextpdf.layout.element.Image
import com.itextpdf.layout.element.Paragraph
import com.itextpdf.layout.property.TextAlignment
import com.visioninspect.data.model.Inspection
import java.io.File
import com.itextpdf.io.image.ImageDataFactory

class PDFReportGenerator(private val context: Context) {

    fun generateReport(inspection: Inspection): File? {
        val fileName = "Inspection_Report_${inspection.timestamp}.pdf"
        val reportFile = File(context.getExternalFilesDir(null), fileName)

        try {
            val writer = PdfWriter(reportFile)
            val pdf = PdfDocument(writer)
            val document = Document(pdf)

            // Title
            document.add(Paragraph("VisionInspect - Inspection Report")
                .setTextAlignment(TextAlignment.CENTER)
                .setFontSize(20f)
                .setBold())

            // Metadata
            document.add(Paragraph("Inspection ID: ${inspection.id}"))
            document.add(Paragraph("Timestamp: ${java.util.Date(inspection.timestamp)}"))
            document.add(Paragraph("GPS: ${inspection.latitude}, ${inspection.longitude}"))
            document.add(Paragraph("Damage Grade: ${inspection.severityGrade}"))
            document.add(Paragraph("Damage Area: ${inspection.damagePercent}%"))

            // Images
            val imageFile = File(inspection.imagePath)
            if (imageFile.exists()) {
                val data = ImageDataFactory.create(imageFile.absolutePath)
                val img = Image(data).setAutoScale(true)
                document.add(Paragraph("Inspection Image:"))
                document.add(img)
            }

            // Recommendations
            document.add(Paragraph("Recommendation:").setBold())
            document.add(Paragraph(inspection.recommendation))

            document.close()
            return reportFile

        } catch (e: Exception) {
            e.printStackTrace()
            return null
        }
    }
}
