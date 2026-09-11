# WebGIS Portfolio — PostGIS · FastAPI · Leaflet

![PostGIS](https://img.shields.io/badge/PostGIS-3.4-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-green)
![Leaflet](https://img.shields.io/badge/Leaflet-1.9-brightgreen)
![Python](https://img.shields.io/badge/Python-3.14-yellow)
![Docker](https://img.shields.io/badge/Docker-ready-blue)

Full-stack geospatial prototypes built end to end — from a spatial database to a
REST API to an interactive web map. Each project takes real data, runs spatial
analysis in SQL, serves the result as GeoJSON, and renders it live in the browser.

## Architecture

All data is processed in a documented coordinate reference system
(SIRGAS 2000 / UTM 21S, EPSG:31981) and reprojected to WGS84 (EPSG:4326) for web display.

---

## Project 1 — Riparian Buffer / APP Analysis
**Miranda, Mato Grosso do Sul**

Maps the legal permanent-preservation strip (APP) along watercourses.

- Municipal boundary and hydrography loaded into PostGIS (EPSG:31981)
- 30 m riparian buffer computed along the drainage network (`ST_Buffer` + `ST_Union`)
- Results validated against known references

| Metric | Value |
|---|---|
| Municipal area | 5,466.92 km² |
| Hydrography network | 1,865.37 km |
| APP buffer (30 m) | 11,576.30 ha |

**Map:** `mapa.html`

---

## Project 2 — Business Site-Selection Heatmap
**Campo Grande, Mato Grosso do Sul**

A location-intelligence prototype that scores where a new business has the
strongest potential, based on population density.

- Brazilian Census 2022 population joined to census-tract geometries (spatial JOIN by tract code)
- Population density and a normalized **0–100 opportunity score** computed in PostGIS
- Interactive choropleth heatmap with legend and per-tract popups (population + score)
- ~1,657 census tracts · validated against known city population (898,100 inhabitants)

**Map:** `mapa_heatmap.html`

---

## Project 3 — Average Carbon Stock by Municipality (CAR × Google Earth Engine)
**Mato Grosso do Sul (statewide)** · *in progress*

Joins the state's rural property registry (CAR/SICAR) with a public Google
Earth Engine carbon dataset to estimate the average carbon stock held by
registered rural properties, per municipality.

- CAR shapefile (imóveis rurais) and IBGE municipal mesh loaded into PostGIS,
  reprojected to EPSG:31981 (`importar_car.py`, `schema_carbono.sql`)
- Each property assigned to a municipality by spatial join (representative
  point within municipal boundary)
- Zonal mean of `NASA/ORNL/biomass_carbon_density/v1` (aboveground +
  belowground biomass carbon, Mg C/ha) computed per municipality via the
  Earth Engine Python API (`gee_carbono.py`)
- Result joined back to CAR area per municipality to get an estimated total
  carbon stock, served as GeoJSON and rendered as a choropleth
  (`carregar_carbono.py`, `/carbono` endpoint, `mapa_carbono.html`)

**Pipeline:** `importar_car.py` → `gee_carbono.py` → `carregar_carbono.py` → `/carbono` → `mapa_carbono.html`

**Map:** `mapa_carbono.html`

---

## Skills demonstrated

- Spatial databases and SQL (PostGIS: `ST_Area`, `ST_Length`, `ST_Buffer`, `ST_Union`, `ST_Transform`, `ST_AsGeoJSON`)
- Data integration (IBGE census data and CAR rural registry joined to territorial meshes, type handling, validation)
- Remote sensing / zonal statistics with the Google Earth Engine Python API
- REST API development (FastAPI serving GeoJSON, CORS)
- Web mapping (Leaflet: choropleth, popups, legends)
- Coordinate reference systems and reprojection
- Reproducible environment with Docker and Python virtual environments

## Tech stack

PostgreSQL · PostGIS · Docker · Python · FastAPI · psycopg2 · Leaflet · QGIS

## How to run (local)

1. Start PostGIS (Docker) and load the layers
2. `pip install -r requirements.txt`
3. `uvicorn main:app --reload --port 8001`
4. Open `mapa.html`, `mapa_heatmap.html` or `mapa_carbono.html` in a browser

For Project 3, run the pipeline once before starting the API:
`psql -f schema_carbono.sql` → `python importar_car.py <municipios.shp> <car.shp>` →
`earthengine authenticate` + `python gee_carbono.py > carbono_municipios.csv` →
`python carregar_carbono.py carbono_municipios.csv`

## Author

**Victória Mathias Souza da Cunha**
Environmental Engineer · GIS & Remote Sensing · Mato Grosso do Sul, Brazil
