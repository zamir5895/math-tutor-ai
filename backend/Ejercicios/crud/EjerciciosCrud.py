from fastapi import APIRouter, HTTPException, Request
from services.EjerciciosService import EjercicioService
from schemas.Temas import Ejercicio, EjercicioCreate
from services.EjerciciosResueltos import EjerciciosResueltosService
from models.Ejerccicio import UpdateRespuesta, EjercicioResueltoCreate
class CrudEjercicios:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route(
            "/generar/{subtema_id}",
            self.create_ejercicio,
            methods=["GET"],
            response_model=dict
        )

        self.router.add_api_route(
            "/{subtema_id}",
            self.get_ejercicios_by_subtema_id,
            methods=["GET"],
            response_model=dict
        )
        self.router.add_api_route(
            "/info/{subtema_id}",
            self.getInfoBySubtemaId,
            methods=["GET"],
            response_model=dict
        )
        self.router.add_api_route(
            "/info/tema/{tema_id}",
            self.getInfoByTemaId,
            methods=["GET"],
            response_model=dict
        )
        self.router.add_api_route(
            "/nivel/{subtema_id}/{nivel}",
            self.getEjerciciosBySubtemaIdAndNivel,
            methods=["GET"],
            response_model=dict
        )
        self.router.add_api_route(
            "/resuelto/{tema_id}",
            self.create_ejercicio_resuelto,
            methods=["POST"],
            response_model=dict
        )
        self.router.add_api_route(
            "/resuelto/alumno/{alumno_id}",
            self.get_ejercicios_resueltos_by_alumno,
            methods=["GET"],
            response_model=dict
        )
        self.router.add_api_route(
            "/resuelto/salon/{salon_id}/count",
            self.get_cantidad_ejercicios_resueltos_by_salon,
            methods=["GET"],
            response_model=dict
        )
        self.router.add_api_route(
            "/resuelto/update/{alumno_id}/{ejercicio_id}",
            self.update_ejercicio_resuelto,
            methods=["PUT"],
            response_model=dict
        )
        self.router.add_api_route(
            "/resuelto/remove/{alumno_id}/{ejercicio_id}",
            self.remove_ejercicio_resuelto,
            methods=["DELETE"],
            response_model=dict
        )
        self.resueltos_service = EjerciciosResueltosService()
        self.service = EjercicioService()

    async def create_ejercicio(self, subtema_id: str):
        try:
            result = await self.service.generar_ejercicios_with_gpt(subtema_id)
            return result
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def get_ejercicios_by_subtema_id(self, subtema_id: str):
        try:
            result = await self.service.getEjerciciosBySubTemaId(subtema_id)
            if "error" in result:
                raise HTTPException(status_code=400, detail=result["error"])
            return result
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def getInfoBySubtemaId(self, subtema_id: str):
        try:
            response = await self.service.getInfoBySubtemId(subtema_id)
            if "error" in response:
                raise HTTPException(status_code=400, detail=response["error"])
            return response
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def getInfoByTemaId(self, tema_id: str):
        try:
            response = await self.service.getInfoByTemaId(tema_id)
            if "error" in response:
                raise HTTPException(status_code=400, detail=response["error"])
            return response
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def getEjerciciosBySubtemaIdAndNivel(self, subtema_id: str, nivel: str):
        try:
            response = await self.service.getEjerciciosByNivel(subtema_id, nivel)
            if "error" in response:
                raise HTTPException(status_code=400, detail=response["error"])
            return response
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    async def create_ejercicio_resuelto(self, tema_id: str, info: EjercicioResueltoCreate, request:Request):
        try:
            token = request.headers.get("Authorization")
            result = await self.resueltos_service.createEjercicioResuelto(tema_id, info, token)
            if not token:
                raise HTTPException(status_code=401, detail="Token not provided")
            if "error" in result:
                raise HTTPException(status_code=400, detail=result["error"])
            return result
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_ejercicios_resueltos_by_alumno(self, alumno_id: str):
        try:
            result = await self.resueltos_service.getEjerciciosResueltosByAlumnoId(alumno_id)
            if "error" in result:
                raise HTTPException(status_code=404, detail=result["error"])
            return result
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_cantidad_ejercicios_resueltos_by_salon(self, salon_id: str):
        try:
            result = await self.resueltos_service.getCantidadDeEjerciciosResueltosBySalonId(salon_id)
            if "error" in result:
                raise HTTPException(status_code=404, detail=result["error"])
            return result
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def update_ejercicio_resuelto(self, alumno_id: str, ejercicio_id: str, respuesta_usuario: UpdateRespuesta):
        try:
            result = await self.resueltos_service.updateEjercicioResuelto(alumno_id, ejercicio_id, respuesta_usuario)
            if "error" in result:
                raise HTTPException(status_code=400, detail=result["error"])
            return result
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def remove_ejercicio_resuelto(self, alumno_id: str, ejercicio_id: str):
        try:
            result = await self.resueltos_service.removeEjercicioResuelto(alumno_id, ejercicio_id)
            if "error" in result:
                raise HTTPException(status_code=400, detail=result["error"])
            return result
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
crud_ejercicios = CrudEjercicios()
router = crud_ejercicios.router
