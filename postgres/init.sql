CREATE DATABASE bbdd_viajes;

\c bbdd_viajes;


CREATE TABLE ciudades (CodCiudad SERIAL PRIMARY KEY,
						Ciudad VARCHAR(50),
						Latitud VARCHAR(50),
						Longitud VARCHAR(50),
						Pais VARCHAR(50),
						Siglas CHAR(3),
						Tipo VARCHAR(50),
						Poblacion INT);

\copy ciudades (Ciudad, Latitud, Longitud, Pais, Siglas, Tipo, Poblacion) FROM '/docker-entrypoint-initdb.d/ciudades.csv' WITH CSV HEADER;

CREATE TABLE viajes (Id_Viaje SERIAL PRIMARY KEY,
					CodCiudad INT,
					Ida DATE,
					Vuelta DATE,
					Hotel VARCHAR(50),
					Web VARCHAR(50),
					Transporte VARCHAR(50),
					Comentarios VARCHAR(200) DEFAULT NULL,
					FOREIGN KEY (CodCiudad) REFERENCES ciudades (CodCiudad));
