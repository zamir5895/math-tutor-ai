import logging

from fastapi import FastAPI, HTTPException

from models import ReporteEstadistica, ProgresoEstadistica
from db.db import database
from service import obtener_totales_postgres, estadisticas_progreso_por_alumno, estadisticas_reportes_por_alumno

app = FastAPI(title="Microservicio Statistics")

# Configure logging
logger = logging.getLogger("uvicorn.error")

@app.on_event("startup")
async def startup():
    try:
        await database.connect()
        logger.info("Database connection established.")
    except Exception as e:
        logger.error(f"Error connecting to database: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")

@app.on_event("shutdown")
async def shutdown():
    try:
        await database.disconnect()
        logger.info("Database connection closed.")
    except Exception as e:
        logger.error(f"Error disconnecting from database: {e}")
        raise HTTPException(status_code=500, detail="Database disconnection failed")

@app.get("/totales", response_model=dict)
async def totales():
    try:
        return await obtener_totales_postgres()
    except Exception as e:
        logger.error(f"Error in /totales endpoint: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch totals")

@app.get("/progreso/{alumno_id}", response_model=ProgresoEstadistica)
async def progreso(alumno_id: str):
    try:
        return await estadisticas_progreso_por_alumno(alumno_id)
    except Exception as e:
        logger.error(f"Error fetching progress for alumno_id {alumno_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch progress for alumno {alumno_id}")

@app.get("/reporte/{alumno_id}", response_model=ReporteEstadistica)
async def reporte(alumno_id: str):
    try:
        return await estadisticas_reportes_por_alumno(alumno_id)
    except Exception as e:
        logger.error(f"Error fetching report for alumno_id {alumno_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch report for alumno {alumno_id}")
