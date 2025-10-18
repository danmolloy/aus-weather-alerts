from sqlalchemy import text, insert, func, delete
from sqlalchemy.orm import Session
from ..database.db import engine
from ..database.models import Locality, BomRadar

""" 
Hardcorded BOM radar data:
https://www.bom.gov.au/australia/radar/info/qld_info.shtml

(Web scraping blocked by BOM.)
"""


QLD_RADARS = [
    {"id": "IDR243", "name": "Bowen (Abbot Point)", "lat": -19.88, "lon": 148.08, "range": 128},
    {"id": "IDR663", "name": "Brisbane (Mt. Stapylton)", "lat": -27.717, "lon": 153.240, "range": 256},
    {"id": "IDR703", "name": "Cairns", "lat": -16.818, "lon": 145.683, "range": 128},
    {"id": "IDR733", "name": "Emerald (Central Highlands)", "lat": -23.5494, "lon": 148.2392, "range": 256},
    {"id": "IDR233", "name": "Gladstone", "lat": -23.86, "lon": 151.26, "range": 128},
    {"id": "IDR743", "name": "Greenvale", "lat": -18.99, "lon": 144.99, "range": 128},  # evaluation radar
    {"id": "IDR083", "name": "Gympie (Mt Kanigan)", "lat": -25.957, "lon": 152.577, "range": 128},
    {"id": "IDR793", "name": "Longreach", "lat": -23.43, "lon": 144.29, "range": 128},
    {"id": "IDR713", "name": "Mackay", "lat": -21.118, "lon": 149.217, "range": 256},
    {"id": "IDR693", "name": "Marburg", "lat": -27.611, "lon": 152.540, "range": 256},
    {"id": "IDR363", "name": "Mornington Island", "lat": -16.67, "lon": 139.17, "range": 128},
    {"id": "IDR753", "name": "Mount Isa", "lat": -20.7114, "lon": 139.5553, "range": 128},
    {"id": "IDR1073", "name": "Richmond", "lat": -20.75, "lon": 143.14, "range": 128},
    {"id": "IDR983", "name": "Taroom", "lat": -25.696, "lon": 149.898, "range": 128},
    {"id": "IDR1083", "name": "Toowoomba", "lat": -27.2740, "lon": 151.9930, "range": 128},
    {"id": "IDR1063", "name": "Townsville", "lat": -19.42, "lon": 146.55, "range": 128},
    {"id": "IDR673", "name": "Warrego", "lat": -26.44, "lon": 147.35, "range": 128},
    {"id": "IDR783", "name": "Weipa", "lat": -12.678, "lon": 141.924, "range": 128},
    {"id": "IDR413", "name": "Willis Island", "lat": -16.288, "lon": 149.965, "range": 128},
]

with engine.begin() as conn:
  conn.execute(delete(BomRadar))
  for radar in QLD_RADARS:
    stmt = insert(BomRadar).values(
        id=radar["id"],
        name=radar["name"],
        geom=func.ST_SetSRID(func.ST_MakePoint(radar["lon"], radar["lat"]), 7844)
    )
    conn.execute(stmt)

with Session(engine) as db:
  sql = """
  UPDATE localities
  SET radar_id = (
      SELECT r.id
      FROM bom_radars r
      ORDER BY localities.geom <-> r.geom
      LIMIT 1
  );
  """
  db.execute(text(sql))
  db.commit()

print("Imported QLD BOM radars and updated nearest radar for each locality.")
