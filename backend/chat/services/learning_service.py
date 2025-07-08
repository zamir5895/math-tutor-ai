from pymongo import MongoClient
from config import settings
from datetime import datetime
from typing import List, Dict
import uuid

class LearningService:
    def __init__(self):
        self.client = MongoClient(settings.mongo_uri)
        self.db = self.client[settings.mongo_db]
        self.sessions = self.db.learning_sessions
        self.exercises = self.db.exercises
        self.responses = self.db.exercise_responses
        self._setup_indexes()

    def _setup_indexes(self):
        self.sessions.create_index([("user_id", 1)])
        self.sessions.create_index([("session_id", 1)])
        self.sessions.create_index([("user_id", 1), ("status", 1)])
        self.exercises.create_index([("exercise_id", 1)])
        self.exercises.create_index([("tema", 1), ("nivel", 1)])
        self.responses.create_index([("user_id", 1), ("exercise_id", 1)])

    def create_learning_session(self, user_id: str, topic: str, subtopic: str = None, level: str = "basico"):
        """Crea una nueva sesión de aprendizaje"""
        session_id = str(uuid.uuid4())
        session = {
            "session_id": session_id,
            "user_id": user_id,
            "topic": topic,
            "subtopic": subtopic,
            "level": level,
            "session_type": "teaching",
            "concepts_covered": [],
            "session_history": [],
            "exercises_completed": [],
            "questions_asked": [], 
            "status": "active",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "last_accessed": datetime.utcnow()
        }
        self.sessions.insert_one(session)
        return session_id

    def update_session_concepts(self, session_id: str, concepts: List[str]):
        """Actualiza los conceptos cubiertos en una sesión"""
        self.sessions.update_one(
            {"session_id": session_id},
            {
                "$addToSet": {"concepts_covered": {"$each": concepts}},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )

    def complete_session(self, session_id: str):
        """Marca una sesión como completada"""
        self.sessions.update_one(
            {"session_id": session_id},
            {
                "$set": {
                    "status": "completed",
                    "completed_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
            }
        )

    def get_session(self, session_id: str):
        """Obtiene una sesión específica"""
        return self.sessions.find_one({"session_id": session_id})

    def get_user_sessions(self, user_id: str, status: str = None):
        """Obtiene las sesiones de un usuario"""
        query = {"user_id": user_id}
        if status:
            query["status"] = status
        return list(self.sessions.find(query).sort("updated_at", -1))

    def save_exercise(self, exercise_data: Dict):
        """Guarda un ejercicio generado"""
        exercise_data["created_at"] = datetime.utcnow()
        self.exercises.insert_one(exercise_data)
        return exercise_data["exercise_id"]

    def get_exercises_by_topic(self, topic: str, nivel: str = None, limit: int = 5):
        """Obtiene ejercicios por tema y nivel"""
        query = {"tema": topic}
        if nivel:
            query["nivel"] = nivel
        return list(self.exercises.find(query).limit(limit))

    def save_exercise_response(self, user_id: str, exercise_id: str, respuesta_usuario: str, es_correcto: bool, tiempo_respuesta: int = None):
        """Guarda la respuesta de un usuario a un ejercicio"""
        response = {
            "user_id": user_id,
            "exercise_id": exercise_id,
            "respuesta_usuario": respuesta_usuario,
            "es_correcto": es_correcto,
            "tiempo_respuesta": tiempo_respuesta,
            "timestamp": datetime.utcnow()
        }
        self.responses.insert_one(response)

    def get_user_exercise_stats(self, user_id: str, topic: str = None):
        """Obtiene estadísticas de ejercicios del usuario"""
        query = {"user_id": user_id}
        if topic:
            pass
        
        total = self.responses.count_documents(query)
        correct = self.responses.count_documents({**query, "es_correcto": True})
        
        return {
            "total_exercises": total,
            "correct_answers": correct,
            "accuracy_rate": correct / total if total > 0 else 0
        }

    def add_session_interaction(self, session_id: str, interaction_type: str, content: str, metadata: Dict = None):
        """Agrega una interacción al historial de la sesión"""
        interaction = {
            "timestamp": datetime.utcnow(),
            "type": interaction_type,
            "content": content,
            "metadata": metadata or {}
        }
        
        self.sessions.update_one(
            {"session_id": session_id},
            {
                "$push": {"session_history": interaction},
                "$set": {
                    "updated_at": datetime.utcnow(),
                    "last_accessed": datetime.utcnow()
                }
            }
        )

    def add_exercise_to_session(self, session_id: str, exercise_data: Dict, user_response: str = None, is_correct: bool = None):
        """Agrega un ejercicio completado a la sesión"""
        exercise_entry = {
            "exercise_id": exercise_data.get("exercise_id"),
            "question": exercise_data.get("pregunta"),
            "correct_answer": exercise_data.get("respuesta_correcta"),
            "user_answer": user_response,
            "is_correct": is_correct,
            "topic": exercise_data.get("tema"),
            "subtopic": exercise_data.get("subtema"),
            "difficulty": exercise_data.get("nivel"),
            "completed_at": datetime.utcnow()
        }
        
        self.sessions.update_one(
            {"session_id": session_id},
            {
                "$push": {"exercises_completed": exercise_entry},
                "$set": {
                    "updated_at": datetime.utcnow(),
                    "last_accessed": datetime.utcnow()
                }
            }
        )

    def add_question_to_session(self, session_id: str, question: str, answer: str, concepts_extracted: List[str] = None):
        """Agrega una pregunta libre realizada en la sesión"""
        question_entry = {
            "question": question,
            "answer": answer,
            "concepts_extracted": concepts_extracted or [],
            "asked_at": datetime.utcnow()
        }
        
        self.sessions.update_one(
            {"session_id": session_id},
            {
                "$push": {"questions_asked": question_entry},
                "$set": {
                    "updated_at": datetime.utcnow(),
                    "last_accessed": datetime.utcnow()
                }
            }
        )

    def reactivate_session(self, session_id: str):
        """Reactiva una sesión pausada o completada para continuar el aprendizaje"""
        result = self.sessions.update_one(
            {"session_id": session_id},
            {
                "$set": {
                    "status": "active",
                    "last_accessed": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
            }
        )
        return result.modified_count > 0

    def pause_session(self, session_id: str):
        """Pausa una sesión activa"""
        self.sessions.update_one(
            {"session_id": session_id},
            {
                "$set": {
                    "status": "paused",
                    "updated_at": datetime.utcnow()
                }
            }
        )

    def get_session_full_history(self, session_id: str):
        """Obtiene el historial completo de una sesión"""
        session = self.sessions.find_one({"session_id": session_id})
        if not session:
            return None
        
        return {
            "session_info": {
                "session_id": session["session_id"],
                "user_id": session["user_id"],
                "topic": session["topic"],
                "subtopic": session.get("subtopic"),
                "level": session.get("level"),
                "status": session["status"],
                "created_at": session["created_at"],
                "updated_at": session["updated_at"],
                "last_accessed": session.get("last_accessed")
            },
            "concepts_covered": session.get("concepts_covered", []),
            "session_history": session.get("session_history", []),
            "exercises_completed": session.get("exercises_completed", []),
            "questions_asked": session.get("questions_asked", [])
        }

    def get_active_sessions(self, user_id: str):
        """Obtiene las sesiones activas de un usuario"""
        return list(self.sessions.find({
            "user_id": user_id, 
            "status": {"$in": ["active", "paused"]}
        }).sort("last_accessed", -1))

    def get_session_summary_stats(self, session_id: str):
        """Obtiene estadísticas resumidas de una sesión"""
        session = self.sessions.find_one({"session_id": session_id})
        if not session:
            return None
        
        exercises = session.get("exercises_completed", [])
        questions = session.get("questions_asked", [])
        concepts = session.get("concepts_covered", [])
        
        total_exercises = len(exercises)
        correct_exercises = sum(1 for ex in exercises if ex.get("is_correct", False))
        accuracy = (correct_exercises / total_exercises * 100) if total_exercises > 0 else 0
        
        created_at = session.get("created_at")
        last_accessed = session.get("last_accessed", session.get("updated_at"))
        total_time = None
        if created_at and last_accessed:
            total_time = (last_accessed - created_at).total_seconds() / 60 
        
        return {
            "session_id": session_id,
            "topic": session.get("topic"),
            "subtopic": session.get("subtopic"),
            "concepts_learned": len(concepts),
            "concepts_list": concepts,
            "total_exercises": total_exercises,
            "correct_exercises": correct_exercises,
            "accuracy_percentage": accuracy,
            "free_questions_asked": len(questions),
            "total_study_time_minutes": total_time,
            "status": session.get("status"),
            "last_accessed": last_accessed
        }

    def complete_exercise_with_analysis(self, user_id: str, session_id: str, exercise_data: Dict, user_answer: str, is_correct: bool, time_taken: int = None):
        """Completa un ejercicio y actualiza el análisis de progreso"""
        self.add_exercise_to_session(session_id, exercise_data, user_answer, is_correct)
        
        from services.ai_service import ai
        ai.update_user_progress_context(
            user_id, 
            session_id, 
            {
                "type": "exercise_completed",
                "topic": exercise_data.get("tema"),
                "difficulty": exercise_data.get("nivel"),
                "is_correct": is_correct,
                "time_taken": time_taken,
                "timestamp": datetime.utcnow(),
                "exercise_id": exercise_data.get("exercise_id")
            }
        )
        
        session = self.get_session(session_id)
        if session:
            from services.qdrant_service import qdrant
            exercises_completed = session.get("exercises_completed", [])
            total = len(exercises_completed)
            correct = sum(1 for ex in exercises_completed if ex.get("is_correct"))
            
            qdrant.update_user_learning_metrics(user_id, {
                "total_exercises": total,
                "correct_exercises": correct,
                "current_accuracy": (correct/total*100) if total > 0 else 0,
                "last_topic": session.get("topic"),
                "last_activity": datetime.utcnow().isoformat()
            })

    def learn_concept_with_tracking(self, user_id: str, session_id: str, concept: str, explanation: str):
        """Aprende un concepto y actualiza el seguimiento"""
        self.update_session_concepts(session_id, [concept])
        
        self.add_session_interaction(session_id, "concept", f"Concepto aprendido: {concept}")
        
        from services.ai_service import ai
        session = self.get_session(session_id)
        ai.update_user_progress_context(
            user_id,
            session_id,
            {
                "type": "concept_learned",
                "topic": session.get("topic") if session else "unknown",
                "concept": concept,
                "explanation_length": len(explanation),
                "timestamp": datetime.utcnow()
            }
        )

    def get_user_progress_analysis(self, user_id: str):
        """Obtiene análisis completo del progreso del usuario"""
        from services.ai_service import ai
        return ai.analyze_student_progress(user_id)

    def get_adaptive_exercises_for_user(self, user_id: str, topic: str, cantidad: int = 5):
        """Genera ejercicios adaptativos basados en el progreso del usuario"""
        from services.ai_service import ai
        return ai.generate_adaptive_exercises(user_id, topic, cantidad)

    def get_personalized_recommendations(self, user_id: str):
        """Obtiene recomendaciones personalizadas para el usuario"""
        from services.ai_service import ai
        
        progress = ai.analyze_student_progress(user_id)
        advice = ai.generate_personalized_advice(user_id)        
        next_topic = ai.get_next_recommended_topic(user_id)
        
        return {
            "progress_analysis": progress,
            "personalized_advice": advice,
            "next_topic_recommendation": next_topic,
            "generated_at": datetime.utcnow()
        }

learning_service = LearningService()
