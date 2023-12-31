from flask import Blueprint, render_template, request, jsonify, redirect, url_for
import os

from src.database.conexion import Conexion

from src.utilidades.utils import fechas_correctas, web_correcta, comentario_incorrecto, crearNombreImagen, extraerExtension
from src.utilidades.utils import generarArchivoImagen, cambiarFormatoFecha, descambiarFormatoFecha, redimension_imagen, comprobarImagen


bp_anadir_viaje=Blueprint("anadir_viaje", __name__)

@bp_anadir_viaje.route("/anadir_viaje", methods=["GET"])
def anadirViaje():

	conexion=Conexion()

	paises=conexion.paises_existentes()

	conexion.cerrarConexion()

	return render_template("anadir.html", paises=paises)

@bp_anadir_viaje.route("/ciudades_pais")
def obtenerCiudades():

	pais=request.args.get("pais")

	conexion=Conexion()

	ciudades=conexion.ciudades_existentes(pais, 10000)

	conexion.cerrarConexion()

	return jsonify(ciudades)


@bp_anadir_viaje.route("/comprobar_viaje", methods=["POST"])
def comprobarViaje():

	pais=request.form.get("pais")
	ciudad=request.form.get("ciudad")
	ida=request.form.get("fecha-ida")
	vuelta=request.form.get("fecha-vuelta")
	hotel=request.form.get("nombre-hotel")
	web=request.form.get("pagina-web-hotel")
	transporte=request.form.get("transporte")
	comentario=request.form.get("comentario")

	if not fechas_correctas(ida, vuelta) or not web_correcta(web):

		return redirect(url_for("anadir_viaje.anadirViaje"))

	if comentario_incorrecto(comentario):

		return redirect(url_for("anadir_viaje.anadirViaje"))

	comentario_limpio="Sin Comentario" if comentario=="" or comentario is None else comentario

	ruta=os.path.dirname(os.path.join(os.path.dirname(__file__)))

	ruta_carpeta=os.path.join(ruta, "static", "imagenes")

	if "imagen" in request.files:

		imagen=request.files["imagen"]

		if imagen.filename!="":

			archivo_imagen=generarArchivoImagen(imagen.filename, ciudad, pais)

			ruta_imagen=os.path.join(ruta_carpeta, archivo_imagen)

			imagen.save(ruta_imagen)

			ancho=redimension_imagen(ruta_imagen)

		else:

			archivo_imagen="Sin Imagen"

	else:

		archivo_imagen="Sin Imagen"

	return render_template("resumen_viaje.html",
							pais=pais,
							ciudad=ciudad,
							ida=cambiarFormatoFecha(ida),
							vuelta=cambiarFormatoFecha(vuelta),
							hotel=hotel,
							web=web,
							transporte=transporte,
							comentario=comentario_limpio,
							archivo_imagen=archivo_imagen,
							ancho=None if archivo_imagen=="Sin Imagen" else ancho)

@bp_anadir_viaje.route("/insertar_viaje", methods=["POST"])
def insertarViaje():

	pais=request.form.get("pais")
	ciudad=request.form.get("ciudad")
	ida=request.form.get("ida")
	vuelta=request.form.get("vuelta")
	hotel=request.form.get("hotel")
	web=request.form.get("web")
	transporte=request.form.get("transporte")
	comentario=request.form.get("comentario")
	archivo_imagen=request.form.get("archivo_imagen")

	conexion=Conexion()

	codigo_ciudad=conexion.obtenerCodCiudad(ciudad)

	if codigo_ciudad is None:

		print(ciudad)

		return redirect(url_for("anadir_viaje.anadirViaje"))

	comentario_limpio="Sin Comentario" if comentario is None else comentario

	archivo_imagen_limpio="Sin Imagen" if archivo_imagen is None else archivo_imagen

	conexion.insertarViaje(codigo_ciudad,
							descambiarFormatoFecha(ida),
							descambiarFormatoFecha(vuelta),
							hotel,
							web,
							transporte,
							comentario_limpio,
							archivo_imagen_limpio)

	conexion.cerrarConexion()

	return redirect(url_for("inicio.inicio"))

@bp_anadir_viaje.route("/cancelar_viaje/<archivo_imagen>", methods=["GET"])
def cancelarViaje(archivo_imagen:str):

	if not comprobarImagen(archivo_imagen):

		return redirect(url_for("inicio.inicio"))

	ruta=os.path.dirname(os.path.join(os.path.dirname(__file__)))

	ruta_carpeta=os.path.join(ruta, "static", "imagenes")

	os.remove(os.path.join(ruta_carpeta, archivo_imagen))

	return redirect(url_for("inicio.inicio"))
