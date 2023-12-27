import pytest

def test_pagina_anadir_viaje(cliente, conexion):

	respuesta=cliente.get("/anadir_viaje")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Añadir viaje realizado" in contenido
	assert "<h3>Destino</h3>" in contenido
	assert "<h3>Fechas</h3>" in contenido
	assert "<h3>Detalles del Viaje</h3>" in contenido

@pytest.mark.parametrize(["ida", "vuelta"],
	[
		("2019-6-22", "2019-4-13"),
		("2019-4-13", "2019-4-12"),
		("2023-12-26", "2022-12-26")
	]
)
def test_pagina_comprobar_viaje_error_fechas(cliente, conexion, ida, vuelta):

	data={"pais":"España",
		"ciudad":"Madrid",
		"fecha-ida":ida,
		"fecha-vuelta":vuelta,
		"nombre-hotel":"Hotel",
		"pagina-web-hotel":"www.hotel.com",
		"transporte":"Transporte"}

	respuesta=cliente.post("/comprobar_viaje", data=data)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/anadir_viaje"
	assert "Redirecting..." in contenido

@pytest.mark.parametrize(["web"],
	[("hola.com",),("adios.es",),("www.hola",),("www.adios.net",),("ww.hola.com",),("www.mal.uk",)]
)
def test_pagina_comprobar_viaje_error_web(cliente, conexion, web):

	data={"pais":"España",
		"ciudad":"Madrid",
		"fecha-ida":"2019-4-13",
		"fecha-vuelta":"2019-6-22",
		"nombre-hotel":"Hotel",
		"pagina-web-hotel":web,
		"transporte":"Transporte"}

	respuesta=cliente.post("/comprobar_viaje", data=data)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/anadir_viaje"
	assert "Redirecting..." in contenido

@pytest.mark.parametrize(["comentario"],
	[
		("Comentariooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo",),
		("Comentarioooooooooooooooooooooooooooooooooooooooooooooooooooo",),
		("Comentarioooooooooooooooooooooooooooooooooooooooooooghfhfhfoooooooooooooooooooo",)
	]
)
def test_pagina_comprobar_viaje_comentario_error(cliente, conexion, comentario):

	data={"pais":"España",
		"ciudad":"Madrid",
		"fecha-ida":"2019-6-22",
		"fecha-vuelta":"2019-6-22",
		"nombre-hotel":"Hotel",
		"pagina-web-hotel":"www.miweb.com",
		"transporte":"Transporte",
		"comentario":comentario}

	respuesta=cliente.post("/comprobar_viaje", data=data)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/anadir_viaje"
	assert "Redirecting..." in contenido


def test_pagina_comprobar_viaje_comentario(cliente, conexion):

	data={"pais":"España",
		"ciudad":"Madrid",
		"fecha-ida":"2019-6-22",
		"fecha-vuelta":"2019-6-22",
		"nombre-hotel":"Hotel",
		"pagina-web-hotel":"www.miweb.com",
		"transporte":"Transporte",
		"comentario":"Comentario"}

	respuesta=cliente.post("/comprobar_viaje", data=data)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Resumen" in contenido
	assert "España" in contenido
	assert "Madrid" in contenido
	assert "2019-6-22" in contenido
	assert "Hotel" in contenido
	assert "www.miweb.com" in contenido
	assert "Transporte" in contenido
	assert "Comentario" in contenido


@pytest.mark.parametrize(["ida", "vuelta", "web"],
	[
		("2019-6-22", "2019-6-22", "www.hola.es"),
		("2019-4-13", "2019-4-14", "www.adios.com"),
		("2023-12-26", "2024-12-26", "www.miweb.es"),
	]
)
def test_pagina_comprobar_viaje(cliente, conexion, ida, vuelta, web):

	data={"pais":"España",
		"ciudad":"Madrid",
		"fecha-ida":ida,
		"fecha-vuelta":vuelta,
		"nombre-hotel":"Hotel",
		"pagina-web-hotel":web,
		"transporte":"Transporte"}

	respuesta=cliente.post("/comprobar_viaje", data=data)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Resumen" in contenido
	assert "España" in contenido
	assert "Madrid" in contenido
	assert ida in contenido
	assert vuelta in contenido
	assert "Hotel" in contenido
	assert web in contenido
	assert "Transporte" in contenido

def test_pagina_insertar_viaje_ciudad_no_existe(cliente, conexion):

	data={"pais":"España",
		"ciudad":"Londothgjhn",
		"fecha-ida":"2019-6-22",
		"fecha-vuelta":"2019-6-22",
		"nombre-hotel":"Hotel",
		"pagina-web-hotel":"www.mihotel.es",
		"transporte":"Transporte",
		"comentario":"Comentario"}

	respuesta=cliente.post("/insertar_viaje", data=data)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/anadir_viaje"
	assert "Redirecting..." in contenido

def test_pagina_insertar_viaje(cliente, conexion):

	data={"pais":"España",
		"ciudad":"London",
		"fecha-ida":"2019-6-22",
		"fecha-vuelta":"2019-6-22",
		"nombre-hotel":"Hotel",
		"pagina-web-hotel":"www.mihotel.es",
		"transporte":"Transporte",
		"comentario":"Comentario"}

	respuesta=cliente.post("/insertar_viaje", data=data)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/"
	assert "Redirecting..." in contenido

	conexion.c.execute("SELECT * FROM viajes")

	assert len(conexion.c.fetchall())==1

def test_pagina_insertar_viajes_multiples(cliente, conexion):

	data={"pais":"España",
		"ciudad":"London",
		"fecha-ida":"2019-6-22",
		"fecha-vuelta":"2019-6-22",
		"nombre-hotel":"Hotel",
		"pagina-web-hotel":"www.mihotel.es",
		"transporte":"Transporte",
		"comentario":"Comentario"}

	cliente.post("/insertar_viaje", data=data)
	cliente.post("/insertar_viaje", data=data)
	cliente.post("/insertar_viaje", data=data)
	cliente.post("/insertar_viaje", data=data)

	conexion.c.execute("SELECT * FROM viajes")

	assert len(conexion.c.fetchall())==4

def test_funcionalidad_completa_insertar_viaje(cliente, conexion):

	data={"pais":"España",
		"ciudad":"Madrid",
		"fecha-ida":"2019-06-22",
		"fecha-vuelta":"2019-06-22",
		"nombre-hotel":"Hotel",
		"pagina-web-hotel":"www.miweb.com",
		"transporte":"Transporte"}

	respuesta1=cliente.post("/comprobar_viaje", data=data)

	contenido1=respuesta1.data.decode()

	assert respuesta1.status_code==200
	assert "Resumen" in contenido1

	respuesta2=cliente.post("/insertar_viaje", data=data)

	contenido2=respuesta2.data.decode()

	assert respuesta2.status_code==302
	assert respuesta2.location=="/"

	conexion.c.execute("SELECT * FROM viajes")

	assert len(conexion.c.fetchall())==1