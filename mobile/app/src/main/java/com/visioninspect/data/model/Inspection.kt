package com.visioninspect.data.model

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "inspections")
data class Inspection(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val timestamp: Long = System.currentTimeMillis(),
    val latitude: Double,
    val longitude: Double,
    val damagePercent: Double,
    val severityGrade: Int, // 1, 2, or 3
    val imagePath: String,
    val reportPath: String? = null,
    val recommendation: String
)
