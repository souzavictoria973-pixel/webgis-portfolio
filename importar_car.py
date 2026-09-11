"""
Carrega a malha municipal do IBGE e o CAR estadual (SICAR) no PostGIS.

Fontes manuais (nao ha download programatico estavel para nenhuma das duas):
  - CAR/MS:     https://www.car.gov.br/publico/estados/downloads -> shapefile "Area do imovel"
  - Municipios: https://www.ibge.gov.br/geociencias/downloads-geociencias.html -> malha municipal MS

Uso:
  python importar_car.py <malha_municipios.shp> <car_imoveis_ms.shp>
"""
import sys

import geopandas as gpd
from sqlalchemy import create_engine

DB_URL = "postgresql://postgres:gis123@localhost:5432/miranda"
EPSG_TRABALHO = 31981  # SIRGAS 2000 / UTM 21S, igual ao resto do projeto


def carregar_municipios(path_shp, engine):
    gdf = gpd.read_file(path_shp).to_crs(EPSG_TRABALHO)
    gdf = gdf.rename(columns={"CD_MUN": "cd_mun", "NM_MUN": "nome"})[["cd_mun", "nome", "geometry"]]
    gdf = gdf.set_geometry(gdf.geometry.buffer(0))  # corrige geometrias invalidas
    gdf.to_postgis("municipios_ms", engine, if_exists="append", index=False)
    print(f"municipios_ms: {len(gdf)} municipios carregados")
    return gdf


def carregar_car(path_shp, municipios_gdf, engine):
    gdf = gpd.read_file(path_shp).to_crs(EPSG_TRABALHO)
    gdf = gdf.rename(columns={"cod_imovel": "cod_imovel"})[["cod_imovel", "geometry"]]
    gdf = gdf.set_geometry(gdf.geometry.buffer(0))
    gdf["area_ha"] = gdf.geometry.area / 10_000

    centroides = gdf.copy()
    centroides["geometry"] = centroides.geometry.representative_point()
    juncao = gpd.sjoin(centroides, municipios_gdf[["cd_mun", "geometry"]], how="left", predicate="within")
    gdf["cd_mun"] = juncao["cd_mun"]

    gdf = gdf.dropna(subset=["cd_mun"])
    gdf.to_postgis("car_imoveis", engine, if_exists="append", index=False)
    print(f"car_imoveis: {len(gdf)} imoveis carregados")


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    path_municipios, path_car = sys.argv[1], sys.argv[2]
    engine = create_engine(DB_URL)

    municipios_gdf = carregar_municipios(path_municipios, engine)
    carregar_car(path_car, municipios_gdf, engine)


if __name__ == "__main__":
    main()
