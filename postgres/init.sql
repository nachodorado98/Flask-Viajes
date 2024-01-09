CREATE DATABASE bbdd_viajes;

\c bbdd_viajes;

CREATE TABLE paises (Pais VARCHAR(50) PRIMARY KEY,
						PaisIngles VARCHAR(50));

\copy paises (Pais, PaisIngles) FROM '/docker-entrypoint-initdb.d/paises.csv' WITH CSV HEADER;

CREATE TABLE ciudades (CodCiudad SERIAL PRIMARY KEY,
						Ciudad VARCHAR(50),
						Latitud VARCHAR(50),
						Longitud VARCHAR(50),
						Pais VARCHAR(50),
						Siglas CHAR(3),
						Tipo VARCHAR(50),
						Poblacion INT,
						FOREIGN KEY (Pais) REFERENCES paises (Pais));

\copy ciudades (Ciudad, Latitud, Longitud, Pais, Siglas, Tipo, Poblacion) FROM '/docker-entrypoint-initdb.d/ciudades.csv' WITH CSV HEADER;

DELETE FROM ciudades WHERE Pais IN ('Artículo 1', 'Anguila', 'Antigua y Barbuda', 'Ciudad del Vaticano', 'Franja de Gaza', 'Isla de Navidad',
'Isla Norfolk', 'Islas Cook', 'Islas Pitcairn', 'Montserrat', 'Nauru', 'Niue', 'Palaos', 'San Bartolomé', 'San Marino', 'Sint Maarten', 'Svalbard', 'Tuvalu')
OR Pais LIKE '%Sandwich%' OR Pais LIKE '%Marianas%' OR Pais LIKE '%Malvinas%' OR Pais LIKE '%Caicos%' OR Pais LIKE '%Vírgenes%' OR Pais LIKE '%Saint%'
OR Pais LIKE '%San Pedro%' OR Pais LIKE '%Santa Elena%' OR Pais LIKE '%Wallis%' OR Pais LIKE '%West%';

CREATE TABLE viajes (Id_Viaje SERIAL PRIMARY KEY,
					CodCiudad INT,
					Ida DATE,
					Vuelta DATE,
					Hotel VARCHAR(50),
					Web VARCHAR(50),
					Transporte VARCHAR(50),
					Comentario VARCHAR(200),
					Imagen VARCHAR(200),
					FOREIGN KEY (CodCiudad) REFERENCES ciudades (CodCiudad));
