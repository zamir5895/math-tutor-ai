from Repositorio.EjercicioRepositorio import EjercicioRepository
from schemas.Temas import Ejercicio, EjercicioCreate
from Repositorio.SubTemaRepositorio import SubTemaRepository
from Repositorio.TemaRepositorio import TemaRepository
from services.IAService import GPTService
from Repositorio.EjerciciosResueltosRepositorio import EjercicioResueltosRepository

class EjercicioService:
    def __init__(self):
        self.ejercicio_repository = EjercicioRepository()
        self.subtema_repository = SubTemaRepository()
        self.tema_repository = TemaRepository()
        self.ia_services = GPTService()
        self.ejercicios_resueltos_repository = EjercicioResueltosRepository()

    async def generar_ejercicios_with_gpt(self, id:str):
        try:
            subtema = await self.subtema_repository.getSubTemaById(id)
            if subtema is None:
                return {"error": "El subtema no existe"}

            ejercicios = await self.ia_services.generateExcersiceBaseOnSubtema(subtema["titulo"])
            if not ejercicios:
                return {"error": "No se pudieron generar ejercicios"}
            print("Ejercicios generados:", ejercicios)
            ejercicios_response = []    
            for ejercicio in ejercicios:
                ejercicio_create = EjercicioCreate(**ejercicio)
                ejercicio_id = await self.ejercicio_repository.createEjercicio(ejercicio_create)
                if ejercicio_id is None:
                    return {"error": "No se pudo crear el ejercicio"}
                
                added = await self.subtema_repository.addEjercicioToSubTema(id, ejercicio_id, ejercicio["nivel"])
                if not added:
                    return {"error": "No se pudo agregar el ejercicio al subtema"}
                ejercicio_response = await self.ejercicio_repository.getEjercicioById(ejercicio_id)
                if ejercicio_response is None:
                    return {"error": "No se pudo obtener el ejercicio creado"}
                
                ejercicios_response.append(ejercicio_response)

            print("Ejercicios creados:", ejercicios_response)
            response = await self.getEjerciciosBySubTemaId(id)
            return response
        except Exception as e:
            return {"error": str(e)}

    async def getEjerciciosBySubTemaId(self, subtema_id:str):
        try:
            subtema = await self.subtema_repository.getSubTemaById(subtema_id)
            if subtema is None:
                return {"error": "El subtema no existe"}
        
            preguntas = subtema.get("preguntas", {})
            if not preguntas:
                return {"ejercicios": [], "count": 0}
            ejercicios_por_nivel = {}
            ejercicios_totales = 0
            total_por_nivel = {"facil": 0, "medio": 0, "dificil": 0}
            for nivel, lista_ids in preguntas.items():
                ejercicios = []
                for ejercicio_id in lista_ids:
                    ejercicio = await self.ejercicio_repository.getEjercicioById(ejercicio_id)
                    if ejercicio:
                        ejercicios.append(ejercicio)
                ejercicios_por_nivel[nivel] = ejercicios
                total_por_nivel[nivel] = len(ejercicios)
                ejercicios_totales += len(ejercicios)
            return {
                "ejercicios": ejercicios_por_nivel,
                "total_ejercicios_por_subtema": ejercicios_totales,
                "total_por_nivel": total_por_nivel
            }

        except Exception as e:
            return {"error": str(e)}
    async def getInfoBySubtemId(self, subtema_id:str):
        try:
            subtema = await self.subtema_repository.getSubTemaById(subtema_id)
            if subtema is None:
                return {"error": "El subtema no existe"}
            
            total_ejercicios = 0
            total_por_nivel = {"facil": 0, "medio": 0, "dificil": 0}
            preguntas = subtema.get("preguntas", {})
            for nivel, lista_ids in preguntas.items():
                total_por_nivel[nivel] = len(lista_ids)
                total_ejercicios += len(lista_ids)
            return {
                "subtema_id": subtema_id,
                "titulo": subtema.get("titulo", ""),
                "total_ejercicios": total_ejercicios,
                "total_por_nivel": total_por_nivel
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def getInfoByTemaId(self, tema_id: str):
        try:
            tema = await self.tema_repository.getTemaById(tema_id)
            if tema is None:
                return {"error": "El tema no existe"}
            
            subtemas = await self.subtema_repository.getSubTemasByTemaId(tema_id)
            cantidad_subtemas = len(subtemas)
            total_ejercicios = 0
            total_por_nivel = {"facil": 0, "medio": 0, "dificil": 0}
            subtemas_info = []
    
            for subtema in subtemas:
                subtema_id = str(subtema["_id"])
                ejercicios_info = await self.getInfoBySubtemId(subtema_id)
                if "error" in ejercicios_info:
                    return ejercicios_info
                subtemas_info.append({
                    "subtema_id": subtema_id,
                    "titulo": subtema.get("titulo", ""),
                    "descripcion": subtema.get("descripcion", ""),
                    "total_ejercicios": ejercicios_info["total_ejercicios"],
                    "total_por_nivel": ejercicios_info["total_por_nivel"]
                })
                total_ejercicios += ejercicios_info["total_ejercicios"]
                for nivel, cantidad in ejercicios_info["total_por_nivel"].items():
                    total_por_nivel[nivel] += cantidad
    
            response = {
                "tema_id": tema_id,
                "cantidad_subtemas": cantidad_subtemas,
                "total_ejercicios": total_ejercicios,
                "subtemas": subtemas_info
            }
            return response
        except Exception as e:
            return {"error": str(e)}
    
    async def getEjerciciosByNivel(self, subtema_id: str, nivel: str):
        try:
            subtema = await self.subtema_repository.getSubTemaById(subtema_id)
            if subtema is None:
                return {"error": "El subtema no existe"}
            
            preguntas = subtema.get("preguntas", {})
            ejercicios = []
            total_ejercicios = 0
            for nivel_key, lista_ids in preguntas.items():
                if nivel_key == nivel:
                    total_ejercicios = len(lista_ids)
                    for ejercicio_id in lista_ids:
                        ejercicio = await self.ejercicio_repository.getEjercicioById(ejercicio_id)
                        if ejercicio:
                            ejercicios.append(ejercicio)
                    break
            return {
                "subtema_id": subtema_id,
                "nivel": nivel,
                "total_ejercicios": total_ejercicios,
                "ejercicios": ejercicios,
            }
        except Exception as e:
            return {"error": str(e)}

    async def updateEjercicio(self, ejercicio_id: str, ejercicio_data: EjercicioCreate):
        try:
            updated = await self.ejercicio_repository.updateEjercicio(ejercicio_id, ejercicio_data)
            if not updated:
                return {"error": "No se pudo actualizar el ejercicio"}
            ejercicio = await self.ejercicio_repository.getEjercicioById(ejercicio_id)
            if ejercicio is None:
                return {"error": "El ejercicio actualizado no existe"}
            return ejercicio
        except Exception as e:
            return {"error": str(e)}
    
    async def createEjercicioManual(self, ejercicio_data: EjercicioCreate):
        try:
            ejercicio_id = await self.ejercicio_repository.createEjercicio(ejercicio_data)
            if ejercicio_id is None:
                return {"error": "No se pudo crear el ejercicio"}
            ejercicio = await self.ejercicio_repository.getEjercicioById(ejercicio_id)
            if ejercicio is None:
                return {"error": "El ejercicio creado no existe"}
            return ejercicio
        except Exception as e:
            return {"error": str(e)}
    
    async def deleteEjercicio(self, ejercicio_id: str):
        try:
            deleted = await self.ejercicio_repository.deleteEjercicio(ejercicio_id)
            if not deleted:
                return {"error": "No se pudo eliminar el ejercicio"}
            return {"message": "Ejercicio eliminado correctamente"}
        except Exception as e:
            return {"error": str(e)}
    
    async def getEjercicioByNivelForAlumno(self, subtema_id:str, nivel:str, alumno_id:str):
        try:
            subtema = await self.subtema_repository.getSubTemaById(subtema_id)
            if subtema is None:
                return {"error": "El subtema no existe"}
            
            reponse = await self.getEjerciciosByNivel(subtema_id, nivel)
            if "error" in reponse:
                return reponse
            ejercicios = reponse.get("ejercicios", [])
            ejercicios_filtrados = []
            for ejercicio in ejercicios:
                ejercicio_resuelto = await self.ejercicios_resueltos_repository.getEjercicioResueltoByAlumnoIdAndEjercicioId(alumno_id, ejercicio["_id"])
                if not ejercicio_resuelto:
                    ejercicios_filtrados.append(ejercicio)

            return {
                "ejercicios": ejercicios_filtrados,
                "total_ejercicios": len(ejercicios_filtrados),    
                "total_resueltos": len(ejercicios) - len(ejercicios_filtrados)
            }
        except Exception as e:
            return {"error": str(e)}