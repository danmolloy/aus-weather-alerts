# Australian Weather Alerts

ABC Australia has a fantastic [Digital Product blog](https://www.abc.net.au/digital-product) exploring how they use technology to connect with Australians.
This app was developed to explore the concepts in ["Lifting the hood on how the ABC combines weather, emergency and location data"](https://www.abc.net.au/digital-product/how-the-abc-combines-weather-emergency-and-location-data/102756766), published on 18 September 2023. Written by Abdul Rehman Mohammad, it discusses how the ABC's Data Services team normalises and stores geospatial representations to make them accessible for retrieval and manipulation using SQL for services such as weather updates and emergency alerts. 

## Stack
* Python & FastAPI
* SQLAlchemy, PostgreSQL & PostGIS
* Docker

## Dataset Base Layer
Keeping consistent with the ABC, I was able to use the Geoscape Geocoded National Address File (G-NAF). To keep the project on a small scale, I filtered to just localities in Queensland. Merging "QLD_LOCALITY_psv.psv" and "QLD_LOCALITY_POINT_psv.psv" files, I was able to associate the place name with longitude and latitude.

```
@router.get("/all")
def get_all_localities(db: Session = Depends(get_db)):
    localities = db.scalars(select(Locality)).all()
    return [
        {
            "id": loc.id,
            "name": loc.name,
        }
        for loc in localities
    ]
    
[
  {
    "name": "EAST BRISBANE"
  },
  {
    "name": "SOUTH BRISBANE"
  },
  {
    "name": "BRISBANE AIRPORT"
  },
  {
    "name": "BRISBANE CITY"
  },
  {
    "name": "PORT OF BRISBANE"
  }
]
```


## Landmarks
Once I had a base layer set up, I was able to import landmarks and map them to their respective localities. After some exploration, I used the Commonwealth Heritage Sites list.

## Querying Locations
For localities, I created a simple API endpoint for querying longitude and latitude, returning the nearest locality. Additionally, I created for returning all localities.
In regards to landmarks, I created three endpoints. One for quering by ID, one for returning all landmarks, and one for finding likeness in the name.


## Bom Radars & Forecasts
## Ingest emergency alert feeds
* Fetch and ingest function
* Delete function
* Schedule background job

# To Do


## Scalability
* Cache with Redis
* R-trees

* Unit tests