import pytest

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