from fastapi import FastAPI
from app.routers import localities, landmarks

app = FastAPI()


@app.get("/")
async def root():
  return { "message": "Hello world" }

app.include_router(localities.router)
app.include_router(landmarks.router)