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

@pytest.mark.parametrize(["ciudad",],
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