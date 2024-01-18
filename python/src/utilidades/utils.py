from datetime import datetime
from typing import Optional, List, Dict
import re
import uuid
import os
from PIL import Image
import requests
import geopandas as gpd
import folium

# Funcion para saber si las fechas son correctas
def fechas_correctas(ida:str, vuelta:str)->bool:

	return False if datetime.strptime(ida, "%Y-%m-%d")>datetime.strptime(vuelta, "%Y-%m-%d") else True

# Funcion para saber si la pagina web es correcta
def web_correcta(web:str)->bool:

	return True if web.startswith("www.") and web.endswith((".com", ".es")) else False

# Funcion para saber si el comentario es correcto:
def comentario_incorrecto(comentario:str)->bool:

	return True if comentario is not None and len(comentario)>50 else False

# Funcion para limpiar la cadena
def limpiarCadena(cadena:str)->str:

	cadena_dividida=re.split(r"\s+|-", cadena)

	return "_".join(cadena_dividida)

# Funcion para crear el nombre de la imagen
def crearNombreImagen(ciudad:str, pais:str)->str:

	id_unico=str(uuid.uuid4())

	ciudad_limpia=limpiarCadena(ciudad.lower())

	pais_limpio=limpiarCadena(pais.lower())

	return f"{ciudad_limpia}_{pais_limpio}_{id_unico}"

# Funcion para extraer la extension de un archivo
def extraerExtension(archivo:str, extension_alternativa:str="jpg")->str:

	return archivo.rsplit(".", 1)[1].lower() if "." in archivo else extension_alternativa

# Funcion para generar el archivo de la imagen completo
def generarArchivoImagen(nombre:str, ciudad:str, pais:str)->str:

	extension=extraerExtension(nombre)

	nombre_imagen=crearNombreImagen(ciudad, pais)

	return f"{nombre_imagen}.{extension}"

# Funcion para cambiar el formato de una fecha
def cambiarFormatoFecha(fecha:str)->str:

	fecha_datetime=datetime.strptime(fecha, "%Y-%m-%d")

	return fecha_datetime.strftime("%d/%m/%Y")

# Funcion para descambiar el formato de una fecha
def descambiarFormatoFecha(fecha:str)->str:

	fecha_datetime=datetime.strptime(fecha, "%d/%m/%Y")

	return fecha_datetime.strftime("%Y-%m-%d")

# Funcion para crear una carpeta si no existe 
def crearCarpeta(ruta_carpeta:str)->None:

	if not os.path.exists(ruta_carpeta):

		os.mkdir(ruta_carpeta)

		print("Creando carpeta...")

# Funcion para obtener el ancho que debe tener la imagen
def obtenerAncho(altura_actual:float, ancho_actual:float, altura:float=115)->int:

	return int((altura/altura_actual)*ancho_actual)

# Funcion para obtener el alto que debe tener la imagen
def obtenerAlto(altura_actual:float, ancho_actual:float, anchura:float=300)->int:

	return int((anchura/ancho_actual)*altura_actual)

# Funcion para obtener el valor de la redimension del ancho de la imagen
def redimension_imagen_ancho(ruta_imagen:str, altura:float=115)->int:

	with Image.open(ruta_imagen) as imagen_pil:

		ancho_original, alto_original=imagen_pil.size

	return obtenerAncho(alto_original, ancho_original, altura)

# Funcion para obtener el valor de la redimension del alto de la imagen
def redimension_imagen_alto(ruta_imagen:str, anchura:float=300)->int:

	with Image.open(ruta_imagen) as imagen_pil:

		ancho_original, alto_original=imagen_pil.size

	return obtenerAlto(alto_original, ancho_original, anchura)

# Funcion para comprobar si la imagen es valida
def comprobarImagen(archivo_imagen:str)->bool:

	ruta=os.path.dirname(os.path.join(os.path.dirname(__file__)))

	ruta_imagen=os.path.join(ruta, "static", "imagenes", archivo_imagen)

	return True if archivo_imagen!="Sin Imagen" and os.path.exists(ruta_imagen) else False

# Funcion para poner los puntos de los miles, millones, etc
def añadirPuntos(numero:str)->str:

	numero_con_puntos=""

	for indice, digito in enumerate(numero[::-1], 1):

		numero_con_puntos+=digito

		if indice%3==0 and indice!=len(numero[::-1]):

			numero_con_puntos+="."

	return numero_con_puntos[::-1]

# Funcion para saber si una bandera existe
def bandera_existe(siglas:str)->bool:

	ruta=os.path.dirname(os.path.join(os.path.dirname(__file__)))

	ruta_imagen=os.path.join(ruta, "static", "imagenes_banderas", f"{siglas.upper()}.png")

	return True if os.path.exists(ruta_imagen) else False

