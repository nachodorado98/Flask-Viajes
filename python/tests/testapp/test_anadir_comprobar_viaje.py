import pytest
import os

def test_pagina_anadir_viaje(cliente, conexion):

	respuesta=cliente.get("/anadir_viaje")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Añadir viaje realizado" in contenido
	assert "<h3>Destino</h3>" in contenido
	assert "<h3>Fechas</h3>" in contenido
	assert "<h3>Detalles del Viaje</h3>" in contenido
	assert "<h3>Informacion Adicional</h3>" in contenido

@pytest.mark.parametrize(["ida", "vuelta"],
	[
		("2019-6-22", "2019-4-13"),
		("2019-4-13", "2019-4-12"),
		("2023-12-26", "2022-12-26")
	]
)
def test_pagina_comprobar_viaje_error_fechas(cliente, conexion, ida, vuelta):

	data={"pais":"España",
		"ciudad":"Madrid",
		"fecha-ida":ida,
		"fecha-vuelta":vuelta,
		"nombre-hotel":"Hotel",
		"pagina-web-hotel":"www.hotel.com",
		"transporte":"Transporte"}

	respuesta=cliente.post("/comprobar_viaje", data=data)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/anadir_viaje"
	assert "Redirecting..." in contenido

@pytest.mark.parametrize(["web"],
	[("hola.com",),("adios.es",),("www.hola",),("www.adios.net",),("ww.hola.com",),("www.mal.uk",)]
)
def test_pagina_comprobar_viaje_error_web(cliente, conexion, web):

	data={"pais":"España",
		"ciudad":"Madrid",
		"fecha-ida":"2019-4-13",
		"fecha-vuelta":"2019-6-22",
		"nombre-hotel":"Hotel",
		"pagina-web-hotel":web,
		"transporte":"Transporte"}

	respuesta=cliente.post("/comprobar_viaje", data=data)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/anadir_viaje"
	assert "Redirecting..." in contenido

@pytest.mark.parametrize(["comentario"],
	[
		("Comentariooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo",),
		("Comentarioooooooooooooooooooooooooooooooooooooooooooooooooooo",),
		("Comentarioooooooooooooooooooooooooooooooooooooooooooghfhfhfoooooooooooooooooooo",)
	]
)
def test_pagina_comprobar_viaje_comentario_error(cliente, conexion, comentario):

	data={"pais":"España",
		"ciudad":"Madrid",
		"fecha-ida":"2019-6-22",
		"fecha-vuelta":"2019-6-22",
		"nombre-hotel":"Hotel",
		"pagina-web-hotel":"www.miweb.com",
		"transporte":"Transporte",
		"comentario":comentario}

	respuesta=cliente.post("/comprobar_viaje", data=data)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/anadir_viaje"
	assert "Redirecting..." in contenido

def test_pagina_comprobar_viaje_sin_comentario_sin_imagen(cliente, conexion):

	data={"pais":"España",
		"ciudad":"Madrid",
		"fecha-ida":"2019-6-22",
		"fecha-vuelta":"2019-6-22",
		"nombre-hotel":"Hotel",
		"pagina-web-hotel":"www.miweb.com",
		"transporte":"Transporte"}

	respuesta=cliente.post("/comprobar_viaje", data=data)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Resumen" in contenido
	assert "España" in contenido
	assert "Madrid" in contenido
	assert "22/06/2019" in contenido
	assert "Hotel" in contenido
	assert "www.miweb.com" in contenido
	assert "Transporte" in contenido
	assert "<p><strong>Comentario:</strong> Sin Comentario</p>" not in contenido
	assert "Sin Comentario" in contenido
	assert "<p>Sin Imagen</p>" not in contenido
	assert "Sin Imagen" in contenido

def test_pagina_comprobar_viaje_con_comentario_sin_imagen(cliente, conexion):

	data={"pais":"España",
		"ciudad":"Madrid",
		"fecha-ida":"2019-6-22",
		"fecha-vuelta":"2019-6-22",
		"nombre-hotel":"Hotel",
		"pagina-web-hotel":"www.miweb.com",
		"transporte":"Transporte",
		"comentario":"Comentario"}

	respuesta=cliente.post("/comprobar_viaje", data=data)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Resumen" in contenido
	assert "España" in contenido
	assert "Madrid" in contenido
	assert "22/06/2019" in contenido
	assert "Hotel" in contenido
	assert "www.miweb.com" in contenido
	assert "Transporte" in contenido
	assert "Comentario" in contenido
	assert "<p>Sin Imagen</p>" not in contenido
	assert "Sin Imagen" in contenido


