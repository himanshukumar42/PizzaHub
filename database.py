from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine


SQLALCHEMY_DATABASE_URL = "sqlite:///./pizza_db.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autoflush=False, bind=engine)
Base = declarative_base()
