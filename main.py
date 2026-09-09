from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def conectar():
    return psycopg2.connect(
        host="localhost", port="5432",
        dbname="miranda", user="postgres", password="gis123"
    )

@app.get("/")
def raiz():
    return {"mensagem": "Ola, Miranda! Minha API esta no ar."}

@app.get("/app-hidrografia")
def app_hidrografia():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT jsonb_build_object(
            'type', 'FeatureCollection',
            'features', jsonb_agg(
                jsonb_build_object(
                    'type', 'Feature',
                    'geometry', ST_AsGeoJSON(ST_Transform(geom, 4326))::jsonb,
                    'properties', jsonb_build_object('id', id)
                )
            )
        )
        FROM app_hidrografia;
    """)
    resultado = cur.fetchone()[0]
    cur.close()
    conn.close()
    return resultado
