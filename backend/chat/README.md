# 🎓 Matemix AI - Microservicio de Tutoría de Matemáticas con IA

## Descripción General

Matemix AI es un microservicio especializado en tutoría de matemáticas que utiliza inteligencia artificial para proporcionar una experiencia de aprendizaje personalizada. El sistema está diseñado con **separación clara de responsabilidades**: chat general para consultas rápidas y sesiones de aprendizaje para experiencias estructuradas con ejercicios.

## 🎯 Arquitectura: Separación de Responsabilidades

### 💬 Chat General (`/chat-stream`)
- **Propósito**: Consultas, explicaciones y orientación matemática
- **Características**: 
  - Solo responde preguntas relacionadas con matemáticas
  - Proporciona explicaciones conceptuales
  - Orienta sobre temas y niveles
  - **NO genera ejercicios ni maneja lógica de sesiones**

### 📚 Sesiones de Aprendizaje (`/learning/session/{id}/chat`)
- **Propósito**: Experiencia de aprendizaje estructurada y completa
- **Características**:
  - Genera ejercicios organizados por dificultad (3 fáciles, 4 intermedios, 3 difíciles)
  - Seguimiento de progreso individual
  - Contexto personalizado basado en la sesión
  - Reportes PDF detallados

## 🚀 Flujo de Sesiones de Aprendizaje

### 1. 🎯 Crear Sesión
```bash
POST /learning/session/create
```
```json
{
  "user_id": "user123",
  "topic": "Álgebra básica",
  "subtopic": "Ecuaciones lineales",
  "level": "basico"
}
```

### 2. 💬 Chat en la Sesión
```bash
POST /learning/session/{session_id}/chat
```
```json
{
  "user_id": "user123", 
  "message": "Quiero ejercicios de álgebra básica"
}
```

**El sistema automáticamente:**
- ✅ Detecta la intención de generar ejercicios
- ✅ Genera 10 ejercicios organizados por dificultad
- ✅ Los guarda vinculados a la sesión
- ✅ Proporciona respuesta contextual sin mostrar todos los ejercicios

### 3. 📝 Obtener Ejercicios Generados
```bash
GET /learning/session/{session_id}/exercises
```
```json
{
  "session_id": "session_789",
  "topic": "Álgebra básica",
  "exercises": [
    {
      "exercise_id": "ex1",
      "pregunta": "Resuelve: 2x + 5 = 13",
      "nivel": "facil",
      "respuesta_correcta": "x = 4"
    }
  ],
  "count": 10
}
```

### 4. 📊 Seguimiento de Progreso
```bash
GET /learning/session/{session_id}/stats
```

### 5. 📄 Generar Reporte PDF
```bash
GET /learning/session/{session_id}/pdf-report
```

## 🛠️ Instalación y Configuración

### Prerrequisitos
- Python 3.8+
- MongoDB
- Qdrant Vector Database
- Google Gemini API

### Dependencias
```bash
pip install -r requirements.txt
```

### Variables de Entorno
```python
# config.py
MONGODB_URL = "mongodb://localhost:27017"
QDRANT_URL = "http://localhost:6333"
GEMINI_API_KEY = "your-gemini-api-key"
```

### Ejecutar el Servicio
```bash
uvicorn main:app --reload --port 8000
```

## 📋 Documentación de Endpoints

### 💬 1. Chat General (Solo Consultas)

#### `POST /chat-stream`
Chat para consultas generales, explicaciones y orientación matemática. **NO genera ejercicios**.

**Request JSON:**
```json
{
  "user_id": "user123",
  "conversation_id": "conv456", // opcional
  "message": "¿Qué son las ecuaciones lineales?"
}
```

**Response (Server-Sent Events):**
```json
{
  "text": "Las ecuaciones lineales son expresiones matemáticas de primer grado...",
  "conversation_id": "conv456"
}
```

**Casos de uso:**
- ✅ "¿Qué son las fracciones?"
- ✅ "Explícame la geometría básica"
- ✅ "¿Cómo resolver ecuaciones?"
- ❌ "Quiero ejercicios" → Se orienta a crear sesión
- ❌ No genera ejercicios ni maneja lógica de sesiones

