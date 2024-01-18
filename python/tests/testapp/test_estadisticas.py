import pytest
from datetime import datetime
import os
import shutil
import time

def test_pagina_estadisticas_no_existe_viaje(cliente, conexion):

	respuesta=cliente.get(f"/estadisticas")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/"
	assert "Redirecting..." in contenido

@pytest.mark.parametrize(["ciudad"],
	[("London",),("Porto",),("Paris",),("Toledo",)]
)
def test_pagina_estadisticas_existe_viaje_viaje_realizado(cliente, conexion, ciudad):

	data={"pais":"Pais",
			"ciudad":ciudad,
			"ida":"22/06/2019",
			"vuelta":"23/06/2019",
			"hotel":"hotel",
			"web":"www.google.com",
			"transporte":"t",
			"comentario":"Sin Comentario",
			"archivo_imagen":"Sin Imagen"}

	cliente.post("/insertar_viaje", data=data)

	respuesta=cliente.get(f"/estadisticas")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Estadisticas de los viajes" in contenido
	assert "1 viajes" in contenido


@pytest.mark.parametrize(["viajes"],
	[(2,),(34,),(5,),(100,)]
)
def test_pagina_estadisticas_existen_viajes_viajes_realizados(cliente, conexion, viajes):

	for viaje in range(viajes):

		data={"pais":"Pais",
				"ciudad":"London",
				"ida":"22/06/2019",
				"vuelta":"23/06/2019",
				"hotel":"hotel",
				"web":"www.google.com",
				"transporte":"t",
				"comentario":"Sin Comentario",
				"archivo_imagen":"Sin Imagen"}

		cliente.post("/insertar_viaje", data=data)

	respuesta=cliente.get(f"/estadisticas")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Estadisticas de los viajes" in contenido
	assert f"{viajes} viajes" in contenido

@pytest.mark.parametrize(["ciudad"],
	[("London",),("Porto",),("Paris",),("Toledo",)]
)
def test_pagina_estadisticas_existe_viaje_pais_visitado(cliente, conexion, ciudad):

	data={"pais":"Pais",
			"ciudad":ciudad,
			"ida":"22/06/2019",
			"vuelta":"23/06/2019",
			"hotel":"hotel",
			"web":"www.google.com",
			"transporte":"t",
			"comentario":"Sin Comentario",
			"archivo_imagen":"Sin Imagen"}

	cliente.post("/insertar_viaje", data=data)

	respuesta=cliente.get(f"/estadisticas")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Estadisticas de los viajes" in contenido
	assert "1 paises" in contenido

@pytest.mark.parametrize(["ciudades", "paises"],
	[
		(["London", "Porto", "Paris", "Toledo"], 4),
		(["London", "Porto", "Paris", "Toledo", "Madrid"], 4),
		(["London", "Porto", "Paris", "Toledo", "Tokyo", "Lyon"], 5),
		(["London", "Liverpool", "Manchester", "Luton"], 1)
	]
)
def test_pagina_estadisticas_existen_viajes_paises_visitados(cliente, conexion, ciudades, paises):

	for ciudad in ciudades:

		data={"pais":"Pais",
				"ciudad":ciudad,
				"ida":"22/06/2019",
				"vuelta":"23/06/2019",
				"hotel":"hotel",
				"web":"www.google.com",
				"transporte":"t",
				"comentario":"Sin Comentario",
				"archivo_imagen":"Sin Imagen"}

		cliente.post("/insertar_viaje", data=data)

	respuesta=cliente.get(f"/estadisticas")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Estadisticas de los viajes" in contenido
	assert f"{paises} paises" in contenido

@pytest.mark.parametrize(["ciudad"],
	[("London",),("Porto",),("Paris",),("Toledo",)]
)
def test_pagina_estadisticas_existe_viaje_ciudad_visitada(cliente, conexion, ciudad):

	data={"pais":"Pais",
			"ciudad":ciudad,
			"ida":"22/06/2019",
			"vuelta":"23/06/2019",
			"hotel":"hotel",
			"web":"www.google.com",
			"transporte":"t",
			"comentario":"Sin Comentario",
			"archivo_imagen":"Sin Imagen"}

	cliente.post("/insertar_viaje", data=data)

	respuesta=cliente.get(f"/estadisticas")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Estadisticas de los viajes" in contenido
	assert "1 ciudades" in contenido

