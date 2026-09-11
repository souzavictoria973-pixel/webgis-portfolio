"""
Junta o CSV de saida do gee_carbono.py com as estatisticas do CAR
(n de imoveis e area por municipio) e grava a tabela carbono_municipio.

Uso:
  python carregar_carbono.py carbono_municipios.csv
"""
import csv
import sys

import psycopg2

DB = dict(host="localhost", port="5432", dbname="miranda", user="postgres", password="gis123")


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)

    with open(sys.argv[1], newline="", encoding="utf-8") as f:
        carbono_por_mun = {row["cd_mun"]: row for row in csv.DictReader(f)}

    conn = psycopg2.connect(**DB)
    cur = conn.cursor()
    cur.execute("""
        SELECT m.cd_mun, m.nome, m.geom, COUNT(c.id), COALESCE(SUM(c.area_ha), 0)
        FROM municipios_ms m
        LEFT JOIN car_imoveis c ON c.cd_mun = m.cd_mun
        GROUP BY m.cd_mun, m.nome, m.geom
    """)

    inseridos = 0
    for cd_mun, nome, geom, n_imoveis, area_car_ha in cur.fetchall():
        linha = carbono_por_mun.get(cd_mun)
        if not linha or not linha["carbono_medio_mgha"]:
            continue
        carbono_medio = float(linha["carbono_medio_mgha"])
        carbono_total = carbono_medio * float(area_car_ha)

        cur.execute("""
            INSERT INTO carbono_municipio
                (cd_mun, nome, n_imoveis, area_car_ha, carbono_medio_mgha, carbono_total_mg, geom)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (cd_mun) DO UPDATE SET
                n_imoveis = EXCLUDED.n_imoveis,
                area_car_ha = EXCLUDED.area_car_ha,
                carbono_medio_mgha = EXCLUDED.carbono_medio_mgha,
                carbono_total_mg = EXCLUDED.carbono_total_mg
        """, (cd_mun, nome, n_imoveis, area_car_ha, carbono_medio, carbono_total, geom))
        inseridos += 1

    conn.commit()
    cur.close()
    conn.close()
    print(f"carbono_municipio: {inseridos} municipios gravados")


if __name__ == "__main__":
    main()
