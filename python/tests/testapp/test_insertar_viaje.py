import pytest

@pytest.mark.parametrize(["ciudad"],
	[("jkjkjkjjk",), ("MADRID",), ("barna",), ("london",), ("Andorra La Vella",)]
)
def test_pagina_insertar_viaje_ciudad_no_existe(cliente, conexion, ciudad):

	data={"pais":"España",
		"ciudad":ciudad,
		"ida":"22/06/2019",
		"vuelta":"22/06/2019",
		"hotel":"Hotel",
		"web":"www.mihotel.es",
		"transporte":"Transporte"}

	respuesta=cliente.post("/insertar_viaje", data=data)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/anadir_viaje"
	assert "Redirecting..." in contenido


@pytest.mark.parametrize(["comentario", "imagen"],
	[
		("Sin Comentario", "Sin Imagen"),
		("Sin Comentario", "imagen.jpg"),
		("Comentario", "Sin Imagen"),
		("Comentario", "imagen.jpg")
	]
)
def test_pagina_insertar_viaje_con_cadenas(cliente, conexion, comentario, imagen):

	data={"pais":"España",
		"ciudad":"London",
		"ida":"22/06/2019",
		"vuelta":"22/06/2019",
		"hotel":"Hotel",
		"web":"www.mihotel.es",
		"transporte":"Transporte",
		"comentario":comentario,
		"archivo_imagen":imagen}

	respuesta=cliente.post("/insertar_viaje", data=data)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/"
	assert "Redirecting..." in contenido

	conexion.c.execute("SELECT * FROM viajes")

	registros=conexion.c.fetchall()

	assert len(registros)==1
	assert registros[0]["comentario"]==comentario
	assert registros[0]["imagen"]==imagen

@pytest.mark.parametrize(["data", "comentario", "imagen"],
	[
		({"pais":"España","ciudad":"London","ida":"22/06/2019","vuelta":"22/06/2019","hotel":"h","web":"www.h.es","transporte":"t"}, "Sin Comentario", "Sin Imagen"),
		({"pais":"España","ciudad":"London","ida":"22/06/2019","vuelta":"22/06/2019","hotel":"h","web":"www.h.es","transporte":"t", "comentario":"Comentario"}, "Comentario", "Sin Imagen"),
		({"pais":"España","ciudad":"London","ida":"22/06/2019","vuelta":"22/06/2019","hotel":"h","web":"www.h.es","transporte":"t", "archivo_imagen":"imagen.jpg"}, "Sin Comentario", "imagen.jpg"),
		({"pais":"España","ciudad":"London","ida":"22/06/2019","vuelta":"22/06/2019","hotel":"h","web":"www.h.es","transporte":"t", "comentario":"Comentario", "archivo_imagen":"imagen.jpg"}, "Comentario", "imagen.jpg")
	]
)
def test_pagina_insertar_viaje_con_nones(cliente, conexion, data, comentario, imagen):

	respuesta=cliente.post("/insertar_viaje", data=data)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/"
	assert "Redirecting..." in contenido

	conexion.c.execute("SELECT * FROM viajes")

	registros=conexion.c.fetchall()

	assert len(registros)==1
	assert registros[0]["comentario"]==comentario
	assert registros[0]["imagen"]==imagen

@pytest.mark.parametrize(["data"],
	[
		({"pais":"España","ciudad":"London","ida":"22/06/2019","vuelta":"22/06/2019","hotel":"h","web":"www.h.es","transporte":"t"},),
		({"pais":"España","ciudad":"London","ida":"22/06/2019","vuelta":"22/06/2019","hotel":"h","web":"www.h.es","transporte":"t", "comentario":"Comentario"},),
		({"pais":"España","ciudad":"London","ida":"22/06/2019","vuelta":"22/06/2019","hotel":"h","web":"www.h.es","transporte":"t", "archivo_imagen":"imagen.jpg"},),
		({"pais":"España","ciudad":"London","ida":"22/06/2019","vuelta":"22/06/2019","hotel":"h","web":"www.h.es","transporte":"t", "comentario":"Comentario", "archivo_imagen":"imagen.jpg"},)
	]
)
def test_pagina_insertar_viajes_multiples(cliente, conexion, data):

	cliente.post("/insertar_viaje", data=data)
	cliente.post("/insertar_viaje", data=data)
	cliente.post("/insertar_viaje", data=data)
	cliente.post("/insertar_viaje", data=data)

	conexion.c.execute("SELECT * FROM viajes")

	assert len(conexion.c.fetchall())==4