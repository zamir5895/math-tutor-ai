# Matemix AI - Microservicio de Tutoría de Matemáticas con IA

## Descripción General

Matemix AI es un microservicio especializado en tutoría de matemáticas que utiliza inteligencia artificial para proporcionar una experiencia de aprendizaje personalizada. El sistema está diseñado con separación clara de responsabilidades: chat general para consultas rápidas y sesiones de aprendizaje para experiencias estructuradas con ejercicios.

## Arquitectura: Separación de Responsabilidades

### Chat General (/chat-stream)
- **Propósito**: Consultas, explicaciones y orientación matemática
- **Características**: 
  - Solo responde preguntas relacionadas con matemáticas
  - Proporciona explicaciones conceptuales
  - Orienta sobre temas y niveles
  - NO genera ejercicios ni maneja lógica de sesiones

### Sesiones de Aprendizaje (/learning/session/{id}/chat)
- **Propósito**: Experiencia de aprendizaje estructurada y completa
- **Características**:
  - Genera ejercicios organizados por dificultad (3 fáciles, 4 intermedios, 3 difíciles)
  - Seguimiento de progreso individual
  - Contexto personalizado basado en la sesión
  - Reportes PDF detallados

## Esquemas de Base de Datos

### MongoDB Collections

#### conversations
```javascript
{
  _id: ObjectId,
  user_id: String,
  conversation_id: String,
  title: String,
  messages: [
    {
      role: String, // "user" | "assistant"
      content: String,
      timestamp: Date
    }
  ],
  created_at: Date,
  updated_at: Date
}
```

#### learning_sessions
```javascript
{
  _id: ObjectId,
  session_id: String,
  user_id: String,
  topic: String,
  subtopic: String,
  level: String, // "basico" | "intermedio" | "avanzado"
  concepts_covered: [String],
  status: String, // "active" | "paused" | "completed"
  session_history: [
    {
      timestamp: Date,
      type: String,
      content: String,
      metadata: Object
    }
  ],
  exercises_completed: [
    {
      exercise_id: String,
      question: String,
      correct_answer: String,
      user_answer: String,
      is_correct: Boolean,
      topic: String,
      subtopic: String,
      difficulty: String,
      completed_at: Date
    }
  ],
  questions_asked: [
    {
      question: String,
      answer: String,
      concepts_extracted: [String],
      asked_at: Date
    }
  ],
  created_at: Date,
  updated_at: Date,
  last_accessed: Date
}
```

#### exercises
```javascript
{
  _id: ObjectId,
  exercise_id: String,
  session_id: String,
  conversation_id: String,
  exercise_number: Number,
  pregunta: String,
  respuesta_correcta: String,
  nivel: String, // "facil" | "intermedio" | "dificil"
  tema: String,
  subtema: String,
  es_multiple_choice: Boolean,
  opciones: [String], // null si no es multiple choice
  solucion: [String], // pasos de la solución
  pistas: [String],
  concepto_principal: String,
  status: String, // "assigned" | "in_progress" | "completed" | "needs_review"
  generated_at: Date,
  updated_at: Date
}
```

#### exercise_responses
```javascript
{
  _id: ObjectId,
  user_id: String,
  exercise_id: String,
  respuesta_usuario: String,
  es_correcto: Boolean,
  tiempo_respuesta: Number, // segundos
  timestamp: Date
}
```

### Qdrant Collections

#### general_context
```javascript
{
  id: String,
  vector: [Number], // embedding del texto
  payload: {
    user_id: String,
    text: String,
    conversation_id: String,
    context_type: "conversation",
    metadata: {
      type: "general_math_chat",
      topic: "conversacion_general"
    },
    created_at: Date
  }
}
```

#### session_context
```javascript
{
  id: String,
  vector: [Number], // embedding del texto
  payload: {
    user_id: String,
    text: String,
    conversation_id: String,
    context_type: "conversation",
    metadata: {
      type: "learning_interaction",
      session_id: String,
      topic: String,
      exercises_generated: Number
    },
    created_at: Date
  }
}
```