@pytest.mark.parametrize(["ciudades", "numero_ciudades"],
	[
		(["London", "Porto", "Paris", "Toledo"], 4),
		(["London", "Porto", "Paris", "Toledo", "London"], 4),
		(["London", "Porto", "Paris", "Toledo", "Porto", "Toledo", "Tokyo"], 5),
		(["London", "Porto", "London", "London", "London", "Porto"], 2),
	]
)
def test_pagina_estadisticas_existen_viajes_ciudades_visitadas(cliente, conexion, ciudades, numero_ciudades):

	for ciudad in ciudades:

		data={"pais":"Pais",
				"ciudad":ciudad,
				"ida":"22/06/2019",
				"vuelta":"23/06/2019",
				"hotel":"hotel",
				"web":"www.google.com",
				"transporte":"t",
				"comentario":"Sin Comentario",
				"archivo_imagen":"Sin Imagen"}

		cliente.post("/insertar_viaje", data=data)

	respuesta=cliente.get(f"/estadisticas")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Estadisticas de los viajes" in contenido
	assert f"{numero_ciudades} ciudades" in contenido

@pytest.mark.parametrize(["vuelta"],
	[("22/06/2019",), ("13/04/2019",), ("23/06/2023",), ("11/03/2021",), ("22/08/2022",)]
)
def test_pagina_estadisticas_existe_viaje_ultimo_viaje(cliente, conexion, vuelta):

	data={"pais":"Pais",
			"ciudad":"London",
			"ida":"22/06/2019",
			"vuelta":vuelta,
			"hotel":"hotel",
			"web":"www.google.com",
			"transporte":"t",
			"comentario":"Sin Comentario",
			"archivo_imagen":"Sin Imagen"}

	cliente.post("/insertar_viaje", data=data)

	respuesta=cliente.get(f"/estadisticas")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Estadisticas de los viajes" in contenido

	hoy=datetime.now()

	dias=(hoy-datetime.strptime(vuelta, "%d/%m/%Y")).days

	assert f"{dias} dias" in contenido

@pytest.mark.parametrize(["vueltas", "vuelta_ultima"],
	[
		(["22/06/2019", "13/04/2019", "23/06/2023", "11/03/2021", "22/08/2022"], "23/06/2023"),
		(["22/06/2019", "13/04/2019", "23/06/2023", "11/03/2021", "22/08/2022", "01/01/2024"], "01/01/2024"),
		(["22/06/2019", "22/06/2019", "22/06/2019", "22/06/2019"], "22/06/2019")
	]
)
def test_pagina_estadisticas_existen_viajes_ultimo_viaje(cliente, conexion, vueltas, vuelta_ultima):

	for vuelta in vueltas:

		data={"pais":"Pais",
				"ciudad":"London",
				"ida":"22/06/2019",
				"vuelta":vuelta,
				"hotel":"hotel",
				"web":"www.google.com",
				"transporte":"t",
				"comentario":"Sin Comentario",
				"archivo_imagen":"Sin Imagen"}

		cliente.post("/insertar_viaje", data=data)

	respuesta=cliente.get(f"/estadisticas")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Estadisticas de los viajes" in contenido

	hoy=datetime.now()

	dias=(hoy-datetime.strptime(vuelta_ultima, "%d/%m/%Y")).days

	assert f"{dias} dias" in contenido

@pytest.mark.parametrize(["vuelta", "dias"],
	[
		("22/06/2019", 0),
		("23/06/2019", 1),
		("27/06/2019", 5),
		("30/06/2019", 8),
		("22/07/2019", 30)
	]
)
def test_pagina_estadisticas_existe_viaje_mas_largo(cliente, conexion, vuelta, dias):

	data={"pais":"Pais",
			"ciudad":"London",
			"ida":"22/06/2019",
			"vuelta":vuelta,
			"hotel":"hotel",
			"web":"www.google.com",
			"transporte":"t",
			"comentario":"Sin Comentario",
			"archivo_imagen":"Sin Imagen"}

	cliente.post("/insertar_viaje", data=data)

	respuesta=cliente.get(f"/estadisticas")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Estadisticas de los viajes" in contenido
	assert f"{dias} dias" in contenido

