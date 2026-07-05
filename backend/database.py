from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./maria_art.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Artwork(Base):
    __tablename__ = "artworks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    technique = Column(String)  # "Масло, холст · 40×50 см"
    price = Column(Integer)     # храним в копейках или рублях
    description = Column(Text, nullable=True)
    image_url = Column(String)
    avito_id = Column(String, nullable=True)  # для синхронизации с Авито
    is_available = Column(Integer, default=1)  # 1 = доступна, 0 = продана


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()