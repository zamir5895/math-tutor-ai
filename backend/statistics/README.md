#  Statistics Microservice - TutorAI

Microservicio de estadísticas para la plataforma de aprendizaje TutorAI. Maneja el seguimiento del progreso de los estudiantes, métricas de desempeño por temas/subtemas y análisis de dominancia de contenidos.

##  Arquitectura

```
statistics/
├── main.py                 # FastAPI endpoints
├── models.py              # Modelos Pydantic para requests
├── requirements.txt       # Dependencias Python
├── Dockerfile            # Containerización
├── docker-compose.yml    # Orquestación de contenedores
├── .env                  # Variables de entorno
├── db/
│   └── db.py            # Conexión MongoDB
├── schemas/
│   ├── alumno.py        # Esquemas del alumno
│   ├── profesor.py      # Esquemas del profesor
│   └── util.py          # Utilidades
└── service/
    └── statsAlumnoService.py  # Lógica de negocio
```

## 🗄️ Esquemas de Base de Datos

### Colección: `alumnos`
Almacena las estadísticas principales de cada alumno por tema, subtema y nivel.

```json
{
  "alumno_id": "alumno123",
  "salon_id": "salon456", 
  "progreso_general": {
    "correctos": 85,
    "errores": 15,
    "completados": 100,
    "total": 150,
    "porcentaje": 56.67
  },
  "temas": [
    {
      "tema_id": "algebra",
      "nombre": "Álgebra Básica",
      "correctos": 25,
      "errores": 5,
      "total": 40,
      "subtemas": [
        {
          "subtema_id": "ecuaciones",
          "nombre": "Ecuaciones Lineales",
          "correctos": 8,
          "errores": 2,
          "total": 12,
          "niveles": {
            "facil": {
              "correctos": 3,
              "errores": 1,
              "total": 4
            },
            "medio": {
              "correctos": 3,
              "errores": 1,
              "total": 4
            },
            "dificil": {
              "correctos": 2,
              "errores": 0,
              "total": 4
            }
          }
        }
      ]
    }
  ],
  "updated_at": "2025-01-08T15:30:00Z"
}
```

### Colección: `temas_dominados_alumno`
Registra qué temas ha dominado completamente cada alumno.

```json
{
  "alumno_id": "alumno123",
  "temas_dominados": [
    {
      "tema_id": "aritmetica",
      "subtemas_dominados": ["suma", "resta", "multiplicacion"]
    },
    {
      "tema_id": "geometria", 
      "subtemas_dominados": ["triangulos", "cuadrados"]
    }
  ]
}
```

### Colección: `subtemas_dominados_alumno`
Lista todos los subtemas dominados por alumno con su tema padre.

```json
{
  "alumno_id": "alumno123",
  "subtemas_dominados": [
    {"tema_id": "aritmetica", "subtema_id": "suma"},
    {"tema_id": "aritmetica", "subtema_id": "resta"},
    {"tema_id": "geometria", "subtema_id": "triangulos"}
  ]
}
```

### Colección: `temas_dominados_salon`
Temas que todos los alumnos de un salón han dominado.

```json
{
  "salon_id": "salon456",
  "temas_dominados": ["aritmetica", "geometria_basica"]
}
```

### Colección: `subtemas_dominados_salon`
Subtemas que todos los alumnos de un salón han dominado.

```json
{
  "salon_id": "salon456", 
  "subtemas_dominados": [
    {"tema_id": "aritmetica", "subtema_id": "suma"},
    {"tema_id": "aritmetica", "subtema_id": "resta"}
  ]
}
```

##  API Endpoints

### Gestión de Estadísticas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/estadisticas/init` | Inicializa estadísticas para un alumno |
| `POST` | `/estadisticas/progreso` | Registra progreso de un ejercicio |
| `GET` | `/estadisticas/alumno/{alumno_id}` | Obtiene todas las estadísticas del alumno |
| `GET` | `/estadisticas/alumno/{alumno_id}/tema/{tema_id}` | Estadísticas por tema |
| `GET` | `/estadisticas/alumno/{alumno_id}/tema/{tema_id}/subtema/{subtema_id}` | Estadísticas por subtema |
| `GET` | `/estadisticas/alumno/{alumno_id}/tema/{tema_id}/subtema/{subtema_id}/nivel/{nivel}` | Estadísticas por nivel |

