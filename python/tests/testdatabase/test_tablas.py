import pytest
from datetime import datetime

def test_tabla_ciudades_llena(conexion):

	conexion.c.execute("SELECT * FROM ciudades")

	assert conexion.c.fetchall()!=[]

def test_tabla_viajes_vacia(conexion):

	conexion.c.execute("SELECT * FROM viajes")

	assert conexion.c.fetchall()==[]

def test_obtener_viajes_existentes(conexion):

	assert conexion.obtenerViajes() is None

@pytest.mark.parametrize(["codigo_ciudad"],
	[(1,),(22,),(2019,),(13,)]
)
def test_obtener_viajes_existente(conexion, codigo_ciudad):

	conexion.c.execute(f"""INSERT INTO viajes (CodCiudad, Ida, Vuelta, Hotel, Web, Transporte, Comentario, Imagen)
							VALUES({codigo_ciudad}, '2019-06-22', '2019-06-22', 'Hotel', 'Web', 'Transporte', 'Comentario', 'Imagen')""")

	conexion.confirmar()

	viajes=conexion.obtenerViajes()

	assert len(viajes)==1
	assert viajes[0][2]==codigo_ciudad

def test_obtener_viajes_existentes(conexion):

	for codigo in range(1, 11):

		conexion.c.execute(f"""INSERT INTO viajes (CodCiudad, Ida, Vuelta, Hotel, Web, Transporte, Comentario, Imagen)
								VALUES({codigo}, '2019-06-22', '2019-06-22', 'Hotel', 'Web', 'Transporte', 'Comentario', 'Imagen')""")

	conexion.confirmar()

	viajes=conexion.obtenerViajes()

	assert len(viajes)==10

	for numero, viaje in enumerate(viajes):

		assert viaje[2]==(numero+1)

	assert viajes[0][0]<viajes[-1][0]

def test_obtener_paises_existentes(conexion):

	paises=conexion.paises_existentes()

	assert len(paises)==210

def test_obtener_ciudades_existentes(conexion):

	ciudades=conexion.ciudades_existentes("España")

	assert len(ciudades)==1135

@pytest.mark.parametrize(["poblacion", "cantidad"],
	[(10000, 650),(100000, 61),(1000000, 2)]
)
def test_obtener_ciudades_existentes_poblacion_limite(conexion, poblacion, cantidad):

	ciudades=conexion.ciudades_existentes("España", poblacion)

	assert len(ciudades)==cantidad

@pytest.mark.parametrize(["ciudad", "codigo_ciudad"],
	[("Tokyo",1), ("Delhi",3), ("London",34), ("Porto",2438), ("Barcelona", 160), ("Andorra la Vella", 809)]
)
def test_obtener_codigo_ciudad(conexion, ciudad, codigo_ciudad):

	assert conexion.obtenerCodCiudad(ciudad)==codigo_ciudad

@pytest.mark.parametrize(["ciudad"],
	[("jkjkjkjjk",), ("MADRID",), ("barna",), ("london",), ("Andorra La Vella",)]
)
def test_obtener_codigo_ciudad_no_existe(conexion, ciudad):

	assert conexion.obtenerCodCiudad(ciudad) is None

@pytest.mark.parametrize(["codigo_ciudad", "ida", "vuelta", "hotel", "web", "transporte", "comentario", "imagen"],
	[
		(1, "2019-06-22", "2019-06-22", "Hotel", "Web", "Transporte", "Comentario", "hjhjhjjhhj.jpg"),
		(34, "2019-06-22", "2019-06-22", "Hotel", "Web", "Transporte", "comentario", "imagen"),
		(160, "2023-06-22", "2019-06-22", "Hotel", "Web", "Transporte", "Sin Comentario", "Sin Imagen"),
		(2438, "2023-06-22", "2019-06-22", "Hotel", "Web", "Transporte", "asdfghjkl", "madrid_españa_jjjjkjbj.png")
	]
)
def test_insertar_viaje(conexion, codigo_ciudad, ida, vuelta, hotel, web, transporte, comentario, imagen):

	conexion.insertarViaje(codigo_ciudad, ida, vuelta, hotel, web, transporte, comentario, imagen)

	conexion.c.execute("SELECT * FROM viajes")

	viajes=conexion.c.fetchall()

	viaje=viajes[0]

	assert len(viajes)==1
	assert viaje["codciudad"]==codigo_ciudad
	assert viaje["ida"].strftime("%Y-%m-%d")==ida
	assert viaje["vuelta"].strftime("%Y-%m-%d")==vuelta
	assert viaje["hotel"]==hotel
	assert viaje["web"]==web
	assert viaje["transporte"]==transporte
	assert viaje["comentario"]==comentario
	assert viaje["imagen"]==imagen

def test_insertar_viaje_multiples(conexion):

	for _ in range(5):

		conexion.insertarViaje(34, "2019-06-22", "2019-06-22", "Hotel", "Web", "Transporte", "comentario", "imagen.jpg"),

	conexion.c.execute("SELECT * FROM viajes")

	viajes=conexion.c.fetchall()

	assert len(viajes)==5

@pytest.mark.parametrize(["codigo_ciudad"],
	[(0,), (100000,), (-1,), (24354366,)]
)
def test_codigo_ciudad_no_existe(conexion, codigo_ciudad):

	assert not conexion.existe_codigo_ciudad(codigo_ciudad)

@pytest.mark.parametrize(["codigo_ciudad"],
	[(1,), (10000,), (22,), (13,)]
)
def test_codigo_ciudad_existe(conexion, codigo_ciudad):

	assert conexion.existe_codigo_ciudad(codigo_ciudad)

@pytest.mark.parametrize(["codigo_ciudad"],
	[(0,), (100000,), (-1,), (24354366,)]
)
def test_detalle_ciudad_no_existe(conexion, codigo_ciudad):

	assert conexion.obtenerDetalleCiudad(codigo_ciudad) is None

@pytest.mark.parametrize(["codigo_ciudad"],
	[(1,), (10000,), (22,), (13,)]
)
def test_detalle_ciudad_existe(conexion, codigo_ciudad):

	ciudad=conexion.obtenerDetalleCiudad(codigo_ciudad)

	assert len(ciudad)==7
	assert isinstance(ciudad[1], float)
	assert isinstance(ciudad[2], float)
	assert isinstance(ciudad[-1], str)

@pytest.mark.parametrize(["pais"],
	[("jkjkjkjjk",), ("españa",), ("ReinoUnido",), ("ANDORRA",), ("Pais",)]
)
def test_pais_no_existe(conexion, pais):

	assert not conexion.existe_pais(pais)

