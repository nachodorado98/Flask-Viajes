import pytest
import shutil
import os

@pytest.mark.parametrize(["id_viaje"],
	[(0,), (10000000,), (-1,), (243544666,)]
)
def test_pagina_detalle_viaje_no_existe(cliente, conexion, id_viaje):

	respuesta=cliente.get(f"/detalle_viaje/{id_viaje}")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/"
	assert "Redirecting..." in contenido

def test_pagina_detalle_viaje_existe_sin_imagen_sin_comentario_sin_bandera(cliente, conexion):

	data={"pais":"España",
			"ciudad":"Oranjestad",
			"ida":"22/06/2019",
			"vuelta":"22/06/2019",
			"hotel":"h",
			"web":"www.google.com",
			"transporte":"t",
			"comentario":"Sin Comentario",
			"archivo_imagen":"Sin Imagen"}

	cliente.post("/insertar_viaje", data=data)

	viajes=conexion.obtenerViajes()

	id_viaje=viajes[0][0]

	respuesta=cliente.get(f"/detalle_viaje/{id_viaje}")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Detalle del viaje a" in contenido
	assert "Oranjestad" in contenido
	assert f"/static/imagenes_banderas/ABW.png" not in contenido
	assert "Destino" in contenido
	assert "Fecha" in contenido
	assert "Hotel" in contenido
	assert "https://" in contenido
	assert "Transporte"
	assert "Sin Comentario" not in contenido
	assert "Sin Imagen" in contenido

def test_pagina_detalle_viaje_existe_sin_imagen_sin_comentario_con_bandera(cliente, conexion):

	data={"pais":"España",
			"ciudad":"London",
			"ida":"22/06/2019",
			"vuelta":"22/06/2019",
			"hotel":"h",
			"web":"www.google.com",
			"transporte":"t",
			"comentario":"Sin Comentario",
			"archivo_imagen":"Sin Imagen"}

	cliente.post("/insertar_viaje", data=data)

	viajes=conexion.obtenerViajes()

	id_viaje=viajes[0][0]

	respuesta=cliente.get(f"/detalle_viaje/{id_viaje}")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Detalle del viaje a" in contenido
	assert "London" in contenido
	assert f"/static/imagenes_banderas/GBR.png" in contenido
	assert "Destino" in contenido
	assert "Fecha" in contenido
	assert "Hotel" in contenido
	assert "https://" in contenido
	assert "Transporte"
	assert "Sin Comentario" not in contenido
	assert "Sin Imagen" in contenido

def test_pagina_detalle_viaje_existe_sin_imagen_con_comentario(cliente, conexion):

	data={"pais":"España",
			"ciudad":"London",
			"ida":"22/06/2019",
			"vuelta":"22/06/2019",
			"hotel":"h",
			"web":"www.google.com",
			"transporte":"t",
			"comentario":"Comentario",
			"archivo_imagen":"Sin Imagen"}

	cliente.post("/insertar_viaje", data=data)

	viajes=conexion.obtenerViajes()

	id_viaje=viajes[0][0]

	respuesta=cliente.get(f"/detalle_viaje/{id_viaje}")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Detalle del viaje a" in contenido
	assert "London" in contenido
	assert f"/static/imagenes_banderas/GBR.png" in contenido
	assert "Destino" in contenido
	assert "Fecha" in contenido
	assert "Hotel" in contenido
	assert "https://" in contenido
	assert "Transporte" in contenido
	assert "Comentario" in contenido
	assert "Sin Imagen" in contenido

def test_pagina_detalle_viaje_existe_con_imagen_no_existente_sin_comentario(cliente, conexion):

	data={"pais":"España",
			"ciudad":"London",
			"ida":"22/06/2019",
			"vuelta":"22/06/2019",
			"hotel":"h",
			"web":"www.google.com",
			"transporte":"t",
			"comentario":"Sin Comentario",
			"archivo_imagen":"miimagen.jpg"}

	cliente.post("/insertar_viaje", data=data)

	viajes=conexion.obtenerViajes()

	id_viaje=viajes[0][0]

	respuesta=cliente.get(f"/detalle_viaje/{id_viaje}")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Detalle del viaje a" in contenido
	assert "London" in contenido
	assert f"/static/imagenes_banderas/GBR.png" in contenido
	assert "Destino" in contenido
	assert "Fecha" in contenido
	assert "Hotel" in contenido
	assert "https://" in contenido
	assert "Transporte" in contenido
	assert "Sin Comentario" not in contenido
	assert "Sin Imagen" in contenido

