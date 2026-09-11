from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

def conectar():
    return psycopg2.connect(host="localhost", port="5432",
        dbname="miranda", user="postgres", password="gis123")

@app.get("/")
def raiz():
    return {"mensagem": "API no ar"}

@app.get("/heatmap")
def heatmap():
    conn = conectar(); cur = conn.cursor()
    cur.execute("""
        SELECT jsonb_build_object(
          'type','FeatureCollection',
          'features', jsonb_agg(
            jsonb_build_object(
              'type','Feature',
              'geometry', ST_AsGeoJSON(ST_Transform(geom,4326))::jsonb,
              'properties', jsonb_build_object('cd_setor',cd_setor,'pop',pop,'score',score)
            )))
        FROM heat_cg;
    """)
    r = cur.fetchone()[0]; cur.close(); conn.close()
    return r

@app.get("/carbono")
def carbono():
    conn = conectar(); cur = conn.cursor()
    cur.execute("""
        SELECT jsonb_build_object(
          'type','FeatureCollection',
          'features', jsonb_agg(
            jsonb_build_object(
              'type','Feature',
              'geometry', ST_AsGeoJSON(ST_Transform(geom,4326))::jsonb,
              'properties', jsonb_build_object(
                'cd_mun', cd_mun, 'nome', nome, 'n_imoveis', n_imoveis,
                'area_car_ha', area_car_ha,
                'carbono_medio_mgha', carbono_medio_mgha,
                'carbono_total_mg', carbono_total_mg
              )
            )))
        FROM carbono_municipio;
    """)
    r = cur.fetchone()[0]; cur.close(); conn.close()
    return r