#### `GET /conversations/{user_id}`
Lista todas las conversaciones del chat general.

#### `GET /conversation/{user_id}/{conversation_id}`
Obtiene una conversación específica.

#### `DELETE /conversation/{user_id}/{conversation_id}`
Elimina una conversación.

### 📚 2. Sesiones de Aprendizaje (Con Ejercicios)

#### `POST /learning/session/create`
Crea una nueva sesión de aprendizaje estructurada.

**Request JSON:**
```json
{
  "user_id": "user123",
  "topic": "Álgebra básica",
  "subtopic": "Ecuaciones lineales",
  "level": "basico"
}
```

**Response JSON:**
```json
{
  "session_id": "session_789",
  "topic": "Álgebra básica",
  "teaching_plan": [
    "Variables y constantes",
    "Operaciones básicas",
    "Resolución de ecuaciones"
  ],
  "status": "active",
  "chat_endpoint": "/learning/session/session_789/chat"
}
```

#### `POST /learning/session/{session_id}/chat`
Chat interactivo dentro de la sesión que **SÍ puede generar ejercicios**.

**Request JSON:**
```json
{
  "user_id": "user123",
  "message": "Quiero ejercicios de práctica"
}
```

**Response (Server-Sent Events):**
```json
{
  "text": "¡Perfecto! He generado 10 ejercicios organizados por dificultad...",
  "session_id": "session_789",
  "topic": "Álgebra básica",
  "exercises_generated": 10
}
```

**Generación automática de ejercicios:**
- 🟢 3 ejercicios fáciles
- 🟡 4 ejercicios intermedios  
- 🔴 3 ejercicios difíciles
- Se guardan automáticamente vinculados a la sesión

#### `GET /learning/session/{session_id}/exercises`
Obtiene todos los ejercicios generados en la sesión.

**Response JSON:**
```json
{
  "session_id": "session_789",
  "topic": "Álgebra básica",
  "exercises": [
    {
      "exercise_id": "ex1",
      "pregunta": "Resuelve: 2x + 5 = 13",
      "respuesta_correcta": "x = 4",
      "nivel": "facil",
      "solucion": ["Resta 5 de ambos lados", "Divide entre 2"],
      "pistas": ["Aísla la variable x"]
    }
  ],
  "count": 10
}
```

#### `GET /learning/session/{session_id}/conversation`
Obtiene el historial completo de la conversación de la sesión de aprendizaje.

**Response JSON:**
```json
{
  "session_id": "session_789",
  "conversation_id": "learning_session_789",
  "user_id": "user123",
  "topic": "Álgebra básica",
  "level": "basico",
  "title": "Chat de sesión: Álgebra básica",
  "messages": [
    {
      "role": "user",
      "content": "Quiero ejercicios de álgebra",
      "timestamp": "2024-01-15T10:00:00Z"
    },
    {
      "role": "assistant", 
      "content": "¡Perfecto! He generado 10 ejercicios organizados por dificultad...",
      "timestamp": "2024-01-15T10:01:00Z"
    }
  ],
  "session_status": "active",
  "created_at": "2024-01-15T09:00:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

#### `GET /learning/session/{session_id}/history`
Historial completo de la sesión con todas las interacciones.

#### `GET /learning/session/{session_id}/stats`
Estadísticas resumidas de la sesión.

#### `GET /learning/session/{session_id}/pdf-report`
Genera y descarga reporte PDF completo.

#### `GET /learning/session/{session_id}/pdf-exercises`
Genera y descarga PDF solo con ejercicios.

### 📊 3. Gestión de Sesiones

#### `GET /learning/sessions/{user_id}`
Obtiene todas las sesiones del usuario (activas, pausadas, completadas).

#### `POST /learning/session/{session_id}/pause`
Pausa una sesión activa.

#### `POST /learning/session/{session_id}/reactivate`
Reactiva una sesión pausada.

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

## ⚙️ Configuración Técnica

### Base de Datos

#### MongoDB Collections
```javascript
// Conversaciones del chat general
conversations: {
  user_id: String,
  conversation_id: String,
  title: String,
  messages: Array,
  created_at: Date,
  updated_at: Date
}

