from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, BigInteger
from database import Base

# ---------------------------------------
# Mapeo mínimo de la tabla existente 'users'
# ---------------------------------------
class User(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True, index=True)
    # No definimos las demás columnas para evitar conflictos,
    # ya que solo necesitamos resolver ForeignKeys.

# ---------------------------------------
# Tema de la pregunta
# ---------------------------------------
class Topic(Base):
    __tablename__ = "topic"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)

# ---------------------------------------
# Pregunta con opciones y dificultad
# ---------------------------------------
class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    pregunta = Column(Text, nullable=False)
    respuesta_correcta = Column(Text, nullable=False)
    respuesta_incorrecta1 = Column(Text, nullable=False)
    respuesta_incorrecta2 = Column(Text, nullable=False)
    respuesta_incorrecta3 = Column(Text, nullable=False)
    dificultad = Column(String(10), nullable=False)  # 'easy', 'medium', 'hard'
    topic_id = Column(Integer, ForeignKey("topic.id"), nullable=False)

# ---------------------------------------
# Relación usuario ↔ pregunta con estado de completado
# ---------------------------------------
class StudentQuestion(Base):
    __tablename__ = "students_questions"
    user_id = Column(BigInteger, ForeignKey("users.id"), primary_key=True)
    question_id = Column(Integer, ForeignKey("questions.id"), primary_key=True)
    completado = Column(Boolean, default=False)



class StudentTopic(Base):
    __tablename__ = "student_topics"
    user_id = Column(BigInteger, ForeignKey("users.id"), primary_key=True)
    topic_id = Column(Integer, ForeignKey("topic.id"), primary_key=True)
    nivel = Column(String(50), nullable=False, default="Facil")
