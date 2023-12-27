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

	# Metodo para confirmar una accion
	def confirmar(self)->None:

		self.bbdd.commit()

	# Metodo para obtener los viajes recorridas
	def obtenerViajes(self)->Optional[List[tuple]]:

		self.c.execute("""SELECT v.Id_Viaje, c.Ciudad, c.CodCiudad, c.Pais, v.Ida, v.Vuelta
							FROM viajes v
							JOIN ciudades c
							USING (CodCiudad)
							ORDER BY v.Id_Viaje""")

		viajes=self.c.fetchall()

		# Funcion para convertir los datos de los viajes en el formator deseado
		def convertirDatos(datos:Dict)->tuple:

			ida=datos["ida"].strftime("%d/%m/%Y")

			vuelta=datos["vuelta"].strftime("%d/%m/%Y")

			return datos["id_viaje"], datos["ciudad"], datos["codciudad"], datos["pais"], f"{ida} - {vuelta}"

		return list(map(convertirDatos, viajes)) if viajes else None

	# Metodo para obtener los paises existentes
	def paises_existentes(self)->List[str]:

		self.c.execute("""SELECT Pais
	                 		FROM ciudades 
	                 		GROUP BY Pais
	                 		ORDER BY Pais""")

		paises=self.c.fetchall()

		return list(map(lambda pais: pais["pais"], paises))

	# Metodo para obtener las ciudades existentes a partir de un pais
	def ciudades_existentes(self, pais:str, poblacion:int=0)->List[str]:

		self.c.execute("""SELECT Ciudad
	                 		FROM ciudades 
	                 		WHERE Pais=%s
	                 		AND Poblacion>=%s
	                 		ORDER BY Ciudad""",
	                 		(pais,poblacion))

		ciudades=self.c.fetchall()

		return list(map(lambda ciudad: ciudad["ciudad"], ciudades))

	# Metodo para obtener el codigo de una ciudad
	def obtenerCodCiudad(self, ciudad:str)->Optional[int]:

		self.c.execute("""SELECT CodCiudad
							FROM Ciudades
							WHERE Ciudad=%s""",
							(ciudad.title(),))

		ciudad=self.c.fetchone()

		return None if ciudad is None else ciudad["codciudad"]

	# Metodo para insertar un viaje en la BBDD
	def insertarViaje(self, codciudad:int, ida:str, vuelta:str, hotel:str, web:str, transporte:str, comentario:Optional[str])->None:

		if comentario is None:

			self.c.execute("""INSERT INTO viajes (CodCiudad, Ida, Vuelta, Hotel, Web, Transporte)
								VALUES(%s, %s, %s, %s, %s, %s)""",
								(codciudad, ida, vuelta, hotel, web, transporte))

		else:

			self.c.execute("""INSERT INTO viajes (CodCiudad, Ida, Vuelta, Hotel, Web, Transporte, Comentarios)
								VALUES(%s, %s, %s, %s, %s, %s, %s)""",
								(codciudad, ida, vuelta, hotel, web, transporte, comentario))


		self.confirmar()