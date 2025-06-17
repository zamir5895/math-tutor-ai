from Repositorio.TemaRepositorio import TemaRepository
from models.Temas import CreateTema
from schemas.Temas import Tema
from Repositorio.SubTemaRepositorio import SubTemaRepository 
import httpx
class TemaService:
    def __init__(self):
        self.tema_repository = TemaRepository()
        self.subtema_repository = SubTemaRepository()
    async def createTema(self, createTema: CreateTema):
        
        try:
            print(createTema)
            if await self.tema_repository.exists(createTema.nombre, createTema.classroom_id):

                return {"error": "El tema ya existe en el salon"}
            print("Paso el error")
            created_tema = await self.tema_repository.createTema(createTema)
            if created_tema is None:
                return {"error": "No se pudo crear el tema"}
            tema = await self.tema_repository.getTemaById(created_tema)
            tema["_id"]=str(tema["_id"])  
            tema["subtema_id"] = [str(subtema) for subtema in tema.get("subtema_id", [])]  # Convertir ObjectId a str
            print(tema)

            return {"tema": Tema(**tema)}
        except Exception as e:
            return {"error": str(e)}
    
    async def getTemasBySalonId(self, classroom_id: int):
        try:
            temas = await self.tema_repository.getTemasBySalonId(classroom_id)
            for tema in temas:
                tema["_id"] = str(tema["_id"]) 
                tema["subtema_id"] = [str(subtema) for subtema in tema.get("subtema_id", [])]  # Convertir ObjectId a str
            return temas
        except Exception as e:
            return {"error": str(e)}
    
    async def getTemaByTemaId(self, tema_id: str):
        try:
            tema = await self.tema_repository.getTemaById(tema_id)
            if tema is None:
                return {"error": "Tema no encontrado"}
            tema["_id"] = str(tema["_id"])
            tema["subtema_id"] = [str(subtema) for subtema in tema.get("subtema_id", [])]  # Convertir ObjectId a str
            return Tema(**tema)
        except Exception as e:
            return {"error": str(e)}
    
    async def deleteTema(self, tema_id: str):
        try:
            tema = await self.tema_repository.getTemaById(tema_id)
            if tema is None:
                return {"error": "Tema no encontrado"}
            deleted_tema = await self.tema_repository.deleteTema(tema_id)
            if deleted_tema is None:
                return {"error": "No se pudo eliminar el tema"}
            return {
                "message": "Tema eliminado exitosamente",
                "tema_id": tema_id
            }
        except Exception as e:
            return {"error": str(e)}
        
    async def getInfoSalonByProfesorToken(self, token:str):
        try:
            url = f"http://localhost:8090/salon/profesor"
            headers = {"Authorization": token}
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()  
                data= response.json()
                print("Datos obtenidos de la API externa:", data)
                cantidadTemas = 0
                cantidadSubtemas = 0
                for id in data.get("salonIds"):
                    temas = await self.tema_repository.getTemasBySalonId(id)
                    if temas is None:
                        cantidadTemas += 0
                    else:    
                        cantidadTemas += len(temas)
                        for tema in temas:
                            subtemas = await self.subtema_repository.getSubTemasByTemaId(tema["_id"])
                            if subtemas is None:
                                cantidadSubtemas += 0
                            else:
                                cantidadSubtemas += len(subtemas)
            return {
                "totalTemas": cantidadTemas,
                "totalSubtemas": cantidadSubtemas,
                "totalAlumnos": data.get("cantidadAlumnos"),
                "totalSalones": len(data.get("salonIds", [])),
            }

        except httpx.RequestError as e: 
            return {"error": f"Error de conexión a la API externa: {str(e)}"}                
        except httpx.HTTPStatusError as e:
            return {"error": f"Error en la API externa: {e.response.text}"}
        except Exception as e:
            return {"error": str(e)}
        
    async def getInfoOfAllSalonByProfesorToken(self, token:str):
        try:
            url = f"http://localhost:8090/salon/profesor/my-salons"
            headers = {"Authorization": token}
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                data = response.json()
                salones = []
                cantidadTemas = 0
                cantidadSubtemas = 0

                for salon in data:
                    salon_id = salon.get("id")
                    temas = await self.tema_repository.getTemasBySalonId(salon_id)
                    if temas is None:
                        cantidadTemas = 0
                    else:
                        cantidadTemas += len(temas)
                        for tema in temas:
                            tema["_id"] = str(tema["_id"])
                            tema["subtema_id"] = [str(subtema) for subtema in tema.get("subtema_id", [])]
                            subtemas = await self.subtema_repository.getSubTemasByTemaId(tema["_id"])
                            if subtemas is None:
                                cantidadSubtemas = 0
                            else:
                                cantidadSubtemas += len(subtemas)
                    
                    salon_info = {
                        "id": salon_id,
                        "nombre": salon.get("nombre"),
                        "grado": salon.get("grado"),
                        "seccion": salon.get("seccion"),
                        "turno": salon.get("turno"),
                        "descripcion": salon.get("descripcion"),
                        "totalTemas": cantidadTemas,
                        "totalSubtemas": cantidadSubtemas,
                        "totalAlumnos": salon.get("cantidadAlumnos", 0)
                    }
                    salones.append(salon_info)
                    cantidadTemas = 0
                    cantidadSubtemas = 0        
                        
                return salones

        except httpx.RequestError as e: 
            return {"error": f"Error de conexión a la API externa: {str(e)}"}                
        except httpx.HTTPStatusError as e:
            return {"error": f"Error en la API externa: {e.response.text}"}
        except Exception as e:
            return {"error": str(e)}
        
    async def getAlumnosBySalonId(self, salon_id: str, token: str):
        try:
            url = f"http://localhost:8090/salon/alumnos/{salon_id}"
            headers = {"Authorization": token}
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                data = response.json()
                return data.get("data", [])
        except httpx.RequestError as e:
            return {"error": f"Error de conexión a la API externa: {str(e)}"}
        except httpx.HTTPStatusError as e:
            return {"error": f"Error en la API externa: {e.response.text}"}
        except Exception as e:
            return {"error": str(e)}
    
    async def getInfoOfSalonId(self, salon_id:str, token:str):
        try:
            url = f"http://localhost:8090/salon/{salon_id}"
            headers = {"Authorization": token}
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                data = response.json().get("data", {})
                cantidadTemas = 0
                cantidadSubtemas = 0
                temasResponse = await self.getTemasBySalonId(salon_id)
                
                temas = await self.tema_repository.getTemasBySalonId(salon_id)
                if temas is None:
                    cantidadTemas = 0
                else:
                    cantidadTemas += len(temas)
                    for tema in temas:
                        tema["_id"] = str(tema["_id"])
                        tema["subtema_id"] = [str(subtema) for subtema in tema.get("subtema_id", [])]
                        subtemas = await self.subtema_repository.getSubTemasByTemaId(tema["_id"])
                        if subtemas is None:
                            cantidadSubtemas = 0
                        else:
                            cantidadSubtemas += len(subtemas)
                alumons = await self.getAlumnosBySalonId(salon_id, token)
                if "error" in alumons:
                    return {"error": alumons["error"]}
                if not data:
                    return {"error": "No se encontraron datos para el salon especificado"}
                return {
                    "id": salon_id,
                    "nombre": data.get("nombre"),
                    "grado": data.get("grado"),
                    "seccion": data.get("seccion"),
                    "turno": data.get("turno"),
                    "descripcion": data.get("descripcion"),
                    "totalTemas": cantidadTemas,
                    "totalSubtemas": cantidadSubtemas,
                    "totalAlumnos": data.get("cantidadAlumnos", 0),
                    "temas": temasResponse,
                    "alumnos": alumons

                }
        except httpx.RequestError as e:
            return {"error": f"Error de conexión a la API externa: {str(e)}"}
        except httpx.HTTPStatusError as e:
            return {"error": f"Error en la API externa: {e.response.text}"}
        except Exception as e:
            return {"error": str(e)}
    
    async def updateTemaOrden(self, tema_id: str, orden: int):
        try:
            tema = await self.tema_repository.getTemaById(tema_id)
            if tema is None:
                return {"error": "Tema no encontrado"}
            updated_tema = await self.tema_repository.updateTemaOrder(tema_id, orden)
            if not updated_tema:
                return {"error": "No se pudo actualizar el orden del tema"}
            return {"message": "Orden del tema actualizado exitosamente", "tema_id": tema_id}
        except Exception as e:
            return {"error": str(e)}
        
    async def getAllTemasAndSubtemasForAlumno(self, token: str):
        try:
            url = f"http://localhost:8090/alumno/student/salon"
            headers = {"Authorization": token}
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers)
                print("Response status code:", response.json())
                response.raise_for_status()
                data = response.json()
                temas = []
                salon_id = data.get("id")
                if not salon_id:
                    return {"error": "No se encontró el salon del alumno"}
                temas_data = await self.tema_repository.getTemasBySalonId(salon_id)
                if not temas_data:
                    return {"error": "No se encontraron temas para el salon del alumno"}
                cantidadTemas = len(temas_data)
                for tema in temas_data:
                    tema["_id"] = str(tema["_id"])
                    # Obtener subtemas completos para cada tema
                    subtemas = await self.subtema_repository.getSubTemasByTemaId(tema["_id"])
                    if subtemas:
                        for subtema in subtemas:
                            subtema["_id"] = str(subtema["_id"])
                            subtema["tema_id"] = str(subtema.get("tema_id", ""))
                        tema["cantidadSubtemas"] = len(subtemas)
                    else:
                        tema["cantidadSubtemas"] = 0
                    tema["subtema_id"] = [str(subtema) for subtema in tema.get("subtema_id", [])]
                    temas.append(tema)
                return {
                    "salon_id": salon_id,
                    "temas": temas,
                    "totalTemas": cantidadTemas 
                }
        except httpx.RequestError as e:
            return {"error": f"Error de conexión a la API externa: {str(e)}"}
        except httpx.HTTPStatusError as e:
            return {"error": f"Error en la API externa: {e.response.text}"}
        except Exception as e:
            return {"error": str(e)}

    async def getAllInfoOfTemas(self, token: str):

        try:

            url = f"http://localhost:8090/salon/profesor/my-salons"

            headers = {"Authorization": token}

            async with httpx.AsyncClient() as client:

                response = await client.get(url, headers=headers)

                response.raise_for_status()

                data = response.json()

                tem = []

                totalTemas = 0

                totalSubtemas = 0

                for salon in data:

                    temas_info= {}

                    salon_id = salon.get("id")

                    temas = await self.tema_repository.getTemasBySalonId(salon_id)

                    if not temas:

                        temas = []

                    totalTemas += len(temas)

                    for tema in temas:

                        tema["_id"] = str(tema["_id"])

                        tema["subtema_id"] = [str(subtema) for subtema in tema.get("subtema_id", [])]

                        totalSubtemas += len(tema.get("subtema_id", []))

                        temas_info = {

                            "_id": tema.get("_id"),

                            "nombre": tema.get("nombre"),

                            "descripcion": tema.get("descripcion"),

                            "orden": tema.get("orden", 0),

                            "totalSubtemas": len(tema.get("subtema_id", [])),

                            "totalAlumnos": salon.get("cantidadAlumnos", 0),

                        }

                        tem.append(temas_info)



                return {

                    "totalSalones": len(data),

                    "totalTemas": totalTemas,

                    "totalSubtemas": totalSubtemas,

                    "temas": tem

                }

        except httpx.RequestError as e:

            return {"error": f"Error de conexión a la API externa: {str(e)}"}

        except httpx.HTTPStatusError as e:

            return {"error": f"Error en la API externa: {e.response.text}"}

        except Exception as e:


            return {"error": str(e)}