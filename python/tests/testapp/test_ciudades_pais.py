import pytest

@pytest.mark.parametrize(["pais"],
	[("jkjkjkjjk",), ("españa",), ("ReinoUnido",), ("ANDORRA",), ("Pais",)]
)
def test_pagina_ciudades_pais_no_existe(cliente, conexion, pais):

	respuesta=cliente.get(f"/ciudades_pais/{pais}")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/"
	assert "Redirecting..." in contenido

@pytest.mark.parametrize(["pais"],
	[("España",),("Netherlands",),("Reino Unido",),("Andorra",),("Emiratos Árabes Unidos",)]
)
def test_pagina_ciudades_pais_sin_visitada(cliente, conexion, pais):

	respuesta=cliente.get(f"/ciudades_pais/{pais}")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Ciudades del pais" in contenido
	assert pais in contenido
	assert "<th>Ciudad</th>" in contenido
	assert "<th>Poblacion</th>" in contenido
	assert "<th>Tipo de Ciudad</th>" in contenido
	assert "<th>Visitado</th>" in contenido
	assert ">Visitada" not in contenido
	assert "fas fa-check" not in contenido
	assert "No Visitada" in contenido
	assert "fas fa-times" in contenido
	assert ">Ordenar" in contenido
	assert "No Ordenar" not in contenido

@pytest.mark.parametrize(["pais", "ciudad"],
	[
		("España", "Madrid"),
		("Netherlands", "Amsterdam"),
		("Reino Unido", "London"),
		("Aruba", "Oranjestad"),
		("Emiratos Árabes Unidos", "Abu Dhabi")
	]
)
def test_pagina_ciudades_pais_visitada(cliente, conexion, pais, ciudad):

	data={"pais":pais,
			"ciudad":ciudad,
			"ida":"22/06/2019",
			"vuelta":"22/06/2019",
			"hotel":"h",
			"web":"www.google.com",
			"transporte":"t",
			"comentario":"Sin Comentario",
			"archivo_imagen":"Sin Imagen"}

	cliente.post("/insertar_viaje", data=data)

	respuesta=cliente.get(f"/ciudades_pais/{pais}")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Ciudades del pais" in contenido
	assert pais in contenido
	assert "<th>Ciudad</th>" in contenido
	assert "<th>Poblacion</th>" in contenido
	assert "<th>Tipo de Ciudad</th>" in contenido
	assert "<th>Visitado</th>" in contenido
	assert ">Visitada" in contenido
	assert "fas fa-check" in contenido
	assert "No Visitada" in contenido
	assert "fas fa-times" in contenido
	assert ">Ordenar" in contenido
	assert "No Ordenar" not in contenido

@pytest.mark.parametrize(["pais"],
	[("jkjkjkjjk",), ("españa",), ("ReinoUnido",), ("ANDORRA",), ("Pais",)]
)
def test_pagina_ciudades_pais_orden_no_existe(cliente, conexion, pais):

	respuesta=cliente.get(f"/ciudades_pais/{pais}?orden=True")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/"
	assert "Redirecting..." in contenido

@pytest.mark.parametrize(["pais"],
	[("España",),("Netherlands",),("Reino Unido",),("Andorra",),("Emiratos Árabes Unidos",)]
)
def test_pagina_ciudades_pais_orden_sin_visitada(cliente, conexion, pais):

	respuesta=cliente.get(f"/ciudades_pais/{pais}?orden=True")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Ciudades del pais" in contenido
	assert pais in contenido
	assert "<th>Ciudad</th>" in contenido
	assert "<th>Poblacion</th>" in contenido
	assert "<th>Tipo de Ciudad</th>" in contenido
	assert "<th>Visitado</th>" in contenido
	assert ">Visitada" not in contenido
	assert "fas fa-check" not in contenido
	assert "No Visitada" in contenido
	assert "fas fa-times" in contenido
	assert ">Ordenar" not in contenido
	assert "No Ordenar" in contenido

@pytest.mark.parametrize(["pais", "ciudad"],
	[
		("España", "Madrid"),
		("Netherlands", "Amsterdam"),
		("Reino Unido", "London"),
		("Aruba", "Oranjestad"),
		("Emiratos Árabes Unidos", "Abu Dhabi")
	]
)
def test_pagina_ciudades_pais_orden_visitada(cliente, conexion, pais, ciudad):

	data={"pais":pais,
			"ciudad":ciudad,
			"ida":"22/06/2019",
			"vuelta":"22/06/2019",
			"hotel":"h",
			"web":"www.google.com",
			"transporte":"t",
			"comentario":"Sin Comentario",
			"archivo_imagen":"Sin Imagen"}

	cliente.post("/insertar_viaje", data=data)

	respuesta=cliente.get(f"/ciudades_pais/{pais}?orden=True")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Ciudades del pais" in contenido
	assert pais in contenido
	assert "<th>Ciudad</th>" in contenido
	assert "<th>Poblacion</th>" in contenido
	assert "<th>Tipo de Ciudad</th>" in contenido
	assert "<th>Visitado</th>" in contenido
	assert ">Visitada" in contenido
	assert "fas fa-check" in contenido
	assert "No Visitada" in contenido
	assert "fas fa-times" in contenido
	assert ">Ordenar" not in contenido
	assert "No Ordenar" in contenido