from flask import Blueprint, render_template, redirect, url_for
import os
import uuid

from src.database.conexion import Conexion

from src.utilidades.utils import obtenerDatosCiudadViaje, crearMapaFolium, eliminarPosiblesMapasFolium

bp_mapa=Blueprint("mapa", __name__)

@bp_mapa.route("/mapa", methods=["GET"])
def verMapa():

	ruta=os.path.dirname(os.path.join(os.path.dirname(__file__)))

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

	return render_template(nombre_mapa)