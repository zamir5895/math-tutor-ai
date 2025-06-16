# 📚 Content Service

## 📝 Descripción
Microservicio encargado de generar y gestionar ejercicios, exámenes y recursos educativos, utilizando IA para personalización y clasificación.

---

## 🗂️ Entidades

### `Exercise`
- `id` (UUID)
- `pregunta` (String)
- `solucion_paso_a_paso` (String)
- `pista` (String)
- `opciones` (Array<String>)
- `respuesta` (String)
- `concepto_principal` (String)
- `respuesta_correcta` (String)
- `dificultad` (Enum: "facil" | "medio" | "dificil")
- `subtopico_id` (UUID)
- `topico_id` (UUID)

### `Subtopico`
- `id` (UUID)
- `nombre` (String)
- `descripcion` (String)
- `video_referencia` (String)
- `ejercicios` (Array<UUID>)

### `Topico`
- `id` (UUID)
- `nombre` (String)
- `descripcion` (String)
- `subtopicos` (Array<UUID>)

### `ExamSubtopic`
- `id` (UUID)
- `title` (String)
- `exercises` (Array<UUID>)
- `subtopico_id` (UUID)
- `topic_id` (UUID)
- `classroom_id` (UUID)

### `ExamTopic`
- `id` (UUID)
- `title` (String)
- `exercises` (Array<UUID>)
- `topic_id` (UUID)
- `classroom_id` (UUID)

### `Exam`
- `id` (UUID)
- `title` (String)
- `exercises` (Array<UUID>)
- `classroom_id` (UUID)

### `PDFResource`
- `id` (UUID)
- `url` (String)
- `classroom_id` (UUID)

### `EjercicioResuelto`
- `id` (UUID)
- `alumno_id` (UUID)
- `exercise_id` (UUID)
- `subtopico_id` (UUID)
- `topico_id` (UUID)
- `fecha_resuelto` (Timestamp)
- `correcto` (Boolean)

---


## 🌐 Endpoints

| Método | Ruta                                         | Descripción                                                        |
|--------|----------------------------------------------|--------------------------------------------------------------------|
| POST   | /exercises/generate                          | Generar ejercicios con IA.                                         |
| GET    | /exercises/{id}                              | Obtener ejercicio por ID.                                          |
| GET    | /exercises/level/{dificultad}                | Listar ejercicios por nivel de dificultad.                         |
| POST   | /exercises/verify                            | Verificar respuesta de un ejercicio y los guarda el solved.        |
| POST   | /exercises/personalized                      | Generar ejercicios personalizados según peticion del alumno.       |
| GET    | /exercises/solved/count/topic/{id}           | Obtener cantidad de ejercicios resueltos por tema.                 |
| GET    | /exercises/solved/count/subtopic/{id}        | Obtener cantidad de ejercicios resueltos por subtema.              |
| POST   | /exams                                       | Crear examen automático.                                           |
| GET    | /exams/{id}                                  | Obtener examen por ID.                                             |
| GET    | /resources/pdf/{id}                          | Obtener recurso PDF por ID.                                        |
| GET    | /exercises                                   | Listar todos los ejercicios por subtema.                           |
| PUT    | /exercises/{id}                              | Actualizar un ejercicio.                                           |
| DELETE | /exercises/{id}                              | Eliminar un ejercicio.                                             |
| GET    | /exercises/subtopic/{subtopico_id}           | Listar ejercicios por subtema.                                     |
| GET    | /exercises/topic/{topico_id}                 | Listar todos los temas.                                            |
| GET    | /exercises/random/{cantidad}                 | Obtener ejercicios aleatorios.                                     |
| GET    | /subtopics                                   | Listar todos los subtemas.                                         |
| GET    | /subtopics/{id}                              | Obtener subtema por ID.                                            |
| POST   | /subtopics                                   | Crear un subtema.                                                  |
| PUT    | /subtopics/{id}                              | Actualizar un subtema.                                             |
| DELETE | /subtopics/{id}                              | Eliminar un subtema.                                               |
| GET    | /topics                                      | Listar todos los temas.                                            |
| GET    | /topics/{id}                                 | Obtener tema por ID.                                               |
| POST   | /topics                                      | Crear un tema.                                                     |
| PUT    | /topics/{id}                                 | Actualizar un tema.                                                |
| DELETE | /topics/{id}                                 | Eliminar un tema.                                                  |
| POST   | /exams/assign                                | Asignar examen a un salón o grupo de alumnos.                      |
| POST   | /exams/submit                                | Enviar respuestas de un examen resuelto por un alumno.             |
| GET    | /exams/results/{exam_id}/student/{alumno_id} | Obtener resultados de un alumno en un examen.                      |
| GET    | /exercises/stats/classroom/{classroom_id}    | Obtener estadísticas de ejercicios por salón.                      |
| GET    | /health                                      | Endpoint de salud del servicio.                                    |

---

### Ejemplos de Requests y Responses

#### Buscar Ejercicios

**GET /exercises/search?query=suma&dificultad=facil&topico_id=uuid-topico**

**Response:**
```json
[
  {
    "id": "uuid-ejercicio",
    "pregunta": "¿Cuánto es 1+1?",
    "opciones": ["1", "2", "3", "4"],
    "respuesta_correcta": "2",
    "dificultad": "facil"
  }
]
```

---

#### Actualizar un Ejercicio

**PUT /exercises/{id}**
```json
{
  "pregunta": "¿Cuánto es 3+3?",
  "opciones": ["5", "6", "7", "8"],
  "respuesta_correcta": "6",
  "dificultad": "facil"
}
```
**Response:**
```json
{
  "mensaje": "Ejercicio actualizado correctamente"
}
```

---

#### Recomendar Ejercicios a un Alumno

**GET /exercises/recommend/alumno/{alumno_id}**

**Response:**
```json
[
  {
    "id": "uuid-ejercicio",
    "pregunta": "¿Cuánto es 5+5?",
    "opciones": ["8", "9", "10", "11"],
    "respuesta_correcta": "10",
    "dificultad": "medio"
  }
]
```

---

#### Enviar Feedback de un Ejercicio

**POST /feedback/exercise/{exercise_id}**
```json
{
  "alumno_id": "uuid-alumno",
  "comentario": "La pregunta es muy clara y útil.",
  "calificacion": 5
}
```
**Response:**
```json
{
  "mensaje": "Feedback recibido, ¡gracias!"
}
```

---

#### Obtener Estadísticas de un Alumno

**GET /exercises/stats/alumno/{alumno_id}**

**Response:**
```json
{
  "total_resueltos": 120,
  "correctos": 100,
  "incorrectos": 20,
  "porcentaje_acierto": 83.3
}
```

---

## 📝 Notas

- Los endpoints de reporte consumen toda la información de ejercicios resueltos, estadísticas y desempeño.
- Los reportes pueden ser exportados a PDF o visualizados en el frontend.
- Se recomienda proteger los endpoints con autenticación y roles.
- Usar fast api con python

---