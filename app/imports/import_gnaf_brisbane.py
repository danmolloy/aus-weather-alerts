from ..database.db import DATABASE_URL, engine
from sqlalchemy.dialects.postgresql import insert
import pandas as pd
from ..database.models import Locality
from pathlib import Path

""" 
Data obtained from:
https://data.gov.au/data/dataset/geocoded-national-address-file-g-naf/resource/5a5bcda9-2aaf-4b14-a851-acb989297988
"""

points_file_path = str(Path.home() / "Downloads/GNAF_QLD/G-NAF/G-NAF AUGUST 2025/Standard/QLD_LOCALITY_POINT_psv.psv")
points_df = pd.read_csv(points_file_path, sep="|", dtype=str)

# points_df.columns:
# ['LOCALITY_POINT_PID', 'DATE_CREATED', 'DATE_RETIRED', 'LOCALITY_PID', 'PLANIMETRIC_ACCURACY', 'LONGITUDE', 'LATITUDE']

locality_file_path = "~/Downloads/GNAF_QLD/G-NAF/G-NAF AUGUST 2025/Standard/QLD_LOCALITY_psv.psv"
locality_df = pd.read_csv(locality_file_path, sep="|", dtype=str)
# locality_df.columns
# ['LOCALITY_PID', 'DATE_CREATED', 'DATE_RETIRED', 'LOCALITY_NAME', 'PRIMARY_POSTCODE', 'LOCALITY_CLASS_CODE', 'STATE_PID', 'GNAF_LOCALITY_PID', 'GNAF_RELIABILITY_CODE']

#brisbane_df = locality_df[locality_df["LOCALITY_NAME"].str.contains("BRISBANE", case=False, na=False)]
#df = brisbane_df.merge(points_df, on="LOCALITY_PID", how="left")
df = locality_df.merge(points_df, on="LOCALITY_PID", how="left")

with engine.begin() as conn:
    for _, row in df.iterrows():
        conn.execute(
            insert(Locality).values(
                locality_name=row["LOCALITY_NAME"],
                state="QLD",
                geom=f"SRID=7844;POINT({row['LONGITUDE']} {row['LATITUDE']})"
            ).on_conflict_do_nothing(index_elements=["locality_name"])
        )
        # geom=f"SRID=4326;POINT({row['LONGITUDE']} {row['LATITUDE']})"



print(f"Imported {len(df)} Queensland localities.")

