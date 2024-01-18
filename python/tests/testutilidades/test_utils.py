import pytest
import re
import os
import shutil
from datetime import datetime

from src.utilidades.utils import fechas_correctas, web_correcta, comentario_incorrecto, limpiarCadena, crearNombreImagen
from src.utilidades.utils import extraerExtension, generarArchivoImagen, cambiarFormatoFecha, descambiarFormatoFecha
from src.utilidades.utils import crearCarpeta, obtenerAncho, obtenerAlto, redimension_imagen_ancho, redimension_imagen_alto
from src.utilidades.utils import comprobarImagen, añadirPuntos, bandera_existe, es_cuadrada, comprobarCuadrada
from src.utilidades.utils import es_horizontal, comprobarHorizontal, obtenerNuevasDimensiones, validarPaginaWeb
from src.utilidades.utils import obtenerNombreCiudades, obtenerLatLongCiudad, limpiarFechasCiudad, obtenerDatosCiudadViaje
from src.utilidades.utils import leerGeoJSON, crearMapaFolium, eliminarPosiblesMapasFolium, fecha_mes_ano_ano_anterior
from src.utilidades.utils import fechas_limite_grafico, limpiarDatosGrafica, fecha_inicio_minimo_fin_maximo, limpiarDatosGraficaLineas
from src.utilidades.utils import comprobarImagenesExisten, obtenerImagenesExistentesDimensionadas, transportes_nombre_imagenes

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

@pytest.mark.parametrize(["ciudades", "resultado"],
	[
		([("London","dsfsdgdgfd"), ("London","dsfsdgdgfd"), ("London","dsfsdgdgfd"), ("London","dsfsdgdgfd")], 1),
		([("London","dsfsdgdgfd"), ("Paris","dsfsdgdgfd"), ("Madrid","dsfsdgdgfd"), ("London","dsfsdgdgfd")], 3),
		([("London","dsfsdgdgfd"), ("Paris","dsfsdgdgfd"), ("Madrid","dsfsdgdgfd"), ("Porto","dsfsdgdgfd")], 4),
		([],0)
	]
)
def test_obtener_nombre_ciudades_unicas(ciudades, resultado):

	assert len(obtenerNombreCiudades(ciudades))==resultado

@pytest.mark.parametrize(["viajes"],
	[
		([("London","latitud1", "longitud1"), ("London","latitud1", "longitud1"), ("London","latitud1", "longitud1"), ("London","latitud1", "longitud1")],),
		([("London","latitud1", "longitud1"), ("London","latitud1", "longitud1"), ("London","latitud1", "longitud1")],),
		([("London","latitud1", "longitud1"), ("London","latitud1", "longitud1")],),
		([("London","latitud1", "longitud1")],)
	]
)
def test_obtener_latutud_longitud_ciudades_viaje(viajes):

	assert obtenerLatLongCiudad(viajes)==("latitud1", "longitud1")


@pytest.mark.parametrize(["viajes", "brs"],
	[
		([("London","latitud1", "longitud1", "fecha1 London"), ("London","latitud1", "longitud1", "fecha2 London"), ("London","latitud1", "longitud1", "fecha3 London"), ("London", "latitud1", "longitud1", "fecha4 London")], 3),
		([("London","latitud1", "longitud1", "fecha1 London"), ("London","latitud1", "longitud1", "fecha2 London"), ("London","latitud1", "longitud1", "fecha3 London")], 2),
		([("London","latitud1", "longitud1", "fecha1 London"), ("London","latitud1", "longitud1", "fecha2 London")], 1),
		([("London","latitud1", "longitud1", "fecha1 London")], 0)
	]
)
def test_limpiar_fechas_ciudades_viaje(viajes, brs):

	fechas=limpiarFechasCiudad(viajes)

	assert fechas.count("<br>")==brs

