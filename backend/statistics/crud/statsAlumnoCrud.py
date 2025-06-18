# statsAlumnoCrud.py

from ..db.db import stats_alumno_coleccion, stats_subtema_alumno_collection
from typing import Dict, Any
from motor.motor_asyncio import AsyncIOMotorClient

# Get student statistics (general statistics)
async def get_student_statistics(student_id: str) -> Dict[str, Any]:
    try:
        student_data = await stats_alumno_coleccion.find_one({"student_id": student_id})
        if student_data is None:
            return {"message": "Student not found"}
        return student_data
    except Exception as e:
        return {"error": str(e)}

# Create or insert student statistics
async def create_student_statistics(data: Dict[str, Any]) -> Dict[str, Any]:
    try:
        result = await stats_alumno_coleccion.insert_one(data)
        return {"message": "Student statistics created successfully", "id": str(result.inserted_id)}
    except Exception as e:
        return {"error": str(e)}

# Update student statistics
async def update_student_statistics(student_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    try:
        result = await stats_alumno_coleccion.update_one(
            {"student_id": student_id},
            {"$set": data}
        )
        if result.matched_count == 0:
            return {"message": "No student found to update"}
        return {"message": "Student statistics updated successfully"}
    except Exception as e:
        return {"error": str(e)}

# Delete student statistics
async def delete_student_statistics(student_id: str) -> Dict[str, Any]:
    try:
        result = await stats_alumno_coleccion.delete_one({"student_id": student_id})
        if result.deleted_count == 0:
            return {"message": "No student found to delete"}
        return {"message": "Student statistics deleted successfully"}
    except Exception as e:
        return {"error": str(e)}

# Get student progress by topic
async def get_student_topic_progress(student_id: str, topic_name: str) -> Dict[str, Any]:
    try:
        topic_data = await stats_subtema_alumno_collection.find_one({"student_id": student_id, "topic": topic_name})
        if topic_data is None:
            return {"message": f"Progress for {topic_name} not found"}
        return topic_data
    except Exception as e:
        return {"error": str(e)}

