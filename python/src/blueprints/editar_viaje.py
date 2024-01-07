from flask import Blueprint, render_template, redirect, url_for, request
import os

from src.database.conexion import Conexion

from src.utilidades.utils import bandera_existe, web_correcta, comentario_incorrecto, generarArchivoImagen

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

	web=request.form.get("web")
	comentario=request.form.get("comentario")
	imagen=request.form.get("imagen")
	ciudad=request.form.get("ciudad")
	pais=request.form.get("pais")

	if comentario!="Sin Comentario":

		if comentario_incorrecto(comentario):

			return redirect(url_for("editar_viaje.editarViaje", id_viaje=id_viaje))

	comentario_limpio="Sin Comentario" if comentario=="" or comentario is None else comentario

	if not web_correcta(web):

		return redirect(url_for("editar_viaje.editarViaje", id_viaje=id_viaje))

	if imagen is not None:

		conexion.actualizarWebComentario(id_viaje, web, comentario_limpio)

		return redirect(url_for("detalle_viaje.detalle_viaje", id_viaje=id_viaje))

	if "imagen" in request.files:

		imagen=request.files["imagen"]

		if imagen.filename!="":

			archivo_imagen=generarArchivoImagen(imagen.filename, ciudad, pais) 

			ruta=os.path.dirname(os.path.join(os.path.dirname(__file__)))

			ruta_carpeta=os.path.join(ruta, "static", "imagenes")

			ruta_imagen=os.path.join(ruta_carpeta, archivo_imagen)

			imagen.save(ruta_imagen)

			conexion.actualizarWebComentarioImagen(id_viaje, web, comentario_limpio, archivo_imagen)

		else:

			conexion.actualizarWebComentarioImagen(id_viaje, web, comentario_limpio, "Sin Imagen")

	else:

		conexion.actualizarWebComentario(id_viaje, web, comentario_limpio)
			
	conexion.cerrarConexion()

	return redirect(url_for("detalle_viaje.detalle_viaje", id_viaje=id_viaje))