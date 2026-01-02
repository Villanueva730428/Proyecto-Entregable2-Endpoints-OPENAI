"""Rutas de tareas.

En este módulo se define el Blueprint de tareas.

Reglas de este paso (según agents.md):
- Mantener funcionando GET /tareas y GET /tareas/<identificador>.
- Implementar POST /tareas para crear una tarea.
- Implementar PUT /tareas/<identificador> para actualizar una tarea.
- No implementar DELETE.

Funcionalidad:
- GET /tareas: lee las tareas desde `datos/tareas.json` usando `GestorTareas`.
- Convierte cada objeto `Tarea` a diccionario con `a_diccionario()`.
- Responde con JSON y código 200.
"""

from flask import Blueprint, jsonify, request

from servicios.gestor_tareas import GestorTareas
from modelos.tarea import Tarea


# Blueprint de rutas de tareas.
plano_rutas_tareas = Blueprint("rutas_tareas", __name__)


@plano_rutas_tareas.get("/tareas")
def obtener_tareas():
	"""Devuelve la lista de tareas almacenadas.

	- Carga tareas usando el servicio `GestorTareas`.
	- Convierte cada tarea a diccionario.
	- Devuelve una lista JSON.
	"""
	lista_tareas = GestorTareas.cargar_tareas()
	lista_diccionarios_tareas = [tarea.a_diccionario() for tarea in lista_tareas]
	return jsonify(lista_diccionarios_tareas), 200


@plano_rutas_tareas.get("/tareas/<identificador>")
def obtener_tarea_por_identificador(identificador: str):
	"""Devuelve una tarea específica por su identificador.

	Intención:
	- Reutilizar la carga de tareas desde `GestorTareas.cargar_tareas()`.
	- Buscar recorriendo la lista, comparando el identificador como string.
	
	Respuestas:
	- 200: si la tarea existe.
	- 404: si no se encuentra.
	"""
	# Cargamos todas las tareas y recorremos la lista para encontrar coincidencia.
	lista_tareas = GestorTareas.cargar_tareas()
	for tarea in lista_tareas:
		# Comparación directa como string (sin conversiones adicionales).
		if tarea.identificador == identificador:
			return jsonify(tarea.a_diccionario()), 200

	# Si no se encontró, devolvemos un mensaje claro con código 404.
	return (
		jsonify({"mensaje": f"No existe la tarea con identificador {identificador}"}),
		404,
	)


@plano_rutas_tareas.post("/tareas")
def crear_tarea():
	"""Crea una tarea nueva a partir de un body JSON.

	Intención:
	- Recibir datos JSON en el body.
	- Validar que existan los campos requeridos.
	- Asignar un identificador incremental automáticamente.
	- Guardar la lista actualizada en `datos/tareas.json` usando `GestorTareas`.
	
	Nota:
	- No se agregan validaciones avanzadas (duplicados, catálogos, etc.).
	"""
	# Leemos el body como JSON. silent=True evita excepciones si el body no es JSON.
	datos_tarea = request.get_json(silent=True)

	# Validamos que el body sea un objeto JSON (dict en Python).
	if not isinstance(datos_tarea, dict):
		return jsonify({"mensaje": "El body debe ser un JSON"}), 400

	# Validamos presencia de campos requeridos.
	campos_requeridos = [
		"titulo",
		"descripcion",
		"prioridad",
		"horas_estimadas",
		"estado",
		"asignado_a",
	]
	campos_faltantes = [
		campo for campo in campos_requeridos if campo not in datos_tarea
	]

	if campos_faltantes:
		return (
			jsonify(
				{
					"mensaje": "Faltan campos requeridos",
					"campos_faltantes": campos_faltantes,
				}
			),
			400,
		)

	# Cargamos tareas existentes para calcular el siguiente identificador.
	lista_tareas = GestorTareas.cargar_tareas()

	# Calculamos el máximo identificador numérico existente.
	maximo_identificador_numerico = 0
	for tarea in lista_tareas:
		try:
			identificador_numerico = int(str(tarea.identificador))
		except (TypeError, ValueError):
			# Si el identificador no es numérico, se ignora.
			continue
		if identificador_numerico > maximo_identificador_numerico:
			maximo_identificador_numerico = identificador_numerico

	# Si no hay tareas, el máximo será 0 y el nuevo será 1.
	nuevo_identificador = maximo_identificador_numerico + 1

	# Creamos el objeto Tarea con los datos recibidos.
	nueva_tarea = Tarea(
		identificador=str(nuevo_identificador),
		titulo=datos_tarea["titulo"],
		descripcion=datos_tarea["descripcion"],
		prioridad=datos_tarea["prioridad"],
		horas_estimadas=datos_tarea["horas_estimadas"],
		estado=datos_tarea["estado"],
		asignado_a=datos_tarea["asignado_a"],
	)

	# Agregamos y guardamos la lista actualizada.
	lista_tareas.append(nueva_tarea)
	GestorTareas.guardar_tareas(lista_tareas)

	# Devolvemos la tarea creada.
	return jsonify(nueva_tarea.a_diccionario()), 201