@pytest.mark.parametrize(["vueltas", "dias"],
	[
		(["22/06/2019", "23/06/2019", "30/06/2019", "24/06/2019", "25/06/2019"], 8),
		(["22/06/2019", "22/07/2019", "30/06/2019", "24/06/2019", "25/06/2019"], 30),
		(["22/06/2019", "23/06/2019", "22/06/2019", "22/06/2019", "22/06/2019"], 1),
		(["22/06/2019", "23/06/2019", "30/06/2019", "24/06/2019", "25/08/2019"], 64),
	]
)
def test_pagina_estadisticas_existen_viajes_mas_largo(cliente, conexion, vueltas, dias):

	for vuelta in vueltas:

		data={"pais":"Pais",
				"ciudad":"London",
				"ida":"22/06/2019",
				"vuelta":vuelta,
				"hotel":"hotel",
				"web":"www.google.com",
				"transporte":"t",
				"comentario":"Sin Comentario",
				"archivo_imagen":"Sin Imagen"}

		cliente.post("/insertar_viaje", data=data)

	respuesta=cliente.get(f"/estadisticas")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Estadisticas de los viajes" in contenido
	assert f"{dias} dias" in contenido

@pytest.mark.parametrize(["ida", "anno"],
	[
		("22/06/2019", 2019),
		("23/06/2021", 2021),
		("27/06/2023", 2023),
		("30/06/2020", 2020),
		("22/07/1998", 1998)
	]
)
def test_pagina_estadisticas_existe_viaje_anno_mas_viajes(cliente, conexion, ida, anno):

	data={"pais":"Pais",
			"ciudad":"London",
			"ida":ida,
			"vuelta":"14/01/2024",
			"hotel":"hotel",
			"web":"www.google.com",
			"transporte":"t",
			"comentario":"Sin Comentario",
			"archivo_imagen":"Sin Imagen"}

	cliente.post("/insertar_viaje", data=data)

	respuesta=cliente.get(f"/estadisticas")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Estadisticas de los viajes" in contenido
	assert f"1 viajes en {anno}" in contenido

@pytest.mark.parametrize(["idas", "anno", "viajes"],
	[
		(["22/06/2019", "22/06/2020", "22/06/2019", "22/06/2021", "22/06/2019"], 2019, 3),
		(["23/06/2021", "22/06/2020", "22/06/2019", "22/06/2021", "22/06/2019"], 2021, 2),
		(["27/06/2023", "22/06/2020", "22/06/2019", "22/06/2021", "22/06/2023"], 2023, 2),
		(["30/06/2020", "22/06/2020", "22/06/2020", "22/06/2020", "22/06/2019"], 2020, 4),
		(["22/07/1998", "22/06/2020", "22/06/2019", "22/06/2021", "22/06/2019"], 2019, 2),
	]
)
def test_pagina_estadisticas_existen_viajes_anno_mas_viajes(cliente, conexion, idas, anno, viajes):

	for ida in idas:

		data={"pais":"Pais",
				"ciudad":"London",
				"ida":ida,
				"vuelta":"14/01/2024",
				"hotel":"hotel",
				"web":"www.google.com",
				"transporte":"t",
				"comentario":"Sin Comentario",
				"archivo_imagen":"Sin Imagen"}

		cliente.post("/insertar_viaje", data=data)

	respuesta=cliente.get(f"/estadisticas")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Estadisticas de los viajes" in contenido
	assert f"{viajes} viajes en {anno}" in contenido

@pytest.mark.parametrize(["ciudad"],
	[("London",),("Porto",),("Paris",),("Toledo",)]
)
def test_pagina_estadisticas_existe_viaje_ciudad_mas_visitada(cliente, conexion, ciudad):

	data={"pais":"Pais",
			"ciudad":ciudad,
			"ida":"22/06/2019",
			"vuelta":"23/06/2019",
			"hotel":"hotel",
			"web":"www.google.com",
			"transporte":"t",
			"comentario":"Sin Comentario",
			"archivo_imagen":"Sin Imagen"}

	cliente.post("/insertar_viaje", data=data)

	respuesta=cliente.get(f"/estadisticas")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Estadisticas de los viajes" in contenido
	assert f"1 viajes a {ciudad}" in contenido