# Funcion para saber si una imagen es cuadrada
def es_cuadrada(ancho:int, alto:int)->bool:

	return True if ancho==alto else False

# Funcion para comprobar si la imagen es cuadrada
def comprobarCuadrada(ruta_imagen:str)->bool:

	with Image.open(ruta_imagen) as imagen_pil:

		ancho, alto=imagen_pil.size

	return es_cuadrada(ancho, alto)

# Funcion para saber si una imagen es horizontal
def es_horizontal(ancho:int, alto:int)->bool:

	return True if ancho>alto else False

# Funcion para comprobar si la imagen es horizontal
def comprobarHorizontal(ruta_imagen:str)->bool:

	with Image.open(ruta_imagen) as imagen_pil:

		ancho, alto=imagen_pil.size

	return es_horizontal(ancho, alto)

# Funcion para obtener las nuevas dimensiones (alto, ancho) de la imagen segun sea cuadrada, horizontal o vertical
def obtenerNuevasDimensiones(ruta_imagen:str)->tuple:

	if not comprobarCuadrada(ruta_imagen):

		ancho=500 if comprobarHorizontal(ruta_imagen) else 300

	else:

		ancho=400

	alto=redimension_imagen_alto(ruta_imagen, ancho)
	
	return ancho, alto

# Funcion para obtener que una pagina web es accesible
def validarPaginaWeb(web:str)->bool:

	url=web if web.startswith("https://") else f"https://{web}"

	try:

		respuesta=requests.head(url)

		return True if respuesta.status_code==200 else False

	except requests.ConnectionError:

		return False

# Funcion para obtener el nombre de las ciudades de manera unica (sin duplicados) por viaje
def obtenerNombreCiudades(ciudades:List[tuple])->List[str]:

	return list(set([ciudad[0]for ciudad in ciudades]))

# Funcion para obtener los datos (latutud y longitud) del viaje de una ciudad concreta
def obtenerLatLongCiudad(viajes:List[tuple])->tuple:

	return tuple(set([(viaje[1], viaje[2]) for viaje in viajes]))[0]

# Funcion para limpiar las fechas de los viajes a una ciudad
def limpiarFechasCiudad(viajes:List[tuple])->str:

	fechas=[viaje[3] for viaje in viajes]

	return "<br> ".join(fechas)

# Funcion para obtener los datos de las ciudades en los viajes correspondientes
def obtenerDatosCiudadViaje(viajes:List[tuple])->Dict:

	diccionario_ciudades={}

	ciudades_unicas=obtenerNombreCiudades(viajes)

	for ciudad in ciudades_unicas:

		datos_ciudad=list(filter(lambda viaje: viaje[0]==ciudad, viajes))

		latitud, longitud=obtenerLatLongCiudad(datos_ciudad)

		fechas=limpiarFechasCiudad(datos_ciudad)

		diccionario_ciudades[ciudad]={"latitud":latitud, "longitud":longitud, "fechas":fechas}

	return diccionario_ciudades

# Funcion para leer el archivo geojson
def leerGeoJSON(ruta:str, paises:List[str])->gpd.geodataframe.GeoDataFrame:

	ruta_carpeta=os.path.join(ruta, "static", "geojson")

	archivo_geojson=os.path.join(ruta_carpeta, "gis.json")

	geodataframe=gpd.read_file(archivo_geojson)

	geodataframe_paises=geodataframe[geodataframe["name"].isin(paises)]

	return geodataframe_paises

# Funcion para crear el mapa con folium y guardarlo en un html
def crearMapaFolium(ruta:str, paises:List[str], datos_ciudades:Dict, nombre_html:str="geojson_mapa.html")->None:

	geodataframe=leerGeoJSON(ruta, paises)

	mapa=folium.Map(location=[51, 22], zoom_start=3)
	 
	folium.GeoJson(geodataframe, name="viajes").add_to(mapa)

	for ciudad, datos_ciudad in datos_ciudades.items():

		folium.Marker([datos_ciudad["latitud"], datos_ciudad["longitud"]],
				tooltip=f"Viaje(s) a {ciudad}",
				popup=folium.Popup(f"<h1>Viajes a {ciudad}</h1><h4>Fechas Ida y Vuelta Viaje(s):<br>{datos_ciudad['fechas']}</h4>",max_width=500)).add_to(mapa)

	ruta_templates=os.path.join(ruta, "templates", "templates_mapas")

	ruta_archivo_html=os.path.join(ruta_templates, nombre_html)

	mapa.save(ruta_archivo_html)
	