// Sesiones de aprendizaje
learning_sessions: {
  session_id: String,
  user_id: String,
  topic: String,
  subtopic: String,
  level: String,
  concepts_covered: Array,
  status: String,
  interaction_history: Array,
  created_at: Date,
  updated_at: Date
}

// Ejercicios generados
exercises: {
  exercise_id: String,
  session_id: String,
  conversation_id: String,
  pregunta: String,
  respuesta_correcta: String,
  nivel: String,
  tema: String,
  generated_at: Date
}
```

#### Qdrant Collections
```python
# Contexto de conversaciones generales
general_context: {
  user_id: String,
  text: String,
  embedding: Vector,
  conversation_id: String,
  context_type: "conversation",
  metadata: {
    type: "general_math_chat",
    topic: "conversacion_general"
  }
}

# Contexto de sesiones de aprendizaje
session_context: {
  user_id: String,
  text: String,
  embedding: Vector,
  conversation_id: String,
  context_type: "conversation",
  metadata: {
    type: "learning_interaction",
    session_id: String,
    topic: String,
    exercises_generated: Number
  }
}
```

### Variables de Entorno
```bash
# config.py
MONGODB_URL=mongodb://localhost:27017/matemix
QDRANT_URL=http://localhost:6333
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-1.5-flash
EMBEDDING_MODEL=models/embedding-001
REDIS_URL=redis://localhost:6379  # opcional para cache
```

### Docker Compose
```yaml
version: '3.8'
services:
  matemix-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - MONGODB_URL=mongodb://mongo:27017/matemix
      - QDRANT_URL=http://qdrant:6333
    depends_on:
      - mongo
      - qdrant

  mongo:
    image: mongo:latest
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db

  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
    volumes:
      - qdrant_data:/qdrant/storage

volumes:
  mongo_data:
  qdrant_data:
```

## 🧪 Testing

### Endpoints de Prueba

#### `GET /test/tutor-demo/{user_id}`
Endpoint de demostración que muestra el flujo completo:
- Crea una sesión de aprendizaje
- Simula el flujo correcto: chat general vs sesiones
- Genera ejercicios automáticamente
- Muestra análisis de progreso

#### `GET /health`
Health check del servicio.

### Pruebas Manuales

```bash
# 1. Verificar que chat general NO genera ejercicios
curl -X POST "http://localhost:8000/chat-stream" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test", "message": "Quiero ejercicios"}'

# 2. Crear sesión y verificar generación de ejercicios
curl -X POST "http://localhost:8000/learning/session/create" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test", "topic": "Álgebra", "level": "basico"}'

# 3. Generar ejercicios en sesión
curl -X POST "http://localhost:8000/learning/session/{session_id}/chat" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test", "message": "Quiero ejercicios"}'
```

## 📝 Changelog

### v4.1.0 - Mejor Integración Frontend
- ✅ Nuevo endpoint `/learning/session/{session_id}/conversation` 
- ✅ Acceso directo al historial de chat de cada sesión de aprendizaje
- ✅ Relación 1:1 entre session_id y conversation_id
- ✅ Respuesta enriquecida con metadatos de la sesión
- ✅ Ejemplos de integración frontend detallados

### v4.0.0 - Separación de Responsabilidades
- ✅ Chat general (`/chat-stream`) limitado a consultas y explicaciones
- ✅ Sesiones de aprendizaje como único lugar para generar ejercicios
- ✅ Eliminación de lógica especial e intenciones del chat general
- ✅ Clarificación de responsabilidades en documentación

### v3.x.x - Versiones Anteriores
- Chat inteligente con generación de ejercicios mixta
- Lógica de intenciones en chat general
- Responsabilidades mezcladas entre endpoints

## 🤝 Contribución

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

## 📜 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 📞 Soporte

Para soporte técnico o preguntas sobre la integración:
- Documentación API: `http://localhost:8000/docs`
- Endpoint de demo: `http://localhost:8000/test/tutor-demo/{user_id}`
- Health check: `http://localhost:8000/health`

