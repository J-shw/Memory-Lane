from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import File, Statistics, FileCreate, FileOut, SessionLocal
from modules.process import process_directory
from datetime import datetime, timezone
import uvicorn

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

@app.get("/files/{event_id}", response_model=FileOut)
def read_file(event_id: int, db: Session = Depends(get_db)):
    db_item = db.query(File).filter(File.id == event_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="File not found")
    return db_item

@app.get("/process")
def process_files():
    process_directory('/files')
    return {"message": "Processing.."}

@app.get("/")
async def root():
    return {"message": "Analysis - System"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9090)