@pytest.mark.parametrize(["pais"],
	[("España",), ("Netherlands",), ("Reino Unido",), ("Andorra",), ("Emiratos Árabes Unidos",)]
)
def test_pais_existe(conexion, pais):

	assert conexion.existe_pais(pais)

@pytest.mark.parametrize(["pais"],
	[("jkjkjkjjk",), ("españa",), ("ReinoUnido",), ("ANDORRA",), ("Pais",)]
)
def test_capital_datos_pais_no_existe(conexion, pais):

	assert conexion.capital_datos_pais(pais) is None

@pytest.mark.parametrize(["pais", "capital", "siglas", "codigo_ciudad"],
	[
		("España", "Madrid", "ESP", 103),
		("Netherlands", "Amsterdam", "NLD", 709),
		("Reino Unido", "London", "GBR", 34),
		("Andorra", "Andorra la Vella", "AND", 809),
		("Emiratos Árabes Unidos", "Abu Dhabi", "ARE", 488)
	]
)
def test_capital_datos_pais_existe(conexion, pais, capital, siglas, codigo_ciudad):

	assert conexion.capital_datos_pais(pais)==(capital, siglas, codigo_ciudad)

@pytest.mark.parametrize(["pais"],
	[("jkjkjkjjk",), ("españa",), ("ReinoUnido",), ("ANDORRA",), ("Pais",)]
)
def test_poblacion_ciudades_pais_no_existe(conexion, pais):

	assert conexion.poblacion_ciudades_pais(pais) is None

@pytest.mark.parametrize(["pais", "poblacion", "ciudades"],
	[
		("España", 44106654, 1135),
		("Netherlands", 14580259, 331),
		("Reino Unido", 46162721, 858),
		("Andorra", 77354, 7),
		("Emiratos Árabes Unidos", 6773563, 9)
	]
)
def test_poblacion_ciudades_pais_existe(conexion, pais, poblacion, ciudades):

	assert conexion.poblacion_ciudades_pais(pais)==(poblacion, ciudades)

@pytest.mark.parametrize(["pais"],
	[("jkjkjkjjk",), ("españa",), ("ReinoUnido",), ("ANDORRA",), ("Pais",)]
)
def test_informacion_pais_no_existe(conexion, pais):

	assert conexion.informacion_pais(pais) is None

@pytest.mark.parametrize(["pais", "capital", "siglas", "codigo_ciudad", "poblacion", "ciudades"],
	[
		("España", "Madrid", "ESP", 103, 44106654, 1135),
		("Netherlands", "Amsterdam", "NLD", 709, 14580259, 331),
		("Reino Unido", "London", "GBR", 34, 46162721, 858),
		("Andorra", "Andorra la Vella", "AND", 809, 77354, 7),
		("Emiratos Árabes Unidos", "Abu Dhabi", "ARE", 488, 6773563, 9)
	]
)
def test_informacion_pais_existe(conexion, pais, capital, siglas, codigo_ciudad, poblacion, ciudades):

	assert conexion.informacion_pais(pais)==(capital, siglas, codigo_ciudad, poblacion, ciudades)

@pytest.mark.parametrize(["id_viaje"],
	[(0,), (10000000,), (-1,), (2564354366,)]
)
def test_id_viaje_no_existe(conexion, id_viaje):

	assert not conexion.existe_id_viaje(id_viaje)

def test_id_viaje_existe(conexion):

	conexion.insertarViaje(34, "2019-06-22", "2019-06-22", "Hotel", "Web", "Transporte", "comentario", "imagen.jpg")

	viajes=conexion.obtenerViajes()

	id_viaje=viajes[0][0]

	assert conexion.existe_id_viaje(id_viaje)
	assert not conexion.existe_id_viaje(id_viaje+1)
	assert not conexion.existe_id_viaje(id_viaje-1)

@pytest.mark.parametrize(["id_viaje"],
	[(0,), (10000000,), (-1,), (2564354366,)]
)
def test_detalle_viaje_no_existe(conexion, id_viaje):

	assert conexion.obtenerDetalleViaje(id_viaje) is None

def test_detalle_viaje_existe(conexion):

	conexion.insertarViaje(34, "2019-06-22", "2019-06-22", "Hotel", "Web", "Transporte", "comentario", "imagen.jpg")

	viajes=conexion.obtenerViajes()

	id_viaje=viajes[0][0]

	viaje=conexion.obtenerDetalleViaje(id_viaje)

	assert viaje is not None
	assert viaje[0]=="London"

@pytest.mark.parametrize(["pais"],
	[("jkjkjkjjk",), ("españa",), ("ReinoUnido",), ("ANDORRA",), ("Pais",)]
)
def test_ciudades_pais_no_existe(conexion, pais):

	assert conexion.ciudades_pais(pais) is None

@pytest.mark.parametrize(["pais", "poblacion"],
	[
		("Reino Unido", 0),
		("España", 10000),
		("Portugal", 24356),
		("Francia", 1000000)
	]
)
def test_ciudades_pais_existe_sin_viaje(conexion, pais, poblacion):

	ciudades=conexion.ciudades_pais(pais, poblacion)

	assert len(ciudades)==len(conexion.ciudades_existentes(pais, poblacion))

@pytest.mark.parametrize(["pais", "poblacion", "codigo_ciudad"],
	[
		("Reino Unido",0, 34),
		("España", 10000, 103),
		("Portugal", 24356, 2438),
		("Francia", 1000000, 35)
	]
)
def test_ciudades_pais_existe_con_viaje(conexion, pais, poblacion, codigo_ciudad):

	conexion.insertarViaje(codigo_ciudad, "2019-06-22", "2019-06-22", "Hotel", "Web", "Transporte", "comentario", "imagen.jpg")

	ciudades=conexion.ciudades_pais(pais, poblacion)

	assert len(ciudades)==len(conexion.ciudades_existentes(pais, poblacion))

	ciudad_visitada=list(filter(lambda ciudad: ciudad[2]==codigo_ciudad, ciudades))

	assert len(ciudad_visitada)==1
	assert ciudad_visitada[0][1]=="Visitada"

	ciudades_no_visitadas=list(filter(lambda ciudad: ciudad[2]!=codigo_ciudad, ciudades))

	assert len(ciudades_no_visitadas)==len(ciudades)-1

	for ciudad_no_visitada in ciudades_no_visitadas:

		assert ciudad_no_visitada[1]=="No Visitada"

