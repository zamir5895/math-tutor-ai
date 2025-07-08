# 🎓 Matemix AI - Microservicio de Tutoría de Matemáticas con IA

## Descripción General

Matemix AI es un microservicio completo de tutoría de matemáticas que utiliza inteligencia artificial para proporcionar una experiencia de aprendizaje personalizada y adaptativa. El sistema gestiona contexto de usuario en Qdrant, permite sesiones de aprendizaje persistentes, genera ejercicios adaptativos, crea reportes PDF y proporciona análisis de progreso con recomendaciones personalizadas.

## 🚀 Características Principales

- **🧠 Chat inteligente con filtro matemático avanzado**
- **📚 Sesiones de aprendizaje persistentes y contextuales**
- **🎯 Ejercicios adaptativos basados en progreso individual**
- **📊 Análisis completo de progreso y debilidades**
- **💡 Recomendaciones personalizadas con IA**
- **🔄 Seguimiento continuo en Qdrant Vector DB**
- **📊 Dashboard completo para estudiantes**
- **🎨 Consejos y motivación personalizada**
- **📄 Reportes PDF detallados de aprendizaje**
- **⚡ API completa para integración frontend**

## 🛠️ Instalación y Configuración

### Prerrequisitos
- Python 3.8+
- MongoDB
- Qdrant Vector Database
- Redis (opcional para cache)

### Dependencias
```bash
pip install -r requirements.txt
```

### Variables de Entorno
Configura las siguientes variables en `config.py`:
- `MONGODB_URL`: URL de conexión a MongoDB
- `QDRANT_URL`: URL de conexión a Qdrant
- `GOOGLE_API_KEY`: Clave API de Google Gemini
- `REDIS_URL`: URL de Redis (opcional)

### Ejecutar el Servicio
```bash
uvicorn main:app --reload --port 8000
```

## 📋 Documentación de Endpoints

### 💬 1. Chat General

#### `POST /chat-stream`
Chat inteligente con detección automática de intención y contexto.

**Request JSON:**
```json
{
  "user_id": "user123",
  "conversation_id": "conv456", // opcional, se genera automáticamente
  "message": "¿Puedes explicarme las ecuaciones lineales?"
}
```

**Response (Server-Sent Events):**
```json
{
  "text": "Las ecuaciones lineales son expresiones matemáticas...",
  "conversation_id": "conv456",
  "session_active": true
}
```

**Funcionalidades:**
- Detección automática de intención del estudiante
- Filtro matemático (solo responde preguntas de matemáticas)
- Integración con sesiones de aprendizaje activas
- Generación automática de títulos para conversaciones
- Streaming de respuestas en tiempo real

#### `GET /conversations/{user_id}`
Obtiene la lista de conversaciones del usuario.