@plano_rutas_tareas.put("/tareas/<identificador>")
def actualizar_tarea(identificador: str):
	"""Actualiza (parcialmente) una tarea existente.

	Intención:
	- Recibir datos JSON en el body.
	- Buscar la tarea por identificador (comparación como string).
	- Actualizar solo los campos enviados (sin permitir cambiar el identificador).
	- Guardar la lista actualizada usando `GestorTareas.guardar_tareas()`.

	Respuestas:
	- 200: tarea actualizada.
	- 400: body no es JSON.
	- 404: la tarea no existe.
	"""
	# Leemos el body como JSON. silent=True evita excepciones si el body no es JSON.
	datos_actualizacion = request.get_json(silent=True)

	# Validamos que el body sea un objeto JSON (dict en Python).
	if not isinstance(datos_actualizacion, dict):
		return jsonify({"mensaje": "El cuerpo de la solicitud debe ser JSON"}), 400

	# Cargamos la lista actual y buscamos la tarea por identificador.
	lista_tareas = GestorTareas.cargar_tareas()
	for tarea in lista_tareas:
		if tarea.identificador != identificador:
			continue

		# Actualización parcial: solo se modifican campos permitidos presentes.
		campos_permitidos = [
			"titulo",
			"descripcion",
			"prioridad",
			"horas_estimadas",
			"estado",
			"asignado_a",
		]

		for campo in campos_permitidos:
			if campo in datos_actualizacion:
				setattr(tarea, campo, datos_actualizacion[campo])

		# Si llega un identificador en el body, se ignora (no se cambia).
		GestorTareas.guardar_tareas(lista_tareas)
		return jsonify(tarea.a_diccionario()), 200

	# Si no se encontró la tarea, devolvemos 404.
	return jsonify({"mensaje": "La tarea no existe"}), 404


@plano_rutas_tareas.delete("/tareas/<identificador>")
def eliminar_tarea(identificador: str):
	"""Elimina una tarea existente por su identificador.

	Intención:
	- Cargar la lista actual de tareas.
	- Encontrar la tarea por identificador (comparación como string).
	- Eliminarla de la lista.
	- Guardar la lista actualizada usando `GestorTareas.guardar_tareas()`.

	Respuestas:
	- 200: tarea eliminada.
	- 404: la tarea no existe.
	"""
	# Cargamos la lista actual y buscamos la tarea por identificador.
	lista_tareas = GestorTareas.cargar_tareas()

	for indice_tarea, tarea in enumerate(lista_tareas):
		if tarea.identificador == identificador:
			# Eliminamos la tarea encontrada y persistimos el cambio.
			del lista_tareas[indice_tarea]
			GestorTareas.guardar_tareas(lista_tareas)
			return jsonify({"mensaje": "Tarea eliminada"}), 200

	# Si no se encontró, devolvemos 404 con un mensaje claro.
	return jsonify({"mensaje": "La tarea no existe"}), 404
