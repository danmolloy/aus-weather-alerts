from fastapi import APIRouter, Depends
from xml.etree import ElementTree as ET
import httpx
from datetime import datetime
from ..database.db import SessionLocal
from ..database.models import Alert
from sqlalchemy.orm import Session
from sqlalchemy import select

router = APIRouter(prefix="/alerts")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


ALERT_CACHE = {
    "last_updated": None,
    "alerts": []
}

@router.get("/all")
async def get_all_alerts(db: Session = Depends(get_db)):
    alerts = db.scalars(select(Alert)).all()
    return [
        {
            "id": alert.id,
            "headline": alert.headline,
            "area": alert.area,
            "localities": [
                {"name": loc.name}
                for loc in alert.localities
            ]
        }
        for alert in alerts
    ]


@router.get("/fire")
async def get_fire_alerts():
  feed_url = "https://publiccontent-gis-psba-qld-gov-au.s3.amazonaws.com/content/Feeds/BushfireCurrentIncidents/bushfireAlert_capau.xml"
  async with httpx.AsyncClient(timeout=10.0) as client:
    response = await client.get(feed_url)
    response.raise_for_status()
    xml_data = response.text

  ns = {"cap": "urn:oasis:names:tc:emergency:cap:1.2"}
  root = ET.fromstring(xml_data)
  alerts = []


  for alert in root.findall(".//cap:alert", ns):
        identifier = alert.findtext("cap:identifier", namespaces=ns)
        headline = alert.findtext("cap:info/cap:headline", namespaces=ns)
        description = alert.findtext("cap:info/cap:description", namespaces=ns)
        area = alert.findtext("cap:info/cap:area/cap:areaDesc", namespaces=ns)
        circle = alert.findtext("cap:info/cap:area/cap:circle", namespaces=ns)

        lat, lon, radius = None, None, None
        if circle:
            parts = circle.split()
            if len(parts) == 2:
                lat, lon = map(float, parts[0].split(","))
                radius = float(parts[1])

        params = {}
        for param in alert.findall(".//cap:parameter", ns):
            name = param.findtext("cap:valueName", namespaces=ns)
            value = param.findtext("cap:value", namespaces=ns)
            if name and value:
                params[name] = value

        alerts.append({
            "id": identifier,
            "headline": headline,
            "description": description,
            "area": area,
            "lat": lat,
            "lon": lon,
            "radius_km": radius,
            "params": params,
        })


  return {
      "count": len(alerts),
      "last_updated": datetime.utcnow().isoformat(),
      "alerts": alerts,
  }