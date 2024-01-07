import pytest
import shutil
import os

@pytest.mark.parametrize(["id_viaje"],
	[(0,), (10000000,), (-1,), (243544666,)]
)
def test_pagina_editar_viaje_no_existe(cliente, conexion, id_viaje):

	respuesta=cliente.get(f"/editar_viaje/{id_viaje}")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/"
	assert "Redirecting..." in contenido

@pytest.mark.parametrize(["ciudad"],
	[("Madrid",),("Amsterdam",),("London",),("Oranjestad",),("Abu Dhabi",)]
)
def test_pagina_editar_viaje_existe_sin_comentario_sin_imagen(cliente, conexion, ciudad):

	data={"pais":"España",
			"ciudad":ciudad,
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

	respuesta=cliente.get(f"/editar_viaje/{id_viaje}")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Editar viaje a" in contenido
	assert ciudad in contenido
	assert "Destino" in contenido
	assert "Fecha" in contenido
	assert "Hotel" in contenido
	assert "<strong>Comentario:</strong>" not in contenido
	assert "Editar Web" in contenido
	assert "Añadir Comentario" in contenido
	assert "Subir Imagen" in contenido

@pytest.mark.parametrize(["ciudad", "comentario"],
	[
		("Madrid", "Comentario"),
		("Amsterdam", "jkhhvjljkvh"),
		("London", "aaaaaaaaa"),
		("Oranjestad", "Me ha gustado mucho"),
		("Abu Dhabi", "No me gusta esta ciudad")
	]
)
def test_pagina_editar_viaje_existe_con_comentario_sin_imagen(cliente, conexion, ciudad, comentario):

	data={"pais":"España",
			"ciudad":ciudad,
			"ida":"22/06/2019",
			"vuelta":"22/06/2019",
			"hotel":"hotel",
			"web":"www.google.com",
			"transporte":"t",
			"comentario":comentario,
			"archivo_imagen":"Sin Imagen"}

	cliente.post("/insertar_viaje", data=data)

	viajes=conexion.obtenerViajes()

	id_viaje=viajes[0][0]

	respuesta=cliente.get(f"/editar_viaje/{id_viaje}")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Editar viaje a" in contenido
	assert ciudad in contenido
	assert "Destino" in contenido
	assert "Fecha" in contenido
	assert "Hotel" in contenido
	assert "<strong>Comentario:</strong>" in contenido
	assert "Editar Web" in contenido
	assert "Añadir Comentario" not in contenido
	assert "Subir Imagen" in contenido

@pytest.mark.parametrize(["ciudad", "imagen"],
	[
		("Madrid", "miimgaen.jpg"),
		("Amsterdam", "jkhhvjljkvh"),
		("London", "mipdf.pdf"),
		("Oranjestad", "madris_espana_fsdgfdgh.png"),
		("Abu Dhabi", "no_existente.jpg")
	]
)
def test_pagina_editar_viaje_existe_sin_comentario_con_imagen_no_existente(cliente, conexion, ciudad, imagen):

	data={"pais":"España",
			"ciudad":ciudad,
			"ida":"22/06/2019",
			"vuelta":"22/06/2019",
			"hotel":"hotel",
			"web":"www.google.com",
			"transporte":"t",
			"comentario":"Sin Comentario",
			"archivo_imagen":imagen}

	cliente.post("/insertar_viaje", data=data)

	viajes=conexion.obtenerViajes()

	id_viaje=viajes[0][0]

	respuesta=cliente.get(f"/editar_viaje/{id_viaje}")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Editar viaje a" in contenido
	assert ciudad in contenido
	assert "Destino" in contenido
	assert "Fecha" in contenido
	assert "Hotel" in contenido
	assert "<strong>Comentario:</strong>" not in contenido
	assert "Editar Web" in contenido
	assert "Añadir Comentario" in contenido
	assert "Subir Imagen" in contenido


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

@pytest.mark.parametrize(["ciudad"],
	[("Madrid",),("Amsterdam",),("London",),("Oranjestad",),("Abu Dhabi",)]
)
def test_pagina_editar_viaje_existe_sin_comentario_con_imagen_existente(cliente, conexion, ciudad):

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	ruta_relativa_carpeta=os.path.join(ruta_relativa, "static", "imagenes")

	copiarImagen(ruta_relativa_carpeta)

	data={"pais":"España",
			"ciudad":ciudad,
			"ida":"22/06/2019",
			"vuelta":"22/06/2019",
			"hotel":"hotel",
			"web":"www.google.com",
			"transporte":"t",
			"comentario":"Sin Comentario",
			"archivo_imagen":"imagen_tests.jpg"}

	cliente.post("/insertar_viaje", data=data)

	viajes=conexion.obtenerViajes()

	id_viaje=viajes[0][0]

	respuesta=cliente.get(f"/editar_viaje/{id_viaje}")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Editar viaje a" in contenido
	assert ciudad in contenido
	assert "Destino" in contenido
	assert "Fecha" in contenido
	assert "Hotel" in contenido
	assert "<strong>Comentario:</strong>" not in contenido
	assert "Editar Web" in contenido
	assert "Añadir Comentario" in contenido
	assert "Subir Imagen" not in contenido
	assert "imagen_tests.jpg" in contenido

	vaciarCarpeta(ruta_relativa_carpeta)

@pytest.mark.parametrize(["ciudad", "comentario"],
	[
		("Madrid", "Comentario"),
		("Amsterdam", "jkhhvjljkvh"),
		("London", "aaaaaaaaa"),
		("Oranjestad", "Me ha gustado mucho"),
		("Abu Dhabi", "No me gusta esta ciudad")
	]
)
def test_pagina_editar_viaje_existe_con_comentario_con_imagen_existente(cliente, conexion, ciudad, comentario):

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	ruta_relativa_carpeta=os.path.join(ruta_relativa, "static", "imagenes")

	copiarImagen(ruta_relativa_carpeta)

	data={"pais":"España",
			"ciudad":ciudad,
			"ida":"22/06/2019",
			"vuelta":"22/06/2019",
			"hotel":"hotel",
			"web":"www.google.com",
			"transporte":"t",
			"comentario":comentario,
			"archivo_imagen":"imagen_tests.jpg"}

	cliente.post("/insertar_viaje", data=data)

	viajes=conexion.obtenerViajes()

	id_viaje=viajes[0][0]

	respuesta=cliente.get(f"/editar_viaje/{id_viaje}")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Editar viaje a" in contenido
	assert ciudad in contenido
	assert "Destino" in contenido
	assert "Fecha" in contenido
	assert "Hotel" in contenido
	assert "<strong>Comentario:</strong>" in contenido
	assert "Editar Web" in contenido
	assert "Añadir Comentario" not in contenido
	assert "Subir Imagen" not in contenido
	assert "imagen_tests.jpg" in contenido

	vaciarCarpeta(ruta_relativa_carpeta)