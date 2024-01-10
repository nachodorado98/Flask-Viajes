import pytest
import os


# Funcion complementaria para vaciar la carpeta de las imagenes
def vaciarCarpetaImagenes()->None:

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	ruta_relativa_carpeta=os.path.join(ruta_relativa, "static", "imagenes")

	for archivo in os.listdir(ruta_relativa_carpeta):

		os.remove(os.path.join(ruta_relativa_carpeta, archivo))

@pytest.mark.parametrize(["id_viaje"],
	[(0,), (10000000,), (-1,), (243544666,)]
)
def test_pagina_actualizar_viaje_no_existe(cliente, conexion, id_viaje):

	respuesta=cliente.post(f"/actualizar_viaje/{id_viaje}")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/"
	assert "Redirecting..." in contenido

	vaciarCarpetaImagenes()

@pytest.mark.parametrize(["comentario"],
	[
		("Comentariooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo",),
		("Comentarioooooooooooooooooooooooooooooooooooooooooooooooooooo",),
		("Comentarioooooooooooooooooooooooooooooooooooooooooooghfhfhfoooooooooooooooooooo",)
	]
)
def test_pagina_actualizar_viaje_existe_comentario_error(cliente, conexion, comentario):

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

	data_actualizada={"comentario":comentario,
						"web":"www.miweb.com",
						"imagen":"miimagen.jpg",
						"ciudad":"Madrid",
						"pais":"España"}

	respuesta=cliente.post(f"/actualizar_viaje/{id_viaje}", data=data_actualizada)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location==f"/editar_viaje/{id_viaje}"
	assert "Redirecting..." in contenido

@pytest.mark.parametrize(["web"],
	[("hola.com",),("adios.es",),("www.hola",),("www.adios.net",),("ww.hola.com",),("www.mal.uk",)]
)
def test_pagina_actualizar_viaje_existe_comentario_error(cliente, conexion, web):

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

	data_actualizada={"comentario":"Comentario",
						"web":web,
						"imagen":"miimagen.jpg",
						"ciudad":"Madrid",
						"pais":"España"}

	respuesta=cliente.post(f"/actualizar_viaje/{id_viaje}", data=data_actualizada)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location==f"/editar_viaje/{id_viaje}"
	assert "Redirecting..." in contenido

@pytest.mark.parametrize(["web", "comentario"],
	[
		("www.miweb.com", "me gusta mucho esta app"),
		("www.holamiweb.com", "me gusta muchissisismo esta app"),
		("www.es", "me gusta mucho esta app"),
		("www.fdgfdhfghfg.com", "Comentario"),
		("www.sdgfdhfgh.com", "Sin Comentario"),
		("www.google.com", "Comentario nuevo")
	]
)
def test_pagina_actualizar_viaje_existe_imagen_existente(cliente, conexion, web, comentario):

	data={"pais":"España",
			"ciudad":"Madrid",
			"ida":"22/06/2019",
			"vuelta":"22/06/2019",
			"hotel":"hotel",
			"web":"www.google.com",
			"transporte":"t",
			"comentario":"Sin Comentario",
			"archivo_imagen":"miimagen.jpg"}

	cliente.post("/insertar_viaje", data=data)

	viajes=conexion.obtenerViajes()

	id_viaje=viajes[0][0]

	data_actualizada={"comentario":comentario,
						"web":web,
						"imagen":"miimagen.jpg",
						"ciudad":"Madrid",
						"pais":"España"}

	respuesta=cliente.post(f"/actualizar_viaje/{id_viaje}", data=data_actualizada)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location==f"/detalle_viaje/{id_viaje}"
	assert "Redirecting..." in contenido

	conexion.c.execute("SELECT * FROM viajes")

	viaje=conexion.c.fetchone()

	assert viaje["id_viaje"]==id_viaje
	assert viaje["web"]==web
	assert viaje["comentario"]==comentario