@pytest.mark.parametrize(["pais", "poblacion", "codigo_ciudad"],
	[
		("Reino Unido",0, 34),
		("España", 10000, 103),
		("Portugal", 24356, 2438),
		("Francia", 1000000, 35)
	]
)
def test_ciudades_pais_existe_con_varios_viajes(conexion, pais, poblacion, codigo_ciudad):

	for _ in range(5):

		conexion.insertarViaje(codigo_ciudad, "2019-06-22", "2019-06-22", "Hotel", "Web", "Transporte", "comentario", "imagen.jpg")

	ciudades=conexion.ciudades_pais(pais, poblacion)

	assert len(ciudades)==len(conexion.ciudades_existentes(pais, poblacion))

	ciudad_visitada=list(filter(lambda ciudad: ciudad[2]==codigo_ciudad, ciudades))

	assert len(ciudad_visitada)==1
	assert ciudad_visitada[0][1]=="Visitada"

	ciudades_no_visitadas=list(filter(lambda ciudad: ciudad[2]!=codigo_ciudad, ciudades))

	assert len(ciudades_no_visitadas)==len(ciudades)-1

	for ciudad_no_visitada in ciudades_no_visitadas:

		assert ciudad_no_visitada[1]=="No Visitada"

@pytest.mark.parametrize(["pais"],
	[("jkjkjkjjk",), ("españa",), ("ReinoUnido",), ("ANDORRA",), ("Pais",)]
)
def test_ciudades_pais_orden_visitadas_no_existe(conexion, pais):

	assert conexion.ciudades_pais_orden_visitadas(pais) is None

@pytest.mark.parametrize(["pais", "poblacion"],
	[
		("Reino Unido", 0),
		("España", 10000),
		("Portugal", 24356),
		("Francia", 1000000)
	]
)
def test_ciudades_pais_orden_visitadas_existe_sin_viaje(conexion, pais, poblacion):

	ciudades=conexion.ciudades_pais_orden_visitadas(pais, poblacion)

	assert len(ciudades)==len(conexion.ciudades_existentes(pais, poblacion))

@pytest.mark.parametrize(["pais", "poblacion", "codigo_ciudad"],
	[
		("Reino Unido",0, 34),
		("España", 10000, 103),
		("Portugal", 24356, 2438),
		("Francia", 1000000, 35)
	]
)
def test_ciudades_pais_orden_visitadas_existe_con_viaje(conexion, pais, poblacion, codigo_ciudad):

	conexion.insertarViaje(codigo_ciudad, "2019-06-22", "2019-06-22", "Hotel", "Web", "Transporte", "comentario", "imagen.jpg")

	ciudades=conexion.ciudades_pais_orden_visitadas(pais, poblacion)

	assert len(ciudades)==len(conexion.ciudades_existentes(pais, poblacion))

	ciudad_visitada=list(filter(lambda ciudad: ciudad[2]==codigo_ciudad, ciudades))

	assert len(ciudad_visitada)==1
	assert ciudad_visitada[0][1]=="Visitada"

	assert ciudades[0]==ciudad_visitada[0]

	ciudades_no_visitadas=list(filter(lambda ciudad: ciudad[2]!=codigo_ciudad, ciudades))

	assert len(ciudades_no_visitadas)==len(ciudades)-1

	for ciudad_no_visitada in ciudades_no_visitadas:

		assert ciudad_no_visitada[1]=="No Visitada"

	assert ciudades[1:]==ciudades_no_visitadas

@pytest.mark.parametrize(["pais", "poblacion", "codigo_ciudad"],
	[
		("Reino Unido",0, 34),
		("España", 10000, 103),
		("Portugal", 24356, 2438),
		("Francia", 1000000, 35)
	]
)
def test_ciudades_pais_orden_visitadas_existe_con_varios_viajes(conexion, pais, poblacion, codigo_ciudad):

	for _ in range(5):

		conexion.insertarViaje(codigo_ciudad, "2019-06-22", "2019-06-22", "Hotel", "Web", "Transporte", "comentario", "imagen.jpg")

	ciudades=conexion.ciudades_pais_orden_visitadas(pais, poblacion)

	assert len(ciudades)==len(conexion.ciudades_existentes(pais, poblacion))

	ciudad_visitada=list(filter(lambda ciudad: ciudad[2]==codigo_ciudad, ciudades))

	assert len(ciudad_visitada)==1
	assert ciudad_visitada[0][1]=="Visitada"

	assert ciudades[0]==ciudad_visitada[0]

	ciudades_no_visitadas=list(filter(lambda ciudad: ciudad[2]!=codigo_ciudad, ciudades))

	assert len(ciudades_no_visitadas)==len(ciudades)-1

	for ciudad_no_visitada in ciudades_no_visitadas:

		assert ciudad_no_visitada[1]=="No Visitada"

	assert ciudades[1:]==ciudades_no_visitadas

@pytest.mark.parametrize(["web", "comentario"],
	[
		("www.miweb.com", "me gusta mucho esta app"),
		("miweb.com", "me gusta muchissisismo esta app"),
		("", "me gusta mucho esta app"),
		("www.miweb.com", ""),
		("www.sdgfdhfgh.com", "dhfdhfghgf"),
		("www.google.com", "Comentario")
	]
)
def test_actualizar_viaje_web_comentario(conexion, web, comentario):

	conexion.insertarViaje(34, "2019-06-22", "2019-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")

	viajes=conexion.obtenerViajes()

	id_viaje=viajes[0][0]

	conexion.actualizarWebComentario(id_viaje, web, comentario)

	conexion.c.execute("SELECT * FROM viajes")

	viaje=conexion.c.fetchone()

	assert viaje["id_viaje"]==id_viaje
	assert viaje["web"]==web
	assert viaje["comentario"]==comentario

@pytest.mark.parametrize(["web", "comentario", "imagen"],
	[
		("www.miweb.com", "me gusta mucho esta app", "Sin Imagen"),
		("miweb.com", "me gusta muchissisismo esta app", "miimagen.jpg"),
		("", "me gusta mucho esta app", "ytytytyttuy"),
		("www.miweb.com", "", "madrid_espana_ggfh.jpg"),
		("www.sdgfdhfgh.com", "dhfdhfghgf", "Imagen"),
		("www.google.com", "Comentario", "Sin Imagen")
	]
)
def test_actualizar_viaje_web_comentario_imagen(conexion, web, comentario, imagen):

	conexion.insertarViaje(34, "2019-06-22", "2019-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")

	viajes=conexion.obtenerViajes()

	id_viaje=viajes[0][0]

	conexion.actualizarWebComentarioImagen(id_viaje, web, comentario, imagen)

	conexion.c.execute("SELECT * FROM viajes")

	viaje=conexion.c.fetchone()

	assert viaje["id_viaje"]==id_viaje
	assert viaje["web"]==web
	assert viaje["comentario"]==comentario
	assert viaje["imagen"]==imagen

def test_ciudades_visitadas_mapa_no_existen(conexion):

	assert conexion.obtenerDatosCiudadesVisitadas() is None

