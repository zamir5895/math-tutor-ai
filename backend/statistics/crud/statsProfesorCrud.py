# statsProfesorCrud.py

from ..db.db import stats_alumno_profesor_collection, stats_tema_profesor_collection
from typing import Dict, Any
from motor.motor_asyncio import AsyncIOMotorClient

# Get teacher statistics (general statistics)
async def get_teacher_classroom_statistics(teacher_id: str, classroom_id: str) -> Dict[str, Any]:
    try:
        pipeline = [
            {"$match": {"teacher_id": teacher_id, "classroom_id": classroom_id}},
            {"$group": {
                "_id": "$classroom_id",
                "average_progress": {"$avg": "$progress"},
                "total_students": {"$sum": 1}
            }}
        ]
        result = await stats_alumno_profesor_collection.aggregate(pipeline).to_list(length=None)
        return result if result else {"message": "No data found"}
    except Exception as e:
        return {"error": str(e)}


# Create or insert teacher statistics
async def create_teacher_statistics(data: Dict[str, Any]) -> Dict[str, Any]:
    try:
        result = await stats_alumno_profesor_collection.insert_one(data)
        return {"message": "Teacher statistics created successfully", "id": str(result.inserted_id)}
    except Exception as e:
        return {"error": str(e)}

# Update teacher statistics
async def update_teacher_statistics(teacher_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    try:
        result = await stats_alumno_profesor_collection.update_one(
            {"teacher_id": teacher_id},
            {"$set": data}
        )
        if result.matched_count == 0:
            return {"message": "No teacher found to update"}
        return {"message": "Teacher statistics updated successfully"}
    except Exception as e:
        return {"error": str(e)}

# Delete teacher statistics
async def delete_teacher_statistics(teacher_id: str) -> Dict[str, Any]:
    try:
        result = await stats_alumno_profesor_collection.delete_one({"teacher_id": teacher_id})
        if result.deleted_count == 0:
            return {"message": "No teacher found to delete"}
        return {"message": "Teacher statistics deleted successfully"}
    except Exception as e:
        return {"error": str(e)}

# Get teacher statistics by topic
async def get_teacher_topic_progress(teacher_id: str, topic_name: str) -> Dict[str, Any]:
    try:
        topic_data = await stats_tema_profesor_collection.find_one({"teacher_id": teacher_id, "topic": topic_name})
        if topic_data is None:
            return {"message": f"Teacher progress for {topic_name} not found"}
        return topic_data
    except Exception as e:
        return {"error": str(e)}

