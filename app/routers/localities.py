from fastapi import APIRouter, Depends
from sqlalchemy import text, select
from sqlalchemy.orm import Session
from ..database.db import SessionLocal
from ..database.models import Locality

router = APIRouter(prefix="/localities")

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()
  
@router.get("/nearest")
def get_nearest_locality(lat: float, lon: float, db: Session = Depends(get_db)):
  sql = text("""
  SELECT locality_name
  FROM localities
  ORDER BY geom <-> ST_SetSRID(ST_MakePoint(:lon, :lat), 7844)
  LIMIT 1;
  """)
  result = db.execute(sql, {"lat": lat, "lon": lon}).fetchone()
  return {
    "result": result.locality_name
    }

@router.get("/all")
def get_all_localities(db: Session = Depends(get_db)):
  localities = db.scalars(select(Locality)).all()
  return [
    {
      "name": loc.locality_name,
      "landmarks": [
        {"name": site.name}
        for site in loc.heritage_sites
        ]
      }
    for loc in localities
  ]