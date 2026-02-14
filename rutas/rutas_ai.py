"""Rutas de IA.

Este módulo define el Blueprint para endpoints de IA del Entregable 2.

Restricciones:
- Implementar únicamente endpoints /ai/tareas/* del Entregable 2.
- No persistir tareas.
- No modificar el CRUD existente.

Nota:
- La integración con el proveedor de IA está encapsulada en `servicios/servicio_ia.py`.
"""

from __future__ import annotations

from flask import Blueprint, jsonify, request

from servicios.servicio_ia import (
	generar_respuesta_prueba,
	obtener_categoria_simulada,
	obtener_estimacion_simulada,
	extraer_primer_numero_como_float,
	generar_analisis_riesgo,
	generar_mitigacion_riesgo,
)


plano_rutas_ai = Blueprint("rutas_ai", __name__, url_prefix="/ai")


@plano_rutas_ai.post("/tareas/describe")
def describir_tarea():
	"""Completa el campo "descripcion" de una tarea usando IA (simulada).

	Reglas:
	- Recibe una tarea en formato JSON.
	- Si "descripcion" está vacía, en blanco o es None: genera una descripción.
	- Si "descripcion" ya tiene contenido: devuelve la tarea sin modificar.
	- No persiste la tarea.
	"""
	datos_tarea = request.get_json(silent=True)
	if not isinstance(datos_tarea, dict):
		return jsonify({"mensaje": "El cuerpo de la solicitud debe ser un JSON"}), 400

	descripcion = datos_tarea.get("descripcion")	
	descripcion_vacia = descripcion is None or str(descripcion).strip() == ""

	if not descripcion_vacia:
		return jsonify(datos_tarea), 200

	titulo = datos_tarea.get("titulo")
	if titulo is None or str(titulo).strip() == "":
		return (
			jsonify({"mensaje": "Falta el campo requerido: titulo"}),
			400,
		)

	prioridad = datos_tarea.get("prioridad")
	estado = datos_tarea.get("estado")
	asignado_a = datos_tarea.get("asignado_a")
	categoria = datos_tarea.get("categoria")

	prompt = (
		"Genera una descripción clara, en español, sin markdown, en 2 a 5 oraciones. "
		"Contexto de la tarea: "
		f"titulo={str(titulo).strip()}"
	)
	if prioridad is not None and str(prioridad).strip() != "":
		prompt += f", prioridad={str(prioridad).strip()}"
	if estado is not None and str(estado).strip() != "":
		prompt += f", estado={str(estado).strip()}"
	if asignado_a is not None and str(asignado_a).strip() != "":
		prompt += f", asignado_a={str(asignado_a).strip()}"
	if categoria is not None and str(categoria).strip() != "":
		prompt += f", categoria={str(categoria).strip()}"

	descripcion_generada = generar_respuesta_prueba(prompt)
	datos_tarea["descripcion"] = descripcion_generada

	return jsonify(datos_tarea), 200


@plano_rutas_ai.post("/tareas/categorize")
def categorizar_tarea():
	"""Completa el campo "categoria" de una tarea usando IA (simulada).

	Reglas:
	- Recibe una tarea en formato JSON.
	- Si "categoria" está vacía, en blanco o es None: clasifica usando IA simulada.
	- Si "categoria" ya tiene contenido: devuelve la tarea sin modificar.
	- La categoría devuelta debe ser una de la lista controlada.
	- No persiste la tarea.
	"""
	datos_tarea = request.get_json(silent=True)
	if not isinstance(datos_tarea, dict):
		return jsonify({"mensaje": "El cuerpo de la solicitud debe ser un JSON"}), 400

	categoria = datos_tarea.get("categoria")
	categoria_vacia = categoria is None or str(categoria).strip() == ""
	if not categoria_vacia:
		return jsonify(datos_tarea), 200

	titulo = datos_tarea.get("titulo")
	if titulo is None or str(titulo).strip() == "":
		return (
			jsonify({"mensaje": "Falta el campo requerido: titulo"}),
			400,
		)

	descripcion = datos_tarea.get("descripcion")
	categoria_generada = obtener_categoria_simulada(
		titulo=str(titulo),
		descripcion=str(descripcion) if descripcion is not None else None,
	)

	datos_tarea["categoria"] = categoria_generada
	return jsonify(datos_tarea), 200


