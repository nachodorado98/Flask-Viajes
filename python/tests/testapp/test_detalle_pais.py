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