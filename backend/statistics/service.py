import logging
from http.client import HTTPException

from bson import ObjectId

from db_mongo import progresos_collection, reportes_collection
from db_postgres import database
from models import ProgresoEstadistica, ReporteEstadistica

logger = logging.getLogger(__name__)

async def obtener_totales_postgres():
    """Fetch total statistics from PostgreSQL."""
    try:
        query_alumnos = "SELECT COUNT(*) FROM alumno"
        query_profesores = "SELECT COUNT(*) FROM profesor"
        query_salones = "SELECT COUNT(*) FROM salon"
        query_roles = "SELECT rol, COUNT(*) as total FROM \"user\" GROUP BY rol"

        total_alumnos = await database.fetch_val(query_alumnos)
        total_profesores = await database.fetch_val(query_profesores)
        total_salones = await database.fetch_val(query_salones)
        roles = await database.fetch_all(query_roles)
        usuarios_por_rol = {r['rol']: r['total'] for r in roles}

        return {
            "total_alumnos": total_alumnos,
            "total_profesores": total_profesores,
            "total_salones": total_salones,
            "usuarios_por_rol": usuarios_por_rol
        }
    except Exception as e:
        logger.error(f"Error while fetching totals from PostgreSQL: {e}")
        raise HTTPException(status_code=500, detail="Database query error")

async def calculate_progreso_statistics(respuestas):
    """Calculate progress statistics for a student."""
    total = len(respuestas)
    correctas = sum(1 for r in respuestas if r.get("correcto", False))
    nivel_promedio = sum(r.get("nivel", 0) for r in respuestas) / total if total > 0 else 0
    porcentaje_aciertos = (correctas / total * 100) if total > 0 else 0

    return nivel_promedio, porcentaje_aciertos, total

async def estadisticas_progreso_por_alumno(alumno_id: str) -> ProgresoEstadistica:
    """Fetch progreso statistics for a single alumno from MongoDB."""
    try:
        filtro = {"alumno_id": ObjectId(alumno_id)}
        progreso = await progresos_collection.find_one(filtro)

        if not progreso or not progreso.get("respuestas"):
            return ProgresoEstadistica(
                alumno_id=alumno_id,
                nivel_promedio=0,
                porcentaje_aciertos=0,
                ejercicios_resueltos=0
            )

        respuestas = progreso.get("respuestas")
        nivel_promedio, porcentaje_aciertos, total = await calculate_progreso_statistics(respuestas)

        return ProgresoEstadistica(
            alumno_id=alumno_id,
            nivel_promedio=nivel_promedio,
            porcentaje_aciertos=porcentaje_aciertos,
            ejercicios_resueltos=total
        )
    except Exception as e:
        logger.error(f"Error while fetching progreso for alumno {alumno_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching progreso for alumno {alumno_id}")

async def estadisticas_reportes_por_alumno(alumno_id: str) -> ReporteEstadistica:
    """Fetch report statistics for a single alumno from MongoDB."""
    try:
        cursor = reportes_collection.find({"alumno_id": ObjectId(alumno_id)})
        reportes = await cursor.to_list(length=100)

        if not reportes:
            return ReporteEstadistica(
                alumno_id=alumno_id,
                promedio_porcentaje=0,
                nivel_maximo_promedio=0
            )

        promedio_porcentaje = sum(r.get("porcentaje", 0) for r in reportes) / len(reportes)
        nivel_maximo_promedio = sum(r.get("nivel_maximo", 0) for r in reportes) / len(reportes)

        return ReporteEstadistica(
            alumno_id=alumno_id,
            promedio_porcentaje=promedio_porcentaje,
            nivel_maximo_promedio=nivel_maximo_promedio
        )
    except Exception as e:
        logger.error(f"Error while fetching reportes for alumno {alumno_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching reportes for alumno {alumno_id}")