def test_ciudades_visitadas_mapa_existe(conexion):

	conexion.insertarViaje(34, "2019-06-22", "2019-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")

	ciudades_visitadas=conexion.obtenerDatosCiudadesVisitadas()

	assert len(ciudades_visitadas)==1
	assert isinstance(ciudades_visitadas[0][1], float)
	assert isinstance(ciudades_visitadas[0][2], float)
	assert ciudades_visitadas[0][3]=="22/06/2019-22/06/2019"

def test_ciudades_visitadas_mapa_existes(conexion):

	conexion.insertarViaje(34, "2019-06-22", "2019-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")
	conexion.insertarViaje(33, "2019-06-22", "2019-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")
	conexion.insertarViaje(22, "2019-06-22", "2019-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")
	conexion.insertarViaje(34, "2019-06-22", "2019-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")

	ciudades_visitadas=conexion.obtenerDatosCiudadesVisitadas()

	assert len(ciudades_visitadas)==4

def test_tabla_paises_llena(conexion):

	conexion.c.execute("SELECT * FROM paises")

	assert conexion.c.fetchall()!=[]

def test_paises_visitados_mapa_no_existen(conexion):

	assert conexion.obtenerPaisesVisitados() is None

def test_paises_visitados_mapa_existe(conexion):

	conexion.insertarViaje(34, "2019-06-22", "2019-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")

	paises_visitados=conexion.obtenerPaisesVisitados()

	assert len(paises_visitados)==1

def test_paises_visitados_mapa_existes(conexion):

	conexion.insertarViaje(34, "2019-06-22", "2019-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")
	conexion.insertarViaje(33, "2019-06-22", "2019-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")
	conexion.insertarViaje(22, "2019-06-22", "2019-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")
	conexion.insertarViaje(34, "2019-06-22", "2019-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")

	paises_visitados=conexion.obtenerPaisesVisitados()

	assert len(paises_visitados)==2

def test_paises_visitados_ingles_mapa_no_existen(conexion):

	assert conexion.paises_visitados_ingles() is None

def test_paises_visitados_ingles_mapa_existe(conexion):

	conexion.insertarViaje(34, "2019-06-22", "2019-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")

	paises_visitados_ingles=conexion.paises_visitados_ingles()

	assert len(paises_visitados_ingles)==1
	assert paises_visitados_ingles[0]=="United Kingdom"

def test_paises_visitados_mapa_existes(conexion):

	conexion.insertarViaje(34, "2019-06-22", "2019-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")
	conexion.insertarViaje(33, "2019-06-22", "2019-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")
	conexion.insertarViaje(22, "2019-06-22", "2019-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")
	conexion.insertarViaje(34, "2019-06-22", "2019-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")

	paises_visitados_ingles=conexion.paises_visitados_ingles()

	assert len(paises_visitados_ingles)==2
	assert paises_visitados_ingles[0]=="Islamic Republic of Pakistan"
	assert paises_visitados_ingles[1]=="United Kingdom"

def test_estadisticas_viajes_realizados_no_existen(conexion):

	assert conexion.estadistica_viajes_realizados()==0

def test_estadisticas_viajes_realizados_existe(conexion):

	conexion.insertarViaje(34, "2019-06-22", "2019-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")

	assert conexion.estadistica_viajes_realizados()==1

def test_estadisticas_viajes_realizados_existen_mismo_pais(conexion):

	for _ in range(5):

		conexion.insertarViaje(34, "2019-06-22", "2019-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")

	assert conexion.estadistica_viajes_realizados()==5

def test_estadisticas_viajes_realizados_existen_distinto_pais(conexion):

	conexion.insertarViaje(34, "2019-06-22", "2019-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")
	conexion.insertarViaje(33, "2019-06-22", "2019-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")
	conexion.insertarViaje(22, "2019-06-22", "2019-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")
	conexion.insertarViaje(1, "2019-06-22", "2019-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")
	conexion.insertarViaje(34, "2019-06-22", "2019-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")
	conexion.insertarViaje(13, "2019-06-22", "2019-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")
	conexion.insertarViaje(1, "2019-06-22", "2019-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")
	
	assert conexion.estadistica_viajes_realizados()==7
	
def test_estadisticas_paises_visitados_no_existen(conexion):

	assert conexion.estadistica_paises_visitados()==0

def test_estadisticas_paises_visitados_existe(conexion):

	conexion.insertarViaje(34, "2019-06-22", "2019-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")

	assert conexion.estadistica_paises_visitados()==1

def test_estadisticas_paises_visitados_existen_mismo_pais(conexion):

	for _ in range(5):

		conexion.insertarViaje(34, "2019-06-22", "2019-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")

	assert conexion.estadistica_paises_visitados()==1

def test_estadisticas_paises_visitados_existen_distinto_pais(conexion):

	conexion.insertarViaje(34, "2019-06-22", "2019-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")
	conexion.insertarViaje(33, "2019-06-22", "2019-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")
	conexion.insertarViaje(22, "2019-06-22", "2019-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")
	conexion.insertarViaje(1, "2019-06-22", "2019-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")
	conexion.insertarViaje(34, "2019-06-22", "2019-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")
	
	assert conexion.estadistica_paises_visitados()==3

def test_estadisticas_ciudades_visitadas_no_existen(conexion):

	assert conexion.estadistica_ciudades_visitadas()==0

def test_estadisticas_ciudades_visitadas_existe(conexion):

	conexion.insertarViaje(34, "2019-06-22", "2019-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")

	assert conexion.estadistica_ciudades_visitadas()==1

def test_estadisticas_ciudades_visitadas_existen_mismo_pais(conexion):

	for _ in range(5):

		conexion.insertarViaje(34, "2019-06-22", "2019-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")

	assert conexion.estadistica_ciudades_visitadas()==1

def test_estadisticas_ciudades_visitadas_existen_distinto_pais(conexion):

	conexion.insertarViaje(34, "2019-06-22", "2019-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")
	conexion.insertarViaje(33, "2019-06-22", "2019-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")
	conexion.insertarViaje(22, "2019-06-22", "2019-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")
	conexion.insertarViaje(1, "2019-06-22", "2019-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")
	conexion.insertarViaje(34, "2019-06-22", "2019-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")
	conexion.insertarViaje(2, "2019-06-22", "2019-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")
	conexion.insertarViaje(13, "2019-06-22", "2019-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")
	conexion.insertarViaje(22, "2019-06-22", "2019-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")
	
	assert conexion.estadistica_ciudades_visitadas()==6

def test_estadisticas_ultimo_dia_viaje_no_existen(conexion):

	assert conexion.estadistica_dias_ultimo_viaje() is None

