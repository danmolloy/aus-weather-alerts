from fastapi import APIRouter
import requests

router = APIRouter(prefix="/weather")

@router.get("/forecast/{lat}/{lon}")
def get_forecast(lat: str, lon: str):
  bom_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,precipitation"
  r = requests.get(bom_url)
  if r.status_code == 200:
    return r.json()
  else:
    return r.json()
  