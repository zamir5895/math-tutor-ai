from fastapi import FastAPI, Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from typing import Optional
import models, crud

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "FastAPI + PostgreSQL funcionando"}

@app.post("/topics/")
def add_topic(nombre: str, db: Session = Depends(get_db)):
    return crud.create_topic(db, nombre)

@app.get("/topics/")
def list_topics(db: Session = Depends(get_db)):
    return crud.get_all_topics(db)

@app.post("/questions/")
def add_question(pregunta: str,
                 respuesta_correcta: str,
                 respuesta_incorrecta1: str,
                 respuesta_incorrecta2: str,
                 respuesta_incorrecta3: str,
                 dificultad: str,
                 topic_id: int,
                 db: Session = Depends(get_db)):
    return crud.create_question(
        db,
        pregunta=pregunta,
        respuesta_correcta=respuesta_correcta,
        respuesta_incorrecta1=respuesta_incorrecta1,
        respuesta_incorrecta2=respuesta_incorrecta2,
        respuesta_incorrecta3=respuesta_incorrecta3,
        dificultad=dificultad,
        topic_id=topic_id
    )

@app.get("/questions/by-topic/{topic_id}")
def questions_by_topic(
    topic_id: int,
    question_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Question).filter(models.Question.topic_id == topic_id)
    
    if question_id is not None:
        query = query.filter(models.Question.id == question_id)
    
    results = query.all()
    return results

@app.get("/students_questions/")
def get_student_questions(user_id: int, db: Session = Depends(get_db)):
    records = db.query(models.StudentQuestion).filter(models.StudentQuestion.user_id == user_id).all()
    if not records:
        raise HTTPException(
            status_code=404,
            detail="No tienes preguntas inscritas. Usa /enroll-topic/?user_id=...&topic_id=... para inscribirte."
        )
    return records

@app.get("/students_questions/by-topic/")
def get_student_questions_by_topic(
    user_id: int,
    topic_id: int,
    completado: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    query = (
        db.query(models.StudentQuestion)
        .join(models.Question, models.StudentQuestion.question_id == models.Question.id)
        .filter(models.StudentQuestion.user_id == user_id)
        .filter(models.Question.topic_id == topic_id)
    )
    
    if completado is not None:
        query = query.filter(models.StudentQuestion.completado == completado)
        
    records = query.all()

    if not records:
        raise HTTPException(
            status_code=404,
            detail="No tienes preguntas inscritas para este topic con ese filtro. Usa /enroll-topic/?user_id=...&topic_id=... para inscribirte."
        )
    return records




@app.post("/students_questions/")
def complete_question(user_id: int, question_id: int, db: Session = Depends(get_db)):
    record = db.query(models.StudentQuestion).filter_by(user_id=user_id, question_id=question_id).first()
    
    if not record:
        raise HTTPException(
            status_code=422,
            detail="No estás inscrito en esta pregunta. Usa el endpoint /enroll-topic/?user_id=...&topic_id=... para registrarte a las preguntas del tema."
        )
    
    record.completado = True
    db.commit()
    return record

@app.post("/enroll-topic/")
def enroll_topic(user_id: int, topic_id: int, db: Session = Depends(get_db)):
    new_links, topic_link = crud.enroll_user_to_topic(db, user_id, topic_id)
    return {
        "message": f"Usuario {user_id} inscrito a {len(new_links)} preguntas del topic {topic_id}.",
        "preguntas_registradas": [link.question_id for link in new_links],
        "topic_inscripcion": {
            "user_id": topic_link.user_id,
            "topic_id": topic_link.topic_id,
            "nivel": topic_link.nivel
        }
    }

@app.get("/student_topics/")
def get_student_topics(
    user_id: int,
    topic_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.StudentTopic).filter(models.StudentTopic.user_id == user_id)

    if topic_id is not None:
        query = query.filter(models.StudentTopic.topic_id == topic_id)

    records = query.all()

    if not records:
        raise HTTPException(
            status_code=404,
            detail="No tienes topics inscritos con ese filtro. Usa /enroll-topic/ para inscribirte."
        )
    return records



@app.post("/student_topics/update-level/")
def update_student_topic_level(
    user_id: int,
    topic_id: int,
    nivel: str,
    db: Session = Depends(get_db)
):
    record = db.query(models.StudentTopic).filter_by(user_id=user_id, topic_id=topic_id).first()
    if not record:
        raise HTTPException(
            status_code=404,
            detail="No existe inscripción para ese usuario y topic."
        )
    record.nivel = nivel
    db.commit()
    db.refresh(record)
    return {
        "user_id": record.user_id,
        "topic_id": record.topic_id,
        "nivel": record.nivel,
        "message": "Nivel actualizado correctamente"
    }