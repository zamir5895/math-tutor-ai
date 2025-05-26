from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Reconstruir la URL a partir de partes
USER = os.getenv("DATASOURCE_USERNAME")
PASS = os.getenv("DATASOURCE_PASSWORD")
HOST = os.getenv("DATABASE_HOST", "localhost")
PORT = os.getenv("DATABASE_PORT", "5432")
DB   = os.getenv("DATABASE_NAME")

DATABASE_URL = f"postgresql://{USER}:{PASS}@{HOST}:{PORT}/{DB}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