@pytest.mark.parametrize(["vuelta"],
	[("2019-06-22",),("2022-06-22",),("2023-06-22",),("2023-08-06",)]
)
def test_estadisticas_ultimo_dia_viaje_existe(conexion, vuelta):

	conexion.insertarViaje(34, "2019-06-22", vuelta, "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")

	hoy=datetime.now()

	dia_vuelta=datetime.strptime(vuelta, "%Y-%m-%d")

	dias=(hoy-dia_vuelta).days

	assert conexion.estadistica_dias_ultimo_viaje()==dias

@pytest.mark.parametrize(["vueltas", "ultima_vuelta"],
	[
		(["2019-06-22", "2024-01-01", "2023-04-13"], "2024-01-01"),
		(["2019-06-22", "2022-01-01", "2023-04-13"], "2023-04-13"),
		(["2024-01-01", datetime.now().strftime("%Y-%m-%d"), "2023-04-13"], datetime.now().strftime("%Y-%m-%d")),
		(["2019-06-22", "2010-01-01", "2019-04-13"], "2019-06-22"),
		(["2019-06-22", "2019-06-22", "2019-06-22"], "2019-06-22"),
		([datetime.now().strftime("%Y-%m-%d"), "2024-01-01", "2023-04-13"], datetime.now().strftime("%Y-%m-%d"))
	]
)
def test_estadisticas_ultimo_dia_viaje_existen(conexion, vueltas, ultima_vuelta):

	conexion.insertarViaje(34, "2019-06-22", vueltas[0], "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")
	conexion.insertarViaje(34, "2022-06-22", vueltas[1], "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")
	conexion.insertarViaje(34, "2023-04-13", vueltas[2], "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")
	
	hoy=datetime.now()

	dia_vuelta=datetime.strptime(ultima_vuelta, "%Y-%m-%d")

	dias=(hoy-dia_vuelta).days

	assert conexion.estadistica_dias_ultimo_viaje()==dias

def test_estadisticas_viaje_mas_largo_no_existen(conexion):

	assert conexion.estadistica_viaje_mas_largo() is None

@pytest.mark.parametrize(["ida", "vuelta", "dias"],
	[
		("2019-06-22", "2019-07-01", 9),
		("2019-06-22", "2019-06-23", 1),
		("2019-06-22", "2019-06-25", 3),
		("2019-04-13", "2019-06-22", 70),
		("2019-06-22", "2019-06-22", 0)
	]
)
def test_estadisticas_viaje_mas_largo_existe(conexion, ida, vuelta, dias):

	conexion.insertarViaje(34, ida, vuelta, "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")

	assert conexion.estadistica_viaje_mas_largo()==dias

@pytest.mark.parametrize(["vueltas", "dias"],
	[
		(["2019-06-22", "2024-01-01", "2023-04-13", "2024-02-01"], 1654),
		(["2019-06-22", "2019-06-25", "2019-07-01", "2023-06-23"], 9),
		(["2019-06-22", "2019-06-22", "2019-06-22", "2023-06-22"], 0),
		(["2019-07-22", "2020-06-22", "2019-07-01", "2023-06-23"], 366),
		(["2022-07-22", "2020-02-22", "2019-06-08", "2023-06-23"], 1126),
		(["2019-06-22", "2019-06-23", "2019-06-22", "2023-06-22"], 1)
	]
)
def test_estadisticas_viaje_mas_largo_existen(conexion, vueltas, dias):

	conexion.insertarViaje(34, "2019-06-22", vueltas[0], "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")
	conexion.insertarViaje(34, "2019-06-22", vueltas[1], "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")
	conexion.insertarViaje(34, "2019-06-22", vueltas[2], "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")
	
	assert conexion.estadistica_viaje_mas_largo()==dias

def test_estadisticas_annos_mas_viajes_no_existen(conexion):

	assert conexion.estadistica_annos_mas_viajes() is None

@pytest.mark.parametrize(["anno"],
	[(2019,),(2023,),(2024,),(2022,)]
)
def test_estadisticas_annos_mas_viajes_existe(conexion, anno):

	conexion.insertarViaje(34, f"{anno}-06-22", "2024-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")

	assert conexion.estadistica_annos_mas_viajes()==[(1, anno)]

@pytest.mark.parametrize(["annos", "resultado"],
	[
		([2019, 2023, 2023, 2019, 2022, 2019], [(3, 2019)]),
		([2019, 2023, 2023, 2019, 2022, 2019, 2023], [(3, 2019),(3, 2023)]),
		([2019, 2023, 2023, 2019, 2022, 2019, 2023, 2019], [(4, 2019)]),
		([2019, 2023, 2023, 2019, 2022, 2019, 2023, 2019, 2022, 2022, 2023, 2022], [(4, 2019),(4, 2023),(4, 2022)])
	]
)
def test_estadisticas_annos_mas_viajes_existen(conexion, annos, resultado):

	for anno in annos:

		conexion.insertarViaje(34, f"{anno}-06-22", "2024-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")

	viajes_anno=conexion.estadistica_annos_mas_viajes()

	assert len(viajes_anno)==len(resultado)

	for viaje_anno in viajes_anno:

		assert viaje_anno in resultado

def test_estadisticas_anno_mas_viajes_no_existen(conexion):

	assert conexion.estadistica_anno_mas_viajes() is None

@pytest.mark.parametrize(["anno"],
	[(2019,),(2023,),(2024,),(2022,)]
)
def test_estadisticas_anno_mas_viajes_existe(conexion, anno):

	conexion.insertarViaje(34, f"{anno}-06-22", "2024-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")

	assert conexion.estadistica_anno_mas_viajes()==(1, anno)

@pytest.mark.parametrize(["annos", "resultado"],
	[
		([2019, 2023, 2023, 2019, 2022, 2019], (3, 2019)),
		([2019, 2023, 2023, 2019, 2022, 2019, 2023], (3, 2023)),
		([2019, 2023, 2023, 2019, 2022, 2019, 2023, 2019], (4, 2019)),
		([2019, 2023, 2023, 2019, 2022, 2019, 2023, 2019, 2022, 2022, 2023, 2022], (4, 2023))
	]
)
def test_estadisticas_anno_mas_viajes_existen(conexion, annos, resultado):

	for anno in annos:

		conexion.insertarViaje(34, f"{anno}-06-22", "2024-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")

	assert conexion.estadistica_anno_mas_viajes()==resultado

def test_estadisticas_ciudades_mas_viajes_no_existen(conexion):

	assert conexion.estadistica_ciudades_mas_viajes() is None

@pytest.mark.parametrize(["cod_ciudad", "ciudad", "pais"],
	[
		(34, "London", "Reino Unido"),
		(1, "Tokyo", "Japón"),
		(22, "Karachi", "Pakistán"),
		(13, "New York", "Estados Unidos")
	]
)
def test_estadisticas_ciudades_mas_viajes_existe(conexion, cod_ciudad, ciudad, pais):

	conexion.insertarViaje(cod_ciudad, "2019-06-22", "2024-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")

	assert conexion.estadistica_ciudades_mas_viajes()==[(1, ciudad, pais)]