@pytest.mark.parametrize(["viajes", "claves"],
	[
		([("London","latitud1", "longitud1", "fecha1 London"), ("London","latitud1", "longitud1", "fecha2 London"), ("London","latitud1", "longitud1", "fecha3 London"), ("London", "latitud1", "longitud1", "fecha4 London")], 1),
		([("London","latitud1", "longitud1", "fecha1 London"), ("Paris","latitud2", "longitud2", "fecha1 Paris"), ("Madrid","latitud3", "longitud3", "fecha1 Madrid"), ("London","latitud1", "longitud1", "fecha2 London")], 3),
		([("London","latitud1", "longitud1", "fecha1 London"), ("Paris","latitud2", "longitud2", "fecha1 Paris"), ("Madrid","latitud3", "longitud3", "fecha1 Madrid"), ("Porto","latitud4", "longitud4", "fecha1 Porto")], 4),
		([],0)
	]
)
def test_obtener_datos_ciudades_viaje(viajes, claves):

	datos=obtenerDatosCiudadViaje(viajes)

	assert len(datos.keys())==claves

def test_leer_geojson_paises_no_existen():

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	assert leerGeoJSON(ruta_relativa, []).empty

@pytest.mark.parametrize(["pais"],
	[("spain",), ("InitedKingdom",), ("Japn",), ("PortuGal",)]
)
def test_leer_geojson_paises_existe_error(pais):

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	assert leerGeoJSON(ruta_relativa, [pais]).empty

@pytest.mark.parametrize(["pais"],
	[("Spain",), ("United Kingdom",), ("Japan",), ("Portugal",)]
)
def test_leer_geojson_paises_existe(pais):

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	geodataframe=leerGeoJSON(ruta_relativa, [pais])

	assert not geodataframe.empty
	assert len(geodataframe)==1

@pytest.mark.parametrize(["paises", "resultado"],
	[
		(["Spain", "United Kingdom", "Japan", "Portugal"], 4),
		(["Spain", "Japan", "Portugal"], 3),
		(["Spain", "United Kingdom"], 2),
		(["Spain", "United Kingdom", "Spain"], 2)
	]
)
def test_leer_geojson_paises_existen(paises, resultado):

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	geodataframe=leerGeoJSON(ruta_relativa, paises)

	assert not geodataframe.empty
	assert len(geodataframe)==resultado

def test_eliminar_posibles_mapas_folium_no_existe():

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	ruta_templates=os.path.join(ruta_relativa, "templates", "templates_mapas")

	archivos_antes=len(os.listdir(ruta_templates))

	eliminarPosiblesMapasFolium(ruta_relativa)

	archivos_despues=len(os.listdir(ruta_templates))

	assert archivos_antes==archivos_despues

#  Funcion complementaria para crear el HTML del geojson
def crearHTML(ruta_html:str)->None:

	contenido="""
			<!DOCTYPE html>
			<html>
			<head>
			    <title>Mi Archivo HTML</title>
			</head>
			<body>
			    <h1>Hola, este es mi archivo HTML creado con Python</h1>
			</body>
			</html>
			"""

	with open(ruta_html, "w") as html:

	    html.write(contenido)

def test_eliminar_posibles_mapa_folium_existe():

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	ruta_templates=os.path.join(ruta_relativa, "templates", "templates_mapas")

	ruta_html=os.path.join(ruta_templates, "geojson_mapa1.html")

	crearHTML(ruta_html)

	archivos_antes=len(os.listdir(ruta_templates))

	eliminarPosiblesMapasFolium(ruta_relativa)

	archivos_despues=len(os.listdir(ruta_templates))

	assert archivos_antes!=archivos_despues
	assert archivos_antes>archivos_despues
	assert archivos_antes-1==archivos_despues

def test_eliminar_posibles_mapa_folium_existen():

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	ruta_templates=os.path.join(ruta_relativa, "templates", "templates_mapas")

	for numero in range(5):

		ruta_html=os.path.join(ruta_templates, f"geojson_mapa{numero}.html")

		crearHTML(ruta_html)

	archivos_antes=len(os.listdir(ruta_templates))

	eliminarPosiblesMapasFolium(ruta_relativa)

	archivos_despues=len(os.listdir(ruta_templates))

	assert archivos_antes!=archivos_despues
	assert archivos_antes>archivos_despues
	assert archivos_antes-5==archivos_despues

