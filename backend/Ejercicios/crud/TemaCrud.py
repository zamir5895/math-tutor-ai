from fastapi import APIRouter, HTTPException, Request
from services.TemaService import TemaService
from models.Temas import CreateTema
from schemas.Temas import Tema

class CrudTemas:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route(
            "/", 
            self.create_tema, methods=["POST"], 
            response_model=Tema
            )
        
        self.router.add_api_route(
            "/{salon_id}",  
            self.get_temas_by_salon_id,
            methods=["GET"],
            response_model=list[Tema]
        )
        self.router.add_api_route(
            "/topic/temas/{tema_id}",
            self.get_tema_by_tema_id,
            methods=["GET"],
            response_model=Tema
        )
        self.router.add_api_route(
            "/{tema_id}",
            self.delete_tema,
            methods=["DELETE"],
            response_model=dict
        )
        self.router.add_api_route(
            "/info/profesor",
            self.get_info_by_profesor_token,
            methods=["GET"],
            response_model=dict
        )
        self.router.add_api_route(
            "/info/salones/profesor",
            self.get_InfoOfAllSalonsByProfesorToken,
            methods=["GET"],
            response_model=dict
        )
        self.router.add_api_route(
            "/info/salon/{salon_id}",
            self.get_info_salon_id,
            methods=["GET"],
            response_model=dict
        )
        self.router.add_api_route(
            "/update/orden/{tema_id}/{orden}",
            self.updateTemaOrden,
            methods=["PUT"],
            response_model=dict
        )
        self.router.add_api_route(
            "/info/all",
            self.getAllInfoOfTemas,
            methods=["GET"],
            response_model=dict
        )
        self.service = TemaService()
    
    async def create_tema(self, tema: CreateTema):
        try:
            result = await self.service.createTema(tema)
            if "error" in result:
                raise HTTPException(status_code=400, detail=result["error"])
            return result["tema"]
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def get_temas_by_salon_id(self, salon_id: str):
        try:
            temas = await self.service.getTemasBySalonId(salon_id)
            if "error" in temas:
                raise HTTPException(status_code=400, detail=temas["error"])
            return temas
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_tema_by_tema_id(self, tema_id: str):
        try:
            tema = await self.service.getTemaByTemaId(tema_id)
            if "error" in tema:
                raise HTTPException(status_code=404, detail=tema["error"])
            return tema
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))    

    async def delete_tema(self, tema_id: str):
        try:
            result = await self.service.deleteTema(tema_id)
            if "error" in result:
                raise HTTPException(status_code=404, detail=result["error"])
            return result
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_info_by_profesor_token(self, request:Request):
        try:
            token = request.headers.get("Authorization")
            if not token:
                raise HTTPException(status_code=401, detail="Token not provided")
            
            response = await self.service.getInfoSalonByProfesorToken(token)
            if "error" in response:
                raise HTTPException(status_code=400, detail=response["error"])
            return response
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def get_InfoOfAllSalonsByProfesorToken(self, request: Request):
        try:
            token = request.headers.get("Authorization")
            if not token:
                raise HTTPException(status_code=401, detail="Token not provided")
            
            response = await self.service.getInfoOfAllSalonByProfesorToken(token)
            if "error" in response:
                raise HTTPException(status_code=400, detail=response["error"])
            return {
                "salones": response
            }
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def get_info_salon_id(self, salon_id:str, request: Request):
        try:
            token = request.headers.get("Authorization")
            if not token:
                raise HTTPException(status_code=401, detail="Token not provided")

            response = await self.service.getInfoOfSalonId(salon_id, token)
            if "error" in response:
                raise HTTPException(status_code=400, detail=response["error"])
            return response
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def updateTemaOrden(self, tema_id: str, orden: int):
        try:
            result = await self.service.updateTemaOrden(tema_id, orden)
            if "error" in result:
                raise HTTPException(status_code=400, detail=result["error"])
            return {
                "message": "Tema orden updated successfully",
                "tema_id": tema_id,
                "new_order": orden
            }
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    async def getAllInfoOfTemas(self, request: Request):
        try:
            token = request.headers.get("Authorization")
            print(token)
            if not token:
                raise HTTPException(status_code=401, detail="Token not provided")
            
            response = await self.service.getAllInfoOfTemas(token)
            if "error" in response:
                print(response)
                raise HTTPException(status_code=400, detail=response["error"])
            return response
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

crud_temas = CrudTemas()
router = crud_temas.router