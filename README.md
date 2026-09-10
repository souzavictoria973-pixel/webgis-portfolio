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

## Skills demonstrated

- Spatial databases and SQL (PostGIS: `ST_Area`, `ST_Length`, `ST_Buffer`, `ST_Union`, `ST_Transform`, `ST_AsGeoJSON`)
- Data integration (IBGE census data joined to territorial meshes, type handling, validation)
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
4. Open `mapa.html` or `mapa_heatmap.html` in a browser

## Author

**Victória Mathias Souza da Cunha**
Environmental Engineer · GIS & Remote Sensing · Mato Grosso do Sul, Brazil
