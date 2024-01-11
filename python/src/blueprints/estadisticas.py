from flask import Blueprint, render_template, redirect, url_for

from src.database.conexion import Conexion

bp_estadisticas=Blueprint("estadisticas", __name__)

@bp_estadisticas.route("/estadisticas", methods=["GET"])
def obtenerEstadisticas():

	conexion=Conexion()

	viajes=conexion.obtenerViajes()

	if viajes is None:

		return redirect(url_for("inicio.inicio"))

	numero_viajes_realizados=conexion.estadistica_viajes_realizados()

	numero_paises_visitados=conexion.estadistica_paises_visitados()

	numero_ciudades_visitadas=conexion.estadistica_ciudades_visitadas()

	numero_dias_ultimo_viaje=conexion.estadistica_dias_ultimo_viaje()

	conexion.cerrarConexion()

	return render_template("estadisticas.html",
							numero_viajes_realizados=numero_viajes_realizados,
							numero_paises_visitados=numero_paises_visitados,
							numero_ciudades_visitadas=numero_ciudades_visitadas,
							numero_dias_ultimo_viaje=numero_dias_ultimo_viaje)