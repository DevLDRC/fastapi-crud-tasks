from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SQLITE_DATABASE_URL = "sqlite:///./sql_app.db"

# connect_args={"check_same_thread": False} é necessário apenas no SQLite para FastAPI
engine = create_engine(
    SQLITE_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency Injection para gerenciar sessões por requisição
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
