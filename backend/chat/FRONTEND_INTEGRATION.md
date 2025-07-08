# 🎓 Matemix AI - Guía de Integración Frontend

## Sistema de Tutor Completo con IA Avanzada

### 🚀 Características Principales

1. **Análisis de Progreso Inteligente**: Seguimiento automático del rendimiento del estudiante
2. **Ejercicios Adaptativos**: Generación automática basada en nivel y debilidades
3. **Recomendaciones Personalizadas**: Consejos y motivación adaptados al estudiante
4. **Sesiones Persistentes**: Continúa aprendiendo días después
5. **Seguimiento en Vector DB**: Contexto completo del estudiante en Qdrant

---

## 📊 Dashboard Principal del Estudiante

### Endpoint: `GET /tutor/dashboard/{user_id}`

**Respuesta de ejemplo:**
```json
{
  "user_id": "estudiante123",
  "active_sessions": [
    {
      "session_id": "sess_001",
      "topic": "Álgebra básica",
      "status": "active",
      "last_accessed": "2025-07-08T15:30:00"
    }
  ],
  "progress_summary": {
    "nivel_actual": "intermedio",
    "total_sessions": 5,
    "total_study_time_minutes": 180,
    "total_concepts_learned": 15,
    "accuracy_percentage": 78.5
  },
  "quick_recommendations": {
    "next_topic": "Ecuaciones lineales",
    "daily_advice": "Practica 15 minutos diarios para consolidar el álgebra",
    "motivation": "¡Excelente progreso! Ya dominas el 78% de los ejercicios."
  },
  "areas_to_improve": ["Factorización", "Sistemas de ecuaciones"],
  "strong_areas": ["Operaciones básicas", "Simplificación"]
}
```

### 🎯 Uso en Frontend:
```javascript
// Cargar dashboard al inicio
const loadDashboard = async (userId) => {
  const response = await fetch(`/tutor/dashboard/${userId}`);
  const dashboard = await response.json();
  
  // Mostrar progreso
  updateProgressBar(dashboard.progress_summary.accuracy_percentage);
  showRecommendations(dashboard.quick_recommendations);
  displayActiveSessions(dashboard.active_sessions);
}
```

---

## 🎯 Ejercicios Adaptativos

### Endpoint: `POST /tutor/exercises/adaptive`

**Request:**
```json
{
  "user_id": "estudiante123",
  "topic": "Álgebra básica",
  "cantidad": 5
}
```

**Respuesta:**
```json
{
  "user_id": "estudiante123",
  "topic": "Álgebra básica",
  "exercises": [
    {
      "exercise_id": "adaptive_algebra_intermedio_1_4567",
      "pregunta": "Resuelve para x: 2x + 5 = 13",
      "respuesta_correcta": "4",
      "es_multiple_choice": true,
      "opciones": ["2", "3", "4", "5"],
      "pistas": ["Aísla la variable x", "Resta 5 de ambos lados"],
      "nivel": "intermedio",
      "adaptation_level": "intermedio",
      "user_accuracy_when_generated": 78.5
    }
  ],
  "adaptation_info": "Ejercicios generados basados en tu progreso personal"
}
```

### 🎯 Uso en Frontend:
```javascript
// Generar ejercicios adaptativos
const getAdaptiveExercises = async (userId, topic) => {
  const response = await fetch('/tutor/exercises/adaptive', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: userId,
      topic: topic,
      cantidad: 3
    })
  });
  
  const data = await response.json();
  displayExercises(data.exercises);
  showAdaptationInfo(data.adaptation_info);
}
```

---

## ✅ Completar Ejercicios con Tracking

### Endpoint: `POST /tutor/exercise/complete`

**Request:**
```json
{
  "user_id": "estudiante123",
  "session_id": "sess_001",
  "exercise_id": "adaptive_algebra_intermedio_1_4567",
  "user_answer": "4",
  "is_correct": true,
  "time_taken": 45
}
```

**Respuesta (Correcto):**
```json
{
  "message": "¡Excelente! Ejercicio completado correctamente",
  "result": "correcto",
  "motivation": "¡Sigue así! Estás progresando muy bien."
}
```

**Respuesta (Incorrecto):**
```json
{
  "message": "Ejercicio completado",
  "result": "incorrecto",
  "advice": "Revisa el orden de operaciones algebraicas",
  "motivation": "No te preocupes, los errores son parte del aprendizaje",
  "next_steps": [
    "Repasa la propiedad distributiva",
    "Practica más ejercicios similares",
    "Pide ayuda con conceptos específicos"
  ]
}
```

### 🎯 Uso en Frontend:
```javascript
// Enviar respuesta del ejercicio
const submitExercise = async (userId, sessionId, exerciseId, answer, timeSpent) => {
  const isCorrect = checkAnswer(answer, correctAnswer);
  
  const response = await fetch('/tutor/exercise/complete', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: userId,
      session_id: sessionId,
      exercise_id: exerciseId,
      user_answer: answer,
      is_correct: isCorrect,
      time_taken: timeSpent
    })
  });
  
  const result = await response.json();
  showFeedback(result);
  
  // Si es incorrecto, mostrar consejos
  if (result.result === 'incorrecto') {
    showAdviceModal(result.advice, result.next_steps);
  }
}
```

