from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from alien import Alien
from pydantic import BaseModel
from typing import List

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic schema for request/response
class AlienCreate(BaseModel):
    name: str
    power: str

class AlienRead(BaseModel):
    id: int
    name: str
    power: str
    class Config:
        orm_mode = True

# Routes

@app.post("/aliens/", response_model=AlienRead)
def create_alien(alien: AlienCreate, db: Session = Depends(get_db)):
    db_alien = Alien(name=alien.name, power=alien.power)
    db.add(db_alien)
    db.commit()
    db.refresh(db_alien)
    return db_alien

@app.get("/aliens/", response_model=List[AlienRead])
def read_aliens(db: Session = Depends(get_db)):
    aliens = db.query(Alien).all()
    return aliens

@app.get("/aliens/{alien_id}", response_model=AlienRead)
def read_alien(alien_id: int, db: Session = Depends(get_db)):
    alien = db.query(Alien).filter(Alien.id == alien_id).first()
    if not alien:
        raise HTTPException(status_code=404, detail="Alien not found")
    return alien