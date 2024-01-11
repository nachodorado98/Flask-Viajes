def test_pagina_estadisticas_no_existe_viaje(cliente, conexion):

	respuesta=cliente.get(f"/estadisticas")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/"
	assert "Redirecting..." in contenido

def test_pagina_estadisticas_existe_viaje(cliente, conexion):

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

	respuesta=cliente.get(f"/estadisticas")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "{}" not in contenido