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
							(ciudad,))

		ciudad=self.c.fetchone()

		return None if ciudad is None else ciudad["codciudad"]

	# Metodo para insertar un viaje en la BBDD
	def insertarViaje(self, codciudad:int, ida:str, vuelta:str, hotel:str, web:str, transporte:str, comentario:str, imagen:str)->None:

		self.c.execute("""INSERT INTO viajes (CodCiudad, Ida, Vuelta, Hotel, Web, Transporte, Comentario, Imagen)
							VALUES(%s, %s, %s, %s, %s, %s, %s, %s)""",
							(codciudad, ida, vuelta, hotel, web, transporte, comentario, imagen))


		self.confirmar()

	# Metodo para saber si existe un codigo de ciudad
	def existe_codigo_ciudad(self, codciudad:int)->bool:

		self.c.execute("""SELECT CodCiudad
							FROM Ciudades
							WHERE CodCiudad=%s""",
							(codciudad,))

		codigo=self.c.fetchone()

		return False if codigo is None else True

	# Metodo para obtener los detalles de una ciudad
	def obtenerDetalleCiudad(self, codciudad:int)->Optional[tuple]:

		self.c.execute("""SELECT Ciudad, Latitud, Longitud, Pais, Siglas, Tipo, Poblacion
							FROM Ciudades
							WHERE CodCiudad=%s""",
							(codciudad,))

		ciudad=self.c.fetchone()

		# Funcion para limpiar los datos de la ciudad
		def limpiarDatos(datos:Dict)->tuple:

			latitud=round(float(datos["latitud"]), 4)

			longitud=round(float(datos["longitud"]), 4)

			poblacion=str(datos["poblacion"])

			return datos["ciudad"], latitud, longitud, datos["pais"], datos["siglas"], datos["tipo"], poblacion

		return None if ciudad is None else limpiarDatos(ciudad)

	# Metodo para saber si un pais existe
	def existe_pais(self, nombre_pais:str)->bool:

		paises_existentes=self.paises_existentes()

		return True if nombre_pais in paises_existentes else False

	# Metodo para obtener los datos de la capital de un pais
	def capital_datos_pais(self, nombre_pais:str)->Optional[tuple]:

		self.c.execute("""SELECT Ciudad, Siglas, CodCiudad
							FROM ciudades
							WHERE Tipo='Capital'
							AND Pais=%s""",
							(nombre_pais,))

		datos=self.c.fetchone()

		return None if datos is None else (datos["ciudad"], datos["siglas"], datos["codciudad"])

	# Metodo para obtener la poblacion y el numero de ciudades de un pais
	def poblacion_ciudades_pais(self, nombre_pais:str)->Optional[tuple]:

		self.c.execute("""SELECT Pais, SUM(Poblacion) as Poblacion_Pais, COUNT(Ciudades) as Numero_Ciudades
							FROM ciudades
							WHERE Pais=%s
							GROUP BY Pais""",
							(nombre_pais,))

		datos=self.c.fetchone()

		return None if datos is None else (datos["poblacion_pais"], datos["numero_ciudades"])

	# Metodo para obtener la informacion de un pais
	def informacion_pais(self, nombre_pais:str)->Optional[tuple]:

		if not self.existe_pais(nombre_pais):

			return None

		capital, siglas, codigo_ciudad=self.capital_datos_pais(nombre_pais)

		poblacion, ciudades=self.poblacion_ciudades_pais(nombre_pais)

		return capital, siglas, codigo_ciudad, poblacion, ciudades