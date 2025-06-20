from Repositorio.EjerciciosResueltosRepositorio import EjercicioResueltosRepository
from models.Ejerccicio import EjercicioResueltoCreate, UpdateRespuesta
from schemas.ejercicios_resueltos import *
import httpx
from Repositorio.EjercicioRepositorio import EjercicioRepository
from Repositorio.SubTemaRepositorio import SubTemaRepository
from Repositorio.TemaRepositorio import TemaRepository
from datetime import date
import requests
import asyncio
class EjerciciosResueltosService:
    def __init__(self):
        self.ejercicio_resuelto_repository = EjercicioResueltosRepository()
        self.ejercicio_repository = EjercicioRepository()
        self.subtema_repository = SubTemaRepository()
        self.tema_repository = TemaRepository()

    async def registrarProgresoEjercicio(self, alumno_id:str, tema_id:str, subtema_id:str, nivel:str, es_correcto:bool):
        try:
            async with httpx.AsyncClient() as client:
                urlEstadisticas = f"http://statistics:8050/estadisticas/progreso"
                json_data = {
                    "alumno_id": str(alumno_id),
                    "tema_id": str(tema_id),
                    "subtema_id": str(subtema_id),
                    "nivel": str(nivel),
                    "es_correcto": es_correcto
                }
                print(f"Registrando progreso: {json_data}")
                response = await client.post(urlEstadisticas, json=json_data)
                response.raise_for_status()
        except httpx.RequestError as e:
            print(f"Error de conexión: {str(e)}")
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    async def createEjercicioResuelto(self,tema_id:str, info:EjercicioResueltoCreate, token: str):
        try:
            ejercicio = await self.ejercicio_repository.getEjercicioById(info.ejercicio_id)
            resolvio = await self.ejercicio_resuelto_repository.getEjercicioResueltoByAlumnoIdAndEjercicioId(info.alumno_id, info.ejercicio_id)
            print(f"Ejercicio: {ejercicio}")
            if resolvio:
                resolvio["respuesta_usuario"] = info.respuesta_usuario
                if ejercicio.get("respuesta_usuario") == ejercicio.get("respuesta_correcta"):
                    resolvio["es_correcto"] = True
                else:
                    resolvio["es_correcto"] = False
                resolvio["fecha_resuelto"] = date.today().isoformat()
                updated = await self.ejercicio_resuelto_repository.add_ejercicio_resuelto(info.alumno_id, ejercicio["salon_id"], resolvio)
                asyncio.create_task(self.registrarProgresoEjercicio(info.alumno_id, tema_id, info.subtema_id, ejercicio.get("nivel", ""), resolvio.get("es_correcto")))
                if not updated:
                    return {"error": "No se pudo actualizar el ejercicio resuelto"}
                return {"message": "Ejercicio resuelto actualizado correctamente",
                        "es_correcto": resolvio.get("es_correcto", False)}
            if not ejercicio:
                return {"error": "El ejercicio no existe"}
            ejercicio_resuelto = {
                "ejercicio_id": info.ejercicio_id,
                "respuesta_usuario": info.respuesta_usuario,
                "nivel": ejercicio.get("nivel", ""),
                "subtema_id": info.subtema_id,
                "tema_id": tema_id,
                "es_correcto": False,
                "fecha_resuelto": date.today().isoformat()
            }
            if info.respuesta_usuario == ejercicio.get("respuesta_correcta"):
                ejercicio_resuelto["es_correcto"] = True
                requests.post(f"http://users:8090/alumno/addfecha/{info.alumno_id}", 
                            headers={
                                'Authorization': f'Bearer {token}',
                                'Content-Type': 'application/json'
                            })            
            created_ejercicio_resuelto = await self.ejercicio_resuelto_repository.add_ejercicio_resuelto(info.alumno_id, info.salon_id, ejercicio_resuelto)
            print(f"Ejercicio: {created_ejercicio_resuelto}")
            asyncio.create_task(self.registrarProgresoEjercicio(info.alumno_id, tema_id, info.subtema_id, ejercicio.get("nivel", ""), ejercicio_resuelto["es_correcto"]))
            print(f"Ejercicio resuelto creado: {created_ejercicio_resuelto}")
            if not created_ejercicio_resuelto:
                return {"error": "No se pudo crear el ejercicio resuelto"}
            return {"es_correcto": ejercicio_resuelto["es_correcto"]}

        except Exception as e:
            return {"error": str(e)}
    
    async def getEjerciciosResueltosByAlumnoId(self, alumno_id: str):
        try:
            ejercicios_resueltos = await self.ejercicio_resuelto_repository.get_ejercicios_resueltos_by_alumno_id(alumno_id)
            if not ejercicios_resueltos:
                return {"error": "No se encontraron ejercicios resueltos para el alumno"}
            return {"ejercicios_resueltos": ejercicios_resueltos,
                    "count": len(ejercicios_resueltos.get("ejercicios_resueltos", []))}
        except Exception as e:
            return {"error": str(e)}
    
    async def getCantidadDeEjerciciosResueltosBySalonId(self, salon_id: str):
        try:
            count = await self.ejercicio_resuelto_repository.get_cantidad_de_ejercicios_resueltos_by_salon_id(salon_id)
            return {"count": count}
        except Exception as e:
            return {"error": str(e)}

    async def updateEjercicioResuelto(self, alumno_id: str, ejercicio_id: str, respuesta_usuario: UpdateRespuesta):
        try:
            ejercicio = await self.ejercicio_resuelto_repository.getEjercicioResueltoByAlumnoIdAndEjercicioId(alumno_id, ejercicio_id)
            if not ejercicio:
                return {"error": "Ejercicio no encontrado"}
            if ejercicio.get("ejercicio_id") == ejercicio_id:
                ejercicio["respuesta_usuario"] = respuesta_usuario.respuesta_usuario
                ejercicio["es_correcto"] = ejercicio.get("respuesta_usuario") == ejercicio.get("respuesta_correcta")
                ejercicio["fecha_resuelto"] = date.today().isoformat()
                updated = await self.ejercicio_resuelto_repository.add_ejercicio_resuelto(alumno_id, ejercicio["salon_id"], ejercicio)
                asyncio.create_task(self.registrarProgresoEjercicio(alumno_id, ejercicio["tema_id"], ejercicio.get("subtema_id", ""), ejercicio.get("nivel", ""), ejercicio["es_correcto"]))
                if not updated:
                    return {"error": "No se pudo actualizar el ejercicio resuelto"}
                return {
                    "message": "Ejercicio resuelto actualizado correctamente",
                    "es_correcto": ejercicio.get("es_correcto")
                }
            return {"error": "Ejercicio no encontrado"}
        except Exception as e:
            return {"error": str(e)}
    
    async def removeEjercicioResuelto(self, alumno_id: str, ejercicio_id: str):
        try:
            removed = await self.ejercicio_resuelto_repository.remove_ejercicio_resuelto(alumno_id, ejercicio_id)
            if not removed:
                return {"error": "No se pudo eliminar el ejercicio resuelto"}
            return {"message": "Ejercicio resuelto eliminado correctamente"}
        except Exception as e:
            return {"error": str(e)}
    
    
    