from flask import Blueprint, render_template, redirect, url_for
import os

from src.database.conexion import Conexion

from src.utilidades.utils import bandera_existe

bp_editar_viaje=Blueprint("editar_viaje", __name__)

@bp_editar_viaje.route("/editar_viaje/<id_viaje>", methods=["GET"])
def editarViaje(id_viaje:int):

	conexion=Conexion()

	if not conexion.existe_id_viaje(id_viaje):

		return redirect(url_for("inicio.inicio"))

	ciudad, pais, siglas, fechas, hotel, web, transporte, comentario, imagen=conexion.obtenerDetalleViaje(id_viaje)

	conexion.cerrarConexion()

	if imagen!="Sin Imagen":

		ruta=os.path.dirname(os.path.join(os.path.dirname(__file__)))

		ruta_carpeta=os.path.join(ruta, "static", "imagenes")

		if imagen not in os.listdir(ruta_carpeta):

			imagen="Sin Imagen"

	return render_template("editar_viaje.html",
							ciudad=ciudad,
							pais=pais,
							siglas=siglas if bandera_existe(siglas) else "Sin Bandera",
							fechas=fechas,
							hotel=hotel,
							web=web,
							transporte=transporte,
							comentario=comentario,
							imagen=imagen,
							id_viaje=id_viaje)

@bp_editar_viaje.route("/actualizar_viaje/<id_viaje>", methods=["POST"])
def actualizarViaje(id_viaje:int):

	conexion=Conexion()

	if not conexion.existe_id_viaje(id_viaje):

		return redirect(url_for("inicio.inicio"))

	return str(id_viaje)