@plano_rutas_ai.post("/tareas/estimate")
def estimar_horas_tarea():
	"""Completa el campo "horas_estimadas" de una tarea usando IA (simulada).

	Reglas:
	- Recibe una tarea en formato JSON.
	- Si "horas_estimadas" está ausente, es null o es "": estima usando IA simulada.
	- Si "horas_estimadas" ya tiene valor: devuelve la tarea sin modificar.
	- La respuesta final debe contener "horas_estimadas" como número (float).
	- No persiste la tarea.
	"""
	datos_tarea = request.get_json(silent=True)
	if not isinstance(datos_tarea, dict):
		return jsonify({"mensaje": "El cuerpo de la solicitud debe ser JSON"}), 400

	titulo = datos_tarea.get("titulo")
	if titulo is None or str(titulo).strip() == "":
		return jsonify({"mensaje": "Falta el campo requerido: titulo"}), 400

	horas_estimadas = datos_tarea.get("horas_estimadas")
	horas_estimadas_vacias = (
		"horas_estimadas" not in datos_tarea
		or horas_estimadas is None
		or str(horas_estimadas).strip() == ""
	)
	if not horas_estimadas_vacias:
		return jsonify(datos_tarea), 200

	descripcion = datos_tarea.get("descripcion")
	respuesta_ia = obtener_estimacion_simulada(
		titulo=str(titulo),
		descripcion=str(descripcion) if descripcion is not None else None,
	)

	horas_estimadas_float = extraer_primer_numero_como_float(respuesta_ia)
	if horas_estimadas_float is None:
		return (
			jsonify(
				{
					"mensaje": "No se pudo interpretar horas_estimadas como número",
					"respuesta_ia": respuesta_ia,
				}
			),
			400,
		)

	datos_tarea["horas_estimadas"] = float(horas_estimadas_float)
	return jsonify(datos_tarea), 200


@plano_rutas_ai.post("/tareas/audit")
def auditar_riesgos_tarea():
	"""Completa analisis_riesgo y mitigacion_riesgo usando IA (simulada) en dos pasos.

	Reglas:
	- Recibe una tarea en formato JSON.
	- Si un campo ya viene con contenido, se mantiene y solo se genera lo faltante.
	- No persiste la tarea.
	"""
	datos_tarea = request.get_json(silent=True)
	if not isinstance(datos_tarea, dict):
		return jsonify({"mensaje": "El cuerpo de la solicitud debe ser JSON"}), 400

	titulo = datos_tarea.get("titulo")
	if titulo is None or str(titulo).strip() == "":
		return jsonify({"mensaje": "Falta el campo requerido: titulo"}), 400

	analisis_riesgo = datos_tarea.get("analisis_riesgo")
	mitigacion_riesgo = datos_tarea.get("mitigacion_riesgo")

	analisis_vacio = analisis_riesgo is None or str(analisis_riesgo).strip() == ""
	mitigacion_vacia = (
		mitigacion_riesgo is None or str(mitigacion_riesgo).strip() == ""
	)

	if analisis_vacio:
		analisis_riesgo_generado = generar_analisis_riesgo(datos_tarea)
		datos_tarea["analisis_riesgo"] = analisis_riesgo_generado
		analisis_riesgo = analisis_riesgo_generado

	if mitigacion_vacia:
		mitigacion_riesgo_generada = generar_mitigacion_riesgo(
			datos_tarea,
			str(analisis_riesgo) if analisis_riesgo is not None else "",
		)
		datos_tarea["mitigacion_riesgo"] = mitigacion_riesgo_generada

	return jsonify(datos_tarea), 200
