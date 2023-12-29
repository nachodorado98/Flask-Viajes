from datetime import datetime
from typing import Optional
import re
import uuid

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