from flask import Blueprint, render_template, request

from src.database.conexion import Conexion

bp_inicio=Blueprint("inicio", __name__)

# Vista de la pagina principal
@bp_inicio.route("/", methods=["GET"])
def inicio():

	conexion=Conexion()

	ciudad=request.args.get("ciudad", default=False, type=bool)
	pais=request.args.get("pais", default=False, type=bool)
	fecha=request.args.get("fecha", default=False, type=bool)

	orden="c.Ciudad" if ciudad else ("c.Pais" if pais else ("v.Ida" if fecha else None))

	viajes=conexion.obtenerViajes(orden) if orden else conexion.obtenerViajes()

	conexion.cerrarConexion()

	return render_template("inicio.html", viajes=viajes)