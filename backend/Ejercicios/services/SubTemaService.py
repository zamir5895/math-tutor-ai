from Repositorio.TemaRepositorio import TemaRepository
from models.Subtema import CreateSubtema,ListYoutubeTemasCreation
from schemas.Temas import Subtema
from Repositorio.SubTemaRepositorio import SubTemaRepository
from services.IAService import GPTService
from services.YoutubeService import YoutubeService
from bson import ObjectId
import json
import os
class SubTemaService:

    def __init__(self):
        self.tema_repository = TemaRepository()
        self.subtema_repository = SubTemaRepository()
        self.ia_service = GPTService()
        self.youtube_service = YoutubeService()
    def fix_objectids(self,doc):
        if not doc:
            return doc
        doc = dict(doc)
        for key, value in doc.items():
            if isinstance(value, ObjectId):
                doc[key] = str(value)
        return doc
    async def createSubTema(self, createSubtema:CreateSubtema):
        try:
            tema = await self.tema_repository.getTemaById(createSubtema.tema_id)
            if tema is None:
                return {"error": "El tema no existe"}
            if await self.subtema_repository.exists(createSubtema.titulo, createSubtema.tema_id):
                return {"error": "El subtema ya existe en el tema"}
            
            created_subtema = await self.subtema_repository.createSubTema(createSubtema)
            if created_subtema is None:
                return {"error": "No se pudo crear el subtema"}

            agregado = await self.tema_repository.addSubTemaToTema(createSubtema.tema_id, created_subtema)
            subtema = await self.subtema_repository.getSubTemaById(created_subtema)
            subtema["_id"] = str(subtema["_id"])
            subtema["tema_id"] = str(subtema.get("tema_id", ""))
            return {"subtema": Subtema(**subtema)}
        
        except Exception as e:
            return {"error": str(e)}
    
    async def getSubTemasByTemaId(self, tema_id: str):
        try:
            tema = await self.tema_repository.getTemaById(tema_id)
            if tema is None:
                return {"error": "El salon no existe"}
            subtemas = await self.subtema_repository.getSubTemasByTemaId(tema_id)
            cont = 0
            for subtema in subtemas:
                subtema["_id"] = str(subtema["_id"])
                subtema["tema_id"] = str(subtema.get("tema_id", ""))
                # Unifica el campo a 'video_url'
                if "video_urls" in subtema:
                    subtema["video_url"] = subtema.pop("video_urls")
                elif "video_url" not in subtema:
                    subtema["video_url"] = []
                cont += 1
            
            return {"subtemas": subtemas, "count": cont}
        except Exception as e:
            return {"error": str(e)}
        
    async def getSubTemaById(self, subtema_id: str):
        try:
            subtema = await self.subtema_repository.getSubTemaById(subtema_id)
            if subtema is None:
                return {"error": "El subtema no existe"}
            subtema["_id"] = str(subtema["_id"])
            subtema["tema_id"] = str(subtema.get("tema_id", ""))
            return Subtema(**subtema)
        except Exception as e:
            return {"error": str(e)}
        
    async def generateSubTemasIdeas(self, tema_id:str):

        try:
            tema = await self.tema_repository.getTemaById(tema_id)
            if tema is None:
                return {"error": "El tema no existe"}
            tema_str = tema.get("nombre", "")
            if not tema_str:
                return {"error": "El tema no tiene un nombre válido"}

            PROMPT_TEMPLATE = """Genera ideas de subtemas para el tema: {tema} de acuerdo a la curricula nacional de educaion del Peru en el 2024 para alumnos de 2 grado de secundaria, la respuesta que sea un json que diga subtema y descripcion
            Ejemplo de respuesta:
            
                {{
                    "subtema": "Subtema 1",
                    "descripcion": "Descripcion del subtema 1"
                }},
                {{
                    "subtema": "Subtema 2",
                    "descripcion": "Descripcion del subtema 2"
                }}
            ]
            """
            print("Generando subtemas para el tema:", tema_str)
            try:
                prompt = PROMPT_TEMPLATE.format(tema=tema_str)
            except Exception as e:
                print("Error al formatear el prompt:", str(e))
                return {"error": f"Error al formatear el prompt: {str(e)}"}            
            resultado = await self.ia_service.gpt_connection(prompt)
            if isinstance(resultado, str):
                return {"error": "Error al procesar la respuesta del LLM"}
            if not isinstance(resultado, list):
                return {"error": "La respuesta del LLM no es una lista"}    
            subtemas = []
            for item in resultado:
                subtema = {
                    "titulo": item.get("subtema", ""),
                    "descripcion": item.get("descripcion", ""),
                    "tema": tema_str
                }
                subtemas.append(subtema)
            return subtemas
        except Exception as e:
            return {"error": str(e)}
    
    async def createListaSubTemas(self, subtemas: list[CreateSubtema]):
        try:
            created_subtemas = []
            errores = []
            for subtema in subtemas:
                created_subtema = await self.createSubTema(subtema)
                if "error" not in created_subtema:
                    created_subtemas.append(created_subtema)
            return {"subtemas": created_subtemas}
        except Exception as e:
            return {"error": str(e)}
    
    async def get_videos_ideas(self, id:str):
        try:
            subtema = await self.subtema_repository.getSubTemaById(id)
            if subtema is None:
                return {"error": "El subtema no existe"}
           
            descripcion = subtema.get("descripcion"," ")
            if not descripcion:
                return {"error": "No hay descripciones disponibles para el tema del subtema"}
            resultado =  await self.youtube_service.get_videos( subtema.get("titulo", ""), descripcion)
            print("Videos encontrados:", resultado)
            return {"videos": resultado}
        except Exception as e:
            return {"error": str(e)}
        
    
    async def addVideosToSubTema(self, subtema_id: str, videos_urls: ListYoutubeTemasCreation):
        try:
            subtema = await self.subtema_repository.getSubTemaById(subtema_id)
            if subtema is None:
                return {"error": "El subtema no existe"}
            videos = videos_urls.videos
            for video in videos:
                print(video)
                if not video.url.startswith("https://www.youtube.com/watch?v="):
                    return {"error": f"URL de video inválida: {video.url}"}
                added = await self.subtema_repository.addVideoToSubTema(subtema_id, video)
                if not added:
                    return {"error": f"No se pudo agregar el video: {video.url}"}
            response = await self.subtema_repository.getSubTemaById(subtema_id)
            response = self.fix_objectids(response)
            return {
                "message": "Videos agregados exitosamente",
                "subtema": response
            }
        except Exception as e:
            return {"error": str(e)}

    async def deleteSubTema(self, subtema_id: str):
        try:
            subtema = await self.subtema_repository.getSubTemaById(subtema_id)
            if subtema is None:
                return {"error": "El subtema no existe"}
            deleted = await self.subtema_repository.deleteSubTema(subtema_id)
            tema_id = subtema.get("tema_id")
            if tema_id:
                await self.tema_repository.removeSubTemaFromTema(tema_id, subtema_id)
            if not deleted:
                return {"error": "No se pudo eliminar el subtema"}
            return {"message": "Subtema eliminado exitosamente"}
        except Exception as e:
            return {"error": str(e)}
    
    async def deleteVideoFromSubTema(self, subtema_id: str, video_id: str):
        try:
            subtema = await self.subtema_repository.getSubTemaById(subtema_id)
            if subtema is None:
                return {"error": "El subtema no existe"}
            deleted = await self.subtema_repository.deleteVideoFromSubTema(subtema_id, video_id)
            if not deleted:
                return {"error": "No se pudo eliminar el video del subtema"}
            return {"message": "Video eliminado exitosamente"}
        except Exception as e:
            return {"error": str(e)}
    
    async def updateSubtemaOrden(self, subtema_id: str, orden: int):
        try:
            subtema = await self.subtema_repository.getSubTemaById(subtema_id)
            if subtema is None:
                return {"error": "El subtema no existe"}
            updated = await self.subtema_repository.updateSubtemaOrden(subtema_id, orden)
            if not updated:
                return {"error": "No se pudo actualizar el orden del subtema"}
            return {"message": "Orden del subtema actualizado exitosamente"}
        except Exception as e:
            return {"error": str(e)}
    
        