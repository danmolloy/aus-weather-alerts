from sqlalchemy.orm import Session
from ..database.models import Alert
from datetime import datetime
from ..database.db import SessionLocal
from fastapi import Depends

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

def delete_expired_alerts(db: Session = Depends(get_db)):
  now = datetime.now(datetime.timezone.utc)
  db.query(Alert).filter(Alert.expires_at < now).delete()
  db.commit()