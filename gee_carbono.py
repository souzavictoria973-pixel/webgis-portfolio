"""
Zonal stats de carbono por municipio, usando o Google Earth Engine.

Dataset: NASA/ORNL/biomass_carbon_density/v1
  - bandas 'agb' (biomassa acima do solo) e 'bgb' (abaixo do solo), em Mg C/ha
  - resolucao ~300 m, referencia 2010 (mosaico global estatico -> nao serve
    para serie temporal, so para uma media estrutural por municipio)

Pre-requisito: `earthengine authenticate` ja rodado nesta maquina e um
projeto GEE valido (substituir EE_PROJECT abaixo).

Uso:
  python gee_carbono.py > carbono_municipios.csv
"""
import csv
import json
import sys

import ee
import psycopg2

DB = dict(host="localhost", port="5432", dbname="miranda", user="postgres", password="gis123")
EE_PROJECT = "SEU-PROJETO-GEE"


def buscar_municipios():
    conn = psycopg2.connect(**DB)
    cur = conn.cursor()
    cur.execute("""
        SELECT cd_mun, nome, ST_AsGeoJSON(ST_Transform(geom, 4326))
        FROM municipios_ms
    """)
    linhas = cur.fetchall()
    cur.close()
    conn.close()
    return linhas


def montar_colecao(linhas):
    feats = []
    for cd_mun, nome, geojson in linhas:
        geom = ee.Geometry(json.loads(geojson))
        feats.append(ee.Feature(geom, {"cd_mun": cd_mun, "nome": nome}))
    return ee.FeatureCollection(feats)


def main():
    ee.Initialize(project=EE_PROJECT)

    linhas = buscar_municipios()
    if not linhas:
        sys.exit("municipios_ms esta vazia -- rode importar_car.py primeiro")

    municipios = montar_colecao(linhas)

    carbono = (
        ee.Image("NASA/ORNL/biomass_carbon_density/v1")
        .select(["agb", "bgb"])
        .reduce(ee.Reducer.sum())
        .rename("carbono_mgha")
    )

    resultado = carbono.reduceRegions(
        collection=municipios,
        reducer=ee.Reducer.mean(),
        scale=300,
        crs="EPSG:4326",
    ).getInfo()

    writer = csv.writer(sys.stdout)
    writer.writerow(["cd_mun", "nome", "carbono_medio_mgha"])
    for f in resultado["features"]:
        p = f["properties"]
        writer.writerow([p["cd_mun"], p["nome"], p.get("carbono_mgha")])


if __name__ == "__main__":
    main()
