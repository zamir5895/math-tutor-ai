
from pydantic import BaseModel, Field



class CreateTema(BaseModel):
    nombre: str
    descripcion: str
    classroom_id: str
    subtema_id: list[str] = Field(default_factory=list)
    orden: int = 1


