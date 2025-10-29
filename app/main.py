from fastapi import FastAPI
from app.routers import localities, landmarks, weather, alerts
from contextlib import asynccontextmanager
from .services.scheduler import start_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
  start_scheduler()
  print("Scheduler started.")
  yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
  return { "message": "Hello world" }

app.include_router(localities.router)
app.include_router(landmarks.router)
app.include_router(weather.router)
app.include_router(alerts.router)