@pytest.mark.parametrize(["ciudad", "fechas"],
	[
		("London", "22/06/2019-22/06/2019"),
		("Madrid", "22/06/2019-22/06/2019"),
		("Ciudad", "22/06/2019-22/06/2019<br> 22/06/2019-22/06/2019"),
		("city", "22/06/2019-22/06/2019<br> 22/06/2019-22/06/2019<br> 22/06/2019-22/06/2019")
	]
)
def test_crear_mapa_paises_no_existen_ciudad_existe(ciudad, fechas):

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	eliminarPosiblesMapasFolium(ruta_relativa)

	ruta_templates=os.path.join(ruta_relativa, "templates", "templates_mapas")

	ruta_html=os.path.join(ruta_templates, "geojson_mapa.html")

	assert not os.path.exists(ruta_html)

	crearMapaFolium(ruta_relativa, [], {ciudad:{"latitud":40, "longitud":-3, "fechas":fechas}})

	assert os.path.exists(ruta_html)

	with open(ruta_html, "r") as html:

		contenido=html.read()

		assert "United Kingdom" not in contenido
		assert f"<h1>Viajes a {ciudad}</h1>" in contenido
		assert f"Viaje(s) a {ciudad}" in contenido
		assert f"<h4>Fechas Ida y Vuelta Viaje(s):<br> {fechas}</h4>"

	eliminarPosiblesMapasFolium(ruta_relativa)

@pytest.mark.parametrize(["ciudades", "fechas"],
	[
		(["London", "Madrid"], "22/06/2019-22/06/2019"),
		(["London", "Madrid", "Porto"], "22/06/2019-22/06/2019<br> 22/06/2019-22/06/2019"),
		(["London", "Madrid", "Porto", "Lisboa"], "22/06/2019-22/06/2019<br> 22/06/2019-22/06/2019"),
		(["London", "Madrid", "Porto", "Lisboa", "Paris", "city"], "22/06/2019-22/06/2019<br> 22/06/2019-22/06/2019<br> 22/06/2019-22/06/2019")
	]
)
def test_crear_mapa_paises_no_existen_ciudad_existen(ciudades, fechas):

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	ruta_templates=os.path.join(ruta_relativa, "templates", "templates_mapas")

	ruta_html=os.path.join(ruta_templates, "geojson_mapa.html")

	data_ciudades={ciudad:{"latitud":40+indice, "longitud":-3+indice, "fechas":fechas} for indice, ciudad in enumerate(ciudades)}

	crearMapaFolium(ruta_relativa, [], data_ciudades)

	assert os.path.exists(ruta_html)

	with open(ruta_html, "r") as html:

		contenido=html.read()

		assert "United Kingdom" not in contenido

		for ciudad in ciudades:

			assert f"<h1>Viajes a {ciudad}</h1>" in contenido
			assert f"Viaje(s) a {ciudad}" in contenido
			assert f"<h4>Fechas Ida y Vuelta Viaje(s):<br> {fechas}</h4>"

	eliminarPosiblesMapasFolium(ruta_relativa)

@pytest.mark.parametrize(["pais", "sigla", "ciudades", "fechas"],
	[
		("Spain", "ESP", ["London", "Madrid"], "22/06/2019-22/06/2019"),
		("Germany", "DEU", ["London", "Madrid", "city"], "22/06/2019-22/06/2019"),
		("Portugal", "PRT", ["London", "Madrid"], "22/06/2019-22/06/2019"),
		("United Kingdom", "GBR", ["London", "Madrid", "Paris", "ciudad"], "22/06/2019-22/06/2019")
	]
)
def test_crear_mapa_paises_existe_ciudad_existen(pais, sigla, ciudades, fechas):

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	ruta_templates=os.path.join(ruta_relativa, "templates", "templates_mapas")

	ruta_html=os.path.join(ruta_templates, "geojson_mapa.html")

	data_ciudades={ciudad:{"latitud":40+indice, "longitud":-3+indice, "fechas":fechas} for indice, ciudad in enumerate(ciudades)}

	crearMapaFolium(ruta_relativa, [pais], data_ciudades)

	assert os.path.exists(ruta_html)

	with open(ruta_html, "r") as html:

		contenido=html.read()

		assert pais in contenido
		assert sigla in contenido

		for ciudad in ciudades:

			assert f"<h1>Viajes a {ciudad}</h1>" in contenido
			assert f"Viaje(s) a {ciudad}" in contenido
			assert f"<h4>Fechas Ida y Vuelta Viaje(s):<br> {fechas}</h4>"

	eliminarPosiblesMapasFolium(ruta_relativa)

