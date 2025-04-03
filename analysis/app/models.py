from sqlalchemy import create_engine, ForeignKey, Column, Integer, Boolean, String, Float, DateTime
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
    volumeId = Column(Integer, ForeignKey("volumes.id"))
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
    dateAdded = Column(DateTime(timezone=True), default=func.now())
    name = Column(String)
    mountPoint = Column(String, nullable=True) # /example/path


class VolumeStats(Base):
    __tablename__ = "volume_stats"

    id = Column(Integer, primary_key=True, index=True)
    volumeId = Column(Integer, ForeignKey("volumes.id"))
    dateScanned = Column(DateTime(timezone=True), default=func.now())
    totalSize = Column(Float, nullable=True) #bytes
    freeSpace = Column(Float, nullable=True) #bytes
    usedSpace = Column(Float, nullable=True) #bytes
    totalFiles = Column(Integer, nullable=True)
    totalFolders = Column(Integer, nullable=True)

Base.metadata.create_all(bind=engine)

class FileCreate(BaseModel):
    volumeId: int
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

class VolumeOut(VolumeCreate):
    id: int
    dateAdded: datetime.datetime

    class Config:
        orm_mode = True

class VolumeStatsCreate(BaseModel):
    volumeId: int
    dateScanned: Optional[datetime.datetime] = None
    totalSize: Optional[float] = None
    freeSpace: Optional[float] = None
    usedSpace: Optional[float] = None
    totalFiles: Optional[int] = None
    totalFolders: Optional[int] = None

class VolumeStatsOut(VolumeStatsCreate):
    id: int

    class Config:
        orm_mode = True