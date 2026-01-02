"""Servicio: Gestor de tareas.

Este módulo implementa persistencia de tareas usando un archivo JSON.

Reglas de este paso (según agents.md):
- No usar Flask.
- No crear endpoints.
- No usar base de datos.

Responsabilidades:
1) cargar_tareas():
   - Leer desde datos/tareas.json
   - Si el archivo no existe: crearlo con una lista vacía []
   - Convertir cada diccionario a objeto Tarea usando Tarea.desde_diccionario()
   - Regresar una lista de objetos Tarea

2) guardar_tareas(lista_tareas):
   - Recibir lista de objetos Tarea
   - Convertir cada Tarea a diccionario con a_diccionario()
   - Guardar en datos/tareas.json (formato legible con indentación)

Notas:
- Se usan rutas relativas robustas basadas en la ubicación del archivo (pathlib).
- Si el JSON está vacío o es inválido, se devuelve una lista vacía sin romper la app.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from modelos.tarea import Tarea


class GestorTareas:
	"""Gestiona la carga y el guardado de tareas en un archivo JSON."""

	@staticmethod
	def _obtener_ruta_archivo_tareas() -> Path:
		"""Obtiene la ruta absoluta al archivo datos/tareas.json.

		Se calcula de forma robusta a partir de la ubicación del archivo actual:
		- servicios/gestor_tareas.py -> raíz del proyecto -> datos/tareas.json
		"""
		# `__file__` apunta a este archivo; subimos a la raíz del proyecto.
		ruta_raiz_proyecto = Path(__file__).resolve().parent.parent
		return ruta_raiz_proyecto / "datos" / "tareas.json"

	@staticmethod
	def cargar_tareas() -> list[Tarea]:
		"""Carga tareas desde datos/tareas.json.

		Comportamiento:
		- Si el archivo no existe, lo crea con contenido [] y devuelve lista vacía.
		- Si el contenido está vacío o el JSON es inválido, devuelve lista vacía.
		- Si el contenido es una lista de diccionarios, convierte cada uno a `Tarea`.
		"""
		ruta_archivo_tareas = GestorTareas._obtener_ruta_archivo_tareas()

		# Si el archivo no existe, se crea con una lista vacía.
		if not ruta_archivo_tareas.exists():
			ruta_archivo_tareas.parent.mkdir(parents=True, exist_ok=True)
			ruta_archivo_tareas.write_text("[]", encoding="utf-8")
			return []

		# Leemos el contenido como texto. Si está vacío, devolvemos lista vacía.
		contenido_texto = ruta_archivo_tareas.read_text(encoding="utf-8").strip()
		if contenido_texto == "":
			return []

		# Interpretamos el contenido como JSON, tolerando contenido inválido.
		try:
			contenido_decodificado: Any = json.loads(contenido_texto)
		except json.JSONDecodeError:
			return []

		# El archivo debe contener una lista; si no, se considera vacío.
		if not isinstance(contenido_decodificado, list):
			return []

		lista_tareas: list[Tarea] = []
		for elemento in contenido_decodificado:
			# Cada elemento debe ser un diccionario con los campos de la tarea.
			if not isinstance(elemento, dict):
				continue
			try:
				tarea = Tarea.desde_diccionario(elemento)
			except (KeyError, TypeError, ValueError):
				# Si algún elemento está mal formado, se ignora sin romper el proceso.
				continue
			lista_tareas.append(tarea)

		return lista_tareas

	@staticmethod
	def guardar_tareas(lista_tareas: list[Tarea]) -> None:
		"""Guarda una lista de objetos `Tarea` en datos/tareas.json.

		- Convierte cada tarea a diccionario con `a_diccionario()`.
		- Guarda un JSON legible usando indentación.
		"""
		# Validación mínima del tipo de entrada.
		if not isinstance(lista_tareas, list):
			raise TypeError("lista_tareas debe ser una lista")

		lista_diccionarios: list[dict[str, Any]] = []
		for tarea in lista_tareas:
			# Se espera recibir instancias de `Tarea`.
			if not isinstance(tarea, Tarea):
				raise TypeError("lista_tareas debe contener objetos Tarea")
			lista_diccionarios.append(tarea.a_diccionario())

		ruta_archivo_tareas = GestorTareas._obtener_ruta_archivo_tareas()
		ruta_archivo_tareas.parent.mkdir(parents=True, exist_ok=True)

		# Guardamos JSON legible (indentación) y con caracteres Unicode intactos.
		contenido_texto = json.dumps(lista_diccionarios, ensure_ascii=False, indent=4)
		ruta_archivo_tareas.write_text(contenido_texto, encoding="utf-8")