@pytest.mark.parametrize(["cod_ciudades", "resultado"],
	[
		([34, 22, 1, 13, 22, 4, 34, 13, 34, 1], [(3, "London", "Reino Unido")]),
		([34, 22, 1, 13, 22, 4, 34, 13, 34, 1, 22], [(3, "London", "Reino Unido"), (3, "Karachi", "Pakistán")]),
		([34, 22, 1, 13, 22, 4, 34, 13, 34, 1, 22, 22], [(4, "Karachi", "Pakistán")]),
		([34, 22, 1, 13, 22, 4, 34, 13, 34, 1, 22, 22, 34, 1, 1], [(4, "London", "Reino Unido"), (4, "Karachi", "Pakistán"), (4, "Tokyo", "Japón")])
	]
)
def test_estadisticas_ciudades_mas_viajes_existen(conexion, cod_ciudades, resultado):

	for cod_ciudad in cod_ciudades:

		conexion.insertarViaje(cod_ciudad, "2019-06-22", "2024-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")

	viajes_ciudades=conexion.estadistica_ciudades_mas_viajes()

	assert len(viajes_ciudades)==len(resultado)

	for viaje_ciudad in viajes_ciudades:

		assert viaje_ciudad in resultado

def test_estadisticas_ciudad_mas_viajes_no_existen(conexion):

	assert conexion.estadistica_ciudad_mas_viajes() is None

@pytest.mark.parametrize(["cod_ciudad", "ciudad", "pais"],
	[
		(34, "London", "Reino Unido"),
		(1, "Tokyo", "Japón"),
		(22, "Karachi", "Pakistán"),
		(13, "New York", "Estados Unidos")
	]
)
def test_estadisticas_ciudad_mas_viajes_existe(conexion, cod_ciudad, ciudad, pais):

	conexion.insertarViaje(cod_ciudad, "2019-06-22", "2024-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")

	assert conexion.estadistica_ciudad_mas_viajes()==(1, ciudad, pais)

@pytest.mark.parametrize(["cod_ciudades", "resultado"],
	[
		([34, 22, 1, 13, 22, 4, 34, 13, 34, 1], (3, "London", "Reino Unido")),
		([34, 22, 1, 13, 22, 4, 34, 13, 34, 1, 22], (3, "Karachi", "Pakistán")),
		([34, 22, 1, 13, 22, 4, 34, 13, 34, 1, 22, 22], (4, "Karachi", "Pakistán")),
		([34, 22, 1, 13, 22, 4, 34, 13, 34, 1, 22, 22, 34, 1, 1], (4, "Karachi", "Pakistán"))
	]
)
def test_estadisticas_ciudad_mas_viajes_existen(conexion, cod_ciudades, resultado):

	for cod_ciudad in cod_ciudades:

		conexion.insertarViaje(cod_ciudad, "2019-06-22", "2024-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")

	assert conexion.estadistica_ciudad_mas_viajes()==resultado

def test_estadisticas_paises_mas_viajes_no_existen(conexion):

	assert conexion.estadistica_paises_mas_viajes() is None

@pytest.mark.parametrize(["cod_ciudad", "pais"],
	[
		(34, "Reino Unido"),
		(1, "Japón"),
		(22, "Pakistán"),
		(13, "Estados Unidos")
	]
)
def test_estadisticas_paises_mas_viajes_existe(conexion, cod_ciudad, pais):

	conexion.insertarViaje(cod_ciudad, "2019-06-22", "2024-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")

	assert conexion.estadistica_paises_mas_viajes()==[(1, pais)]

@pytest.mark.parametrize(["cod_ciudades", "resultado"],
	[
		([34, 22, 1, 13, 22, 4, 1185, 13, 1185, 1], [(3, "Reino Unido")]),
		([34, 22, 1, 13, 22, 4, 989, 13, 1185, 1, 22], [(3, "Reino Unido"), (3, "Pakistán")]),
		([34, 22, 1, 13, 33, 4, 34, 13, 34, 1, 33, 22], [(4, "Pakistán")]),
		([34, 22, 1, 13, 33, 4, 989, 13, 1185, 1, 236, 375, 603, 1, 1], [(4, "Reino Unido"), (4, "Pakistán"), (4, "Japón")])
	]
)
def test_estadisticas_paises_mas_viajes_existen(conexion, cod_ciudades, resultado):

	for cod_ciudad in cod_ciudades:

		conexion.insertarViaje(cod_ciudad, "2019-06-22", "2024-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")

	viajes_paises=conexion.estadistica_paises_mas_viajes()

	assert len(viajes_paises)==len(resultado)

	for viaje_pais in viajes_paises:

		assert viaje_pais in resultado

def test_estadisticas_pais_mas_viajes_no_existen(conexion):

	assert conexion.estadistica_pais_mas_viajes() is None

@pytest.mark.parametrize(["cod_ciudad", "pais"],
	[
		(34, "Reino Unido"),
		(1, "Japón"),
		(22, "Pakistán"),
		(13, "Estados Unidos")
	]
)
def test_estadisticas_pais_mas_viajes_existe(conexion, cod_ciudad, pais):

	conexion.insertarViaje(cod_ciudad, "2019-06-22", "2024-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")

	assert conexion.estadistica_pais_mas_viajes()==(1, pais)

@pytest.mark.parametrize(["cod_ciudades", "resultado"],
	[
		([34, 22, 1, 13, 22, 4, 1185, 13, 1185, 1], (3, "Reino Unido")),
		([34, 22, 1, 13, 22, 4, 989, 13, 1185, 1, 22], (3, "Pakistán")),
		([34, 22, 1, 13, 33, 4, 34, 13, 34, 1, 33, 22], (4, "Pakistán")),
		([34, 22, 1, 13, 33, 4, 989, 13, 1185, 1, 236, 375, 603, 1, 1], (4, "Japón"))
	]
)
def test_estadisticas_pais_mas_viajes_existen(conexion, cod_ciudades, resultado):

	for cod_ciudad in cod_ciudades:

		conexion.insertarViaje(cod_ciudad, "2019-06-22", "2024-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")

	assert conexion.estadistica_pais_mas_viajes()==resultado

def test_estadisticas_ciudad_mas_grande_no_existen(conexion):

	assert conexion.estadistica_ciudad_mas_grande() is None