---

## 💡 Recomendaciones Personalizadas

### Endpoint: `GET /tutor/recommendations/{user_id}`

**Respuesta:**
```json
{
  "progress_analysis": {
    "nivel_actual": "intermedio",
    "areas_fuertes": ["Operaciones básicas", "Simplificación"],
    "areas_debiles": ["Factorización", "Sistemas de ecuaciones"],
    "consejos_mejora": [
      "Practica factorización 10 minutos diarios",
      "Usa ejemplos visuales para sistemas de ecuaciones"
    ],
    "motivacion": "¡Estás mejorando constantemente! Ya dominas el álgebra básica."
  },
  "personalized_advice": {
    "consejo_principal": "Enfócate en la factorización, es clave para ecuaciones avanzadas",
    "estrategias_estudio": [
      "Divide problemas complejos en pasos simples",
      "Practica 15-20 minutos diarios",
      "Revisa errores para identificar patrones"
    ],
    "mensaje_motivacional": "Cada error es una oportunidad de aprender algo nuevo"
  },
  "next_topic_recommendation": {
    "tema_recomendado": "Ecuaciones cuadráticas",
    "razon": "Tienes buena base en álgebra lineal",
    "dificultad_estimada": "intermedio"
  }
}
```

---

## 🎮 Chat Inteligente Integrado

### Endpoint: `POST /chat-stream`

El chat ahora detecta automáticamente:
- Si el usuario tiene sesiones activas
- Su nivel actual de progreso  
- Qué ejercicios necesita
- Recomendaciones personalizadas

**Ejemplo de conversación:**
```
Usuario: "Quiero hacer ejercicios de álgebra"

IA: "¡Perfecto! Veo que estás en nivel intermedio con 78% de precisión. 
He generado ejercicios adaptativos para ti.

Opciones:
🎯 Ejercicios personalizados: GET /tutor/exercises/estudiante123/next-batch?topic=álgebra
📊 Ver tu progreso: GET /tutor/dashboard/estudiante123
📚 Continuar tu sesión activa de álgebra básica

¿Qué prefieres hacer?"
```

---

## 📄 Reportes PDF Completos

### Endpoint: `GET /learning/session/{session_id}/pdf-report`

Genera PDF con:
- ✅ Información completa de la sesión
- 📊 Estadísticas de progreso
- 📚 Conceptos aprendidos
- 📝 Ejercicios completados con respuestas
- 💬 Preguntas realizadas
- 📈 Cronología de aprendizaje

---

## 🔄 Flujo Completo de Integración

```javascript
class MatemixTutor {
  constructor(userId) {
    this.userId = userId;
  }
  
  // 1. Cargar estado inicial
  async initialize() {
    this.dashboard = await this.getDashboard();
    this.recommendations = await this.getRecommendations();
    this.setupUI();
  }
  
  // 2. Obtener ejercicios adaptativos
  async getNextExercises(topic) {
    return await fetch(`/tutor/exercises/${this.userId}/next-batch?topic=${topic}`);
  }
  
  // 3. Procesar respuesta del estudiante
  async submitAnswer(exerciseId, sessionId, answer, timeSpent) {
    const result = await this.completeExercise(exerciseId, sessionId, answer, timeSpent);
    this.updateProgress();
    return result;
  }
  
  // 4. Actualizar estado
  async updateProgress() {
    this.dashboard = await this.getDashboard();
    this.refreshUI();
  }
  
  // 5. Chat inteligente
  async chatWithAI(message) {
    // El chat ahora incluye contexto automático del progreso
    return await this.sendChatMessage(message);
  }
}

// Uso
const tutor = new MatemixTutor('estudiante123');
await tutor.initialize();
```

---

## 🎯 Endpoints Clave para Frontend

| Funcionalidad | Endpoint | Método | Descripción |
|---------------|----------|---------|-------------|
| **Dashboard** | `/tutor/dashboard/{user_id}` | GET | Estado completo del estudiante |
| **Ejercicios Adaptativos** | `/tutor/exercises/adaptive` | POST | Ejercicios personalizados |
| **Completar Ejercicio** | `/tutor/exercise/complete` | POST | Enviar respuesta con tracking |
| **Recomendaciones** | `/tutor/recommendations/{user_id}` | GET | Consejos personalizados |
| **Chat Inteligente** | `/chat-stream` | POST | Chat con contexto automático |
| **Sesión Nueva** | `/learning/session/create` | POST | Crear sesión de aprendizaje |
| **Chat en Sesión** | `/learning/session/{id}/chat` | POST | Chat dentro de sesión |
| **Reporte PDF** | `/learning/session/{id}/pdf-report` | GET | Descargar progreso |

---

## 🚀 ¡Tutor Completo Listo!

El sistema ahora incluye:
- ✅ **Análisis de progreso inteligente**
- ✅ **Ejercicios adaptativos automáticos** 
- ✅ **Recomendaciones personalizadas**
- ✅ **Seguimiento continuo en Vector DB**
- ✅ **Chat contextual avanzado**
- ✅ **Reportes PDF completos**
- ✅ **API completa para frontend**

**¡Matemix AI es ahora un tutor completo con IA que se adapta a cada estudiante!** 🎓✨