@pytest.mark.parametrize(["ciudades", "ciudad_mas_visitada", "viajes"],
	[
		(["London", "Porto", "Paris", "Toledo", "Tokyo", "Madrid", "Karachi"], "Karachi", 1),
		(["London", "Porto", "Paris", "Toledo", "Madrid", "Madrid", "Karachi"], "Madrid", 2),
		(["London", "Porto", "Paris", "Paris", "Tokyo", "Madrid", "Karachi", "Madrid"], "Madrid", 2),
		(["London", "Porto", "London", "Toledo", "Tokyo", "Madrid", "Karachi", "London"], "London", 3)
	]
)
def test_pagina_estadisticas_existen_viajes_ciudad_mas_visitada(cliente, conexion, ciudades, ciudad_mas_visitada, viajes):

	for ciudad in ciudades:

		data={"pais":"Pais",
				"ciudad":ciudad,
				"ida":"22/06/2019",
				"vuelta":"23/06/2019",
				"hotel":"hotel",
				"web":"www.google.com",
				"transporte":"t",
				"comentario":"Sin Comentario",
				"archivo_imagen":"Sin Imagen"}

		cliente.post("/insertar_viaje", data=data)

	respuesta=cliente.get(f"/estadisticas")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Estadisticas de los viajes" in contenido
	assert f"{viajes} viajes a {ciudad_mas_visitada}" in contenido

@pytest.mark.parametrize(["ciudad", "pais"],
	[
		("London", "Reino Unido"),
		("Porto", "Portugal"),
		("Paris", "Francia"),
		("Toledo", "España")
	]
)
def test_pagina_estadisticas_existe_viaje_pais_mas_visitado(cliente, conexion, ciudad, pais):

	data={"pais":"Pais",
			"ciudad":ciudad,
			"ida":"22/06/2019",
			"vuelta":"23/06/2019",
			"hotel":"hotel",
			"web":"www.google.com",
			"transporte":"t",
			"comentario":"Sin Comentario",
			"archivo_imagen":"Sin Imagen"}

	cliente.post("/insertar_viaje", data=data)

	respuesta=cliente.get(f"/estadisticas")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Estadisticas de los viajes" in contenido
	assert f"1 viajes a {pais}" in contenido

@pytest.mark.parametrize(["ciudades", "pais", "viajes"],
	[
		(["London", "Porto", "Toledo", "Paris", "Liverpool"], "Reino Unido", 2),
		(["London", "Porto", "Toledo", "Paris", "Liverpool", "Madrid"], "España", 2),
		(["London", "Porto", "Toledo", "Paris", "Liverpool", "Madrid", "Manchester"], "Reino Unido", 3),
		(["London", "Porto", "Toledo", "Paris", "Liverpool", "Madrid", "Barcelona", "Madrid"], "España", 4)
	]
)
def test_pagina_estadisticas_existen_viajes_pais_mas_visitado(cliente, conexion, ciudades, pais, viajes):

	for ciudad in ciudades:

		data={"pais":"Pais",
				"ciudad":ciudad,
				"ida":"22/06/2019",
				"vuelta":"23/06/2019",
				"hotel":"hotel",
				"web":"www.google.com",
				"transporte":"t",
				"comentario":"Sin Comentario",
				"archivo_imagen":"Sin Imagen"}

		cliente.post("/insertar_viaje", data=data)

	respuesta=cliente.get(f"/estadisticas")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Estadisticas de los viajes" in contenido
	assert f"{viajes} viajes a {pais}" in contenido

@pytest.mark.parametrize(["ciudad", "poblacion"],
	[
		("London", "11.120.000"),
		("Madrid", "6.006.000"),
		("Paris", "11.027.000"),
		("Tokyo", "39.105.000"),
		("Porto", "237.591"),
		("Manila", "23.971.000"),
		("Toledo", "85.449"),
	]
)
def test_pagina_estadisticas_existe_viaje_ciudad_mas_grande(cliente, conexion, ciudad, poblacion):

	data={"pais":"Pais",
			"ciudad":ciudad,
			"ida":"22/06/2019",
			"vuelta":"23/06/2019",
			"hotel":"hotel",
			"web":"www.google.com",
			"transporte":"t",
			"comentario":"Sin Comentario",
			"archivo_imagen":"Sin Imagen"}

	cliente.post("/insertar_viaje", data=data)

	respuesta=cliente.get(f"/estadisticas")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Estadisticas de los viajes" in contenido
	assert f"{ciudad} - {poblacion} habitantes" in contenido

