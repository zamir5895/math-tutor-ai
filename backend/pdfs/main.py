
# main.py
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from database import connect_to_mongo, close_mongo_connection
from pdf_processor import PDFProcessor
from services import ExerciseService
from models import ProcessPDFResponse, ExerciseResponse
from typing import List
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="PDF Exercises Processor API",
    description="API para procesar PDFs con ejercicios y almacenarlos en MongoDB",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Eventos de inicio y cierre
@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()
    logger.info("Connected to MongoDB")

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()
    logger.info("Disconnected from MongoDB")

# Instancia del procesador
pdf_processor = PDFProcessor()

@app.post("/upload-pdf/", response_model=ProcessPDFResponse)
async def upload_and_process_pdf(file: UploadFile = File(...)):
    """
    Endpoint principal: Sube un PDF, lo procesa y guarda los ejercicios en MongoDB
    """
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="El archivo debe ser un PDF")
    
    try:
        # 1. Extraer texto del PDF
        logger.info(f"Processing PDF: {file.filename}")
        text = pdf_processor.extract_text_from_pdf(file.file)
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="No se pudo extraer texto del PDF")
        
        # 2. Procesar texto y extraer ejercicios
        exercises = await pdf_processor.process_with_ai(text)
        
        if not exercises:
            raise HTTPException(status_code=400, detail="No se encontraron ejercicios en el PDF")
        
        # 3. Guardar ejercicios en MongoDB
        exercise_ids = await ExerciseService.save_exercises(exercises)
        
        logger.info(f"Saved {len(exercises)} exercises from {file.filename}")
        
        return ProcessPDFResponse(
            message=f"PDF procesado exitosamente. Se encontraron {len(exercises)} ejercicios.",
            total_exercises=len(exercises),
            exercises_ids=exercise_ids
        )
        
    except Exception as e:
        logger.error(f"Error processing PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error procesando PDF: {str(e)}")



@app.get("/")
async def root():
    return {"message": "PDF Exercises Processor API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# .env (archivo de configuración)
