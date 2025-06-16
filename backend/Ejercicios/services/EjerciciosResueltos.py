from Repositorio.EjerciciosResueltosRepositorio import EjercicioResueltosRepository
from models.Ejerccicio import EjercicioResueltoCreate, UpdateRespuesta
from schemas.ejercicios_resueltos import *

from Repositorio.EjercicioRepositorio import EjercicioRepository
from Repositorio.SubTemaRepositorio import SubTemaRepository
from Repositorio.TemaRepositorio import TemaRepository
from datetime import date

class EjerciciosResueltosService:
    def __init__(self):
        self.ejercicio_resuelto_repository = EjercicioResueltosRepository()
        self.ejercicio_repository = EjercicioRepository()
        self.subtema_repository = SubTemaRepository()
        self.tema_repository = TemaRepository()

    async def createEjercicioResuelto(self,tema_id:str, info:EjercicioResueltoCreate):
        try:
            ejercicio = await self.ejercicio_repository.getEjercicioById(info.ejercicio_id)
            if not ejercicio:
                return {"error": "El ejercicio no existe"}
            ejercicio_resuelto = {
                "ejercicio_id": info.ejercicio_id,
                "usuario_id": info.usuario_id,
                "respuesta_usuario": info.respuesta_usuario,
                "nivel": ejercicio.get("nivel", ""),
                "subtema_id": ejercicio.get("subtema_id", ""),
                "tema_id": tema_id,
                "es_correcto": False, 
                "fecha_resuelto":date.today().isoformat() 
            }
            rpt = False
            if info.respuesta_usuario == ejercicio.get("respuesta_correcta"):
                ejercicio_resuelto["es_correcto"] = True
                rpt = True
            created_ejercicio_resuelto = await self.ejercicio_resuelto_repository.add_ejercicio_resuelto(info.usuario_id, info.salon_id, ejercicio_resuelto)
            if not created_ejercicio_resuelto:
                return {"error": "No se pudo crear el ejercicio resuelto"}
            return {"es_correcto": rpt}

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
            ejercicio_resuelto = await self.ejercicio_resuelto_repository.get_ejercicios_resueltos_by_alumno_id(alumno_id)
            if not ejercicio_resuelto:
                return {"error": "No se encontraron ejercicios resueltos para el alumno"}
            
            for ejercicio in ejercicio_resuelto.get("ejercicios_resueltos", []):
                if ejercicio.get("ejercicio_id") == ejercicio_id:
                    ejercicio["respuesta_usuario"] = respuesta_usuario.respuesta_usuario
                    updated = await self.ejercicio_resuelto_repository.add_ejercicio_resuelto(alumno_id, ejercicio_resuelto["salon_id"], ejercicio)
                    if not updated:
                        return {"error": "No se pudo actualizar el ejercicio resuelto"}
                    return {"message": "Ejercicio resuelto actualizado correctamente",
                            "es_correcto": ejercicio.get("es_correcto", False)}
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