import pytest
import re

from src.utilidades.utils import fechas_correctas, web_correcta, comentario_incorrecto, limpiarCadena, crearNombreImagen, extraerExtension, generarArchivoImagen

@pytest.mark.parametrize(["ida","vuelta"],
	[
		("2019-6-22", "2019-4-13"),
		("2019-4-13", "2019-4-12"),
		("2023-12-26", "2022-12-26")
	]
)
def test_fechas_incorrectas(ida, vuelta):

	assert not fechas_correctas(ida, vuelta)

@pytest.mark.parametrize(["ida","vuelta"],
	[
		("2019-4-13", "2019-4-13"),
		("2019-4-13", "2019-6-22"),
		("2022-12-26", "2023-12-26")
	]
)
def test_fechas_correctas(ida, vuelta):

	assert fechas_correctas(ida, vuelta)

@pytest.mark.parametrize(["web"],
	[("hola.com",),("adios.es",),("www.hola",),("www.adios.net",),("ww.hola.com",),("www.mal.uk",)]
)
def test_web_incorrecta(web):

	assert not web_correcta(web)

@pytest.mark.parametrize(["web"],
	[("www.hola.com",),("www.adios.es",)]
)
def test_web_correcta(web):

	assert web_correcta(web)

@pytest.mark.parametrize(["comentario"],
	[(None,),("comentario",),("comentariooooooooo",),("www.adios.net",)]
)
def test_comentario_correcto(comentario):

	assert not comentario_incorrecto(comentario)

@pytest.mark.parametrize(["comentario"],
	[
		("comentariooooooooooooooooooooooooooooooooooooooooooooghkhkhjkoooooooooooooooo",),
		("www.adiossssssssssssssssssssddddddddddddddddddddddddddddddgfdhfhfgjgjghdddddddd.net",)
	]
)
def test_comentario_incorrecto(comentario):

	assert comentario_incorrecto(comentario)

@pytest.mark.parametrize(["cadena", "resultado"],
	[
		("hola", "hola"),
		("Adios", "Adios"),
		("hola que tal", "hola_que_tal"),
		("muy-bien", "muy_bien"),
		("me alegro-mucho", "me_alegro_mucho")
	]
)
def test_limpiar_cadena(cadena, resultado):

	assert limpiarCadena(cadena)==resultado


@pytest.mark.parametrize(["ciudad", "pais", "resultado"],
	[
		("Berlin", "Alemania", "berlin_alemania_"),
		("Andorra La Vella", "Andorra", "andorra_la_vella_andorra_"),
		("Ciudad-Guion", "Pais", "ciudad_guion_pais_"),
		("Ciudad-Guion Espacio", "Pais", "ciudad_guion_espacio_pais_"),
	]
)
def test_crear_nombre_imagen(ciudad, pais, resultado):

	assert resultado in crearNombreImagen(ciudad, pais)

@pytest.mark.parametrize(["archivo", "extension"],
	[
		("mipdf.pdf", "pdf"),
		("miimagen.jpeg", "jpeg"),
		("imagen", "jpg"),
		("mitxt.txt", "txt"),
	]
)
def test_extraer_extension(archivo, extension):

	assert extraerExtension(archivo)==extension

@pytest.mark.parametrize(["imagen", "ciudad", "pais", "nombre", "extension"],
	[
		("miimagen.png", "Berlin", "Alemania", "berlin_alemania_", ".png"),
		("miword.docs", "Andorra La Vella", "Andorra", "andorra_la_vella_andorra_", ".docs"),
		("mipdf.pdf", "Ciudad-Guion", "Pais", "ciudad_guion_pais_", ".pdf"),
		("miimagen", "Ciudad-Guion Espacio", "Pais", "ciudad_guion_espacio_pais_", ".jpg"),
	]
)
def test_generar_archivo_imagen(imagen, ciudad, pais, nombre, extension):

	archivo=generarArchivoImagen(imagen, ciudad, pais)

	assert archivo.startswith(nombre)
	assert archivo.endswith(extension)