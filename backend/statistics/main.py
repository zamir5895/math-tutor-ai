from fastapi import FastAPI, HTTPException
from service import *
from db_postgres import database

app = FastAPI(title="Microservicio Statistics")

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/totales", response_model=dict)
async def totales():
    try:
        return await obtener_totales_postgres()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/progreso/{alumno_id}", response_model=ProgresoEstadistica)
async def progreso(alumno_id: str):
    try:
        return await estadisticas_progreso_por_alumno(alumno_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/reporte/{alumno_id}", response_model=ReporteEstadistica)
async def reporte(alumno_id: str):
    try:
        return await estadisticas_reportes_por_alumno(alumno_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
