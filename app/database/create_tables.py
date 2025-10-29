from .db import engine, Base
from .models import Locality, HeritageSite, Alert, alert_locality

Base.metadata.create_all(bind=engine)
print("Tables created successfully.")