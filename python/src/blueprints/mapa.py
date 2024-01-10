from flask import Blueprint, render_template, redirect, url_for, send_file
import os
import uuid

from src.database.conexion import Conexion

from src.utilidades.utils import obtenerDatosCiudadViaje, crearMapaFolium, eliminarPosiblesMapasFolium

bp_mapa=Blueprint("mapa", __name__)

@bp_mapa.route("/mapa", methods=["GET"])
def verMapa():

	conexion=Conexion()

	ciudades_visitadas=conexion.obtenerDatosCiudadesVisitadas()

	if ciudades_visitadas is None:

		return redirect(url_for("inicio.inicio"))

	datos_ciudades_visitadas=obtenerDatosCiudadViaje(ciudades_visitadas)

	paises_visitados=conexion.paises_visitados_ingles()

	conexion.cerrarConexion()

	ruta=os.path.dirname(os.path.join(os.path.dirname(__file__)))

	nombre_mapa=f"geojson_mapa_{uuid.uuid4().hex}.html"

	eliminarPosiblesMapasFolium(ruta)

	crearMapaFolium(ruta, paises_visitados, datos_ciudades_visitadas, nombre_mapa)

	return render_template("mapa.html", nombre_mapa=nombre_mapa)


@bp_mapa.route("/visualizar_mapa/<nombre_mapa>", methods=["GET"])
def visualizarMapa(nombre_mapa:str):

	ruta=os.path.dirname(os.path.join(os.path.dirname(__file__)))

	ruta_mapa=os.path.join(ruta, "templates", "templates_mapas", nombre_mapa)

	return send_file(ruta_mapa)