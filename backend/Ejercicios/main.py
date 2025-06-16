from fastapi import FastAPI
from crud.EjerciciosCrud import router as ejercicios_router 
from crud.TemaCrud import router as tema_router
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from crud.SubTemaCrud import router as subtema_router

app = FastAPI(
    title="Matemix Content Service",
    description="Microservicio para ejercicios y recursos educativos",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(ejercicios_router, prefix="/exercises", tags=["Ejercicios"])
app.include_router(tema_router, prefix="/topics", tags=["Temas"])
app.include_router(subtema_router, prefix="/subtopics", tags=["Subtemas"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Matemix Content Service!"}