from fastapi import APIRouter, HTTPException
from services.SubTemaService import SubTemaService
from models.Subtema import CreateSubtema,ListYoutubeTemasCreation
from schemas.Temas import Subtema

class CrudSubTemas:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route(
            "/", 
            self.create_subtema, 
            methods=["POST"], 
            response_model=Subtema)
        self.router.add_api_route(
            "/topic/subtemas/{tema_id}",
            self.get_subtemas_by_tema_id,
            methods=["GET"],
            response_model=dict
        )
        self.router.add_api_route(
            "/generate/{tema_id}",
            self.generateSubTemasIdeasByTemaId,
            methods=["GET"],
            response_model=list[dict]
        )
        self.router.add_api_route(
            "/{subtema_id}",
            self.get_subtema_by_id,
            methods=["GET"],
            response_model=Subtema
        )
        self.router.add_api_route(
            "/list",
            self.createSubtemasForList,
            methods=["POST"],
            response_model=dict

        )
        self.router.add_api_route(
            "/generate/video/{subtema_id}",
            self.generateVideosBySubTemaId,
            methods=["GET"],
            response_model=dict
        )
        self.router.add_api_route(
            "/videos/save/{subtema_id}",
            self.guardarvideos,
            methods=["POST"],
            response_model=dict
        )
        self.router.add_api_route(
            "/delete/{subtema_id}",
            self.deleteSubtema,
            methods=["DELETE"],
            response_model=dict
        )
        self.router.add_api_route(
            "/videos/delete/{subtema_id}/{video_id}",
            self.deleteVideoFromSubTema,
            methods=["DELETE"],
            response_model=dict
        )

        self.router.add_api_route(
            "/update/orden/{subtema_id}/{orden}",
            self.updateSubtemaOrden,
            methods=["PUT"],
            response_model=dict
        )
        self.router.add_api_route(
            "/student/{tema_id}",
            self.getSubtemasForStudent,
            methods=["GET"],
            response_model=dict
        )
        
        self.service = SubTemaService()

    async def create_subtema(self, subtema: CreateSubtema):
        try:
            result = await self.service.createSubTema(subtema)
            if "error" in result:
                raise HTTPException(status_code=400, detail=result["error"])
            return result["subtema"]
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_subtemas_by_tema_id(self, tema_id: str):
        try:
            subtemas = await self.service.getSubTemasByTemaId(tema_id)
            if "error" in subtemas:
                raise HTTPException(status_code=400, detail=subtemas["error"])
            return subtemas
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def generateSubTemasIdeasByTemaId(self, tema_id:str):
        try:
            print("Generando subtemas para el tema:", tema_id)
            result = await self.service.generateSubTemasIdeas(tema_id)
            if "error" in result:
                raise HTTPException(status_code=400, detail=result["error"])
            return result
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def get_subtema_by_id(self, subtema_id: str):
        try:
            subtema = await self.service.getSubTemaById(subtema_id)
            if "error" in subtema:
                raise HTTPException(status_code=400, detail=subtema["error"])
            return subtema
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def createSubtemasForList(self, subtemas: list[CreateSubtema]):
        try:
            result = await self.service.createListaSubTemas(subtemas)
            if "error" in result:
                raise HTTPException(status_code=400, detail=result["error"])
            return result
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def generateVideosBySubTemaId(self, subtema_id:str):
        try:
            print("Generando videos para el subtema:", subtema_id)
            result = await self.service.get_videos_ideas(subtema_id)
            if "error" in result:
                raise HTTPException(status_code=400, detail=result["error"])
            print("Videos generados:", result)
            return result
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def guardarvideos(self, subtema_id: str, videos:ListYoutubeTemasCreation):
        try:
            
            print("Guardando videos para el subtema:", subtema_id)
            result = await self.service.addVideosToSubTema(subtema_id, videos)
            if "error" in result:
                raise HTTPException(status_code=400, detail=result["error"])
            return result
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def deleteSubtema(self, subtema_id: str):
        try:
            result = await self.service.deleteSubTema(subtema_id)
            if "error" in result:
                raise HTTPException(status_code=400, detail=result["error"])
            return {"message": "Subtema deleted successfully"}
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    async def deleteVideoFromSubTema(self, subtema_id: str, video_id: str):
        try:
            result = await self.service.deleteVideoFromSubTema(subtema_id, video_id)
            if "error" in result:
                raise HTTPException(status_code=400, detail=result["error"])
            return {"message": "Video deleted successfully"}
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def updateSubtemaOrden(self, subtema_id: str, orden: int):
        try:
            result = await self.service.updateSubtemaOrden(subtema_id, orden)
            if "error" in result:
                raise HTTPException(status_code=400, detail=result["error"])
            return {"message": "Subtema order updated successfully"}
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def getSubtemasForStudent(self, tema_id: str):
        try:
            subtemas = await self.service.getSubtemasByTemaIdForStudent(tema_id)
            if "error" in subtemas:
                raise HTTPException(status_code=400, detail=subtemas["error"])
            return subtemas
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
crud_subtemas = CrudSubTemas()
router = crud_subtemas.router