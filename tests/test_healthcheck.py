"""Tests del endpoint de healthcheck."""


def test_get_root_devuelve_estado(cliente):
	respuesta = cliente.get("/")
	assert respuesta.status_code == 200
	assert respuesta.get_json() == {"estado": "aplicacion_en_ejecucion"}
