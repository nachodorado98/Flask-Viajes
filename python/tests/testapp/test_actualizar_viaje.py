import pytest

@pytest.mark.parametrize(["id_viaje"],
	[(0,), (10000000,), (-1,), (243544666,)]
)
def test_pagina_actualizar_viaje_no_existe(cliente, conexion, id_viaje):

	respuesta=cliente.post(f"/actualizar_viaje/{id_viaje}")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/"
	assert "Redirecting..." in contenido

def test_pagina_actualizar_viaje_existe(cliente, conexion):

	data={"pais":"España",
			"ciudad":"Madrid",
			"ida":"22/06/2019",
			"vuelta":"22/06/2019",
			"hotel":"hotel",
			"web":"www.google.com",
			"transporte":"t",
			"comentario":"Sin Comentario",
			"archivo_imagen":"Sin Imagen"}

	cliente.post("/insertar_viaje", data=data)

	viajes=conexion.obtenerViajes()

	id_viaje=viajes[0][0]

	respuesta=cliente.post(f"/actualizar_viaje/{id_viaje}")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert str(id_viaje) in contenido