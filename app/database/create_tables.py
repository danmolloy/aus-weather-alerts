from .db import engine, Base
from .models import Locality, HeritageSite  

Base.metadata.create_all(bind=engine)
print("Tables created successfully.")