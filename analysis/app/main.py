from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import SessionLocal, File, FileCreate, FileOut, Volume, VolumeCreate, VolumeOut, VolumeStats, VolumeStatsCreate, VolumeStatsOut
import os
from modules.process import process_directory
from datetime import datetime, timezone
import uvicorn, logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/files/", response_model=FileOut)
def create_file(item: FileCreate, db: Session = Depends(get_db)):
    db_item = File(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/files/", response_model=list[FileOut])
def read_files(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(File).offset(skip).limit(limit).all()
    return items

@app.get("/files/{id}", response_model=FileOut)
def read_file(id: int, db: Session = Depends(get_db)):
    db_item = db.query(File).filter(File.id == id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="File not found")
    return db_item

@app.post("/volumes/", response_model=VolumeOut)
def create_volume(item: VolumeCreate, db: Session = Depends(get_db)):
    db_item = Volume(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/volumes/", response_model=list[VolumeOut])
def read_volumes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(Volume).offset(skip).limit(limit).all()
    return items

@app.get("/volumes/{id}", response_model=VolumeOut)
def read_volume(id: int, db: Session = Depends(get_db)):
    db_item = db.query(Volume).filter(Volume.id == id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Volume not found")
    return db_item

@app.post("/volume_stats/", response_model=VolumeStats)
def create_volume_stats(volume_stats: VolumeStats, db: Session = Depends(get_db)):
    db_volume_stats = VolumeStats(**volume_stats.dict())
    db.add(db_volume_stats)
    db.commit()
    db.refresh(db_volume_stats)
    return db_volume_stats

@app.get("/process/volume/{id}")
def process_volume(id: int, db: Session = Depends(get_db)):
    if id:
        db_item = db.query(Volume).filter(File.id == id).first()
    else:
        db_item = db.query(File).all()
    
    if db_item is None:
        raise HTTPException(status_code=404, detail="Volume not found")
    
    for volume in db_item:
        try:
            process_directory(volume.path, volume.id)
        except Exception as e:
            logging.error(f"Error processing directory {volume.path}: {e}")
        volume.dateScanned = datetime.now(timezone.utc)
        db.commit()
    return {"message": "Processing complete."}

@app.get("/")
async def root():
    return {"message": "Analysis - System"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9090)