@pytest.mark.parametrize(["paises", "siglas", "ciudades", "fechas"],
	[
		(["Spain", "Portugal"], ["ESP", "PRT"], ["London", "Madrid"], "22/06/2019-22/06/2019"),
		(["Germany", "United Kingdom"], ["DEU", "GBR"], ["London", "Madrid", "city"], "22/06/2019-22/06/2019"),
		(["Spain", "Portugal", "Germany", "United Kingdom"], ["ESP", "PRT", "DEU", "GBR"], ["London", "Madrid"], "22/06/2019-22/06/2019"),
		(["Spain", "Portugal", "Germany", "United Kingdom", "France"], ["ESP", "PRT", "DEU", "GBR", "FRA"], ["London", "Madrid", "Paris", "ciudad"], "22/06/2019-22/06/2019")
	]
)
def test_crear_mapa_paises_existen_ciudad_existen(paises, siglas, ciudades, fechas):

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	ruta_templates=os.path.join(ruta_relativa, "templates", "templates_mapas")

	ruta_html=os.path.join(ruta_templates, "geojson_mapa.html")

	data_ciudades={ciudad:{"latitud":40+indice, "longitud":-3+indice, "fechas":fechas} for indice, ciudad in enumerate(ciudades)}

	crearMapaFolium(ruta_relativa, paises, data_ciudades)

	assert os.path.exists(ruta_html)

	with open(ruta_html, "r") as html:

		contenido=html.read()

		for pais, sigla in zip(paises, siglas):

			assert pais in contenido
			assert sigla in contenido

		for ciudad in ciudades:

			assert f"<h1>Viajes a {ciudad}</h1>" in contenido
			assert f"Viaje(s) a {ciudad}" in contenido
			assert f"<h4>Fechas Ida y Vuelta Viaje(s):<br> {fechas}</h4>"

	eliminarPosiblesMapasFolium(ruta_relativa)

@pytest.mark.parametrize(["fecha", "fecha_mes_ano", "fecha_mes_ano_anterior"],
	[
		("2019-06-22", "2018-06-01", "2019-06-01"),
		("2020-07-02", "2019-07-01", "2020-07-01"),
		("2024-01-30", "2023-01-01", "2024-01-01"),
		("2022-04-01", "2021-04-01", "2022-04-01"),
	]
)
def test_fechas_mes_ano_ano_anterior(fecha, fecha_mes_ano, fecha_mes_ano_anterior):

	assert fecha_mes_ano_ano_anterior(fecha)==(fecha_mes_ano, fecha_mes_ano_anterior)

def test_fechas_limite_grafico():

	hoy=datetime.now()

	limite_mes_ano=datetime(hoy.year, hoy.month, 1).strftime("%Y-%m-%d")

	limite_mes_ano_anterior=datetime(hoy.year-1, hoy.month, 1).strftime("%Y-%m-%d")

	assert fechas_limite_grafico()==(limite_mes_ano_anterior, limite_mes_ano)

