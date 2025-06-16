from pydantic import BaseModel, Field

class CreateSubtema(BaseModel):
    titulo: str
    descripcion: str | None = None
    video_url: list[str] = Field(default_factory=list)
    preguntas: dict[str, list[str]] = Field(default_factory=dict)
    tema_id:str
    orden: int



class YoutubeTemasCreation(BaseModel):
    url: str
    id: str
    title: str
    thumbnail: str

class ListYoutubeTemasCreation(BaseModel):
    videos: list[YoutubeTemasCreation] = Field(default_factory=list)



