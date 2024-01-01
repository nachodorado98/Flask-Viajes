import pytest

@pytest.mark.parametrize(["codigo_ciudad"],
	[(0,), (100000,), (-1,), (24354366,)]
)
def test_pagina_detalle_ciudad_no_existe(cliente, conexion, codigo_ciudad):

	respuesta=cliente.get(f"/detalle_ciudad/{codigo_ciudad}")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/"
	assert "Redirecting..." in contenido

@pytest.mark.parametrize(["codigo_ciudad", "ciudad"],
	[(1, "Tokyo"), (3, "Delhi"), (34, "London"), (2438, "Porto"), (160, "Barcelona"), (809, "Andorra la Vella")]
)
def test_pagina_detalle_ciudad(cliente, conexion, codigo_ciudad, ciudad):

	respuesta=cliente.get(f"/detalle_ciudad/{codigo_ciudad}")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Detalle de la ciudad de" in contenido
	assert ciudad in contenido
	assert "Tipo de ciudad:" in contenido
	assert "Poblacion" in contenido