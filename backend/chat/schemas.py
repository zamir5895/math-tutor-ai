from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum

class UserMessage(BaseModel):
    user_id: str
    conversation_id: Optional[str] = None
    message: str

class AIResponse(BaseModel):
    conversation_id: str
    response: str
    context_used: List[str]

class Conversation(BaseModel):
    user_id: str
    conversation_id: str
    title: str
    messages: List[dict]
    created_at: datetime
    updated_at: datetime

class ConversationSummary(BaseModel):
    id: str
    title: str
    last_message: str
    updated_at: str

# Nuevos schemas para sesiones de aprendizaje
class LearningSessionType(str, Enum):
    TEACHING = "teaching"
    PRACTICE = "practice"
    REVIEW = "review"

class LearningSession(BaseModel):
    session_id: str
    user_id: str
    topic: str
    subtopic: Optional[str] = None
    session_type: LearningSessionType
    concepts_covered: List[str] = []
    status: str = "active"  # active, completed, paused
    created_at: datetime
    updated_at: datetime

class CreateLearningSessionRequest(BaseModel):
    user_id: str
    topic: str
    subtopic: Optional[str] = None
    level: str = "basico"  # basico, intermedio, avanzado

# Schemas para ejercicios
class DifficultyLevel(str, Enum):
    FACIL = "facil"
    INTERMEDIO = "intermedio"
    DIFICIL = "dificil"

class Exercise(BaseModel):
    exercise_id: str
    pregunta: str
    respuesta_correcta: str
    tema: str
    subtema: str
    es_multiple_choice: bool
    opciones: Optional[List[str]] = None
    solucion: List[str]
    pistas: List[str]
    concepto_principal: str
    nivel: DifficultyLevel

class ExerciseRequest(BaseModel):
    user_id: str
    topic: str
    subtopic: Optional[str] = None
    nivel: DifficultyLevel = DifficultyLevel.FACIL
    cantidad: int = 5

class ExerciseResponse(BaseModel):
    user_id: str
    exercise_id: str
    respuesta_usuario: str
    es_correcto: bool
    tiempo_respuesta: Optional[int] = None

# Schemas para reportes
class LearningReport(BaseModel):
    user_id: str
    session_id: str
    topic: str
    concepts_learned: List[str]
    exercises_completed: int
    accuracy_rate: float
    generated_at: datetime

# Nuevos schemas para sesiones extendidas
class SessionInteraction(BaseModel):
    timestamp: datetime
    type: str  # "question", "explanation", "exercise", "answer", "concept"
    content: str
    metadata: Optional[Dict] = {}

class SessionHistoryResponse(BaseModel):
    session_info: Dict
    concepts_covered: List[str]
    session_history: List[SessionInteraction]
    exercises_completed: List[Dict]
    questions_asked: List[Dict]

class SessionSummaryStats(BaseModel):
    session_id: str
    topic: str
    subtopic: Optional[str]
    concepts_learned: int
    concepts_list: List[str]
    total_exercises: int
    correct_exercises: int
    accuracy_percentage: float
    free_questions_asked: int
    total_study_time_minutes: Optional[float]
    status: str
    last_accessed: Optional[datetime]

class ReactivateSessionRequest(BaseModel):
    session_id: str

class SessionChatMessage(BaseModel):
    user_id: str
    session_id: str
    message: str

# Schemas para análisis de progreso y recomendaciones
class ProgressAnalysis(BaseModel):
    nivel_actual: str
    areas_fuertes: List[str]
    areas_debiles: List[str]
    siguiente_tema_recomendado: str
    dificultad_recomendada: str
    consejos_mejora: List[str]
    motivacion: str
    tiempo_estudio_sugerido: str
    estadisticas_reales: Dict

class PersonalizedAdvice(BaseModel):
    consejo_principal: str
    estrategias_estudio: List[str]
    ejercicios_recomendados: List[str]
    habitos_sugeridos: List[str]
    mensaje_motivacional: str
    proximos_pasos: List[str]
    tiempo_estudio_diario: str
    frecuencia_recomendada: str

class TopicRecommendation(BaseModel):
    tema_recomendado: str
    razon: str
    prerequisitos: List[str]
    dificultad_estimada: str
    tiempo_estimado: str
    conceptos_clave: List[str]

class UserRecommendations(BaseModel):
    progress_analysis: ProgressAnalysis
    personalized_advice: PersonalizedAdvice
    next_topic_recommendation: TopicRecommendation
    generated_at: datetime

class AdaptiveExerciseRequest(BaseModel):
    user_id: str
    topic: str
    cantidad: int = 5

class ExerciseCompletion(BaseModel):
    user_id: str
    session_id: str
    exercise_id: str
    user_answer: str
    is_correct: bool
    time_taken: Optional[int] = None

class SessionExercisesResponse(BaseModel):
    session_id: str
    topic: str
    subtopic: Optional[str]
    level: str
    exercises: List[Exercise]
    count: int
    generated_at: str

class ConversationExercisesResponse(BaseModel):
    conversation_id: str
    exercises: List[Exercise]
    count: int
    generated_at: str