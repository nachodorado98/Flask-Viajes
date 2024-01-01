from flask import Blueprint, render_template, redirect, url_for

from src.database.conexion import Conexion

from src.utilidades.utils import añadirPuntos, bandera_existe

bp_detalle_pais=Blueprint("detalle_pais", __name__)

@bp_detalle_pais.route("/detalle_pais/<nombre_pais>", methods=["GET"])
def detalle_pais(nombre_pais:str):

	conexion=Conexion()

	if not conexion.existe_pais(nombre_pais):

		return redirect(url_for("inicio.inicio"))

	capital, siglas, codigo_ciudad, poblacion, ciudades=conexion.informacion_pais(nombre_pais)

	conexion.cerrarConexion()

	return render_template("detalle_pais.html",
							pais=nombre_pais,
							capital=capital,
							siglas=siglas if bandera_existe(siglas) else "Sin Bandera",
							codigo_ciudad=codigo_ciudad,
							poblacion=añadirPuntos(str(poblacion)),
							ciudades=añadirPuntos(str(ciudades)))