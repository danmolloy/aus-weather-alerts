from sqlalchemy.orm import Session
from ..database.models import Alert
from dateutil import parser as date_parser
from ..database.db import SessionLocal
from fastapi import Depends
import httpx
from xml.etree import ElementTree as ET

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

async def fetch_and_store_alerts(db: Session = Depends(get_db)):
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
        expires_at = alert.findtext("cap:info/cap:expires", namespaces=ns)

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
            "expires_at": expires_at
        })
  print(f"alerts: {alerts}")


  for a in alerts:
    existing = db.query(Alert).filter_by(id=a["id"]).first()

    if existing:
       continue
    db.add(Alert(
      id=a["id"],
      headline=a["headline"],
      area=a.get("area"),
      expires_at=a["expires_at"],
      localities=a.get("area")
    ))
  db.commit()