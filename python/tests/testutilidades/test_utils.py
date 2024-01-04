import pytest
import re
import os
import shutil

from src.utilidades.utils import fechas_correctas, web_correcta, comentario_incorrecto, limpiarCadena, crearNombreImagen
from src.utilidades.utils import extraerExtension, generarArchivoImagen, cambiarFormatoFecha, descambiarFormatoFecha
from src.utilidades.utils import crearCarpeta, obtenerAncho, obtenerAlto, redimension_imagen_ancho, redimension_imagen_alto
from src.utilidades.utils import comprobarImagen, añadirPuntos, bandera_existe, es_cuadrada, comprobarCuadrada
from src.utilidades.utils import es_horizontal, comprobarHorizontal, obtenerNuevasDimensiones, validarPaginaWeb

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

@pytest.mark.parametrize(["fecha", "fecha_cambiada"],
	[
		("2022-06-22", "22/06/2022"),
		("2019-11-22", "22/11/2019")
	]
)
def test_cambiar_formato_fecha(fecha, fecha_cambiada):

	assert cambiarFormatoFecha(fecha)==fecha_cambiada

@pytest.mark.parametrize(["fecha", "fecha_descambiada"],
	[
		("22/06/2022", "2022-06-22"),
		("22/11/2019", "2019-11-22")
	]
)
def test_descambiar_formato_fecha(fecha, fecha_descambiada):

	assert descambiarFormatoFecha(fecha)==fecha_descambiada


def borrarCarpeta(ruta):

	if os.path.exists(ruta):

		os.rmdir(ruta)

def test_crear_carpeta_no_existe():

	ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

	assert not os.path.exists(ruta_carpeta)

	crearCarpeta(ruta_carpeta)

	assert os.path.exists(ruta_carpeta)

def test_crear_carpeta_existe():

	ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

	assert os.path.exists(ruta_carpeta)

	crearCarpeta(ruta_carpeta)

	assert os.path.exists(ruta_carpeta)

	borrarCarpeta(ruta_carpeta)

@pytest.mark.parametrize(["altura", "ancho", "resultado"],
	[
		(220, 50, 26),
		(500, 300, 69),
		(145, 200, 158),
		(20.56, 2.5, 13)
	]
)
def test_obtener_ancho(altura, ancho, resultado):

	assert obtenerAncho(altura, ancho)==resultado

def test_redimension_imagen():

	ruta_imagen=os.path.join(os.getcwd(), "testapp", "imagen_tests.jpg")

	ancho=redimension_imagen_ancho(ruta_imagen)

	assert isinstance(ancho, int)

@pytest.mark.parametrize(["altura", "ancho", "resultado"],
	[
		(220, 50, 1320),
		(500, 300, 500),
		(145, 200, 217),
		(20.56, 2.5, 2467)
	]
)
def test_obtener_alto(altura, ancho, resultado):

	assert obtenerAlto(altura, ancho)==resultado

def test_redimension_imagen_alto():

	ruta_imagen=os.path.join(os.getcwd(), "testapp", "imagen_tests.jpg")

	alto=redimension_imagen_alto(ruta_imagen)

	assert isinstance(alto, int)

@pytest.mark.parametrize(["archivo_imagen"],
	[("imagen",), ("Sin Imagen",), ("imagen.jpg",), ("london_uk_",), ("mipdf.pdf",)]
)
def test_comprobar_imagen_no_valida(archivo_imagen):

	assert not comprobarImagen(archivo_imagen)


# Funcion complementaria para vaciar la carpeta de las imagenes
def vaciarCarpeta(ruta:str)->None:

	if os.path.exists(ruta):

		for archivo in os.listdir(ruta):

			os.remove(os.path.join(ruta, archivo))