# Funcion para eliminar los posibles mapas (archivos html) si existen
def eliminarPosiblesMapasFolium(ruta:str)->None:

	ruta_templates=os.path.join(ruta, "templates", "templates_mapas")

	posibles_mapas=[archivo for archivo in os.listdir(ruta_templates) if archivo.startswith("geojson_mapa")]

	for mapa in posibles_mapas:

		os.remove(os.path.join(ruta_templates, mapa))

# Funcion para obtener la fecha del mes y la fecha un año antes
def fecha_mes_ano_ano_anterior(fecha:str)->tuple[str]:

	fecha_datetime=datetime.strptime(fecha, "%Y-%m-%d")

	anno, mes=fecha_datetime.year, fecha_datetime.month

	fecha_mes_ano=datetime(anno, mes, 1)

	fecha_mes_ano_anterior=datetime(anno-1, mes, 1)

	return fecha_mes_ano_anterior.strftime("%Y-%m-%d"), fecha_mes_ano.strftime("%Y-%m-%d")

# Funcion para obtener las fechas limite de inicio y fin del grafico
def fechas_limite_grafico()->tuple[str]:

	hoy=datetime.now().strftime("%Y-%m-%d")

	return fecha_mes_ano_ano_anterior(hoy)

# Funcion para limpiar los datos que se muestran en la grafica
def limpiarDatosGrafica(datos:List[tuple])->Dict:

	meses_espanol={"January":"Enero",
					"February":"Febrero",
					"March":"Marzo",
					"April":"Abril",
					"May":"Mayo",
					"June":"Junio",
					"July":"Julio",
					"August":"Agosto",
					"September":"Septiembre",
					"October":"Octubre",
					"November":"Noviembre",
					"December":"Diciembre"}

	annos, meses, viajes=zip(*((dato[0], meses_espanol[dato[1]], dato[2]) for dato in datos))

	return {"annos": list(annos), "meses": list(meses), "viajes_por_mes": list(viajes)}

# Funcion para obtener la fecha de inicio del año minimo y la fecha de fin del año maximo
def fecha_inicio_minimo_fin_maximo(minimo:int, maximo:int)->tuple[str]:

	fecha_inicio_minimo=datetime(minimo, 1, 1)

	fecha_fin_maximo=datetime(maximo, 12, 1)

	return fecha_inicio_minimo.strftime("%Y-%m-%d"), fecha_fin_maximo.strftime("%Y-%m-%d")

# Funcion para limpiar los datos que se muestran en la grafica de lienas
def limpiarDatosGraficaLineas(datos:List[tuple])->Dict:

	annos=sorted(list(set([dato[0] for dato in datos])))

	datos_anno_viajes={anno:[dato[2] for dato in datos if dato[0]==anno] for anno in annos}

	datasets=[{"label":anno_clave, "data":datos_viajes} for anno_clave, datos_viajes in datos_anno_viajes.items()]

	datos_lineas={"labels":['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio',
							'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
					"datasets":datasets}

	return datos_lineas

# Funcion para comprobar que las imagenes existen
def comprobarImagenesExisten(imagenes:List[tuple])->List[Optional[tuple]]:

	ruta=os.path.dirname(os.path.join(os.path.dirname(__file__)))

	ruta_carpeta_imagenes=os.path.join(ruta, "static", "imagenes")

	return list(filter(lambda imagen: os.path.exists(os.path.join(ruta_carpeta_imagenes, imagen[0])), imagenes))

# Funcion para obtener las imagenes que existen con la dimension de altura que deben tener
def obtenerImagenesExistentesDimensionadas(imagenes_existen:List[Optional[tuple]], alto:int=200)->List[Optional[tuple]]:

	ruta=os.path.dirname(os.path.join(os.path.dirname(__file__)))

	ruta_carpeta=os.path.join(ruta, "static", "imagenes")

	return [(nombre_imagen, ciudad, pais, redimension_imagen_alto(os.path.join(ruta_carpeta, nombre_imagen), alto)) for nombre_imagen, ciudad, pais in imagenes_existen]

# Funcion para obtener los nombres de las imagenes de los transportes
def transportes_nombre_imagenes(transportes:List[tuple])->List[tuple]:

	diccionario_transportes={"Avion":"Avion",
							"Autobus":"Autobus",
							"Autobus EMT":"AutobusEMT",
							"Autobus verde":"AutobusVerde",
							"Tren/AVE":"Tren",
							"La Renfe":"Renfe",
							"Andando":"Pie",
							"Coche":"Coche"}

	return [(transporte, viajes) if diccionario_transportes.get(transporte) is None else (f"{diccionario_transportes.get(transporte)}.png", viajes) for transporte, viajes in transportes]