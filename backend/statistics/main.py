from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import EstadisticaCreateRequest, ProgresoEvent
from service.statsAlumnoService import StatsAlumnoService

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/estadisticas/init", status_code=202)
async def inicializar_estadisticas(
    request: EstadisticaCreateRequest,
    background_tasks: BackgroundTasks
):
    try:
        background_tasks.add_task(StatsAlumnoService.procesar_estadistica_init, request.dict())
        return {"message": "Solicitud recibida, procesando en segundo plano"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/estadisticas/progreso", status_code=202)
async def registrar_progreso(
    event: ProgresoEvent,
    background_tasks: BackgroundTasks
):
    try:
        background_tasks.add_task(StatsAlumnoService.procesar_progreso_event, event.dict())
        return {"message": "Evento recibido, actualizando estadísticas"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/estadisticas/alumno/{alumno_id}")
async def obtener_estadisticas_alumno(alumno_id: str):
    try:
        result = await StatsAlumnoService.obtener_por_alumno_id(alumno_id)
        if not result:
            raise HTTPException(status_code=404, detail="Alumno no encontrado")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/estadisticas/alumno/{alumno_id}/tema/{tema_id}")
async def obtener_estadisticas_tema(alumno_id: str, tema_id: str):
    try:
        result = await StatsAlumnoService.obtener_por_tema_id(alumno_id, tema_id)
        if not result:
            raise HTTPException(status_code=404, detail="Tema no encontrado")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/estadisticas/alumno/{alumno_id}/tema/{tema_id}/subtema/{subtema_id}")
async def obtener_estadisticas_subtema(alumno_id: str, tema_id: str, subtema_id: str):
    try:
        result = await StatsAlumnoService.obtener_por_subtema_id(alumno_id, tema_id, subtema_id)
        if not result:
            raise HTTPException(status_code=404, detail="Subtema no encontrado")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/estadisticas/alumno/{alumno_id}/tema/{tema_id}/subtema/{subtema_id}/nivel/{nivel}")
async def obtener_estadisticas_nivel(alumno_id: str, tema_id: str, subtema_id: str, nivel: str):
    try:
        result = await StatsAlumnoService.obtener_por_subtema_y_nivel(alumno_id, tema_id, subtema_id, nivel)
        if not result:
            raise HTTPException(status_code=404, detail="Nivel no encontrado")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/dominados/alumno/{alumno_id}/temas")
async def get_temas_dominados_alumno(alumno_id: str):
    try:
        result = await StatsAlumnoService.get_temas_dominados_alumno(alumno_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/dominados/alumno/{alumno_id}/subtemas")
async def get_subtemas_dominados_alumno(alumno_id: str):
    try:
        result = await StatsAlumnoService.get_subtemas_dominados_alumno(alumno_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/dominados/salon/{salon_id}/temas")
async def get_temas_dominados_salon(salon_id: str):
    try:
        result = await StatsAlumnoService.get_temas_dominados_salon(salon_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/dominados/salon/{salon_id}/subtemas")
async def get_subtemas_dominados_salon(salon_id: str):
    try:
        result = await StatsAlumnoService.get_subtemas_dominados_salon(salon_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/dominados/alumno/{alumno_id}/tema/{tema_id}")
async def eliminar_tema_dominado_alumno(alumno_id: str, tema_id: str):
    try:
        await StatsAlumnoService.eliminar_tema_dominado_alumno(alumno_id, tema_id)
        return {"detail": "Tema dominado eliminado para alumno"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/dominados/alumno/{alumno_id}/tema/{tema_id}/subtema/{subtema_id}")
async def eliminar_subtema_dominado_alumno(alumno_id: str, tema_id: str, subtema_id: str):
    try:
        await StatsAlumnoService.eliminar_subtema_dominado_alumno(alumno_id, tema_id, subtema_id)
        return {"detail": "Subtema dominado eliminado para alumno"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/dominados/salon/{salon_id}/tema/{tema_id}")
async def eliminar_tema_dominado_salon(salon_id: str, tema_id: str):
    try:
        await StatsAlumnoService.eliminar_tema_dominado_salon(salon_id, tema_id)
        return {"detail": "Tema dominado eliminado para salón"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/dominados/salon/{salon_id}/tema/{tema_id}/subtema/{subtema_id}")
async def eliminar_subtema_dominado_salon(salon_id: str, tema_id: str, subtema_id: str):
    try:
        await StatsAlumnoService.eliminar_subtema_dominado_salon(salon_id, tema_id, subtema_id)
        return {"detail": "Subtema dominado eliminado para salón"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "ok"}