from sqlalchemy import create_engine, Column, Integer, Boolean, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from pydantic import BaseModel
from typing import Optional
import logging, uuid, datetime

logging.basicConfig(level=logging.INFO)

DATABASE_URL = f"postgresql://db/analysis"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    dateScanned = Column(DateTime(timezone=True), default=func.now())
    name = Column(String)
    description = Column(String, nullable=True)
    dateCreated = Column(DateTime(timezone=True))
    location = Column(String, nullable=True)
    type = Column(String)

class Statistics(Base):
    __tablename__ = "statistics"

    id = Column(Integer, primary_key=True, index=True)
    totalStorageGB = Column(Float)
    totalFiles = Column(Integer)
    totalFolders = Column(Integer)

Base.metadata.create_all(bind=engine)

class FileCreate(BaseModel):
    name: str
    description: Optional[str] = None
    dateCreated: datetime.datetime
    location: Optional[str] = None
    type: str

class FileOut(FileCreate):
    id: int
    dateScanned: datetime.datetime

    class Config:
        orm_mode = True