@pytest.mark.parametrize(["ciudades", "ciudad_mas_grande", "poblacion"],
	[
		(["Toledo", "Madrid", "Barcelona", "Paris", "London", "Valencia", "Porto"], "London", "11.120.000"),
		(["Toledo", "Madrid", "Barcelona", "Paris", "London", "Valencia", "Porto", "Tokyo", "Madrid"], "Tokyo", "39.105.000"),
		(["Toledo", "Madrid", "Barcelona", "Porto", "Madrid", "Barcelona", "Lisbon"], "Madrid", "6.006.000")
	]
)
def test_pagina_estadisticas_existen_viajes_ciudad_mas_grande(cliente, conexion, ciudades, ciudad_mas_grande, poblacion):

	for ciudad in ciudades:

		data={"pais":"Pais",
				"ciudad":ciudad,
				"ida":"22/06/2019",
				"vuelta":"23/06/2019",
				"hotel":"hotel",
				"web":"www.google.com",
				"transporte":"t",
				"comentario":"Sin Comentario",
				"archivo_imagen":"Sin Imagen"}

		cliente.post("/insertar_viaje", data=data)

	respuesta=cliente.get(f"/estadisticas")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Estadisticas de los viajes" in contenido
	assert f"{ciudad_mas_grande} - {poblacion} habitantes" in contenido

@pytest.mark.parametrize(["ciudad", "kilometros"],
	[
		("London", "1.263"),
		("Madrid", "0"),
		("Paris", "1.053"),
		("Tokyo", "10.766"),
		("Porto", "419"),
		("Manila", "11.656"),
		("Toledo", "67"),
		("Karachi", "6.667")
	]
)
def test_pagina_estadisticas_existe_viaje_ciudad_mas_lejana(cliente, conexion, ciudad, kilometros):

	data={"pais":"Pais",
			"ciudad":ciudad,
			"ida":"22/06/2019",
			"vuelta":"23/06/2019",
			"hotel":"hotel",
			"web":"www.google.com",
			"transporte":"t",
			"comentario":"Sin Comentario",
			"archivo_imagen":"Sin Imagen"}

	cliente.post("/insertar_viaje", data=data)

	respuesta=cliente.get(f"/estadisticas")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Estadisticas de los viajes" in contenido
	assert f"{ciudad} - {kilometros} KM" in contenido

@pytest.mark.parametrize(["ciudades", "ciudad_mas_lejana", "kilometros"],
	[
		(["Madrid", "Barcelona", "Paris", "London", "Toledo", "Valencia", "Porto"], "London", "1.263"),
		(["Madrid", "Barcelona", "Paris", "Rome", "Toledo", "Milan", "Brussels", "London"], "Rome", "1.364"),
		(["Madrid", "Barcelona", "Paris", "Rome", "Toledo", "Milan", "Karachi"], "Karachi", "6.667"),
		(["Madrid", "Barcelona", "Paris", "Rome", "Toledo", "Milan", "Karachi", "Tokyo"], "Tokyo", "10.766"),
		(["Madrid", "Barcelona", "Paris", "Rome", "Toledo", "Milan", "Karachi", "Tokyo", "Manila"], "Manila", "11.656"),
		(["Madrid", "Toledo", "Barcelona", "Barcelona", "Barcelona", "Barcelona"], "Barcelona", "506"),
	]
)
def test_pagina_estadisticas_existen_viajes_ciudad_mas_lejana(cliente, conexion, ciudades, ciudad_mas_lejana, kilometros):

	for ciudad in ciudades:

		data={"pais":"Pais",
				"ciudad":ciudad,
				"ida":"22/06/2019",
				"vuelta":"23/06/2019",
				"hotel":"hotel",
				"web":"www.google.com",
				"transporte":"t",
				"comentario":"Sin Comentario",
				"archivo_imagen":"Sin Imagen"}

		cliente.post("/insertar_viaje", data=data)

	respuesta=cliente.get(f"/estadisticas")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Estadisticas de los viajes" in contenido
	assert f"{ciudad_mas_lejana} - {kilometros} KM" in contenido

