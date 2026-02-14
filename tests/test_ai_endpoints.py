"""Tests de endpoints IA.

Se mockean las funciones importadas en `rutas.rutas_ai` para evitar llamadas reales
al proveedor OpenAI.
"""

from __future__ import annotations

import pytest


def test_ai_describe_completa_descripcion(cliente, monkeypatch: pytest.MonkeyPatch):
	import rutas.rutas_ai as rutas_ai

	monkeypatch.setattr(rutas_ai, "generar_respuesta_prueba", lambda _prompt: "Desc generada")

	resp = cliente.post(
		"/ai/tareas/describe",
		json={"titulo": "Algo", "descripcion": ""},
	)
	assert resp.status_code == 200
	assert resp.get_json()["descripcion"] == "Desc generada"


def test_ai_categorize_completa_categoria(cliente, monkeypatch: pytest.MonkeyPatch):
	import rutas.rutas_ai as rutas_ai

	monkeypatch.setattr(rutas_ai, "obtener_categoria_simulada", lambda titulo, descripcion=None: "Backend")

	resp = cliente.post(
		"/ai/tareas/categorize",
		json={"titulo": "API", "descripcion": "", "categoria": ""},
	)
	assert resp.status_code == 200
	assert resp.get_json()["categoria"] == "Backend"


def test_ai_estimate_parsea_float(cliente, monkeypatch: pytest.MonkeyPatch):
	import rutas.rutas_ai as rutas_ai

	monkeypatch.setattr(rutas_ai, "obtener_estimacion_simulada", lambda titulo, descripcion=None: "2.5")

	resp = cliente.post(
		"/ai/tareas/estimate",
		json={"titulo": "Estimar", "descripcion": "", "horas_estimadas": None},
	)
	assert resp.status_code == 200
	assert resp.get_json()["horas_estimadas"] == 2.5


def test_ai_estimate_devuelve_400_si_no_parsea(cliente, monkeypatch: pytest.MonkeyPatch):
	import rutas.rutas_ai as rutas_ai

	monkeypatch.setattr(rutas_ai, "obtener_estimacion_simulada", lambda titulo, descripcion=None: "mucho")

	resp = cliente.post(
		"/ai/tareas/estimate",
		json={"titulo": "Estimar", "descripcion": "", "horas_estimadas": None},
	)
	assert resp.status_code == 400
	assert resp.get_json()["mensaje"] == "No se pudo interpretar horas_estimadas como número"


def test_ai_audit_solo_genera_lo_faltante(cliente, monkeypatch: pytest.MonkeyPatch):
	import rutas.rutas_ai as rutas_ai

	def _no_deberia_llamarse(_tarea):
		raise AssertionError("No se debía generar analisis_riesgo")

	monkeypatch.setattr(rutas_ai, "generar_analisis_riesgo", _no_deberia_llamarse)
	monkeypatch.setattr(
		rutas_ai,
		"generar_mitigacion_riesgo",
		lambda tarea, analisis_riesgo: "Mitigación generada",
	)

	resp = cliente.post(
		"/ai/tareas/audit",
		json={
			"titulo": "Auditar",
			"descripcion": "",
			"analisis_riesgo": "Riesgo ya definido",
			"mitigacion_riesgo": "",
		},
	)
	assert resp.status_code == 200
	data = resp.get_json()
	assert data["analisis_riesgo"] == "Riesgo ya definido"
	assert data["mitigacion_riesgo"] == "Mitigación generada"