## Endpoints Implementados

### Chat General

#### POST /chat-stream
Chat para consultas generales, explicaciones y orientación matemática. NO genera ejercicios.

**Request:**
```json
{
  "user_id": "string",
  "conversation_id": "string", // opcional
  "message": "string"
}
```

**Response:** Server-Sent Events
```json
{
  "text": "string",
  "conversation_id": "string"
}
```

#### GET /conversations/{user_id}
Lista todas las conversaciones del chat general.

**Response:**
```json
[
  {
    "id": "string",
    "title": "string",
    "last_message": "string",
    "updated_at": "string"
  }
]
```

#### GET /conversation/{user_id}/{conversation_id}
Obtiene una conversación específica.

**Response:**
```json
{
  "conversation_id": "string",
  "user_id": "string",
  "title": "string",
  "messages": [
    {
      "role": "string",
      "content": "string",
      "timestamp": "string"
    }
  ],
  "created_at": "string",
  "updated_at": "string"
}
```

#### DELETE /conversation/{user_id}/{conversation_id}
Elimina una conversación.

**Response:**
```json
{
  "message": "Conversación eliminada correctamente"
}
```

### Sesiones de Aprendizaje

#### POST /learning/session/create
Crea una nueva sesión de aprendizaje estructurada.

**Request:**
```json
{
  "user_id": "string",
  "topic": "string",
  "subtopic": "string",
  "level": "string"
}
```

**Response:**
```json
{
  "session_id": "string",
  "topic": "string",
  "subtopic": "string",
  "level": "string",
  "teaching_plan": ["string"],
  "status": "active",
  "message": "string",
  "chat_endpoint": "string"
}
```

#### POST /learning/session/{session_id}/chat
Chat interactivo dentro de la sesión que puede generar ejercicios y ayudar con ejercicios específicos.

**Request:**
```json
{
  "user_id": "string",
  "message": "string"
}
```

**Response:** Server-Sent Events
```json
{
  "text": "string",
  "session_id": "string",
  "topic": "string",
  "exercises_generated": "number"
}
```

**Capacidades del chat de sesión:**
- Generar ejercicios: "Quiero ejercicios"
- Trabajar ejercicio específico: "Ejercicio 3"
- Pedir ayuda: "Ayuda con ejercicio 2"
- Solicitar pistas: "Dame una pista"
- Enviar respuestas: "Mi respuesta es: 25"

#### GET /learning/session/{session_id}/conversation
Obtiene el historial completo de la conversación de la sesión de aprendizaje.

**Response:**
```json
{
  "session_id": "string",
  "conversation_id": "string",
  "user_id": "string",
  "topic": "string",
  "subtopic": "string",
  "level": "string",
  "title": "string",
  "messages": [
    {
      "role": "string",
      "content": "string",
      "timestamp": "string"
    }
  ],
  "session_status": "string",
  "created_at": "string",
  "updated_at": "string"
}
```

#### GET /learning/session/{session_id}/exercises
Obtiene todos los ejercicios generados en la sesión.

**Response:**
```json
{
  "session_id": "string",
  "topic": "string",
  "subtopic": "string",
  "level": "string",
  "exercises": [
    {
      "_id": "string",
      "exercise_number": "number",
      "pregunta": "string",
      "respuesta_correcta": "string",
      "nivel": "string",
      "tema": "string",
      "status": "string",
      "generated_at": "string"
    }
  ],
  "count": "number",
  "generated_at": "string"
}
```

#### GET /learning/session/{session_id}
Obtiene información de una sesión de aprendizaje.

**Response:**
```json
{
  "session_id": "string",
  "user_id": "string",
  "topic": "string",
  "subtopic": "string",
  "level": "string",
  "concepts_covered": ["string"],
  "status": "string",
  "created_at": "string",
  "updated_at": "string",
  "last_accessed": "string"
}
```

#### GET /learning/session/{session_id}/history
Obtiene el historial completo de una sesión de aprendizaje.

