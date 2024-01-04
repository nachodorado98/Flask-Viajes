from flask import Blueprint, render_template, redirect, url_for
import os

from src.database.conexion import Conexion

from src.utilidades.utils import bandera_existe, redimension_imagen_alto, comprobarCuadrada, comprobarHorizontal
from src.utilidades.utils import obtenerNuevasDimensiones, validarPaginaWeb

bp_detalle_viaje=Blueprint("detalle_viaje", __name__)

@bp_detalle_viaje.route("/detalle_viaje/<id_viaje>", methods=["GET"])
def detalle_viaje(id_viaje:int):

	conexion=Conexion()

	if not conexion.existe_id_viaje(id_viaje):

		return redirect(url_for("inicio.inicio"))

	ciudad, pais, siglas, fechas, hotel, web, transporte, comentario, imagen=conexion.obtenerDetalleViaje(id_viaje)

	conexion.cerrarConexion()

	if imagen!="Sin Imagen":

		ruta=os.path.dirname(os.path.join(os.path.dirname(__file__)))

		ruta_carpeta=os.path.join(ruta, "static", "imagenes")

		if imagen in os.listdir(ruta_carpeta):

			ruta_imagen=os.path.join(ruta_carpeta, imagen)

			ancho, alto=obtenerNuevasDimensiones(ruta_imagen)

		else:

			imagen="Sin Imagen"

	return render_template("detalle_viaje.html",
							ciudad=ciudad,
							pais=pais,
							siglas=siglas if bandera_existe(siglas) else "Sin Bandera",
							fechas=fechas,
							hotel=hotel,
							web=web,
							transporte=transporte,
							comentario=comentario,
							imagen=imagen,
							alto=None if imagen=="Sin Imagen" else alto,
							ancho=None if imagen=="Sin Imagen" else ancho,
							accesible=validarPaginaWeb(web))