## 🚀 Próximos Pasos

Para comenzar a usar el API:

1. Configura las variables de entorno
2. Inicia el servicio con `uvicorn main:app --reload`
3. Prueba el endpoint demo: `GET /test/tutor-demo/{user_id}`
4. Integra con tu frontend siguiendo los flujos documentados
5. Utiliza `/docs` para explorar la documentación interactiva de Swagger

¡El sistema está listo para proporcionar una experiencia de tutoría matemática completa y personalizada!.

## 🚀 Arquitectura Separada: Chat General vs Sesiones de Aprendizaje

### 💬 Chat General (`/chat-stream`)
**Propósito:** Consultas, explicaciones y orientación matemática

**Funcionalidades:**
- ✅ Responder preguntas de matemáticas
- ✅ Explicar conceptos teóricos
- ✅ Orientar al usuario sobre qué estudiar
- ✅ Recomendar crear sesiones de aprendizaje
- ❌ **NO genera ejercicios** (solo orienta al usuario)

**Cuando el usuario pide ejercicios:**
- Si tiene sesión activa → Lo dirige al chat de la sesión
- Si no tiene sesión → Le recomienda crear una sesión de aprendizaje

### 📚 Chat de Sesiones (`/learning/session/{session_id}/chat`)
**Propósito:** Aprendizaje estructurado con generación de ejercicios

**Funcionalidades:**
- ✅ Todo lo del chat general + contexto de sesión
- ✅ **Generación automática de ejercicios** (10 por set: 3-4-3)
- ✅ Seguimiento de progreso en la sesión  
- ✅ Ejercicios adaptativos al nivel de la sesión
- ✅ Conceptos contextualizados al tema de la sesión

### 🔄 Flujo Recomendado

#### Para Consultas Generales:
```http
POST /chat-stream
{
  "user_id": "user123",
  "message": "¿Qué es una derivada?"
}
```

#### Para Ejercicios:
```http
# 1. Crear sesión
POST /learning/session/create
{
  "user_id": "user123", 
  "topic": "Cálculo",
  "level": "intermedio"
}

# 2. Pedir ejercicios en la sesión
POST /learning/session/{session_id}/chat
{
  "user_id": "user123",
  "message": "Quiero ejercicios de derivadas"
}

# 3. Obtener ejercicios generados
GET /learning/session/{session_id}/exercises
```

### Ejemplo 2: Flujo Completo de Sesión de Aprendizaje

#### Paso 1: Crear Sesión
```bash
curl -X POST "http://localhost:8000/learning/session/create" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "topic": "Álgebra básica",
    "subtopic": "Ecuaciones lineales",
    "level": "basico"
  }'
```

#### Paso 2: Chatear en la Sesión
```bash
curl -X POST "http://localhost:8000/learning/session/session_789/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "message": "Quiero ejercicios de álgebra básica"
  }'
```

**Respuesta esperada:** Mensaje de confirmación y generación de ejercicios.

#### Paso 3: Obtener Historial de la Conversación
```bash
curl "http://localhost:8000/learning/session/session_789/conversation"
```

**Respuesta:** Historial completo de mensajes de la sesión con información enriquecida.

#### Paso 4: Obtener Ejercicios
```bash
curl "http://localhost:8000/learning/session/session_789/exercises"
```

#### Paso 5: Generar Reporte PDF
```bash
curl "http://localhost:8000/learning/session/session_789/pdf-report" \
  --output reporte_algebra.pdf
```

### Ejemplo 3: Flujo Frontend para Chat de Sesión

