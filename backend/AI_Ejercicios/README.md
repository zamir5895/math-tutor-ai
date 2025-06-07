# Plataforma de Aprendizaje - API

Este proyecto es una API desarrollada en **FastAPI** para la gestión de usuarios, ejercicios de matemáticas, progreso, reportes y análisis de patrones de aprendizaje. Utiliza MongoDB como base de datos y modelos generados por IA para la generación y resolución de ejercicios.

---

## Tabla de Contenidos

- [Instalación](#instalación)
- [Ejecución](#ejecución)
- [Endpoints](#endpoints)
  - [Usuarios](#usuarios)
  - [Ejercicios](#ejercicios)
  - [Solucionario](#solucionario)
  - [Progreso](#progreso)
  - [Reportes](#reportes)
  - [Análisis y Patrones](#análisis-y-patrones)
  - [Información](#información)
- [Notas](#notas)

---

## Instalación

1. Clona el repositorio.
2. Instala las dependencias:
  Linux:
   ```sh
   python3 -m venv venv
   ```
   ```sh
   source venv/bin/activate
   ```
   ```sh
   pip install -r requirements.txt
   ```
3. Asegúrate de tener MongoDB corriendo en `localhost:27017` o configura tu URI en `.env`:
   ```
   MONGO_URI=mongodb://localhost:27017
   ```

---

## Ejecución

Inicia el servidor con:

```sh
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
o

```sh
uvicorn main:app --reload --host 0.0.0.0 --port 8000 --log-level debug
```

Accede a la documentación interactiva en [http://localhost:8000/docs](http://localhost:8000/docs).

---

## Endpoints

### Usuarios

#### `POST /usuarios/registrar`
Registra un nuevo usuario.

**Body JSON:**
```json
{
  "nombre": "Juan Pérez",
  "email": "juan.perez@email.com",
  "password": "123456"
}
```
**Respuesta:**  
Usuario registrado y datos del usuario.

---

#### `POST /usuarios/login`
Inicia sesión de usuario.

**Body JSON:**
```json
{
  "email": "juan.perez@email.com",
  "password": "123456"
}
```
**Respuesta:**  
Usuario autenticado y datos del usuario.

---

#### `GET /usuarios/{usuario_id}`
Obtiene información de un usuario por su ID.

---

### Ejercicios

#### `GET /ejercicios`
Genera ejercicios para un tema específico.  
**Query params:**  
- `tema`: Nombre del tema (ej: "fracciones")
- `forzar_generacion`: (opcional, default `false`) Fuerza la generación aunque el tema exista.

**Ejemplo:**  
`/ejercicios?tema=fracciones&forzar_generacion=false`

---

#### `GET /ejercicios/{tema}`
Obtiene ejercicios de un tema específico. Si no existen, los genera automáticamente.

---

#### `GET /ejercicios/{tema}/nivel/{nivel}`
Obtiene ejercicios de un tema filtrados por nivel (`facil`, `medio`, `dificil`).

---

#### `POST /ejercicios/personalizados`
Genera ejercicios personalizados según dificultades del alumno.

**Body JSON:**
```json
{
  "alumno_id": "664f1b2c1234567890abcdef",
  "tema": "fracciones",
  "dificultades_identificadas": ["suma de fracciones", "fracciones equivalentes"]
}
```

---

#### `POST /ejercicios/adicionales`
Genera ejercicios adicionales según nivel y tema.

**Body JSON:**
```json
{
  "tema": "fracciones",
  "nivel": "facil",
  "cantidad": 5,
  "alumno_id": "664f1b2c1234567890abcdef"
}
```

---

### Solucionario

#### `POST /solucionario/resolver`
Resuelve un ejercicio paso a paso con explicación detallada.

**Body JSON:**
```json
{
  "pregunta": "Resuelve 1/2 + 1/4",
  "tema": "fracciones",
  "nivel": "facil"
}
```

---

#### `POST /solucionario/evaluar`
Evalúa la respuesta de un estudiante y proporciona retroalimentación.

**Body JSON:**
```json
{
  "pregunta": "Resuelve 1/2 + 1/4",
  "respuesta_correcta": "3/4",
  "respuesta_alumno": "2/4",
  "tema": "fracciones"
}
```

---

### Progreso

#### `POST /progreso/iniciar`
Inicia el progreso de un alumno en un tema específico.

**Body JSON:**
```json
{
  "alumno_id": "664f1b2c1234567890abcdef",
  "tema_id": "664f1b2c1234567890abcdea"
}
```

---

#### `POST /progreso/responder`
Registra la respuesta de un alumno a una pregunta.

**Body JSON:**
```json
{
  "progreso_id": "664f1b2c1234567890abcdeb",
  "nivel": 1,
  "pregunta": "Resuelve 1/2 + 1/4",
  "respuesta_alumno": "3/4",
  "respuesta_correcta": "3/4",
  "tema": "fracciones"
}
```

---

#### `GET /progreso/{alumno_id}/{tema_id}`
Obtiene el progreso de un alumno en un tema específico.

---

### Reportes

#### `POST /reportes/generar`
Genera un reporte de rendimiento del alumno.

**Body JSON:**
```json
{
  "alumno_id": "664f1b2c1234567890abcdef",
  "tema_id": "664f1b2c1234567890abcdea"
}
```

---

#### `GET /reportes/{alumno_id}`
Obtiene todos los reportes de un alumno.

---

### Análisis y Patrones

#### `POST /analisis/patrones`
Analiza patrones de errores del alumno y proporciona recomendaciones.

**Body JSON:**
```json
{
  "alumno_id": "664f1b2c1234567890abcdef",
  "tema_id": "664f1b2c1234567890abcdea"
}
```

---

### Información

#### `GET /temas`
Lista todos los temas disponibles.

---

#### `GET /estadisticas/{alumno_id}`
Obtiene estadísticas generales de un alumno.

---

## Notas

- Todos los endpoints que requieren IDs deben recibir IDs válidos de MongoDB.
- Los endpoints que generan o evalúan ejercicios usan modelos de IA para la generación y explicación.
- Para probar los endpoints, puedes usar herramientas como **Postman** o la documentación interactiva de FastAPI en `/docs`.
- Cambia los IDs de ejemplo por los que existan en tu base de datos.

---