@pytest.mark.parametrize(["web", "comentario"],
	[
		("www.miweb.com", "me gusta mucho esta app"),
		("www.holamiweb.com", "me gusta muchissisismo esta app"),
		("www.es", "me gusta mucho esta app"),
		("www.fdgfdhfghfg.com", "Comentario"),
		("www.sdgfdhfgh.com", "Sin Comentario"),
		("www.google.com", "Comentario nuevo")
	]
)
def test_pagina_actualizar_viaje_existe_imagen_no_existente_sin_imagen(cliente, conexion, web, comentario):

	data={"pais":"España",
			"ciudad":"Madrid",
			"ida":"22/06/2019",
			"vuelta":"22/06/2019",
			"hotel":"hotel",
			"web":"www.google.com",
			"transporte":"t",
			"comentario":"Sin Comentario",
			"archivo_imagen":"miimagen.jpg"}

	cliente.post("/insertar_viaje", data=data)

	viajes=conexion.obtenerViajes()

	id_viaje=viajes[0][0]

	data_actualizada={"comentario":comentario,
						"web":web,
						"ciudad":"Madrid",
						"pais":"España"}

	respuesta=cliente.post(f"/actualizar_viaje/{id_viaje}", data=data_actualizada)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location==f"/detalle_viaje/{id_viaje}"
	assert "Redirecting..." in contenido

	conexion.c.execute("SELECT * FROM viajes")

	viaje=conexion.c.fetchone()

	assert viaje["id_viaje"]==id_viaje
	assert viaje["web"]==web
	assert viaje["comentario"]==comentario
	assert viaje["imagen"]=="miimagen.jpg"

@pytest.mark.parametrize(["web", "comentario"],
	[
		("www.miweb.com", "me gusta mucho esta app"),
		("www.holamiweb.com", "me gusta muchissisismo esta app"),
		("www.es", "me gusta mucho esta app"),
		("www.fdgfdhfghfg.com", "Comentario"),
		("www.sdgfdhfgh.com", "Sin Comentario"),
		("www.google.com", "Comentario nuevo")
	]
)
def test_pagina_actualizar_viaje_existe_imagen_no_existente_con_imagen_vacia(cliente, conexion, web, comentario):

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

	data_actualizada={"comentario":comentario,
						"web":web,
						"ciudad":"Madrid",
						"pais":"España"}

	ruta_imagen=os.path.join(os.getcwd(), "testapp", "imagen_tests.jpg")

	with open(ruta_imagen, "rb") as imagen_file:
		
		data_actualizada["imagen"]=(imagen_file, "")

		respuesta=cliente.post(f"/actualizar_viaje/{id_viaje}", data=data_actualizada, buffered=True, content_type="multipart/form-data")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location==f"/detalle_viaje/{id_viaje}"
	assert "Redirecting..." in contenido

	conexion.c.execute("SELECT * FROM viajes")

	viaje=conexion.c.fetchone()

	assert viaje["id_viaje"]==id_viaje
	assert viaje["web"]==web
	assert viaje["comentario"]==comentario
	assert viaje["imagen"]=="Sin Imagen"


# Funcion complementaria para vaciar la carpeta de las imagenes
def vaciarCarpeta(ruta:str)->None:

	if os.path.exists(ruta):

		for archivo in os.listdir(ruta):

			os.remove(os.path.join(ruta, archivo))

@pytest.mark.parametrize(["web", "comentario"],
	[
		("www.miweb.com", "me gusta mucho esta app"),
		("www.holamiweb.com", "me gusta muchissisismo esta app"),
		("www.es", "me gusta mucho esta app"),
		("www.fdgfdhfghfg.com", "Comentario"),
		("www.sdgfdhfgh.com", "Sin Comentario"),
		("www.google.com", "Comentario nuevo")
	]
)
def test_pagina_actualizar_viaje_existe_imagen_no_existente_con_imagen(cliente, conexion, web, comentario):

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

	data_actualizada={"comentario":comentario,
						"web":web,
						"ciudad":"Madrid",
						"pais":"España"}

	ruta_imagen=os.path.join(os.getcwd(), "testapp", "imagen_tests.jpg")

	with open(ruta_imagen, "rb") as imagen_file:
		
		data_actualizada["imagen"]=(imagen_file, "imagen_tests.jpg")

		respuesta=cliente.post(f"/actualizar_viaje/{id_viaje}", data=data_actualizada, buffered=True, content_type="multipart/form-data")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location==f"/detalle_viaje/{id_viaje}"
	assert "Redirecting..." in contenido

	conexion.c.execute("SELECT * FROM viajes")

	viaje=conexion.c.fetchone()

	assert viaje["id_viaje"]==id_viaje
	assert viaje["web"]==web
	assert viaje["comentario"]==comentario
	assert viaje["imagen"]!="Sin Imagen"

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	ruta_relativa_carpeta=os.path.join(ruta_relativa, "static", "imagenes")

	archivos=os.listdir(ruta_relativa_carpeta)

	imagen=archivos[0]

	assert imagen.startswith("madrid_españa_")
	assert imagen.endswith(".jpg")

	vaciarCarpeta(ruta_relativa_carpeta)