"""Configuración compartida de pytest.

Estos tests usan un archivo JSON temporal para evitar tocar `datos/tareas.json`.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest


# Garantiza imports desde la raíz del proyecto (app.py, rutas/, servicios/, etc.).
RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
if str(RAIZ_PROYECTO) not in sys.path:
	sys.path.insert(0, str(RAIZ_PROYECTO))


from app import crear_aplicacion


@pytest.fixture()
def ruta_tareas_temporal(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
	"""Crea y configura un archivo `tareas.json` temporal para los tests."""
	ruta = tmp_path / "tareas.json"
	ruta.write_text("[]", encoding="utf-8")
	monkeypatch.setenv("TAREAS_JSON_PATH", str(ruta))
	return ruta


@pytest.fixture()
def cliente(ruta_tareas_temporal: Path):
	"""Cliente de pruebas Flask con storage aislado."""
	aplicacion = crear_aplicacion()
	aplicacion.config.update({"TESTING": True})
	with aplicacion.test_client() as cliente:
		yield cliente
