import pytest

@pytest.mark.parametrize(["pais"],
	[("jkjkjkjjk",), ("españa",), ("ReinoUnido",), ("ANDORRA",), ("Pais",)]
)
def test_pagina_detalle_pais_no_existe(cliente, conexion, pais):

	respuesta=cliente.get(f"/detalle_pais/{pais}")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/"
	assert "Redirecting..." in contenido

@pytest.mark.parametrize(["pais", "capital"],
	[
		("España", "Madrid"),
		("Netherlands", "Amsterdam"),
		("Reino Unido", "London"),
		("Andorra", "Andorra la Vella"),
		("Emiratos Árabes Unidos", "Abu Dhabi")
	]
)
def test_pagina_detalle_pais(cliente, conexion, pais, capital):

	respuesta=cliente.get(f"/detalle_pais/{pais}")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Detalle del pais" in contenido
	assert pais in contenido
	assert "Capital" in contenido
	assert capital in contenido
	assert "Poblacion" in contenido
	assert "Ciudades" in contenido

@pytest.mark.parametrize(["pais", "capital", "siglas"],
	[
		("Aruba", "Oranjestad", "ABW"),
		("Bermudas", "Hamilton", "BMU"),
		("Guam", "Guam", "GUM"),
		("Hong Kong", "Hong Kong", "HKG")
	]
)
def test_pagina_detalle_pais_sin_bandera(cliente, conexion, pais, capital, siglas):

	respuesta=cliente.get(f"/detalle_pais/{pais}")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Detalle del pais" in contenido
	assert pais in contenido
	assert "Capital" in contenido
	assert "Bandera" not in contenido
	assert f"/static/imagenes_banderas/{siglas}.png" not in contenido
	assert "Sin Bandera" not in contenido

@pytest.mark.parametrize(["pais", "capital", "siglas"],
	[
		("Reino Unido", "London", "GBR"),
		("Japón", "Tokyo", "JPN"),
		("España", "Madrid", "ESP"),
		("Netherlands", "Amsterdam", "NLD"),
		("Andorra", "Andorra la Vella", "AND")
	]
)
def test_pagina_detalle_pais_con_bandera(cliente, conexion, pais, capital, siglas):

	respuesta=cliente.get(f"/detalle_pais/{pais}")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Detalle del pais" in contenido
	assert pais in contenido
	assert "Capital" in contenido
	assert "Bandera" in contenido
	assert f"/static/imagenes_banderas/{siglas}.png" in contenido