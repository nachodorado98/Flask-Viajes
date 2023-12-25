import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Optional, Dict

from .confconexion import *

# Clase para la conexion a la BBDD
class Conexion:

	def __init__(self)->None:

		try:

			self.bbdd=psycopg2.connect(host=HOST, user=USUARIO, password=CONTRASENA, port=PUERTO, database=BBDD)
			self.c=self.bbdd.cursor(cursor_factory=RealDictCursor)

		except psycopg2.OperationalError as e:

			print("Error en la conexion a la BBDD")
			print(e)

	# Metodo para cerrar la conexion a la BBDD
	def cerrarConexion(self)->None:

		self.c.close()
		self.bbdd.close()

	# Metodo para cconfirmar una accion
	def confirmar(self)->None:

		self.bbdd.commit()

	# Metodo para obtener las lineas recorridas
	def obtenerViajes(self)->Optional[List[tuple]]:

		self.c.execute("""SELECT v.Id_Viaje, c.Ciudad, c.CodCiudad, v.Ida, v.Vuelta
							FROM viajes v
							JOIN ciudades c
							USING (CodCiudad)""")

		viajes=self.c.fetchall()

		# Funcion para convertir los datos de los viajes en el formator deseado
		def convertirDatos(datos:Dict)->tuple:

			ida=datos["ida"].strftime("%d/%m/%Y")

			vuelta=datos["ida"].strftime("%d/%m/%Y")

			return datos["id_viaje"], datos["ciudad"], datos["codciudad"], f"{ida} - {vuelta}"

		return list(map(convertirDatos, viajes)) if viajes else None