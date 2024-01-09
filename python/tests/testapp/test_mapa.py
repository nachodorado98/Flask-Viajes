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
	assert f"<h1>Viajes a {ciudad}</h1>" in contenido
	assert f"Viaje(s) a {ciudad}" in contenido

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	eliminarPosiblesMapasFolium(ruta_relativa)

@pytest.mark.parametrize(["paises", "siglas", "ciudades", "fechas"],
	[
		(["Spain", "United Kingdom"], ["ESP", "GBR"], ["London", "Madrid"], "22/06/2019-22/06/2019"),
		(["Germany", "United Kingdom"], ["DEU", "GBR"], ["Berlin", "London"], "22/06/2019-22/06/2019"),
		(["Spain", "Portugal", "Germany", "United Kingdom"], ["ESP", "PRT", "DEU", "GBR"], ["Madrid", "Porto", "Berlin", "London"], "22/06/2019-22/06/2019"),
	]
)
def test_pagina_mapa_existen_viajes(cliente, conexion, paises, siglas, ciudades, fechas):

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

	for pais, sigla in zip(paises, siglas):

			assert pais in contenido
			assert sigla in contenido

	for ciudad in ciudades:

		assert f"<h1>Viajes a {ciudad}</h1>" in contenido
		assert f"Viaje(s) a {ciudad}" in contenido
		assert f"<h4>Fechas Ida y Vuelta Viaje(s):<br> {fechas}</h4>"

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	eliminarPosiblesMapasFolium(ruta_relativa)