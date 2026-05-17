package com.visioninspect.data.db

import androidx.room.*
import com.visioninspect.data.model.Inspection
import kotlinx.coroutines.flow.Flow

@Dao
interface InspectionDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertInspection(inspection: Inspection): Long

    @Query("SELECT * FROM inspections ORDER BY timestamp DESC")
    fun getAllInspections(): Flow<List<Inspection>>

    @Query("SELECT * FROM inspections WHERE id = :id")
    suspend fun getInspectionById(id: Long): Inspection?

    @Delete
    suspend fun deleteInspection(inspection: Inspection)
}
