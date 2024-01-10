import pytest
import os

from src.utilidades.utils import eliminarPosiblesMapasFolium

def test_pagina_mapa_no_existe_viaje(cliente, conexion):

	respuesta=cliente.get(f"/mapa")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/"
	assert "Redirecting..." in contenido

@pytest.mark.parametrize(["ciudad"],
	[("Madrid",),("Porto",),("Toledo",),("Guadalajara",),("London",)]
)
def test_pagina_mapa_existe_viaje(cliente, conexion, ciudad):

	data={"pais":"España",
			"ciudad":ciudad,
			"ida":"22/06/2019",
			"vuelta":"22/06/2019",
			"hotel":"hotel",
			"web":"www.google.com",
			"transporte":"t",
			"comentario":"Sin Comentario",
			"archivo_imagen":"Sin Imagen"}

	cliente.post("/insertar_viaje", data=data)

	respuesta=cliente.get(f"/mapa")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Mapa Mundial" in contenido
	assert "iframe" in contenido
	assert "/visualizar_mapa/geojson_mapa_" in contenido

@pytest.mark.parametrize(["ciudades"],
	[
		(["Madrid", "Porto"],),
		(["Madrid", "Porto", "Toledo"],),
		(["Madrid", "Porto", "London"],),
		(["Madrid", "Porto", "Toledo", "London"],),
		(["Madrid", "Porto", "Toledo", "London", "Paris"],),
		(["Madrid", "Porto", "Toledo", "London", "Paris", "Guadalajara"],)
	]
)
def test_pagina_mapa_existen_viajes(cliente, conexion, ciudades):

	for ciudad in ciudades:

		data={"pais":"España",
					"ciudad":ciudad,
					"ida":"22/06/2019",
					"vuelta":"22/06/2019",
					"hotel":"hotel",
					"web":"www.google.com",
					"transporte":"t",
					"comentario":"Sin Comentario",
					"archivo_imagen":"Sin Imagen"}

		cliente.post("/insertar_viaje", data=data)

	respuesta=cliente.get(f"/mapa")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Mapa Mundial" in contenido
	assert "iframe" in contenido
	assert "/visualizar_mapa/geojson_mapa_" in contenido

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	eliminarPosiblesMapasFolium(ruta_relativa)