**Response JSON:**
```json
[
  {
    "id": "conv123",
    "title": "Ecuaciones lineales - Conceptos básicos",
    "last_message": "Excelente, ahora entiendo mejor...",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

#### `GET /conversation/{user_id}/{conversation_id}`
Obtiene una conversación específica con todo su historial.

**Response JSON:**
```json
{
  "conversation_id": "conv123",
  "user_id": "user123",
  "title": "Ecuaciones lineales - Conceptos básicos",
  "messages": [
    {
      "role": "user",
      "content": "¿Puedes explicarme las ecuaciones lineales?",
      "timestamp": "2024-01-15T10:00:00Z"
    },
    {
      "role": "assistant",
      "content": "Las ecuaciones lineales son...",
      "timestamp": "2024-01-15T10:01:00Z"
    }
  ],
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

#### `DELETE /conversation/{user_id}/{conversation_id}`
Elimina una conversación específica.

**Response JSON:**
```json
{
  "message": "Conversación eliminada correctamente"
}
```

### 📚 2. Sesiones de Aprendizaje

#### `POST /learning/session/create`
Crea una nueva sesión de aprendizaje estructurada.

**Request JSON:**
```json
{
  "user_id": "user123",
  "topic": "Álgebra básica",
  "subtopic": "Ecuaciones lineales", // opcional
  "level": "basico" // basico, intermedio, avanzado
}
```

**Response JSON:**
```json
{
  "session_id": "session_789",
  "topic": "Álgebra básica",
  "subtopic": "Ecuaciones lineales",
  "level": "basico",
  "teaching_plan": [
    "Variables y constantes",
    "Operaciones básicas con variables",
    "Resolución de ecuaciones simples"
  ],
  "message": "Sesión de aprendizaje creada para Álgebra básica. Comenzaremos con 3 conceptos."
}
```

#### `POST /learning/session/{session_id}/chat`
Chat interactivo dentro de una sesión de aprendizaje específica.

**Request JSON:**
```json
{
  "user_id": "user123",
  "message": "¿Puedes generar algunos ejercicios de práctica?"
}
```

**Response (Server-Sent Events):**
```json
{
  "text": "¡Perfecto! He generado algunos ejercicios de Álgebra básica para ti:\n\n**Ejercicio 1:**\nResuelve: 2x + 5 = 13\n\n**Ejercicio 2:**\nSi x - 3 = 7, ¿cuál es el valor de x?",
  "session_id": "session_789",
  "topic": "Álgebra básica"
}
```

#### `GET /learning/session/{session_id}`
Obtiene información básica de una sesión de aprendizaje.

**Response JSON:**
```json
{
  "session_id": "session_789",
  "user_id": "user123",
  "topic": "Álgebra básica",
  "subtopic": "Ecuaciones lineales",
  "concepts_covered": [
    "Variables y constantes",
    "Operaciones básicas con variables"
  ],
  "status": "active",
  "created_at": "2024-01-15T09:00:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

#### `GET /learning/session/{session_id}/history`
Obtiene el historial completo de una sesión con todas las interacciones.

**Response JSON:**
```json
{
  "session_info": {
    "session_id": "session_789",
    "topic": "Álgebra básica",
    "status": "active"
  },
  "concepts_covered": [
    "Variables y constantes",
    "Operaciones básicas con variables"
  ],
  "session_history": [
    {
      "timestamp": "2024-01-15T09:30:00Z",
      "type": "question",
      "content": "¿Qué es una variable?",
      "metadata": {"intent": "pregunta_concepto"}
    },
    {
      "timestamp": "2024-01-15T09:31:00Z",
      "type": "answer",
      "content": "Una variable es un símbolo...",
      "metadata": {"response_type": "general"}
    }
  ],
  "exercises_completed": [
    {
      "exercise_id": "ex123",
      "pregunta": "Resuelve: 2x + 5 = 13",
      "respuesta_usuario": "x = 4",
      "es_correcto": true,
      "timestamp": "2024-01-15T10:00:00Z"
    }
  ],
  "questions_asked": [
    {
      "pregunta": "¿Qué es una variable?",
      "respuesta": "Una variable es un símbolo...",
      "timestamp": "2024-01-15T09:30:00Z"
    }
  ]
}
```

#### `GET /learning/session/{session_id}/stats`
Obtiene estadísticas resumidas de una sesión.

**Response JSON:**
```json
{
  "session_id": "session_789",
  "topic": "Álgebra básica",
  "subtopic": "Ecuaciones lineales",
  "concepts_learned": 3,
  "concepts_list": [
    "Variables y constantes",
    "Operaciones básicas con variables",
    "Resolución de ecuaciones simples"
  ],
  "total_exercises": 8,
  "correct_exercises": 6,
  "accuracy_percentage": 75.0,
  "free_questions_asked": 12,
  "total_study_time_minutes": 45.5,
  "status": "active",
  "last_accessed": "2024-01-15T10:30:00Z"
}
```

#### `POST /learning/session/{session_id}/reactivate`
Reactiva una sesión pausada o completada.

**Response JSON:**
```json
{
  "message": "Sesión reactivada exitosamente",
  "session_id": "session_789"
}
```

#### `POST /learning/session/{session_id}/pause`
Pausa una sesión activa.

**Response JSON:**
```json
{
  "message": "Sesión pausada exitosamente",
  "session_id": "session_789"
}
```

#### `POST /learning/session/{session_id}/complete`
Marca una sesión como completada.

**Response JSON:**
```json
{
  "session_id": "session_789",
  "message": "Sesión completada exitosamente",
  "concepts_learned": 5,
  "next_steps": "Puedes generar ejercicios o un reporte de tu aprendizaje"
}
```

#### `GET /learning/sessions/{user_id}`
Obtiene todas las sesiones de aprendizaje de un usuario.

**Query Parameters:**
- `status` (opcional): Filtra por estado (active, completed, paused)

**Response JSON:**
```json
{
  "user_id": "user123",
  "status_filter": "active",
  "sessions": [
    {
      "session_id": "session_789",
      "topic": "Álgebra básica",
      "status": "active",
      "created_at": "2024-01-15T09:00:00Z"
    }
  ],
  "count": 1
}
```

#### `GET /learning/sessions/{user_id}/active`
Obtiene solo las sesiones activas de un usuario.

**Response JSON:**
```json
{
  "user_id": "user123",
  "active_sessions": [
    {
      "session_id": "session_789",
      "topic": "Álgebra básica",
      "status": "active",
      "last_accessed": "2024-01-15T10:30:00Z"
    }
  ],
  "count": 1
}
```

### 🎯 3. Tutor IA Completo

#### `GET /tutor/dashboard/{user_id}`
Dashboard completo del estudiante para el frontend.

**Response JSON:**
```json
{
  "user_id": "user123",
  "active_sessions": [
    {
      "session_id": "session_789",
      "topic": "Álgebra básica",
      "status": "active"
    }
  ],
  "progress_summary": {
    "nivel_actual": "intermedio",
    "total_sessions": 5,
    "total_study_time_minutes": 245.5,
    "total_concepts_learned": 18,
    "accuracy_percentage": 78.5
  },
  "quick_recommendations": {
    "next_topic": "Geometría básica",
    "daily_advice": "Practica resolver 3-4 ejercicios diarios para mantener el ritmo",
    "motivation": "¡Excelente progreso! Estás dominando el álgebra básica."
  },
  "areas_to_improve": [
    "Factorización de polinomios",
    "Sistemas de ecuaciones"
  ],
  "strong_areas": [
    "Ecuaciones lineales simples",
    "Operaciones con variables"
  ],
  "generated_at": "2024-01-15T10:30:00Z"
}
```

#### `GET /tutor/progress/{user_id}`
Análisis completo del progreso del usuario.

**Response JSON:**
```json
{
  "nivel_actual": "intermedio",
  "areas_fuertes": [
    "Ecuaciones lineales simples",
    "Operaciones con variables",
    "Resolución de sistemas 2x2"
  ],
  "areas_debiles": [
    "Factorización de polinomios",
    "Ecuaciones cuadráticas",
    "Problemas de aplicación"
  ],
  "siguiente_tema_recomendado": "Geometría básica",
  "dificultad_recomendada": "intermedio",
  "consejos_mejora": [
    "Practica más ejercicios de factorización",
    "Revisa los conceptos de ecuaciones cuadráticas",
    "Trabaja en problemas de aplicación paso a paso"
  ],
  "motivacion": "¡Excelente progreso! Has dominado el 75% del álgebra básica.",
  "tiempo_estudio_sugerido": "30-45 minutos diarios",
  "estadisticas_reales": {
    "overall_accuracy": 78.5,
    "total_exercises": 45,
    "correct_exercises": 35,
    "study_sessions": 8,
    "avg_session_duration": 32.5
  }
}
```

#### `GET /tutor/recommendations/{user_id}`
Recomendaciones personalizadas completas.

**Response JSON:**
```json
{
  "progress_analysis": {
    "nivel_actual": "intermedio",
    "areas_fuertes": ["Ecuaciones lineales", "Variables"],
    "areas_debiles": ["Factorización", "Ecuaciones cuadráticas"],
    "siguiente_tema_recomendado": "Geometría básica",
    "dificultad_recomendada": "intermedio"
  },
  "personalized_advice": {
    "consejo_principal": "Enfócate en practicar factorización durante los próximos días",
    "estrategias_estudio": [
      "Dedica 15 minutos diarios a ejercicios de factorización",
      "Usa diagramas visuales para ecuaciones cuadráticas",
      "Practica problemas de aplicación en pasos pequeños"
    ],
    "ejercicios_recomendados": [
      "Factorización de trinomios",
      "Diferencia de cuadrados",
      "Problemas de aplicación básicos"
    ],
    "habitos_sugeridos": [
      "Estudia a la misma hora cada día",
      "Toma descansos de 5 minutos cada 25 minutos",
      "Revisa conceptos anteriores semanalmente"
    ],
    "mensaje_motivacional": "¡Estás progresando genial! Cada error es una oportunidad de aprender.",
    "proximos_pasos": [
      "Completar 5 ejercicios de factorización",
      "Repasar fórmula cuadrática",
      "Practicar un problema de aplicación"
    ],
    "tiempo_estudio_diario": "30-45 minutos",
    "frecuencia_recomendada": "5-6 días por semana"
  },
  "next_topic_recommendation": {
    "tema_recomendado": "Geometría básica",
    "razon": "Has dominado suficiente álgebra para avanzar",
    "prerequisitos": [
      "Ecuaciones lineales",
      "Operaciones básicas",
      "Resolución de problemas"
    ],
    "dificultad_estimada": "intermedio",
    "tiempo_estimado": "2-3 semanas",
    "conceptos_clave": [
      "Perímetros y áreas",
      "Ángulos y triángulos",
      "Teorema de Pitágoras"
    ]
  },
  "generated_at": "2024-01-15T10:30:00Z"
}
```

#### `POST /tutor/exercises/adaptive`
Genera ejercicios adaptativos basados en el progreso del usuario.

**Request JSON:**
```json
{
  "user_id": "user123",
  "topic": "Álgebra básica",
  "cantidad": 5
}
```

**Response JSON:**
```json
{
  "user_id": "user123",
  "topic": "Álgebra básica",
  "exercises": [
    {
      "exercise_id": "ex456",
      "pregunta": "Resuelve la ecuación: 3x - 7 = 14",
      "respuesta_correcta": "x = 7",
      "tema": "Álgebra básica",
      "subtema": "Ecuaciones lineales",
      "es_multiple_choice": false,
      "opciones": null,
      "solucion": [
        "3x - 7 = 14",
        "3x = 14 + 7",
        "3x = 21",
        "x = 21/3",
        "x = 7"
      ],
      "pistas": [
        "Suma 7 a ambos lados",
        "Divide entre 3"
      ],
      "concepto_principal": "Ecuaciones lineales",
      "nivel": "intermedio"
    }
  ],
  "adaptation_info": "Ejercicios generados basados en tu progreso personal",
  "count": 5
}
```

#### `GET /tutor/exercises/{user_id}/next-batch`
Obtiene el siguiente lote de ejercicios recomendados.

**Query Parameters:**
- `topic` (requerido): El tema para generar ejercicios
- `count` (opcional): Número de ejercicios (default: 3)

**Response JSON:**
```json
{
  "user_id": "user123",
  "topic": "Álgebra básica",
  "exercises": [
    {
      "exercise_id": "ex789",
      "pregunta": "Factoriza: x² - 9",
      "respuesta_correcta": "(x+3)(x-3)",
      "nivel": "intermedio"
    }
  ],
  "difficulty_level": "intermedio",
  "personalized_note": "Estos ejercicios están adaptados a tu nivel actual: intermedio",
  "tips": [
    "Recuerda la fórmula de diferencia de cuadrados",
    "Verifica tu respuesta expandiendo el resultado"
  ]
}
```

#### `POST /tutor/exercise/complete`
Completa un ejercicio con seguimiento de progreso.

**Request JSON:**
```json
{
  "user_id": "user123",
  "session_id": "session_789",
  "exercise_id": "ex456",
  "user_answer": "x = 7",
  "is_correct": true,
  "time_taken": 120 // segundos, opcional
}
```

**Response JSON (si es correcto):**
```json
{
  "message": "¡Excelente! Ejercicio completado correctamente",
  "result": "correcto",
  "motivation": "¡Sigue así! Estás progresando muy bien."
}
```

**Response JSON (si es incorrecto):**
```json
{
  "message": "Ejercicio completado",
  "result": "incorrecto",
  "advice": "Enfócate en practicar factorización durante los próximos días",
  "motivation": "¡No te desanimes! Cada error es una oportunidad de aprender.",
  "next_steps": [
    "Revisa los pasos de factorización",
    "Practica con ejercicios más simples",
    "Pide ayuda si lo necesitas"
  ]
}
```

#### `POST /tutor/concept/learn`
Registra el aprendizaje de un concepto con seguimiento.

**Request JSON:**
```json
{
  "user_id": "user123",
  "session_id": "session_789",
  "concept": "Variables y constantes",
  "explanation": "Una variable es un símbolo que representa un número desconocido"
}
```

**Response JSON:**
```json
{
  "message": "Concepto 'Variables y constantes' aprendido y registrado",
  "session_id": "session_789",
  "progress_updated": true
}
```

### 📝 4. Ejercicios Tradicionales

#### `POST /exercises/generate`
Genera ejercicios para un tema específico (método tradicional).

**Request JSON:**
```json
{
  "user_id": "user123",
  "topic": "Álgebra básica",
  "subtopic": "Ecuaciones lineales", // opcional
  "nivel": "intermedio", // facil, intermedio, dificil
  "cantidad": 5
}
```

**Response JSON:**
```json
{
  "topic": "Álgebra básica",
  "subtopic": "Ecuaciones lineales",
  "nivel": "intermedio",
  "exercises": [
    {
      "exercise_id": "ex123",
      "pregunta": "Resuelve: 2x + 5 = 13",
      "respuesta_correcta": "x = 4",
      "solucion": ["2x = 13 - 5", "2x = 8", "x = 4"],
      "pistas": ["Resta 5 de ambos lados", "Divide entre 2"]
    }
  ],
  "message": "Se generaron 5 ejercicios de Álgebra básica"
}
```

#### `GET /exercises/topic/{topic}`
Obtiene ejercicios guardados por tema.

**Query Parameters:**
- `nivel` (opcional): Filtra por nivel de dificultad
- `limit` (opcional): Número máximo de ejercicios (default: 5)

**Response JSON:**
```json
{
  "topic": "Álgebra básica",
  "nivel": "intermedio",
  "exercises": [
    {
      "exercise_id": "ex123",
      "pregunta": "Resuelve: 2x + 5 = 13",
      "respuesta_correcta": "x = 4"
    }
  ],
  "count": 3
}
```

#### `POST /exercises/submit`
Envía respuesta a un ejercicio (método tradicional).

**Request JSON:**
```json
{
  "user_id": "user123",
  "exercise_id": "ex123",
  "respuesta_usuario": "x = 4",
  "tiempo_respuesta": 120 // segundos, opcional
}
```

**Response JSON:**
```json
{
  "exercise_id": "ex123",
  "es_correcto": true,
  "respuesta_correcta": "x = 4",
  "feedback": "¡Correcto! Excelente trabajo.",
  "solucion": ["2x = 13 - 5", "2x = 8", "x = 4"],
  "pistas": [] // vacío si es correcto
}
```

#### `GET /exercises/stats/{user_id}`
Obtiene estadísticas de ejercicios del usuario.

**Query Parameters:**
- `topic` (opcional): Filtra por tema específico

**Response JSON:**
```json
{
  "user_id": "user123",
  "topic": "Álgebra básica",
  "stats": {
    "total_exercises": 25,
    "correct_exercises": 18,
    "accuracy_percentage": 72.0,
    "avg_time_per_exercise": 135.5,
    "topics_practiced": [
      "Ecuaciones lineales",
      "Factorización",
      "Sistemas de ecuaciones"
    ]
  }
}
```

### 📄 5. Reportes PDF

#### `GET /learning/session/{session_id}/pdf-report`
Genera y descarga el reporte PDF completo de una sesión.

**Response:** Archivo PDF descargable

**Nombre del archivo:** `reporte_aprendizaje_{topic}_{session_id}.pdf`

**Contenido del PDF:**
- Resumen de la sesión
- Conceptos aprendidos
- Ejercicios completados
- Estadísticas de progreso
- Recomendaciones personalizadas

#### `GET /learning/session/{session_id}/pdf-exercises`
Genera y descarga un PDF solo con los ejercicios de una sesión.

**Response:** Archivo PDF descargable

**Nombre del archivo:** `ejercicios_{topic}_{session_id}.pdf`

**Contenido del PDF:**
- Lista de ejercicios resueltos
- Respuestas del usuario
- Soluciones correctas
- Comentarios y retroalimentación

#### `GET /learning/report/{session_id}`
Genera reporte JSON de una sesión de aprendizaje.

**Response JSON:**
```json
{
  "session_id": "session_789",
  "user_id": "user123",
  "topic": "Álgebra básica",
  "subtopic": "Ecuaciones lineales",
  "concepts_learned": [
    "Variables y constantes",
    "Operaciones básicas con variables",
    "Resolución de ecuaciones simples"
  ],
  "level": "basico",
  "status": "completed",
  "created_at": "2024-01-15T09:00:00Z",
  "updated_at": "2024-01-15T11:30:00Z",
  "exercise_stats": {
    "total_exercises": 12,
    "correct_exercises": 9,
    "accuracy_percentage": 75.0
  },
  "message": "Reporte generado exitosamente"
}
```

### 🎮 6. Demo y Testing

#### `GET /test/tutor-demo/{user_id}`
Endpoint de demostración que ejecuta todas las funcionalidades del tutor.

**Response JSON:**
```json
{
  "message": "🎓 Demo del Tutor Completo ejecutada exitosamente",
  "user_id": "user123",
  "demo_results": {
    "session_created": "session_demo_123",
    "adaptive_exercises": 2,
    "progress_analysis": {
      "nivel": "principiante",
      "consejos": 3
    },
    "recommendations": {
      "next_topic": "Geometría básica",
      "advice": "Practica ecuaciones lineales diariamente"
    }
  },
  "next_steps": [
    "Ver dashboard: GET /tutor/dashboard/user123",
    "Chatear en sesión: POST /learning/session/session_demo_123/chat",
    "Obtener más ejercicios: GET /tutor/exercises/user123/next-batch?topic=Álgebra básica",
    "Generar PDF: GET /learning/session/session_demo_123/pdf-report"
  ],
  "status": "success"
}
```

### ⚡ 7. Endpoints de Sistema

#### `GET /`
Información general del microservicio y documentación de endpoints.

**Response JSON:**
```json
{
  "message": "🎓 Matemix AI - Tutor Completo de Matemáticas con IA Avanzada",
  "version": "4.0.0",
  "description": "Sistema completo de tutoría matemática con IA...",
  "features": [
    "🧠 Chat inteligente con filtro matemático avanzado",
    "📚 Sesiones de aprendizaje persistentes y contextuales",
    "🎯 Ejercicios adaptativos basados en progreso individual"
  ],
  "api_sections": {
    "🎯 Tutor IA Completo": {...},
    "📚 Sesiones de Aprendizaje": {...},
    "📄 Reportes y Análisis": {...}
  }
}
```

#### `GET /health`
Verificación de estado del servicio.

**Response JSON:**
```json
{
  "status": "healthy"
}
```

## 🔄 Flujos de Integración Frontend

### Flujo Completo Recomendado

1. **Obtener Dashboard:**
   ```
   GET /tutor/dashboard/{user_id}
   ```

2. **Ver Recomendaciones:**
   ```
   GET /tutor/recommendations/{user_id}
   ```

3. **Crear/Reactivar Sesión:**
   ```
   POST /learning/session/create
   ```

4. **Chatear en la Sesión:**
   ```
   POST /learning/session/{session_id}/chat
   ```

5. **Solicitar Ejercicios Adaptativos:**
   ```
   POST /tutor/exercises/adaptive
   ```

6. **Completar Ejercicios:**
   ```
   POST /tutor/exercise/complete
   ```

7. **Ver Progreso Actualizado:**
   ```
   GET /tutor/progress/{user_id}
   ```

8. **Generar Reportes PDF:**
   ```
   GET /learning/session/{session_id}/pdf-report
   ```

### Flujo para Chat Libre

1. **Iniciar Chat:**
   ```
   POST /chat-stream
   ```

2. **Listar Conversaciones:**
   ```
   GET /conversations/{user_id}
   ```

3. **Ver Conversación Específica:**
   ```
   GET /conversation/{user_id}/{conversation_id}
   ```

### Flujo para Ejercicios Tradicionales

1. **Generar Ejercicios:**
   ```
   POST /exercises/generate
   ```

2. **Enviar Respuestas:**
   ```
   POST /exercises/submit
   ```

3. **Ver Estadísticas:**
   ```
   GET /exercises/stats/{user_id}
   ```

## 🛡️ Manejo de Errores

Todos los endpoints pueden retornar los siguientes códigos de error:

- **400 Bad Request:** Datos de entrada inválidos
- **404 Not Found:** Recurso no encontrado
- **403 Forbidden:** Acceso denegado
- **500 Internal Server Error:** Error interno del servidor

**Formato de respuesta de error:**
```json
{
  "detail": "Descripción del error"
}
```

## 🎯 Arquitectura de Contexto

El sistema utiliza **Qdrant Vector Database** para gestionar tres tipos de contexto:

1. **Contexto de Conversación:** Interacciones específicas por conversación
2. **Contexto de Sesión:** Aprendizaje dentro de sesiones estructuradas  
3. **Contexto General:** Progreso y conocimiento global del usuario

### Metadatos de Contexto

Cada entrada en Qdrant incluye metadatos que permiten:
- Filtrar por usuario, conversación o sesión
- Identificar el tipo de interacción
- Rastrear el progreso temporal
- Asociar con temas específicos

## 📊 Análisis de Progreso

El sistema proporciona análisis detallado que incluye:

- **Nivel actual del estudiante**
- **Áreas fuertes y débiles**
- **Siguiente tema recomendado**
- **Consejos personalizados de mejora**
- **Estadísticas de rendimiento**
- **Motivación personalizada**
- **Tiempo de estudio sugerido**

## 🎨 Personalización con IA

La IA del sistema proporciona:

- **Detección automática de nivel de competencia**
- **Adaptación de dificultad en tiempo real**
- **Generación de ejercicios personalizados**
- **Consejos motivacionales específicos**
- **Recomendaciones de estudio personalizadas**
- **Análisis de patrones de aprendizaje**

## 📱 Consideraciones para Frontend

### Endpoints Críticos para UI

- **Dashboard:** `/tutor/dashboard/{user_id}`
- **Chat en Tiempo Real:** `/chat-stream` (Server-Sent Events)
- **Ejercicios Adaptativos:** `/tutor/exercises/adaptive`
- **Progreso:** `/tutor/progress/{user_id}`

### Gestión de Estado

Se recomienda mantener en el frontend:
- ID de usuario activo
- Sesión de aprendizaje activa
- Conversación actual
- Estado de progreso

### Optimización

- Cachear respuestas del dashboard
- Implementar loading states para PDFs
- Manejar reconexión para SSE
- Implementar retry logic para errores

---

## 🚀 Próximos Pasos

Para comenzar a usar el API:

1. Configura las variables de entorno
2. Inicia el servicio con `uvicorn main:app --reload`
3. Prueba el endpoint demo: `GET /test/tutor-demo/{user_id}`
4. Integra con tu frontend siguiendo los flujos documentados
5. Utiliza `/docs` para explorar la documentación interactiva de Swagger

¡El sistema está listo para proporcionar una experiencia de tutoría matemática completa y personalizada!.