@pytest.mark.parametrize(["cod_ciudad", "ciudad", "pais"],
	[
		(34, "London", "Reino Unido"),
		(1, "Tokyo", "Japón"),
		(22, "Karachi", "Pakistán"),
		(13, "New York", "Estados Unidos")
	]
)
def test_estadisticas_ciudad_mas_grande_existe(conexion, cod_ciudad, ciudad, pais):

	conexion.insertarViaje(cod_ciudad, "2019-06-22", "2024-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")

	poblacion, ciudad_grande, pais_ciudad=conexion.estadistica_ciudad_mas_grande()

	assert isinstance(poblacion, int)
	assert ciudad_grande==ciudad
	assert pais_ciudad==pais


@pytest.mark.parametrize(["cod_ciudades", "ciudad", "pais"],
	[
		([34, 122, 3546, 34, 546, 757], "London", "Reino Unido"),
		([34, 122, 3546, 34, 546, 757, 1], "Tokyo", "Japón"),
		([34, 122, 22, 3546, 34, 546, 757], "Karachi", "Pakistán"),
		([34, 122, 3546, 34, 546, 757, 34, 22, 13, 16], "New York", "Estados Unidos")
	]
)
def test_estadisticas_ciudad_mas_grande_existen(conexion, cod_ciudades, ciudad, pais):

	for cod_ciudad in cod_ciudades:

		conexion.insertarViaje(cod_ciudad, "2019-06-22", "2024-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")

	poblacion, ciudad_grande, pais_ciudad=conexion.estadistica_ciudad_mas_grande()

	assert isinstance(poblacion, int)
	assert ciudad_grande==ciudad
	assert pais_ciudad==pais

def test_estadisticas_ciudad_mas_lejana_no_existen(conexion):

	assert conexion.estadistica_ciudad_mas_lejana() is None

@pytest.mark.parametrize(["cod_ciudad", "ciudad", "pais"],
	[
		(34, "London", "Reino Unido"),
		(1, "Tokyo", "Japón"),
		(22, "Karachi", "Pakistán"),
		(13, "New York", "Estados Unidos")
	]
)
def test_estadisticas_ciudad_mas_lejana_existe(conexion, cod_ciudad, ciudad, pais):

	conexion.insertarViaje(cod_ciudad, "2019-06-22", "2024-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")

	distancia, ciudad_lejana, pais_ciudad=conexion.estadistica_ciudad_mas_lejana()

	assert isinstance(distancia, int)
	assert ciudad_lejana==ciudad
	assert pais_ciudad==pais

@pytest.mark.parametrize(["cod_ciudades", "ciudad", "pais"],
	[
		([1343, 34, 103, 160, 938, 35, 987], "London", "Reino Unido"),
		([35, 34, 1, 22, 13, 938, 103, 160, 16], "Tokyo", "Japón"),
		([22, 160, 938, 34, 721, 35, 21], "Karachi", "Pakistán"),
		([13, 34, 788, 160, 938, 35, 21, 160], "New York", "Estados Unidos")
	]
)
def test_estadisticas_ciudad_mas_lejana_existen(conexion, cod_ciudades, ciudad, pais):

	for cod_ciudad in cod_ciudades:

		conexion.insertarViaje(cod_ciudad, "2019-06-22", "2024-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")

	distancia, ciudad_lejana, pais_ciudad=conexion.estadistica_ciudad_mas_lejana()

	assert isinstance(distancia, int)
	assert ciudad_lejana==ciudad
	assert pais_ciudad==pais

def test_estadisticas_ciudad_mas_lejana_no_existen_origen_no_existe(conexion):

	assert conexion.estadistica_ciudad_mas_lejana(0) is None

@pytest.mark.parametrize(["cod_ciudad", "ciudad", "pais", "origen"],
	[
		(34, "London", "Reino Unido", 160),
		(1, "Tokyo", "Japón", 34),
		(22, "Karachi", "Pakistán", 35),
		(13, "New York", "Estados Unidos", 22)
	]
)
def test_estadisticas_ciudad_mas_lejana_existe_origen_existe(conexion, cod_ciudad, ciudad, pais, origen):

	conexion.insertarViaje(cod_ciudad, "2019-06-22", "2024-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")

	distancia, ciudad_lejana, pais_ciudad=conexion.estadistica_ciudad_mas_lejana(origen)

	assert isinstance(distancia, int)
	assert ciudad_lejana==ciudad
	assert pais_ciudad==pais

