import geopandas as gpd
from pathlib import Path
from sqlalchemy import insert, text
from ..database.db import DATABASE_URL, engine
from ..database.models import HeritageSite


""" 
Data obtained from:
https://data.gov.au/data/dataset/57720684-4948-45db-a2c8-37259d531d87/resource/a1260575-efe1-4bfa-a303-b5382fdffbc6
"""

landmarks_file_path = str(Path.home() / "Downloads/CwHeritage/CwHeritage.gdb")
landmarks = gpd.read_file(landmarks_file_path)
#print(gpd.list_layers(landmarks_file_path))

gdf = gpd.read_file(landmarks_file_path, layer="SDE_COMMONWEALTH_HER_LIST")
qld_gdf = gdf[gdf["STATE"] == "QLD"]
"""
print(qld_gdf.columns)
['PLACE_ID', 'FILE_', 'NAME', 'CLASS', 'STATUS', 'STATE', 'SOURCE',
       'UPDATE_', 'AREA_HA', 'REGISTER', 'ADDRESS', 'ElementID',
       'SHAPE_Length', 'SHAPE_Area', 'geometry']
"""

with engine.begin() as conn:
  for _, row in qld_gdf.iterrows():
    wkt = row.geometry.wkt
    nearest = conn.execute(
          text("""
              SELECT locality_name
              FROM localities
              ORDER BY geom <-> ST_GeomFromText(:geom, 7844)
              LIMIT 1;
          """),
          {"geom": wkt}
      ).fetchone()
    locality_name = nearest.locality_name if nearest else None
      
    conn.execute(
      insert(HeritageSite).values(
        id = row["PLACE_ID"],
        name = row["NAME"],
        geom=f"SRID=7844;{wkt}",
        locality_name = locality_name
      )
    )



print(f"Imported {len(gdf)} heritage sites.")
