# WebGIS Portfolio — PostGIS + FastAPI + Leaflet

Full-stack geospatial prototypes built end to end: spatial database, REST API, and interactive web maps.

## Architecture

**PostGIS** (spatial database) -> **FastAPI** (REST API serving GeoJSON) -> **Leaflet** (web map)

## Projects

### 1. Riparian buffer / APP analysis — Miranda/MS
- Loads municipal boundary and hydrography (SIRGAS 2000 / UTM 21S, EPSG:31981)
- Computes a 30 m riparian-protection buffer (APP) along the drainage network in PostGIS
- Municipal area: 5,466.92 km2 | Hydrography: 1,865.37 km | APP buffer: 11,576.30 ha
- Map: mapa.html

### 2. Business site-selection heatmap — Campo Grande/MS
- Integrates Brazilian Census 2022 population data with census-tract geometries (spatial JOIN)
- Computes population density and a normalized 0-100 opportunity score in PostGIS
- Renders an interactive choropleth heatmap with legend and per-tract popups
- ~1,657 tracts | validated against known city population (898,100)
- Map: mapa_heatmap.html

## Tech stack

PostgreSQL + PostGIS · Docker · Python · FastAPI · psycopg2 · Leaflet · QGIS

## Author

Victoria Mathias Souza da Cunha — Environmental Engineer | GIS & Remote Sensing
