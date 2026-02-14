"""Tests de CRUD de tareas (persistencia JSON aislada)."""


def _body_tarea_base() -> dict:
	return {
		"titulo": "Tarea de prueba",
		"descripcion": "Descripción de prueba",
		"prioridad": "Media",
		"horas_estimadas": 1,
		"estado": "pendiente",
		"asignado_a": "Guillermo",
	}


def test_crud_completo(cliente):
	# Lista inicial vacía
	resp = cliente.get("/tareas")
	assert resp.status_code == 200
	assert resp.get_json() == []

	# Crear
	resp = cliente.post("/tareas", json=_body_tarea_base())
	assert resp.status_code == 201
	creada = resp.get_json()
	assert creada["identificador"] == "1"
	assert creada["titulo"] == "Tarea de prueba"

	# Obtener por id
	resp = cliente.get("/tareas/1")
	assert resp.status_code == 200
	assert resp.get_json()["identificador"] == "1"

	# Actualizar parcialmente
	resp = cliente.put("/tareas/1", json={"estado": "en_progreso"})
	assert resp.status_code == 200
	assert resp.get_json()["estado"] == "en_progreso"

	# Eliminar
	resp = cliente.delete("/tareas/1")
	assert resp.status_code == 200
	assert resp.get_json()["mensaje"] == "Tarea eliminada"

	# Verificar que ya no existe
	resp = cliente.get("/tareas/1")
	assert resp.status_code == 404
