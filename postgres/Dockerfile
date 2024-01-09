FROM postgres:latest

COPY init.sql /docker-entrypoint-initdb.d/
COPY data/ciudades.csv /docker-entrypoint-initdb.d/ciudades.csv
COPY data/paises.csv /docker-entrypoint-initdb.d/paises.csv