### Temas y Subtemas Dominados

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/dominados/alumno/{alumno_id}/temas` | Temas dominados por alumno |
| `GET` | `/dominados/alumno/{alumno_id}/subtemas` | Subtemas dominados por alumno |
| `GET` | `/dominados/salon/{salon_id}/temas` | Temas dominados por todo el salón |
| `GET` | `/dominados/salon/{salon_id}/subtemas` | Subtemas dominados por todo el salón |

### Eliminación de Dominados

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `DELETE` | `/dominados/alumno/{alumno_id}/tema/{tema_id}` | Elimina tema dominado del alumno |
| `DELETE` | `/dominados/alumno/{alumno_id}/tema/{tema_id}/subtema/{subtema_id}` | Elimina subtema dominado del alumno |
| `DELETE` | `/dominados/salon/{salon_id}/tema/{tema_id}` | Elimina tema dominado del salón |
| `DELETE` | `/dominados/salon/{salon_id}/tema/{tema_id}/subtema/{subtema_id}` | Elimina subtema dominado del salón |

##  Modelos de Datos

### EstadisticaCreateRequest
```python
{
  "alumno_id": "string",
  "tema_id": "string", 
  "salon_id": "string",
  "subtema_id": "string",
  "ejercicios_por_nivel": {
    "facil": 10,
    "medio": 8,
    "dificil": 5
  }
}
```

### ProgresoEvent
```python
{
  "alumno_id": "string",
  "tema_id": "string",
  "subtema_id": "string", 
  "nivel": "facil|medio|dificil",
  "es_correcto": true
}
```

##  Configuración

### Variables de Entorno
```bash
MONGO_URI=mongodb://host:port/database
MONGO_DB_NAME=learning_platform
```

### Instalación Local

1. **Clona el repositorio**
```bash
git clone <repository_url>
cd statistics
```

2. **Crea entorno virtual**
```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
```

3. **Instala dependencias**
```bash
pip install -r requirements.txt
```

4. **Configura variables de entorno**
```bash
cp .env.example .env
# Edita .env con tus valores
```

5. **Ejecuta el servidor**
```bash
uvicorn main:app --reload --port 8050
```

### Docker

```bash
# Construir y ejecutar
docker-compose up --build

# Solo ejecutar
docker-compose up

# Ver logs
docker-compose logs -f statistics
```

## 🏃 Uso

### Ejemplo: Inicializar estadísticas
```bash
curl -X POST "http://localhost:8050/estadisticas/init" \
-H "Content-Type: application/json" \
-d '{
  "alumno_id": "alumno123",
  "tema_id": "algebra",
  "salon_id": "salon456",
  "subtema_id": "ecuaciones",
  "ejercicios_por_nivel": {
    "facil": 5,
    "medio": 4, 
    "dificil": 3
  }
}'
```

### Ejemplo: Registrar progreso
```bash
curl -X POST "http://localhost:8050/estadisticas/progreso" \
-H "Content-Type: application/json" \
-d '{
  "alumno_id": "alumno123",
  "tema_id": "algebra",
  "subtema_id": "ecuaciones",
  "nivel": "facil",
  "es_correcto": true
}'
```

## 🎯 Lógica de Dominancia

### Subtema Dominado
Un subtema se considera dominado cuando:
- `correctos == total` ejercicios del subtema
- `total > 0` (tiene ejercicios)

### Tema Dominado
Un tema se considera dominado cuando:
- Todos sus subtemas están dominados
- Tiene al menos un subtema

### Dominancia por Salón
- **Tema dominado por salón**: Todos los alumnos del salón dominan el tema
- **Subtema dominado por salón**: Todos los alumnos del salón dominan el subtema

## 📈 Funcionalidades Clave

-  Seguimiento de progreso en tiempo real
-  Métricas por nivel de dificultad (fácil, medio, difícil)
-  Análisis de dominancia individual y grupal
-  Actualización automática de estadísticas agregadas
-  API RESTful con documentación automática
-  Manejo de errores con try/catch
-  Procesamiento en background para mejor rendimiento
-  Containerización con Docker

##  Puerto

El servicio corre en el puerto **8050** por defecto.

##  Documentación API

Una vez ejecutando, visita: `http://localhost:8050/docs` para la documentación interactiva de Swagger.

## 🔍 Monitoreo

- **Health Check**: `GET /health`
- **Logs**: `docker-compose logs -f statistics`
- **Métricas**: MongoDB Compass o Studio 3T para inspeccionar datos

---

**Desarrollado para TutorAI** 🎓📊