# Funcion para copiar la imagen de los tests
def copiarImagen():

	ruta_imagen=os.path.join(os.getcwd(), "testapp", "imagen_tests.jpg")

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	ruta_relativa_carpeta=os.path.join(ruta_relativa, "static", "imagenes")

	ruta_destino=os.path.join(ruta_relativa_carpeta, "imagen_tests.jpg")

	shutil.copy(ruta_imagen, ruta_destino)

	assert os.path.exists(ruta_destino)

def test_comprobar_imagen_valida():

	copiarImagen()	

	assert comprobarImagen("imagen_tests.jpg")

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	ruta_relativa_carpeta=os.path.join(ruta_relativa, "static", "imagenes")

	vaciarCarpeta(ruta_relativa_carpeta)

@pytest.mark.parametrize(["numero", "numero_puntos"],
	[
		("100", "100"),
		("1234", "1.234"),
		("987654", "987.654"),
		("1", "1"),
		("1000000", "1.000.000")
	]
)
def test_añadir_puntos(numero, numero_puntos):

	assert añadirPuntos(numero)==numero_puntos

@pytest.mark.parametrize(["siglas"],
	[("avs",), ("epñ",), ("sig",), ("hgjhg",), ("siglas",)]
)
def test_bandera_no_existe(siglas):

	assert not bandera_existe(siglas)

@pytest.mark.parametrize(["siglas"],
	[("esp",), ("USA",), ("URY",), ("and",), ("PRT",)]
)
def test_bandera_existe(siglas):

	assert bandera_existe(siglas)

@pytest.mark.parametrize(["altura", "ancho", "resultado"],
	[
		(220, 50, False),
		(500, 300, False),
		(200, 200, True),
		(20.56, 2.5, False)
	]
)
def test_es_cuadrada(altura, ancho, resultado):

	assert es_cuadrada(ancho, altura)==resultado

@pytest.mark.parametrize(["imagen", "resultado"],
	[
		("imagen_tests_horizontal.jpg", False),
		("imagen_tests_cuadrada.jpg", True),
		("imagen_tests_vertical.jpg", False)
	]
)
def test_comprobar_cuadrada(imagen, resultado):

	ruta_imagen=os.path.join(os.getcwd(), "testutilidades", "imagenes_formato", imagen)

	assert comprobarCuadrada(ruta_imagen)==resultado

@pytest.mark.parametrize(["altura", "ancho", "resultado"],
	[
		(220, 50, False),
		(500, 600, True),
		(200, 200, False),
		(20.56, 2.5, False)
	]
)
def test_es_horizontal(altura, ancho, resultado):

	assert es_horizontal(ancho, altura)==resultado

@pytest.mark.parametrize(["imagen", "resultado"],
	[
		("imagen_tests_horizontal.jpg", True),
		("imagen_tests_cuadrada.jpg", False),
		("imagen_tests_vertical.jpg", False)
	]
)
def test_comprobar_horizontal(imagen, resultado):

	ruta_imagen=os.path.join(os.getcwd(), "testutilidades", "imagenes_formato", imagen)

	assert comprobarHorizontal(ruta_imagen)==resultado

@pytest.mark.parametrize(["imagen", "resultado"],
	[
		("imagen_tests_horizontal.jpg", 500),
		("imagen_tests_cuadrada.jpg", 400),
		("imagen_tests_vertical.jpg", 300)
	]
)
def test_obtener_nuevas_dimensiones(imagen, resultado):

	ruta_imagen=os.path.join(os.getcwd(), "testutilidades", "imagenes_formato", imagen)

	ancho, alto=obtenerNuevasDimensiones(ruta_imagen)

	assert ancho==resultado

@pytest.mark.parametrize(["web", "resultado"],
	[
		("www.google.com", True),
		("https://www.google.com", True),
		("www.fgfhfghfg.com", False),
		("https://www.jhkfhfgj.com", False),
		("https://www.github.com", False),
		("https://fbref.com/en/comps/12/schedule/La-Liga-Scores-and-Fixtures", True)
	]
)
def test_validar_pagina_web(web, resultado):

	assert validarPaginaWeb(web)==resultado