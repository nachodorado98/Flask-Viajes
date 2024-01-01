from flask import Blueprint, render_template, redirect, url_for

from src.database.conexion import Conexion

from src.utilidades.utils import añadirPuntos

bp_detalle_ciudad=Blueprint("detalle_ciudad", __name__)

@bp_detalle_ciudad.route("/detalle_ciudad/<codigo_ciudad>", methods=["GET"])
def detalle_ciudad(codigo_ciudad):

	conexion=Conexion()

	if not conexion.existe_codigo_ciudad(codigo_ciudad):

		return redirect(url_for("inicio.inicio"))

	ciudad, latitud, longitud, pais, siglas, tipo, poblacion=conexion.obtenerDetalleCiudad(codigo_ciudad)

	conexion.cerrarConexion()

	return render_template("detalle_ciudad.html",
							ciudad=ciudad,
							latitud=latitud,
							longitud=longitud,
							pais=pais,
							siglas=siglas,
							tipo=tipo,
							poblacion=añadirPuntos(poblacion))