@pytest.mark.parametrize(["datos"],
	[
		([("2022", "January", 0), ("2023", "February", 4), ("2019", "March", 1)],),
		([("2019", "April", 10), ("2019", "May", 3), ("2019", "June", 2)],),
		([("2025", "July", 0), ("2023", "August", 10), ("2024", "September", 30)],),
		([("2021", "October", 4), ("1998", "November", 3), ("1999", "December", 0)],),
		([("2022", "January", 0), ("2023", "February", 4), ("2019", "March", 1), ("2025", "July", 0), ("2023", "August", 10), ("2024", "September", 30)],),
	]
)
def test_limpiar_datos_grafica(datos):

	datos_limpios=limpiarDatosGrafica(datos)

	claves=datos_limpios.keys()

	assert "annos" in claves
	assert "meses" in claves
	assert "viajes_por_mes" in claves

	assert len(datos_limpios["annos"])==len(datos_limpios["meses"])
	assert len(datos_limpios["meses"])==len(datos_limpios["viajes_por_mes"])

@pytest.mark.parametrize(["minimo", "maximo"],
	[(2023, 2023),(2019, 2023),(2021, 2023),(2010, 2023),(2024, 2023)]
)
def test_fecha_inicio_minimo_fin_maximo(minimo, maximo):

	assert fecha_inicio_minimo_fin_maximo(minimo, maximo)==(f"{minimo}-01-01", f"{maximo}-12-01")

@pytest.mark.parametrize(["labels"],
	[
		(["2019"],),
		(["2019", "2024", "2016"],),
		(["2019", "2010", "2021", "2012"],)
	]
)
def test_limpiar_datos_grafica_lineas(labels):

	datos=[]

	for label in labels:

		datos+=[(label, "January", 0), (label, "February", 4), (label, "March", 1),
				(label, "April", 10), (label, "May", 3), (label, "June", 2),
				(label, "July", 0), (label, "August", 10), (label, "September", 30),
				(label, "October", 4), (label, "November", 3), (label, "December", 0)]

	datos_limpios=limpiarDatosGraficaLineas(datos)

	claves=datos_limpios.keys()
	assert "labels" in claves
	assert "datasets" in claves
	assert len(datos_limpios["labels"])==12

	for dataset in datos_limpios["datasets"]:

		assert dataset["label"] in labels
		assert len(dataset["data"])==12

@pytest.mark.parametrize(["imagenes"],
	[
		([('imagen.jpg', 'London', 'Reino Unido'), ('imagen.jpg', 'London', 'Reino Unido')],),
		([],),
		([('imagen.jpg', 'London', 'Reino Unido')],),
		([('imagen.jpg', 'London', 'Reino Unido'), ('imagen1.jpg', 'London', 'Reino Unido'), ('imagen2.jpg', 'London', 'Reino Unido'), ('imagen3.jpg', 'London', 'Reino Unido')],),
	]
)
def test_comprobar_existen_imagenes_no_existen(imagenes):

	assert len(comprobarImagenesExisten(imagenes))==0

# Funcion para copiar la imagen de los tests
def copiarImagenNombre(nombre_imagen:str):

	ruta_imagen=os.path.join(os.getcwd(), "testapp", "imagen_tests.jpg")

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	ruta_relativa_carpeta=os.path.join(ruta_relativa, "static", "imagenes")

	ruta_destino=os.path.join(ruta_relativa_carpeta, f"{nombre_imagen}.jpg")

	shutil.copy(ruta_imagen, ruta_destino)

	assert os.path.exists(ruta_destino)

@pytest.mark.parametrize(["nombre_imagen"],
	[("imagen1",),("imagen2",),("hhjfffh",),("madrid_espana",)]
)		
def test_comprobar_existen_imagenes_existe(nombre_imagen):

	copiarImagenNombre(nombre_imagen)

	imagenes=[(f'{nombre_imagen}.jpg', 'London', 'Reino Unido'), ('imagen.jpg', 'London', 'Reino Unido'), ('imagen.jpg', 'London', 'Reino Unido')]

	assert len(comprobarImagenesExisten(imagenes))==1

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	ruta_relativa_carpeta=os.path.join(ruta_relativa, "static", "imagenes")

	vaciarCarpeta(ruta_relativa_carpeta)