@pytest.mark.parametrize(["origen", "ciudades"],
	[
		(5454654765, ["Madrid", "Paris", "Milan", "Karachi", "Tokyo", "Manila", "New York"]),
		(0, ["Madrid", "Barcelona", "Paris", "Milan", "Karachi", "Tokyo", "Manila", "New York"]),
		(-1, ["Madrid", "Barcelona", "Paris", "Milan", "Karachi", "Tokyo", "Manila", "Rome", "London"]),
		(34325467, ["Paris", "London", "Porto", "Lisbon", "A Coruna", "Milan", "Madrid"]),
	]
)
def test_pagina_estadisticas_existen_viajes_ciudad_mas_lejana_origen_distinto_no_existe(cliente, conexion, origen, ciudades):

	for ciudad in ciudades:

		data={"pais":"Pais",
				"ciudad":ciudad,
				"ida":"22/06/2019",
				"vuelta":"23/06/2019",
				"hotel":"hotel",
				"web":"www.google.com",
				"transporte":"t",
				"comentario":"Sin Comentario",
				"archivo_imagen":"Sin Imagen"}

		cliente.post("/insertar_viaje", data=data)

	respuesta=cliente.get(f"/estadisticas?codigo_ciudad={origen}")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/"
	assert "Redirecting..." in contenido

@pytest.mark.parametrize(["origen", "ciudades", "ciudad_mas_lejana"],
	[
		(160, ["Madrid", "Paris", "Milan", "Karachi", "Tokyo", "Manila", "New York"], "Manila"),
		(22, ["Madrid", "Barcelona", "Paris", "Milan", "Karachi", "Tokyo", "Manila", "New York"], "New York"),
		(1, ["Madrid", "Barcelona", "Paris", "Milan", "Karachi", "Tokyo", "Manila", "Rome", "London"], "Madrid"),
		(160, ["Paris", "London", "Porto", "Lisbon", "A Coruna", "Milan", "Madrid"], "London"),
		(34, ["Paris", "London", "Porto", "Lisbon", "A Coruna", "Milan", "Madrid"], "Lisbon")
	]
)
def test_pagina_estadisticas_existen_viajes_ciudad_mas_lejana_origen_distinto(cliente, conexion, origen, ciudades, ciudad_mas_lejana):

	for ciudad in ciudades:

		data={"pais":"Pais",
				"ciudad":ciudad,
				"ida":"22/06/2019",
				"vuelta":"23/06/2019",
				"hotel":"hotel",
				"web":"www.google.com",
				"transporte":"t",
				"comentario":"Sin Comentario",
				"archivo_imagen":"Sin Imagen"}

		cliente.post("/insertar_viaje", data=data)

	respuesta=cliente.get(f"/estadisticas?codigo_ciudad={origen}")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Estadisticas de los viajes" in contenido
	assert f"{ciudad_mas_lejana} -" in contenido

def test_pagina_estadisticas_existe_viaje_sin_imagen(cliente, conexion):

	data={"pais":"Pais",
				"ciudad":"Madrid",
				"ida":"22/06/2019",
				"vuelta":"23/06/2019",
				"hotel":"hotel",
				"web":"www.google.com",
				"transporte":"t",
				"comentario":"Sin Comentario",
				"archivo_imagen":"Sin Imagen"}

	cliente.post("/insertar_viaje", data=data)

	respuesta=cliente.get(f"/estadisticas")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Estadisticas de los viajes" in contenido
	assert "Vaya, no hay imagenes recientes que mostrar..." in contenido

def test_pagina_estadisticas_existe_viaje_con_imagen_no_existen(cliente, conexion):

	data={"pais":"Pais",
				"ciudad":"Madrid",
				"ida":"22/06/2019",
				"vuelta":"23/06/2019",
				"hotel":"hotel",
				"web":"www.google.com",
				"transporte":"t",
				"comentario":"Sin Comentario",
				"archivo_imagen":"imagen_no_existe.jpg"}

	cliente.post("/insertar_viaje", data=data)

	respuesta=cliente.get(f"/estadisticas")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Estadisticas de los viajes" in contenido
	assert "Vaya, no hay imagenes recientes que mostrar..." in contenido

