def test_pagina_viajes_sin_viajes(cliente, conexion):

	respuesta=cliente.get("/")

	contenido=respuesta.data.decode()

	respuesta.status_code==200
	assert "Viajes Realizados" in contenido
	assert "No hay viajes realizados..." in contenido

def test_pagina_viajes_con_viajes(cliente, conexion):

	conexion.c.execute(f"""INSERT INTO viajes (CodCiudad, Ida, Vuelta, Hotel, Web, Transporte)
							VALUES(22, '2019-06-22', '2019-06-22', 'Hotel', 'Web', 'Transporte')""")

	conexion.confirmar()

	respuesta=cliente.get("/")

	contenido=respuesta.data.decode()

	respuesta.status_code==200
	assert "Viajes Realizados" in contenido
	assert "No hay viajes realizados..." not in contenido
	assert "<table>" in contenido
	assert "<th>Viaje</th>" in contenido
	assert "<th>Ciudad</th>" in contenido
	assert "<th>Fecha</th>" in contenido