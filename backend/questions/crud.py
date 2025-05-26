from sqlalchemy.orm import Session
from models import Topic, Question, StudentQuestion, StudentTopic

def create_topic(db: Session, nombre: str):
    topic = Topic(nombre=nombre)
    db.add(topic)
    db.commit()
    db.refresh(topic)
    return topic

def get_all_topics(db: Session):
    return db.query(Topic).all()

def create_question(db: Session, **kwargs):
    question = Question(**kwargs)
    db.add(question)
    db.commit()
    db.refresh(question)
    return question

def get_questions_by_topic(db: Session, topic_id: int):
    return db.query(Question).filter(Question.topic_id == topic_id).all()

def mark_question_completed(db: Session, student_id: int, question_id: int):
    record = db.query(StudentQuestion).filter_by(student_id=student_id, question_id=question_id).first()
    if record:
        record.completado = True
    else:
        record = StudentQuestion(student_id=student_id, question_id=question_id, completado=True)
        db.add(record)
    db.commit()
    return record

def enroll_user_to_topic(db: Session, user_id: int, topic_id: int):
    # Inscribir preguntas
    questions = db.query(Question).filter(Question.topic_id == topic_id).all()
    new_links = []

    for q in questions:
        exists = db.query(StudentQuestion).filter_by(user_id=user_id, question_id=q.id).first()
        if not exists:
            link = StudentQuestion(user_id=user_id, question_id=q.id, completado=False)
            db.add(link)
            new_links.append(link)

    # Inscribir topic con nivel inicial "Facil"
    topic_link = db.query(StudentTopic).filter_by(user_id=user_id, topic_id=topic_id).first()
    if not topic_link:
        topic_link = StudentTopic(user_id=user_id, topic_id=topic_id, nivel="Facil")
        db.add(topic_link)

    db.commit()
    return new_links, topic_link

