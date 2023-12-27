from flask import Blueprint, render_template

from src.database.conexion import Conexion

bp_inicio=Blueprint("inicio", __name__)

# Vista de la pagina principal
@bp_inicio.route("/", methods=["GET"])
def inicio()->str:

	conexion=Conexion()

	viajes=conexion.obtenerViajes()

	conexion.cerrarConexion()

	return render_template("inicio.html", viajes=viajes)