# Funcion para copiar la imagen de los tests
def copiarImagenNombre(nombre_imagen:str):

	ruta_imagen=os.path.join(os.getcwd(), "testapp", "imagen_tests.jpg")

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	ruta_relativa_carpeta=os.path.join(ruta_relativa, "static", "imagenes")

	ruta_destino=os.path.join(ruta_relativa_carpeta, f"{nombre_imagen}.jpg")

	shutil.copy(ruta_imagen, ruta_destino)

	assert os.path.exists(ruta_destino)

# Funcion complementaria para vaciar la carpeta de las imagenes
def vaciarCarpeta(ruta:str)->None:

	if os.path.exists(ruta):

		for archivo in os.listdir(ruta):

			os.remove(os.path.join(ruta, archivo))

@pytest.mark.parametrize(["nombre_imagen"],
	[("imagen1",),("imagen2",),("hhjfffh",),("madrid_espana",)]
)
def test_pagina_estadisticas_existe_viaje_con_imagen_existe(cliente, conexion, nombre_imagen):

	copiarImagenNombre(nombre_imagen)

	data={"pais":"Pais",
				"ciudad":"Madrid",
				"ida":"22/06/2019",
				"vuelta":"23/06/2019",
				"hotel":"hotel",
				"web":"www.google.com",
				"transporte":"t",
				"comentario":"Sin Comentario",
				"archivo_imagen":f"{nombre_imagen}.jpg"}

	cliente.post("/insertar_viaje", data=data)

	respuesta=cliente.get(f"/estadisticas")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Estadisticas de los viajes" in contenido
	assert "Vaya, no hay imagenes recientes que mostrar..." not in contenido
	assert f"/static/imagenes/{nombre_imagen}.jpg" in contenido

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	ruta_relativa_carpeta=os.path.join(ruta_relativa, "static", "imagenes")

	vaciarCarpeta(ruta_relativa_carpeta)

@pytest.mark.parametrize(["numero_imagenes"],
	[(5,),(2,),(3,),(1,),(4,)]
)
def test_pagina_estadisticas_existe_viaje_con_imagen_existen_todas(cliente, conexion, numero_imagenes):

	for numero in range(numero_imagenes):

		nombre_imagen=f"imagen{numero}"

		copiarImagenNombre(nombre_imagen)

		data={"pais":"Pais",
					"ciudad":"Madrid",
					"ida":"22/06/2019",
					"vuelta":"23/06/2019",
					"hotel":"hotel",
					"web":"www.google.com",
					"transporte":"t",
					"comentario":"Sin Comentario",
					"archivo_imagen":f"{nombre_imagen}.jpg"}

		cliente.post("/insertar_viaje", data=data)

	respuesta=cliente.get(f"/estadisticas")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Estadisticas de los viajes" in contenido
	assert "Vaya, no hay imagenes recientes que mostrar..." not in contenido

	for numero in range(numero_imagenes):

		nombre_imagen=f"imagen{numero}"

		assert f"/static/imagenes/{nombre_imagen}.jpg" in contenido

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	ruta_relativa_carpeta=os.path.join(ruta_relativa, "static", "imagenes")

	vaciarCarpeta(ruta_relativa_carpeta)

@pytest.mark.parametrize(["numero_imagenes", "numero_imagenes_no_existen"],
	[(5, 4),(2, 6),(3, 7),(1, 10),(4, 1)]
)
def test_pagina_estadisticas_existe_viaje_con_imagen_existen_algunas(cliente, conexion, numero_imagenes, numero_imagenes_no_existen):

	for numero in range(numero_imagenes):

		nombre_imagen=f"imagen{numero}"

		copiarImagenNombre(nombre_imagen)

		data={"pais":"Pais",
					"ciudad":"Madrid",
					"ida":"22/06/2019",
					"vuelta":"23/06/2019",
					"hotel":"hotel",
					"web":"www.google.com",
					"transporte":"t",
					"comentario":"Sin Comentario",
					"archivo_imagen":f"{nombre_imagen}.jpg"}

		cliente.post("/insertar_viaje", data=data)

	for _ in range(numero_imagenes_no_existen):

		data={"pais":"Pais",
			"ciudad":"Madrid",
			"ida":"22/05/2019",
			"vuelta":"23/06/2019",
			"hotel":"hotel",
			"web":"www.google.com",
			"transporte":"t",
			"comentario":"Sin Comentario",
			"archivo_imagen":"imagen_no_existe.jpg"}

		cliente.post("/insertar_viaje", data=data)

	respuesta=cliente.get(f"/estadisticas")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Estadisticas de los viajes" in contenido
	assert "Vaya, no hay imagenes recientes que mostrar..." not in contenido

	for numero in range(numero_imagenes):

		nombre_imagen=f"imagen{numero}"

		assert f"/static/imagenes/{nombre_imagen}.jpg" in contenido

	assert "imagen_no_existe.jpg" not in contenido

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	ruta_relativa_carpeta=os.path.join(ruta_relativa, "static", "imagenes")

	vaciarCarpeta(ruta_relativa_carpeta)

