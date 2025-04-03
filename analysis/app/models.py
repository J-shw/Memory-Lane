from sqlalchemy import create_engine, Column, Integer, Boolean, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from pydantic import BaseModel
from typing import Optional
import logging, uuid, datetime

logging.basicConfig(level=logging.INFO)

DATABASE_URL = f"postgresql://postgres:password@db:5432/analysis"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    dateScanned = Column(DateTime(timezone=True), default=func.now())
    name = Column(String)
    dateCreated = Column(DateTime(timezone=True))
    dateModified = Column(String, nullable=True)
    path = Column(String, nullable=True)
    mimeType = Column(String, nullable=True)
    extension = Column(String)
    size = Column(Float) #bytes
    

class Volume(Base):
    __tablename__ = "volumes"

    id = Column(Integer, primary_key=True, index=True)
    dateScanned = Column(DateTime(timezone=True), default=func.now())
    name = Column(String)
    mountPoint = Column(String) # /example/path
    totalSize = Column(Float) #bytes
    freeSpace = Column(Float) #bytes
    usedSpace = Column(Float) #bytes
    totalFiles = Column(Integer)
    totalFolders = Column(Integer)

Base.metadata.create_all(bind=engine)

class FileCreate(BaseModel):
    name: str
    dateCreated: datetime.datetime
    dateModified: datetime.datetime
    path: str
    mimeType: Optional[str] = None
    extension: str
    size: float

class FileOut(FileCreate):
    id: int
    dateScanned: datetime.datetime

    class Config:
        orm_mode = True

class VolumeCreate(BaseModel):
    name: str
    mountPoint: str
    totalSize: float
    freeSpace: float
    usedSpace: float
    totalFiles: int
    totalFolders: int

class VolumeOut(VolumeCreate):
    id: int
    dateScanned: datetime.datetime

    class Config:
        orm_mode = True