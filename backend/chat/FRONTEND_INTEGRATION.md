# 📚 Matemix AI - Guía de Integración Frontend

## Endpoints Principales y Flujos

### 1. Chat General
- `POST /chat-stream` — Chat inteligente con IA, detecta intención, recomienda crear sesión, genera ejercicios, etc.
- `GET /conversation/{user_id}/{conversation_id}` — Obtener una conversación específica.
- `GET /conversations/{user_id}` — Listar todas las conversaciones del usuario.
- `DELETE /conversation/{user_id}/{conversation_id}` — Eliminar una conversación.

### 2. Sesiones de Aprendizaje
- `POST /learning/session/create` — Crear una nueva sesión de aprendizaje.
- `GET /learning/session/{session_id}` — Obtener detalles de una sesión.
- `POST /learning/session/{session_id}/teach/{concept_index}` — Explicar un concepto específico de la sesión.
- `POST /learning/session/{session_id}/complete` — Marcar una sesión como completada.
- `POST /learning/session/{session_id}/chat` — Chat dentro de una sesión de aprendizaje.
- `GET /learning/session/{session_id}/history` — Historial completo de la sesión (para mostrar todo lo aprendido).
- `GET /learning/session/{session_id}/stats` — Estadísticas resumidas de la sesión.
- `POST /learning/session/{session_id}/reactivate` — Reactivar una sesión pausada/completada.
- `POST /learning/session/{session_id}/pause` — Pausar una sesión activa.
- `GET /learning/sessions/{user_id}` — Listar todas las sesiones del usuario.
- `GET /learning/sessions/{user_id}/active` — Listar solo sesiones activas/pausadas.
- `POST /learning/session/{session_id}/interaction` — Agregar interacción manual al historial de la sesión.

### 3. Ejercicios
- `POST /exercises/generate` — Generar ejercicios para un tema específico.
- `GET /exercises/topic/{topic}` — Obtener ejercicios guardados por tema.
- `POST /exercises/submit` — Enviar respuesta a un ejercicio (básico).
- `GET /exercises/stats/{user_id}` — Estadísticas de ejercicios del usuario.
- `POST /tutor/exercises/adaptive` — Generar ejercicios adaptativos según el progreso del usuario.
- `POST /tutor/exercise/complete` — Completar un ejercicio con tracking y feedback personalizado.
- `GET /tutor/exercises/{user_id}/next-batch?topic=...` — Obtener el siguiente lote de ejercicios recomendados.

### 4. Reportes y PDFs
- `GET /learning/report/{session_id}` — Reporte JSON de la sesión (resumen).
- `GET /learning/session/{session_id}/pdf-report` — Descargar PDF completo de la sesión (historial, conceptos, ejercicios, progreso).
- `GET /learning/session/{session_id}/pdf-exercises` — Descargar PDF solo con los ejercicios de la sesión.

### 5. Progreso, Recomendaciones y Dashboard
- `GET /tutor/dashboard/{user_id}` — Dashboard completo del estudiante (progreso, sesiones, recomendaciones, etc).
- `GET /tutor/progress/{user_id}` — Análisis completo del progreso del usuario.
- `GET /tutor/recommendations/{user_id}` — Recomendaciones personalizadas (consejos, próximos pasos, motivación).

### 6. Demo y Salud
- `GET /test/tutor-demo/{user_id}` — Ejecuta un flujo de demo completo para pruebas.
- `GET /health` — Health check del backend.

---

## Ejemplo de Flujo Frontend

1. **Inicio:**
   - Llama a `GET /tutor/dashboard/{user_id}` para mostrar el estado general, sesiones activas, progreso y recomendaciones.
2. **Crear sesión:**
   - `POST /learning/session/create` con `{ user_id, topic, subtopic, level }`.
   - Muestra el plan de enseñanza y permite iniciar chat en la sesión.
3. **Chat en sesión:**
   - `POST /learning/session/{session_id}/chat` para interactuar y aprender conceptos, pedir ejercicios, etc.
   - Muestra historial con `GET /learning/session/{session_id}/history`.
4. **Ejercicios:**
   - Genera ejercicios adaptativos con `POST /tutor/exercises/adaptive` o por tema con `POST /exercises/generate`.
   - Envía respuestas con `POST /tutor/exercise/complete` (tracking completo) o `POST /exercises/submit` (básico).
   - Muestra feedback y consejos personalizados.
5. **Progreso y recomendaciones:**
   - Muestra análisis con `GET /tutor/progress/{user_id}` y recomendaciones con `GET /tutor/recommendations/{user_id}`.
6. **Reportes:**
   - Permite descargar PDF de la sesión con `GET /learning/session/{session_id}/pdf-report` o solo ejercicios con `GET /learning/session/{session_id}/pdf-exercises`.
7. **Demo:**
   - Prueba todo el flujo con `GET /test/tutor-demo/{user_id}`.

---

## Ejemplo de llamadas desde el frontend (pseudo-código)

```js
// 1. Dashboard inicial
const dashboard = await fetch(`/tutor/dashboard/${userId}`).then(r => r.json());

// 2. Crear sesión
const session = await fetch('/learning/session/create', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ user_id: userId, topic: 'Álgebra', level: 'basico' })
}).then(r => r.json());

// 3. Chat en sesión
const chatResp = await fetch(`/learning/session/${session.session_id}/chat`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ user_id: userId, message: 'Explícame fracciones' })
});

// 4. Generar ejercicios adaptativos
const exercises = await fetch('/tutor/exercises/adaptive', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ user_id: userId, topic: 'Álgebra', cantidad: 3 })
}).then(r => r.json());

// 5. Completar ejercicio
const feedback = await fetch('/tutor/exercise/complete', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ user_id: userId, session_id: session.session_id, exercise_id: exercises.exercises[0].exercise_id, user_answer: '4', is_correct: true })
}).then(r => r.json());

// 6. Descargar PDF
window.open(`/learning/session/${session.session_id}/pdf-report`);
```

---

## Resumen de Integración
- **Todos los endpoints están listos para integración directa.**
- **El historial, progreso, ejercicios y reportes son accesibles por endpoints dedicados.**
- **El chat IA y las sesiones están conectados y adaptan la experiencia automáticamente.**
- **Puedes mostrar el dashboard, recomendaciones, historial y ejercicios en cualquier momento.**

---

**¡Matemix AI es ahora un tutor completo, listo para usarse desde cualquier frontend moderno!**
