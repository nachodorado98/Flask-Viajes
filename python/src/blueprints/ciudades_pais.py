from flask import Blueprint, render_template, redirect, url_for, request

from src.database.conexion import Conexion

from src.utilidades.utils import añadirPuntos

bp_ciudades_pais=Blueprint("ciudades_pais", __name__)

@bp_ciudades_pais.route("/ciudades_pais/<nombre_pais>", methods=["GET"])
def ciudades_pais(nombre_pais:str):

	conexion=Conexion()

	if not conexion.existe_pais(nombre_pais):

		return redirect(url_for("inicio.inicio"))

	orden=request.args.get("orden", default=False, type=bool)

	ciudades=conexion.ciudades_pais_orden_visitadas(nombre_pais, 18000) if orden else conexion.ciudades_pais(nombre_pais, 18000)

	ciudades_limpias=list(map(lambda ciudad: (ciudad[0], añadirPuntos(str(ciudad[3])), ciudad[4], ciudad[1]), ciudades))

	conexion.cerrarConexion()

	return render_template("ciudades_pais.html", pais=nombre_pais, ciudades=ciudades_limpias, orden=orden)