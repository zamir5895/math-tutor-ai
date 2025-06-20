from Repositorio.EjercicioRepositorio import EjercicioRepository
from Repositorio.SubTemaRepositorio import SubTemaRepository
from Repositorio.TemaRepositorio import TemaRepository
from services.IAService import GPTService
from Repositorio.EjerciciosResueltosRepositorio import EjercicioResueltosRepository
import httpx
import asyncio
from models.Ejerccicio import EjercicioCreate, EjercicioResueltoCreate, UpdateRespuesta, GetEjercicios, EstadisticaCreateRequest
class EjercicioService:
    def __init__(self):
        self.ejercicio_repository = EjercicioRepository()
        self.subtema_repository = SubTemaRepository()
        self.tema_repository = TemaRepository()
        self.ia_services = GPTService()
        self.ejercicios_resueltos_repository = EjercicioResueltosRepository()

    async def notificarEstadisticas(self, token:str, salon_id:str, tema_id:str, subtema_id:str, nivel:dict[str,int]):
        try:
            print("Entrando a notificarEstadisticas")
            url = f"http://users:8090/salon/{salon_id}"
            headers = {"Authorization": token}
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers)
                print("Respuesta de salon:", response.status_code, response.text)
                response.raise_for_status()
                data = response.json().get("data", {})
                alumnos = data.get("alumnosIds", [])
                print("Alumnos encontrados:", alumnos)
                tareas = []
                urlEstadisticas = f"http://statistics:8050/estadisticas/init"
                for alumno in alumnos:
                    json_data = {
                        "alumno_id": str(alumno),
                        "tema_id": str(tema_id),
                        "salon_id": str(salon_id),
                        "subtema_id": str(subtema_id),
                        "ejercicios_por_nivel": nivel
                    }
                    print("Enviando estadística para:", json_data)
                    tareas.append(client.post(urlEstadisticas, json=json_data, headers=headers))
                resultados = await asyncio.gather(*tareas, return_exceptions=True)
                print("Resultados de POST estadísticas:", resultados)
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    async def generar_ejercicios_with_gpt(self, id:str, token:str):
        try:
            subtema = await self.subtema_repository.getSubTemaById(id)
            if subtema is None:
                return {"error": "El subtema no existe"}

            ejercicios = await self.ia_services.generateExcersiceBaseOnSubtema(subtema["titulo"])
            if not ejercicios:
                return {"error": "No se pudieron generar ejercicios"}
            tema = await self.tema_repository.getTemaBySubtemaId(id)
            print("Tema encontrado:", tema)
            print("Subtema encontrado:", subtema)
            if tema is None:
                return {"error": "El tema del subtema no existe"}
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
            response = await self.getEjerciciosBySubTemaId(id)
            ejercicio_por_nivel = {
                "facil": len(response["ejercicios"].get("facil", [])),
                "medio": len(response["ejercicios"].get("medio", [])),
                "dificil": len(response["ejercicios"].get("dificil", [])),
            }
            print(f"token aca " + token)
            asyncio.create_task(
                self.notificarEstadisticas(token, tema["classroom_id"], tema["_id"], id, ejercicio_por_nivel)
            )
            return response
        except Exception as e:
            print(f"Error al generar ejercicios: {str(e)}")
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
    
    async def createEjercicioManual(self,subtema_id:str, token:str, ejercicio_data: EjercicioCreate):
        try:
            ejercicio_id = await self.ejercicio_repository.createEjercicio(ejercicio_data)
            if ejercicio_id is None:
                return {"error": "No se pudo crear el ejercicio"}
            ejercicio = await self.ejercicio_repository.getEjercicioById(ejercicio_id)
            if ejercicio is None:
                return {"error": "El ejercicio creado no existe"}
            added = await self.subtema_repository.addEjercicioToSubTema(subtema_id, ejercicio_id, ejercicio["nivel"])
            if not added:
                return {"error": "No se pudo agregar el ejercicio al subtema"}
            tema = await self.tema_repository.getTemaBySubtemaId(subtema_id)
            if tema is None:
                return {"error": "El tema del subtema no existe"}   
            nivel = ejercicio_data.nivel.value if hasattr(ejercicio_data.nivel, "value") else ejercicio_data.nivel
            ejercicio_nivel = {
                "facil": 1 if nivel == "facil" else 0,
                "medio": 1 if nivel == "medio" else 0,
                "dificil": 1 if nivel == "dificil" else 0
            }
            asyncio.create_task(
                self.notificarEstadisticas(token, tema["classroom_id"], tema["_id"], subtema_id, ejercicio_nivel)
            )
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

    async def createEjercicioManualmente(self, ejercicio: EjercicioCreate, subtema_id: str):
        try:
            ejercicio_id = await self.ejercicio_repository.createEjercicio(ejercicio)
            if ejercicio_id is None:
                return {"error": "No se pudo crear el ejercicio"}
            ejercicio = ejercicio.dict()
            added = await self.subtema_repository.addEjercicioToSubTema(subtema_id, ejercicio_id, ejercicio["nivel"].value)
            if not added:
                return {"error": "No se pudo agregar el ejercicio al subtema"}
            print(added)
            ejercicio_response = await self.ejercicio_repository.getEjercicioById(ejercicio_id)
            if ejercicio_response is None:
                return {"error": "No se pudo obtener el ejercicio creado"}
            return ejercicio_response
        except Exception as e:
            return {"error": str(e)}
    
    async def deleteEjercicio(self, ejercicio_id:str, subtema_id: str):
        try:
            ejercicio = await self.ejercicio_repository.getEjercicioById(ejercicio_id)
            removed = await self.subtema_repository.removeEjercicioFromSubTema(subtema_id, ejercicio_id, ejercicio["nivel"])
            if ejercicio is None:
                return {"error": "El ejercicio no existe"}
            
            if not removed:
                return {"error": "No se pudo eliminar el ejercicio del subtema"}
            
            # Elimina el ejercicio de la base de datos
            deleted = await self.ejercicio_repository.deleteEjercicio(ejercicio_id)
            if not deleted:
                return {"error": "No se pudo eliminar el ejercicio"}
            # Elimina los registros de ejercicios resueltos relacionados
            await self.ejercicios_resueltos_repository.deleteEjercicioResueltoByEjercicioId(ejercicio_id)
            return {"message": "Ejercicio eliminado correctamente"}
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