from flask import Flask
import os

from .blueprints.inicio import bp_inicio
from .blueprints.anadir_viaje import bp_anadir_viaje
from .blueprints.detalle_ciudad import bp_detalle_ciudad
from .blueprints.detalle_pais import bp_detalle_pais
from .blueprints.detalle_viaje import bp_detalle_viaje
from .blueprints.ciudades_pais import bp_ciudades_pais

from .utilidades.utils import crearCarpeta

# Funcion para crear el entorno
def creacionEntorno()->None:

	ruta=os.path.dirname(os.path.join(os.path.dirname(__file__)))

	ruta_carpeta=os.path.join(ruta, "src", "static", "imagenes")

	crearCarpeta(ruta_carpeta)

# Funcion para crear la instancia de la aplicacion
def crear_app(configuracion:object)->Flask:

	app=Flask(__name__, template_folder="templates")

	app.config.from_object(configuracion)

	app.register_blueprint(bp_inicio)
	app.register_blueprint(bp_anadir_viaje)
	app.register_blueprint(bp_detalle_ciudad)
	app.register_blueprint(bp_detalle_pais)
	app.register_blueprint(bp_detalle_viaje)
	app.register_blueprint(bp_ciudades_pais)

	creacionEntorno()

	return app