# Funcion para copiar la imagen de los tests en la carpeta de imagenes
def copiarImagen(ruta:str)->None:

	ruta_origen=os.path.join(os.getcwd(), "testapp", "imagen_tests.jpg")

	ruta_relativa_destino=os.path.join(ruta, "imagen_tests.jpg")

	shutil.copyfile(ruta_origen, ruta_relativa_destino)

# Funcion complementaria para vaciar la carpeta de las imagenes
def vaciarCarpeta(ruta:str)->None:

	if os.path.exists(ruta):

		for archivo in os.listdir(ruta):

			os.remove(os.path.join(ruta, archivo))

def test_pagina_detalle_viaje_existe_con_imagen_existente_sin_comentario(cliente, conexion):

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	ruta_relativa_carpeta=os.path.join(ruta_relativa, "static", "imagenes")

	copiarImagen(ruta_relativa_carpeta)

	data={"pais":"España",
			"ciudad":"London",
			"ida":"22/06/2019",
			"vuelta":"22/06/2019",
			"hotel":"h",
			"web":"www.google.com",
			"transporte":"t",
			"comentario":"Sin Comentario",
			"archivo_imagen":"imagen_tests.jpg"}

	cliente.post("/insertar_viaje", data=data)

	viajes=conexion.obtenerViajes()

	id_viaje=viajes[0][0]

	respuesta=cliente.get(f"/detalle_viaje/{id_viaje}")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Detalle del viaje a" in contenido
	assert "London" in contenido
	assert f"/static/imagenes_banderas/GBR.png" in contenido
	assert "Destino" in contenido
	assert "Fecha" in contenido
	assert "Hotel" in contenido
	assert "https://" in contenido
	assert "Transporte" in contenido
	assert "Sin Comentario" not in contenido
	assert "imagen_tests.jpg" in contenido

	vaciarCarpeta(ruta_relativa_carpeta)

@pytest.mark.parametrize(["web"],
	[("www.fdhgfhgf.com",), ("www.h.com",),("www.jhkfhfgj.com",),("www.github.com",),("www.fbref.com",)]
)
def test_pagina_detalle_viaje_existe_web_invalida(cliente, conexion, web):

	data={"pais":"España",
			"ciudad":"Oranjestad",
			"ida":"22/06/2019",
			"vuelta":"22/06/2019",
			"hotel":"h",
			"web":web,
			"transporte":"t",
			"comentario":"Sin Comentario",
			"archivo_imagen":"Sin Imagen"}

	cliente.post("/insertar_viaje", data=data)

	viajes=conexion.obtenerViajes()

	id_viaje=viajes[0][0]

	respuesta=cliente.get(f"/detalle_viaje/{id_viaje}")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "web-button-invalido" in contenido
	assert web not in contenido

@pytest.mark.parametrize(["web"],
	[("www.google.com",),("www.hotelparquesur.com",)]
)
def test_pagina_detalle_viaje_existe_web_valida(cliente, conexion, web):

	data={"pais":"España",
			"ciudad":"Oranjestad",
			"ida":"22/06/2019",
			"vuelta":"22/06/2019",
			"hotel":"h",
			"web":web,
			"transporte":"t",
			"comentario":"Sin Comentario",
			"archivo_imagen":"Sin Imagen"}

	cliente.post("/insertar_viaje", data=data)

	viajes=conexion.obtenerViajes()

	id_viaje=viajes[0][0]

	respuesta=cliente.get(f"/detalle_viaje/{id_viaje}")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "web-button-valido" in contenido
	assert web in contenido