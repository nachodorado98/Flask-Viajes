from flask import Blueprint, render_template, redirect, url_for

from src.database.conexion import Conexion

bp_ciudades_pais=Blueprint("ciudades_pais", __name__)

@bp_ciudades_pais.route("/ciudades_pais/<nombre_pais>", methods=["GET"])
def ciudades_pais(nombre_pais:str):

	conexion=Conexion()

	if not conexion.existe_pais(nombre_pais):

		return redirect(url_for("inicio.inicio"))

	ciudades=conexion.ciudades_pais(nombre_pais, 18000)

	conexion.cerrarConexion()

	return render_template("ciudades_pais.html", pais=nombre_pais, ciudades=ciudades)