**Response:**
```json
{
  "session_info": {
    "session_id": "string",
    "user_id": "string",
    "topic": "string",
    "subtopic": "string",
    "level": "string",
    "status": "string",
    "created_at": "string",
    "updated_at": "string",
    "last_accessed": "string"
  },
  "concepts_covered": ["string"],
  "session_history": [
    {
      "timestamp": "string",
      "type": "string",
      "content": "string",
      "metadata": {}
    }
  ],
  "exercises_completed": [{}],
  "questions_asked": [{}]
}
```

#### GET /learning/session/{session_id}/stats
Obtiene estadísticas resumidas de una sesión.

**Response:**
```json
{
  "session_id": "string",
  "topic": "string",
  "subtopic": "string",
  "concepts_learned": "number",
  "concepts_list": ["string"],
  "total_exercises": "number",
  "correct_exercises": "number",
  "accuracy_percentage": "number",
  "free_questions_asked": "number",
  "total_study_time_minutes": "number",
  "status": "string",
  "last_accessed": "string"
}
```

#### POST /learning/session/{session_id}/complete
Marca una sesión como completada.

**Response:**
```json
{
  "session_id": "string",
  "message": "Sesión completada exitosamente",
  "concepts_learned": "number",
  "status": "completed",
  "next_steps": "string"
}
```

#### POST /learning/session/{session_id}/pause
Pausa una sesión activa.

**Response:**
```json
{
  "message": "Sesión pausada exitosamente",
  "session_id": "string",
  "status": "paused"
}
```

#### POST /learning/session/{session_id}/reactivate
Reactiva una sesión pausada o completada.

**Response:**
```json
{
  "message": "Sesión reactivada exitosamente",
  "session_id": "string",
  "status": "active"
}
```

#### GET /learning/sessions/{user_id}
Obtiene todas las sesiones de aprendizaje de un usuario.

**Query Parameters:**
- `status` (optional): Filter by status

**Response:**
```json
{
  "user_id": "string",
  "status_filter": "string",
  "sessions": [{}],
  "count": "number"
}
```

#### GET /learning/sessions/{user_id}/active
Obtiene las sesiones activas o pausadas de un usuario.

**Response:**
```json
{
  "user_id": "string",
  "active_sessions": [{}],
  "count": "number"
}
```

### Reportes y Análisis

#### GET /learning/session/{session_id}/pdf-report
Genera y descarga el reporte PDF completo de una sesión.

**Response:** PDF file

#### GET /learning/session/{session_id}/pdf-exercises
Genera y descarga un PDF solo con los ejercicios de una sesión.

**Response:** PDF file

#### GET /tutor/progress/{user_id}
Obtiene análisis completo del progreso del usuario.

**Response:**
```json
{
  "nivel_actual": "string",
  "areas_fuertes": ["string"],
  "areas_debiles": ["string"],
  "siguiente_tema_recomendado": "string",
  "dificultad_recomendada": "string",
  "consejos_mejora": ["string"],
  "motivacion": "string",
  "tiempo_estudio_sugerido": "string",
  "estadisticas_reales": {}
}
```

#### GET /tutor/recommendations/{user_id}
Obtiene recomendaciones personalizadas completas para el usuario.

**Response:**
```json
{
  "progress_analysis": {},
  "personalized_advice": {
    "consejo_principal": "string",
    "estrategias_estudio": ["string"],
    "ejercicios_recomendados": ["string"],
    "habitos_sugeridos": ["string"],
    "mensaje_motivacional": "string",
    "proximos_pasos": ["string"],
    "tiempo_estudio_diario": "string",
    "frecuencia_recomendada": "string"
  },
  "next_topic_recommendation": {
    "tema_recomendado": "string",
    "razon": "string",
    "prerequisitos": ["string"],
    "dificultad_estimada": "string",
    "tiempo_estimado": "string",
    "conceptos_clave": ["string"]
  },
  "generated_at": "string"
}
```

#### GET /tutor/dashboard/{user_id}
Obtiene un dashboard completo del estudiante para el frontend.