@pytest.mark.parametrize(["cod_ciudades", "ciudad", "pais", "origen"],
	[
		([13, 34, 788, 160, 938, 35, 21, 160, 22, 16], "Bangkok", "Tailandia", 160),
		([13, 34, 788, 160, 938, 35, 21, 160, 22, 16], "New York", "Estados Unidos", 22),
		([13, 34, 788, 160, 938, 35, 21, 160, 22, 16], "New York", "Estados Unidos", 21),
		([13, 34, 788, 160, 938, 35, 21, 160, 22, 16], "Karachi", "Pakistán", 28)
	]
)
def test_estadisticas_ciudad_mas_lejana_existen_origen_existe(conexion, cod_ciudades, ciudad, pais, origen):

	for cod_ciudad in cod_ciudades:

		conexion.insertarViaje(cod_ciudad, "2019-06-22", "2024-06-22", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")

	distancia, ciudad_lejana, pais_ciudad=conexion.estadistica_ciudad_mas_lejana(origen)

	assert isinstance(distancia, int)
	assert ciudad_lejana==ciudad
	assert pais_ciudad==pais

def test_ciudades_origen_poblacion_defecto(conexion):

	ciudades=conexion.ciudades_origen()

	assert len(ciudades)==67

@pytest.mark.parametrize(["poblacion", "numero_ciudades"],
	[
		(100000000, 52),
		(1000000, 148),
		(5000000, 82),
		(20000000, 57),
	]
)
def test_ciudades_origen_poblacion_variable(conexion, poblacion, numero_ciudades):

	ciudades=conexion.ciudades_origen(poblacion)

	assert len(ciudades)==numero_ciudades

@pytest.mark.parametrize(["codigo_ciudad"],
	[(0,), (100000,), (-1,), (24354366,)]
)
def test_nombre_ciudad_no_existe(conexion, codigo_ciudad):

	assert conexion.nombre_ciudad(codigo_ciudad) is None

@pytest.mark.parametrize(["codigo_ciudad", "nombre"],
	[
		(1, "Tokyo"), 
		(10000, "Nakapiripirit"), 
		(22, "Karachi"),
		(13, "New York"),
		(103, "Madrid"),
		(34, "London"),
		(160, "Barcelona")
	]
)
def test_nombre_ciudad_existe(conexion, codigo_ciudad, nombre):

	assert conexion.nombre_ciudad(codigo_ciudad)==nombre

@pytest.mark.parametrize(["inicio", "fin"],
	[
		("2023-08-06", "2022-01-13"),
		("2023-08-06", "2023-01-13"),
		("2022-08-06", "2022-01-13"),
		("2019-06-01", "2019-05-31"),
	]
)
def test_viajes_meses_fechas_incorrectas_no_existen_viajes(conexion, inicio, fin):

	assert conexion.viajes_por_meses(inicio, fin) is None

@pytest.mark.parametrize(["inicio", "fin", "meses"],
	[
		("2023-08-06", "2023-08-13", 1),
		("2019-06-22", "2019-06-22", 1),
		("2019-06-22", "2019-08-22", 3),
		("2019-06-22", "2020-06-13", 12),
		("2019-06-22", "2020-06-22", 13),
		("2022-05-01", "2023-04-07", 12),
		("2022-05-02", "2023-04-01", 11)
	]
)
def test_viajes_meses_no_existen_viajes(conexion, inicio, fin, meses):

	viajes_meses=conexion.viajes_por_meses(inicio, fin)

	assert len(viajes_meses)==meses

@pytest.mark.parametrize(["idas", "resultados"],
	[
		(["2019-06-06", "2019-06-06", "2019-06-06"], [("2019", "June", 3)]),
		(["2019-06-06", "2019-06-06", "2019-07-06"], [("2019", "June", 2), ("2019", "July", 1)]),
		(["2019-06-06", "2019-08-06", "2019-07-06"], [("2019", "June", 1), ("2019", "July", 1), ("2019", "August", 1)]),
	]
)
def test_viajes_meses_existen_viajes_rango_correcto(conexion, idas, resultados):

	for ida in idas:

		conexion.insertarViaje(34, ida, "2024-01-15", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")

	viajes_meses=conexion.viajes_por_meses("2019-06-22", "2019-10-23")

	for resultado in resultados:

		assert resultado in viajes_meses

@pytest.mark.parametrize(["idas", "resultados"],
	[
		(["2019-06-06", "2019-06-06", "2019-06-06", "2019-05-22"], [("2019", "May", 1)]),
		(["2019-06-06", "2019-06-06", "2019-06-06", "2019-05-22", "2019-01-13"], [("2019", "May", 1), ("2019", "January", 1)]),
		(["2019-06-06", "2019-06-06", "2019-02-06", "2019-05-22", "2019-01-13"], [("2019", "May", 1), ("2019", "January", 1), ("2019", "February", 1)]),
		(["2019-05-06", "2019-05-06", "2019-05-16", "2019-05-22", "2019-05-13"], [("2019", "May", 5)]),
	]
)
def test_viajes_meses_existen_viajes_rango_incorrecto(conexion, idas, resultados):

	for ida in idas:

		conexion.insertarViaje(34, ida, "2024-01-15", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")

	viajes_meses=conexion.viajes_por_meses("2019-06-22", "2019-10-23")

	for resultado in resultados:

		assert resultado not in viajes_meses

def test_anno_minimo_maximo_ida_no_existen_viajes(conexion):

	assert conexion.anno_minimo_maximo_ida() is None

@pytest.mark.parametrize(["anno"],
	[(2019,),(2023,),(2021,),(2010,),(2022,),(2024,)]
)
def test_anno_minimo_maximo_ida_existe_viaje(conexion, anno):

	conexion.insertarViaje(34, f"{anno}-06-22", "2024-01-15", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")

	assert conexion.anno_minimo_maximo_ida()==(anno, anno)

@pytest.mark.parametrize(["annos", "minimo", "maximo"],
	[
		([2019, 2023, 2021, 2010, 2022, 2024], 2010, 2024),
		([2019, 2023, 2021, 2019, 2023, 2024], 2019, 2024),
		([2009, 2023, 2021, 2010, 2022, 2023], 2009, 2023),
		([2019, 2019, 2019, 2019, 2019, 2019], 2019, 2019)
	]
)
def test_anno_minimo_maximo_ida_existen_viajes(conexion, annos, minimo, maximo):

	for anno in annos:

		conexion.insertarViaje(34, f"{anno}-06-22", "2024-01-15", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")

	assert conexion.anno_minimo_maximo_ida()==(minimo, maximo)

def test_obtener_imagenes_no_existen(conexion):

	assert conexion.obtenerImagenes()==[]

@pytest.mark.parametrize(["registros"],
	[(1,),(5,),(3,),(10,),(13,),(22,)]
)
def test_obtener_imagenes_existen_sin_imagen(conexion, registros):

	for _ in range(registros):

		conexion.insertarViaje(34, "2019-06-22", "2024-01-15", "Hotel", "www.google.com", "Transporte", "comentario", "Sin Imagen")

	assert conexion.obtenerImagenes()==[]

@pytest.mark.parametrize(["registros", "numero_imagenes"],
	[(1, 1),(5, 5),(3, 3),(10, 5),(13, 5),(22,5)]
)
def test_obtener_imagenes_existen_con_imagen(conexion, registros, numero_imagenes):

	for _ in range(registros):

		conexion.insertarViaje(34, "2019-06-22", "2024-01-15", "Hotel", "www.google.com", "Transporte", "comentario", "imagen.jpg")

	assert len(conexion.obtenerImagenes())==numero_imagenes

def test_obtener_transportes_mas_usados_no_existen_viajes(conexion):

	assert conexion.obtenerTransportesMasUsados() is None

@pytest.mark.parametrize(["transporte"],
	[("transporte",),("avion",),("coche",),("bus",)]
)
def test_obtener_transportes_mas_usados_existe(conexion, transporte):

	conexion.insertarViaje(34, "2019-06-22", "2024-01-15", "Hotel", "www.google.com", transporte, "comentario", "imagen.jpg")

	assert conexion.obtenerTransportesMasUsados()==[(transporte, 1)]

@pytest.mark.parametrize(["transportes", "resultados"],
	[
		(["transporte", "avion", "coche", "bus", "renfe", "tren"], [("avion",1),("bus",1),("coche",1)]),
		(["transporte", "avion", "coche", "bus", "bus", "tren"], [("bus",2),("avion",1),("coche",1)]),
		(["transporte", "avion", "avion", "bus", "avion", "tren"], [("avion",3),("bus",1),("transporte",1)]),
		(["transporte", "avion", "transporte", "bus", "avion", "tren"], [("avion",2),("transporte",2),("bus",1)]),
		(["transporte", "avion", "avion", "transporte", "transporte", "avion", "avion"], [("avion",4),("transporte",3)])
	]
)
def test_obtener_transportes_mas_usados_existen(conexion, transportes, resultados):

	for transporte in transportes:

		conexion.insertarViaje(34, "2019-06-22", "2024-01-15", "Hotel", "www.google.com", transporte, "comentario", "imagen.jpg")

	transportes=conexion.obtenerTransportesMasUsados()

	for resultado in resultados:

		assert resultado in transportes