```javascript
// 1. Lista de sesiones del usuario
const sessions = await fetch(`/learning/sessions/${userId}/active`);

// 2. Al hacer click en una sesión, obtener su conversación
const sessionId = "session_789";
const conversation = await fetch(`/learning/session/${sessionId}/conversation`);

// 3. Mostrar historial en la UI
const messages = conversation.messages;
renderChatMessages(messages);

// 4. Enviar nuevo mensaje en la sesión
const response = await fetch(`/learning/session/${sessionId}/chat`, {
  method: 'POST',
  body: JSON.stringify({
    user_id: userId,
    message: 'Explícame las ecuaciones lineales'
  })
});

// 5. Procesar respuesta streaming
const reader = response.body.getReader();
while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  
  const text = new TextDecoder().decode(value);
  const data = JSON.parse(text.replace('data: ', ''));
  appendMessageToChat(data.text);
}

// 6. Si el usuario pide ejercicios, obtenerlos después
if (userMessage.includes('ejercicios')) {
  const exercises = await fetch(`/learning/session/${sessionId}/exercises`);
  displayExercises(exercises.exercises);
}
```

### Ejemplo 4: Diferencia Clara de Responsabilidades

```javascript
// ❌ INCORRECTO: Buscar ejercicios en chat general
const chatResponse = await fetch('/chat-stream', {
  body: JSON.stringify({ message: 'Quiero ejercicios' })
});
// → Solo recibirás orientación, no ejercicios

// ✅ CORRECTO: Buscar ejercicios en sesión
const sessionResponse = await fetch(`/learning/session/${sessionId}/chat`, {
  body: JSON.stringify({ message: 'Quiero ejercicios' })
});
// → Se generan automáticamente 10 ejercicios organizados

// ✅ CORRECTO: Obtener ejercicios ya generados
const exercises = await fetch(`/learning/session/${sessionId}/exercises`);
// → Lista completa de ejercicios de la sesión

// ✅ CORRECTO: Obtener historial de la sesión
const conversation = await fetch(`/learning/session/${sessionId}/conversation`);
// → Historial completo de chat de la sesión
```

### Sistema de Ejercicios Inteligente

#### Flujo de Ejercicios Paso a Paso

1. **Generación de Ejercicios:**
   ```bash
   POST /learning/session/{session_id}/chat
   Body: {"user_id": "user123", "message": "Quiero ejercicios"}
   ```
   
   **Respuesta:** "¡Te he asignado 10 ejercicios! Para empezar, dime: 'Ejercicio 1', 'Ejercicio 5' o cualquier número del 1 al 10."

2. **Trabajar en un Ejercicio Específico:**
   ```bash
   POST /learning/session/{session_id}/chat
   Body: {"user_id": "user123", "message": "Ejercicio 3"}
   ```
   
   **Respuesta:** Muestra el ejercicio 3 completo con opciones de ayuda.

3. **Solicitar Pistas:**
   ```bash
   POST /learning/session/{session_id}/chat
   Body: {"user_id": "user123", "message": "Dame una pista"}
   ```
   
   **Respuesta:** Proporciona una pista contextualizada sin revelar la respuesta.

4. **Enviar Respuesta:**
   ```bash
   POST /learning/session/{session_id}/chat
   Body: {"user_id": "user123", "message": "Mi respuesta es: 42"}
   ```
   
   **Respuesta:** Evalúa la respuesta y proporciona retroalimentación detallada.

#### Patrones de Reconocimiento Inteligente

El sistema reconoce automáticamente diferentes tipos de mensajes:

| Patrón del Usuario | Respuesta del Sistema |
|---|---|
| `"Ejercicio 1"`, `"Ejercicio 5"` | Muestra el ejercicio específico |
| `"Ayuda con ejercicio 2"` | Ayuda contextualizada para ese ejercicio |
| `"Dame una pista"` | Pista para el ejercicio actual |
| `"Mi respuesta es: 15"` | Evaluación de la respuesta |
| `"Respuesta: x = 3"` | Evaluación automática |
| `"42"` (solo número) | Interpreta como respuesta al ejercicio actual |

#### Estados de Ejercicios

- **assigned**: Ejercicio generado pero no iniciado
- **in_progress**: Usuario está trabajando en él
- **completed**: Respondido correctamente
- **needs_review**: Respuesta incorrecta, necesita revisión