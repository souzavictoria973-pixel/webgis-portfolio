-- Projeto 3 — Carbono medio por imovel rural (CAR) x Mato Grosso do Sul
-- Roda no mesmo banco "miranda" (PostGIS), reaproveitando a malha municipal
-- como unidade de agregacao entre o CAR e o dataset de carbono do GEE.

CREATE TABLE IF NOT EXISTS municipios_ms (
    id      SERIAL PRIMARY KEY,
    cd_mun  VARCHAR(7) UNIQUE NOT NULL,   -- codigo IBGE do municipio
    nome    VARCHAR(100) NOT NULL,
    geom    GEOMETRY(MultiPolygon, 31981) NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_municipios_ms_geom ON municipios_ms USING GIST (geom);

CREATE TABLE IF NOT EXISTS car_imoveis (
    id          SERIAL PRIMARY KEY,
    cod_imovel  VARCHAR(60) UNIQUE NOT NULL,  -- codigo do recibo CAR (SICAR)
    cd_mun      VARCHAR(7) REFERENCES municipios_ms(cd_mun),
    area_ha     NUMERIC(14,4),
    geom        GEOMETRY(MultiPolygon, 31981) NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_car_imoveis_geom   ON car_imoveis USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_car_imoveis_cd_mun ON car_imoveis (cd_mun);

-- Resultado final: um registro por municipio, pronto para o choropleth.
CREATE TABLE IF NOT EXISTS carbono_municipio (
    cd_mun              VARCHAR(7) PRIMARY KEY REFERENCES municipios_ms(cd_mun),
    nome                VARCHAR(100) NOT NULL,
    n_imoveis           INTEGER,
    area_car_ha         NUMERIC(14,4),
    carbono_medio_mgha  NUMERIC(10,4),   -- media de Mg C/ha (agb+bgb) sobre a area do CAR
    carbono_total_mg    NUMERIC(16,4),   -- carbono_medio_mgha * area_car_ha
    geom                GEOMETRY(MultiPolygon, 31981) NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_carbono_municipio_geom ON carbono_municipio USING GIST (geom);
