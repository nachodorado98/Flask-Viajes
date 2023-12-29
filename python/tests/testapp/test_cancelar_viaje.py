import pytest

@pytest.mark.parametrize(["archivo_imagen"],
	[("imagen",), ("Sin Imagen",), ("imagen.jpg",), ("london_uk_",), ("mipdf.pdf",)]
)
def test_pagina_cancelar_viaje(cliente, conexion, archivo_imagen):

	respuesta=cliente.get(f"/cancelar_viaje/{archivo_imagen}")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/"
	assert "Redirecting..." in contenido
