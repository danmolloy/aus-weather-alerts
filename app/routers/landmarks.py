from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database.db import SessionLocal
from ..database.models import HeritageSite

router = APIRouter(prefix="/landmarks")

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()


@router.get("/search")
def search_heritage_sites(q: str, db: Session = Depends(get_db)):
    results = db.scalars(
        select(HeritageSite)
        .where(HeritageSite.name.ilike(f"%{q}%"))
        .limit(20)
    ).all()

    return [
       {"id": s.id, 
        "name": s.name, 
        "locality": s.locality_name
        } 
       for s in results]


  
@router.get("/all")
def get_all_landmarks(db: Session = Depends(get_db)):
  landmarks = db.scalars(select(HeritageSite)).all()
  return [
    {
      "name": site.name,
      "locality": site.locality_name,
      "id": site.id,
    }
    for site in landmarks
  ]

@router.get("/{id}")
def get_heritage_site(id: str, db: Session = Depends(get_db)):
  site = db.scalar(select(HeritageSite).where(HeritageSite.id == id))
  if not site:
        raise HTTPException(status_code=404, detail="Heritage site not found")
  return {
        "id": site.id,
        "name": site.name,
        "locality": site.locality_name,
    }