@pytest.mark.parametrize(["numero_imagenes", "resultado"],
	[(5, 5),(10, 10),(2, 2),(22, 22)]
)		
def test_comprobar_existen_imagenes_existen_todas(numero_imagenes, resultado):

	imagenes=[]

	for numero in range(numero_imagenes):

		nombre_imagen=f"imagen{numero}"

		copiarImagenNombre(nombre_imagen)

		imagenes.append((f"{nombre_imagen}.jpg", 'London', 'Reino Unido'))

	assert len(comprobarImagenesExisten(imagenes))==resultado

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	ruta_relativa_carpeta=os.path.join(ruta_relativa, "static", "imagenes")

	vaciarCarpeta(ruta_relativa_carpeta)

@pytest.mark.parametrize(["numero_imagenes", "numero_imagenes_no_existen", "resultado"],
	[(5, 7, 5),(10, 1, 10),(2, 3, 2),(22, 4, 22)]
)		
def test_comprobar_existen_imagenes_existen_algunas(numero_imagenes, numero_imagenes_no_existen, resultado):

	imagenes=[]

	for numero in range(numero_imagenes):

		nombre_imagen=f"imagen{numero}"

		copiarImagenNombre(nombre_imagen)

		imagenes.append((f"{nombre_imagen}.jpg", 'London', 'Reino Unido'))

	for _ in range(numero_imagenes_no_existen):

		imagenes.append(("imagen_no_existe.jpg", 'London', 'Reino Unido'))

	assert len(imagenes)==numero_imagenes+numero_imagenes_no_existen

	assert len(comprobarImagenesExisten(imagenes))==resultado

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	ruta_relativa_carpeta=os.path.join(ruta_relativa, "static", "imagenes")

	vaciarCarpeta(ruta_relativa_carpeta)

def test_obtener_imagenes_existentes_dimensionadas_no_existen():

	assert len(obtenerImagenesExistentesDimensionadas([]))==0

@pytest.mark.parametrize(["numero_imagenes", "resultado"],
	[(5, 5),(10, 10),(2, 2),(22, 22)]
)		
def test_obtener_imagenes_existentes_dimensionadas_existen(numero_imagenes, resultado):

	imagenes=[]

	for numero in range(numero_imagenes):

		nombre_imagen=f"imagen{numero}"

		copiarImagenNombre(nombre_imagen)

		imagenes.append((f"{nombre_imagen}.jpg", 'London', 'Reino Unido'))

	imagenes_dimensionadas=obtenerImagenesExistentesDimensionadas(imagenes)

	assert len(imagenes_dimensionadas)==resultado

	for imagen_dimensionada in imagenes_dimensionadas:

		assert len(imagen_dimensionada)==4

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	ruta_relativa_carpeta=os.path.join(ruta_relativa, "static", "imagenes")

	vaciarCarpeta(ruta_relativa_carpeta)

def test_transporte_nombre_imagenes_no_existen():

	assert transportes_nombre_imagenes([])==[]

@pytest.mark.parametrize(["transportes", "transportes_nuevos", "transportes_antiguos"],
	[
		([("Avion", 1),("La Renfe", 5)], [("Avion.png", 1),("Renfe.png", 5)], []),
		([("Avion", 1),("La Renfe", 5), ("transporte", 22)], [("Avion.png", 1),("Renfe.png", 5)], [("transporte", 22)]),
		([("Avion", 1),("La Renfe", 5), ("transporte", 22), ("Andando", 0)], [("Avion.png", 1),("Renfe.png", 5), ("Pie.png", 0)], [("transporte", 22)]),
		([("Avion", 1),("La Renfe", 5), ("transporte", 22), ("Andando", 0), ("Hola", 13)], [("Avion.png", 1),("Renfe.png", 5), ("Pie.png", 0)], [("transporte", 22), ("Hola", 13)]),
	]
)
def test_transporte_nombre_imagenes_existen(transportes, transportes_nuevos, transportes_antiguos):

	assert len(transportes_nuevos)+len(transportes_antiguos)==len(transportes)

	transportes_imagenes=transportes_nombre_imagenes(transportes)

	assert len(transportes)==len(transportes_imagenes)

	for transporte_nuevo in transportes_nuevos:

		assert transporte_nuevo in transportes_imagenes

	for transporte_antiguo in transportes_antiguos:

		assert transporte_antiguo in transportes_imagenes