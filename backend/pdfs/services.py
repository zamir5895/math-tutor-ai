from bson import ObjectId
from database import get_database
from models import Exercise, ExerciseResponse
from typing import List

class ExerciseService:
    
    @staticmethod
    async def save_exercise(exercise: Exercise) -> str:
        """Guarda un ejercicio en MongoDB"""
        db = await get_database()
        collection = db.exercises
        
        exercise_dict = exercise.dict()
        result = await collection.insert_one(exercise_dict)
        return str(result.inserted_id)
    
    @staticmethod
    async def save_exercises(exercises: List[Exercise]) -> List[str]:
        """Guarda múltiples ejercicios"""
        db = await get_database()
        collection = db.exercises
        
        exercises_dict = [exercise.dict() for exercise in exercises]
        result = await collection.insert_many(exercises_dict)
        return [str(id) for id in result.inserted_ids]
    
    @staticmethod
    async def get_exercise(exercise_id: str) -> ExerciseResponse:
        """Obtiene un ejercicio por ID"""
        db = await get_database()
        collection = db.exercises
        
        exercise = await collection.find_one({"_id": ObjectId(exercise_id)})
        if exercise:
            exercise["id"] = str(exercise["_id"])
            del exercise["_id"]
            return ExerciseResponse(**exercise)
        return None
    
    @staticmethod
    async def get_exercises_by_topic(tema: str) -> List[ExerciseResponse]:
        """Obtiene ejercicios por tema"""
        db = await get_database()
        collection = db.exercises
        
        cursor = collection.find({"tema": {"$regex": tema, "$options": "i"}})
        exercises = []
        
        async for exercise in cursor:
            exercise["id"] = str(exercise["_id"])
            del exercise["_id"]
            exercises.append(ExerciseResponse(**exercise))
        
        return exercises