**Response:**
```json
{
  "user_id": "string",
  "active_sessions": [{}],
  "progress_summary": {
    "nivel_actual": "string",
    "total_sessions": "number",
    "total_study_time_minutes": "number",
    "total_concepts_learned": "number",
    "accuracy_percentage": "number"
  },
  "quick_recommendations": {
    "next_topic": "string",
    "daily_advice": "string",
    "motivation": "string"
  },
  "areas_to_improve": ["string"],
  "strong_areas": ["string"],
  "generated_at": "string"
}
```

### Ejercicios Adaptativos

#### POST /tutor/exercises/adaptive
Genera ejercicios adaptativos basados en el progreso del usuario.

**Request:**
```json
{
  "user_id": "string",
  "topic": "string",
  "cantidad": "number"
}
```

**Response:**
```json
{
  "user_id": "string",
  "topic": "string",
  "exercises": [{}],
  "adaptation_info": "string",
  "count": "number"
}
```

#### POST /tutor/exercise/complete
Completa un ejercicio con seguimiento de progreso.

**Request:**
```json
{
  "user_id": "string",
  "session_id": "string",
  "exercise_id": "string",
  "user_answer": "string",
  "is_correct": "boolean",
  "time_taken": "number"
}
```

**Response:**
```json
{
  "message": "string",
  "result": "string",
  "advice": "string",
  "motivation": "string",
  "next_steps": ["string"]
}
```

#### GET /tutor/exercises/{user_id}/next-batch
Obtiene el siguiente lote de ejercicios recomendados.

**Query Parameters:**
- `topic`: Topic name
- `count`: Number of exercises (default: 3)

**Response:**
```json
{
  "user_id": "string",
  "topic": "string",
  "exercises": [{}],
  "difficulty_level": "string",
  "personalized_note": "string",
  "tips": ["string"]
}
```

### Endpoints de Utilidad

#### GET /
Información general del microservicio y endpoints disponibles.

#### GET /health
Verificación de salud del servicio.

**Response:**
```json
{
  "status": "healthy"
}
```

## Flujo de Ejercicios Mejorado

### 1. Generación Interna de Ejercicios
Cuando el usuario solicita ejercicios en una sesión:
```
Usuario: "Quiero ejercicios"
Sistema: Genera 10 ejercicios internamente y responde "Te he asignado 10 ejercicios..."
```

### 2. Trabajo con Ejercicios Específicos
El usuario puede referenciar ejercicios por número:
```
Usuario: "Ejercicio 3"
Sistema: Muestra el ejercicio 3 y ofrece ayuda
```

### 3. Solicitud de Ayuda
```
Usuario: "Ayuda con ejercicio 2"
Sistema: Proporciona pistas y orientación específica
```

### 4. Evaluación de Respuestas
```
Usuario: "Mi respuesta es: 25"
Sistema: Evalúa la respuesta y proporciona retroalimentación
```

### 5. Gestión de Estado
Los ejercicios tienen estados que se actualizan automáticamente:
- `assigned`: Ejercicio asignado pero no iniciado
- `in_progress`: Usuario está trabajando en él
- `completed`: Resuelto correctamente
- `needs_review`: Incorrecto, necesita revisión

## Tecnologías Utilizadas

- **FastAPI**: Framework web para Python
- **MongoDB**: Base de datos NoSQL para persistencia
- **Qdrant**: Base de datos vectorial para contexto semántico
- **Google Gemini**: Modelo de IA para generación de contenido
- **Pydantic**: Validación de esquemas de datos
- **Python**: Lenguaje de programación principal

## Configuración y Despliegue

### Variables de Entorno Requeridas
```
MONGO_URI=mongodb://localhost:27017
MONGO_DB=matemix_ai
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-pro
EMBEDDING_MODEL=models/embedding-001
QDRANT_HOST=localhost
QDRANT_PORT=6333
```

### Instalación
```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Documentación API
La documentación interactiva está disponible en `/docs` cuando el servicio está ejecutándose.
