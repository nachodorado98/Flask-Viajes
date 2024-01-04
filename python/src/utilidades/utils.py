from datetime import datetime
from typing import Optional
import re
import uuid
import os
from PIL import Image
import requests

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