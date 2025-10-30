# Australian Weather Alerts
*Australian Weather Alerts* is a geospatial backend that integrates Queensland locality, heritage site, weather radar and emergency data. It explores how the ABC combines this data in their digital products, explained in the blog article ["Lifting the hood on how the ABC combines weather, emergency and location data"](https://www.abc.net.au/digital-product/how-the-abc-combines-weather-emergency-and-location-data/102756766). Published on 18 September 2023 and written by Abdul Rehman Mohammad, it discusses how the ABC's Data Services team normalises and stores geospatial representations to make them accessible for retrieval and manipulation using SQL for services such as weather updates and emergency alerts. 

## Stack
* Python & FastAPI
* SQLAlchemy, PostgreSQL & PostGIS
* Docker

## Dataset Base Layer
To begin with, my app required a base layer of locations. Similar to the ABC, I was able to use the Geoscape Geocoded National Address File (G-NAF). To keep the project on a small scale, I filtered to just localities in Queensland. Merging "QLD_LOCALITY_psv.psv" and "QLD_LOCALITY_POINT_psv.psv" files, I was able to associate the place name with geometric polygons.

## Landmarks
As stated in the article, it was important to have landmarks mapped into localities. After some exploration of different datasets, I used the Commonwealth Heritage Sites list. 

## Bom Radars & Weather Forecasts
For BOM radars, I imported all active stations in Queensland. I attempted to scrape the data, however my efforts were blocked by the BOM website. I instead hardcoded the small amount of data. I mapped each locality to its nearest station.
For forecasts, I took a simple route of fetching from the Open Meteo API.

## Emergency Alert Feeds
I integrated just a single emergency alerts feed - Queensland Fire Service. 
A background job is scheduled to fetch the data every 15 minutes and ingest into the database, and a cleanup function every hour to delete expired alerts. 

## Scalability
Rather than integrating Redis, the emergency alerts are integrated into the database and treated as a cache. This reduces the number of QFS queries while keeping the architecture straightforward.
For locality queries, I've added a GiST index rather than building an R-tree from scratch. 

## Endpoints

| Endpoint | Method | Description |
|-----------|---------|-------------|
| `/localities/all` | GET | Returns all localities in Queensland |
| `/localities/nearest` | GET | Returns a locality nearest to a geo point |
| `/landmarks/all` | GET | Returns all heritage landmarks in Queensland |
| `/landmarks/{id}` | GET | Returns a heritage site by ID |
| `/landmarks/search` | GET | Returns a heritage landmark by name search |
| `/forcast/lat/lon` | GET | Returns Open Meteo forecast for geo coordinates  |
| `/alerts/all` | GET | Returns all current emergency alerts in the database |
| `/alerts/fire` | GET | Fetches all alerts from QFS feed |

---

## Getting Started

### Requirements
- Python 3.12+
- Docker (for PostgreSQL/PostGIS)

### Installation
```bash
git clone https://github.com/yourname/aus-weather-alerts.git
cd aus-weather-alerts
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Import data
```bash
python3 -m app.imports.import_gnaf_brisbane.py
python3 -m app.imports.import_landmarks.py
python3 -m app.imports.bom_radars.py
```
### Running the API
```bash
uvicorn app.main:app --reload
```
Then open http://localhost:8000/docs


## Under Development
- Unit tests 
- Deployment
- Frontend map visualization 

## Credits
The entire project is designed and developed by Daniel Molloy. 
It is inspired by Abdul Rehman Mohammad's blog post ["Lifting the hood on how the ABC combines weather, emergency and location data"](https://www.abc.net.au/digital-product/how-the-abc-combines-weather-emergency-and-location-data/102756766), published on 18 September 2023.