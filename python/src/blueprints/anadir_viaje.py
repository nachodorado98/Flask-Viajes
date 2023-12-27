from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from datetime import datetime

from src.database.conexion import Conexion

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

	# Funcion para saber si las fechas son correctas
	def fechas_correctas(ida:str, vuelta:str)->bool:

		return False if datetime.strptime(ida, "%Y-%m-%d")>datetime.strptime(vuelta, "%Y-%m-%d") else True

	# Funcion para saber si la pagina web es correcta
	def web_correcta(web:str)->bool:

		return True if web.startswith("www.") and web.endswith((".com", ".es")) else False

	if not fechas_correctas(ida, vuelta) or not web_correcta(web):

		return redirect(url_for("anadir_viaje.anadirViaje"))

	if comentario is not None and len(comentario)>50:

		return redirect(url_for("anadir_viaje.anadirViaje"))

	return render_template("resumen_viaje.html", pais=pais, ciudad=ciudad, ida=ida, vuelta=vuelta, hotel=hotel, web=web, transporte=transporte, comentario=comentario)