# Funcion complementaria para vaciar la carpeta de las imagenes
def vaciarCarpeta(ruta:str)->None:

	if os.path.exists(ruta):

		for archivo in os.listdir(ruta):

			os.remove(os.path.join(ruta, archivo))

def test_limpieza_imagenes_posible_existencia():

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	ruta_relativa_carpeta=os.path.join(ruta_relativa, "static", "imagenes")

	vaciarCarpeta(ruta_relativa_carpeta)

	assert len(os.listdir(ruta_relativa_carpeta))==0


def test_pagina_comprobar_viaje_con_comentario_con_imagen(cliente, conexion):

	ruta_imagen=os.path.join(os.getcwd(), "testapp", "imagen_tests.jpg")

	data={"pais":"España",
		"ciudad":"Madrid",
		"fecha-ida":"2019-6-22",
		"fecha-vuelta":"2019-6-22",
		"nombre-hotel":"Hotel",
		"pagina-web-hotel":"www.miweb.com",
		"transporte":"Transporte",
		"comentario":"Comentario"}

	with open(ruta_imagen, "rb") as imagen_file:
		
		data["imagen"]=(imagen_file, "imagen_tests.jpg")

		respuesta=cliente.post("/comprobar_viaje", data=data, buffered=True, content_type="multipart/form-data")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Resumen" in contenido
	assert "España" in contenido
	assert "Madrid" in contenido
	assert "22/06/2019" in contenido
	assert "Hotel" in contenido
	assert "www.miweb.com" in contenido
	assert "Transporte" in contenido
	assert "Comentario" in contenido
	assert "madrid_españa_" in contenido
	
	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	ruta_relativa_carpeta=os.path.join(ruta_relativa, "static", "imagenes")

	archivos=os.listdir(ruta_relativa_carpeta)

	imagen=archivos[0]

	assert imagen.startswith("madrid_españa_")
	assert imagen.endswith(".jpg")

	vaciarCarpeta(ruta_relativa_carpeta)

def test_pagina_comprobar_viaje_sin_comentario_con_imagen(cliente, conexion):

	ruta_imagen=os.path.join(os.getcwd(), "testapp", "imagen_tests.jpg")

	data={"pais":"España",
		"ciudad":"Madrid",
		"fecha-ida":"2019-6-22",
		"fecha-vuelta":"2019-6-22",
		"nombre-hotel":"Hotel",
		"pagina-web-hotel":"www.miweb.com",
		"transporte":"Transporte"}

	with open(ruta_imagen, 'rb') as imagen_file:
		
		data["imagen"]=(imagen_file, "imagen_tests.jpg")

		respuesta=cliente.post("/comprobar_viaje", data=data, buffered=True, content_type="multipart/form-data")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Resumen" in contenido
	assert "España" in contenido
	assert "Madrid" in contenido
	assert "22/06/2019" in contenido
	assert "Hotel" in contenido
	assert "www.miweb.com" in contenido
	assert "Transporte" in contenido
	assert "<p><strong>Comentario:</strong> Sin Comentario</p>" not in contenido
	assert "Sin Comentario" in contenido
	assert "madrid_españa_" in contenido

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	ruta_relativa_carpeta=os.path.join(ruta_relativa, "static", "imagenes")

	archivos=os.listdir(ruta_relativa_carpeta)

	imagen=archivos[0]

	assert imagen.startswith("madrid_españa_")
	assert imagen.endswith(".jpg")

	vaciarCarpeta(ruta_relativa_carpeta)


def test_pagina_comprobar_viaje_todo_multiples(cliente, conexion):

	ruta_imagen=os.path.join(os.getcwd(), "testapp", "imagen_tests.jpg")

	viajes=[("Madrid", "España"), ("Porto", "Portugal"), ("London", "Reino Unido"), ("Ciudad", "Pais")]

	for ciudad, pais in viajes:

		data={"pais":pais,
			"ciudad":ciudad,
			"fecha-ida":"2019-6-22",
			"fecha-vuelta":"2019-6-22",
			"nombre-hotel":"Hotel",
			"pagina-web-hotel":"www.miweb.com",
			"transporte":"Transporte",
			"comentario":"Comentario"}

		with open(ruta_imagen, 'rb') as imagen_file:
			
			data["imagen"]=(imagen_file, "imagen_tests.jpg")

			cliente.post("/comprobar_viaje", data=data, buffered=True, content_type="multipart/form-data")
	
	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	ruta_relativa_carpeta=os.path.join(ruta_relativa, "static", "imagenes")

	archivos=os.listdir(ruta_relativa_carpeta)

	assert len(archivos)==len(viajes)

	vaciarCarpeta(ruta_relativa_carpeta)