@pytest.mark.parametrize(["transporte"],
	[("transporte",),("avion",),("hola",),("t",)]
)
def test_pagina_estadisticas_existe_viaje_trasporte_sin_imagen(cliente, conexion, transporte):

	data={"pais":"Pais",
					"ciudad":"Madrid",
					"ida":"22/06/2019",
					"vuelta":"23/06/2019",
					"hotel":"hotel",
					"web":"www.google.com",
					"transporte":transporte,
					"comentario":"Sin Comentario",
					"archivo_imagen":"imagen.jpg"}

	cliente.post("/insertar_viaje", data=data)

	respuesta=cliente.get(f"/estadisticas")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Estadisticas de los viajes" in contenido
	assert f"<p>{transporte}</p>" in contenido
	assert f"/static/imagenes_transportes/{transporte}.jpg" not in contenido

@pytest.mark.parametrize(["transporte", "transporte_imagen"],
	[
		("Avion", "Avion"),
		("Andando", "Pie"),
		("Autobus EMT", "AutobusEMT"),
		("Autobus verde", "AutobusVerde"),
		("La Renfe", "Renfe"),
		("Autobus", "Autobus"),
		("Tren/AVE", "Tren"),
		("Coche", "Coche")
	]
)
def test_pagina_estadisticas_existe_viaje_trasporte_con_imagen(cliente, conexion, transporte, transporte_imagen):

	data={"pais":"Pais",
					"ciudad":"Madrid",
					"ida":"22/06/2019",
					"vuelta":"23/06/2019",
					"hotel":"hotel",
					"web":"www.google.com",
					"transporte":transporte,
					"comentario":"Sin Comentario",
					"archivo_imagen":"imagen.jpg"}

	cliente.post("/insertar_viaje", data=data)

	respuesta=cliente.get(f"/estadisticas")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Estadisticas de los viajes" in contenido
	assert f"<p>{transporte}</p>" not in contenido
	assert f"/static/imagenes_transportes/{transporte_imagen}.png" in contenido

@pytest.mark.parametrize(["transportes", "transportes_imagen"],
	[
		(["Avion","Avion","Coche","Autobus verde","Autobus"],["Avion","AutobusVerde","Autobus"]),
		(["Avion","Avion","Coche","Coche","Autobus verde","Autobus","La Renfe","La Renfe"],["Avion","Coche","Renfe"]),
		(["Avion","Avion","Coche","Coche","Autobus verde","Autobus","La Renfe","La Renfe","Autobus"],["Avion","Coche","Autobus"])
	]
)
def test_pagina_estadisticas_existen_viajes_trasporte_con_imagen(cliente, conexion, transportes, transportes_imagen):

	for transporte in transportes:

		data={"pais":"Pais",
						"ciudad":"Madrid",
						"ida":"22/06/2019",
						"vuelta":"23/06/2019",
						"hotel":"hotel",
						"web":"www.google.com",
						"transporte":transporte,
						"comentario":"Sin Comentario",
						"archivo_imagen":"imagen.jpg"}

		cliente.post("/insertar_viaje", data=data)

	respuesta=cliente.get(f"/estadisticas")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Estadisticas de los viajes" in contenido

	for transporte_imagen in transportes_imagen:

		assert f"/static/imagenes_transportes/{transporte_imagen}.png" in contenido
