from flask import Blueprint, render_template, redirect, url_for

from src.database.conexion import Conexion

from src.utilidades.utils import añadirPuntos

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

	viaje_mas_largo=conexion.estadistica_viaje_mas_largo()

	viajes, anno=conexion.estadistica_anno_mas_viajes()

	viajes_ciudad, ciudad, pais_ciudad=conexion.estadistica_ciudad_mas_viajes()

	viajes_pais, pais=conexion.estadistica_pais_mas_viajes()

	poblacion, ciudad_mas_grande, pais_ciudad_mas_grande=conexion.estadistica_ciudad_mas_grande()

	distancia, ciudad_mas_lejana, pais_ciudad_mas_lejana=conexion.estadistica_ciudad_mas_lejana()

	conexion.cerrarConexion()

	return render_template("estadisticas.html",
							numero_viajes_realizados=numero_viajes_realizados,
							numero_paises_visitados=numero_paises_visitados,
							numero_ciudades_visitadas=numero_ciudades_visitadas,
							numero_dias_ultimo_viaje=numero_dias_ultimo_viaje,
							viaje_mas_largo=viaje_mas_largo,
							viajes=viajes,
							anno=anno,
							viajes_ciudad=viajes_ciudad,
							ciudad=ciudad,
							pais_ciudad=pais_ciudad,
							viajes_pais=viajes_pais,
							pais=pais,
							poblacion=añadirPuntos(str(poblacion)),
							ciudad_mas_grande=ciudad_mas_grande,
							distancia=añadirPuntos(str(distancia)),
							ciudad_mas_lejana=ciudad_mas_lejana)