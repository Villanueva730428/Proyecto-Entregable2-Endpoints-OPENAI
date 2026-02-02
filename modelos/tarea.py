"""Modelo: Tarea.

Este módulo define la clase `Tarea`, que representa una tarea dentro del sistema.

Reglas de este paso (según agents.md):
- No usar Flask.
- No usar JSON.
- Implementar únicamente: __init__, a_diccionario(), desde_diccionario().

Campos del modelo:
- identificador
- titulo
- descripcion
- prioridad
- horas_estimadas
- estado
- asignado_a

Campos nuevos (Entregable 2 - IA):
- categoria
- analisis_riesgo
- mitigacion_riesgo
"""

from __future__ import annotations

from typing import Any


class Tarea:
	"""Representa una tarea del sistema.

	Esta clase es un contenedor simple de datos y provee:
	- Conversión a diccionario (para transporte o persistencia en pasos posteriores).
	- Construcción desde diccionario (para reconstruir instancias).
	"""

	def __init__(
		self,
		identificador: str,
		titulo: str,
		descripcion: str,
		prioridad: str,
		horas_estimadas: float,
		estado: str,
		asignado_a: str,
		categoria: str | None = None,
		analisis_riesgo: str | None = None,
		mitigacion_riesgo: str | None = None,
	) -> None:
		"""Inicializa una instancia de `Tarea`.

		Parámetros:
		- identificador: identificador único de la tarea.
		- titulo: título corto de la tarea.
		- descripcion: descripción detallada.
		- prioridad: nivel de prioridad (por ejemplo: baja, media, alta).
		- horas_estimadas: número de horas estimadas para completar la tarea.
		- estado: estado actual (por ejemplo: pendiente, en_progreso, completada).
		- asignado_a: usuario responsable de la tarea.
		- categoria: categoría de la tarea (opcional).
		- analisis_riesgo: análisis de riesgo (opcional).
		- mitigacion_riesgo: mitigación del riesgo (opcional).
		"""
		# Guardamos cada campo en la instancia.
		# No se implementan validaciones avanzadas en este paso.
		self.identificador = identificador
		self.titulo = titulo
		self.descripcion = descripcion
		self.prioridad = prioridad
		self.horas_estimadas = horas_estimadas
		self.estado = estado
		self.asignado_a = asignado_a
		self.categoria = categoria
		self.analisis_riesgo = analisis_riesgo
		self.mitigacion_riesgo = mitigacion_riesgo

	def a_diccionario(self) -> dict[str, Any]:
		"""Convierte la tarea a un diccionario.

		Este diccionario está pensado para:
		- serialización en pasos posteriores (por ejemplo, guardado en archivo).
		- respuestas de API en pasos posteriores.
		
		En este paso solo devolvemos un `dict` de Python (sin JSON).
		"""
		# Se devuelve un diccionario con las claves esperadas.
		return {
			"identificador": self.identificador,
			"titulo": self.titulo,
			"descripcion": self.descripcion,
			"prioridad": self.prioridad,
			"horas_estimadas": self.horas_estimadas,
			"estado": self.estado,
			"asignado_a": self.asignado_a,
			"categoria": self.categoria,
			"analisis_riesgo": self.analisis_riesgo,
			"mitigacion_riesgo": self.mitigacion_riesgo,
		}

	@staticmethod
	def desde_diccionario(diccionario_tarea: dict[str, Any]) -> Tarea:
		"""Crea una instancia de `Tarea` a partir de un diccionario.

		Requisitos mínimos:
		- `diccionario_tarea` debe contener las claves del modelo.

		Nota:
		- No se usa JSON; el parámetro ya debe ser un diccionario de Python.
		"""
		# Verificación básica del tipo de entrada.
		if not isinstance(diccionario_tarea, dict):
			raise TypeError("diccionario_tarea debe ser un diccionario")

		# Accedemos a cada campo. Si falta alguno, Python lanzará KeyError.
		return Tarea(
			identificador=str(diccionario_tarea["identificador"]),
			titulo=str(diccionario_tarea["titulo"]),
			descripcion=str(diccionario_tarea["descripcion"]),
			prioridad=str(diccionario_tarea["prioridad"]),
			horas_estimadas=float(diccionario_tarea["horas_estimadas"]),
			estado=str(diccionario_tarea["estado"]),
			asignado_a=str(diccionario_tarea["asignado_a"]),
			categoria=(
				str(diccionario_tarea["categoria"]) if "categoria" in diccionario_tarea else None
			),
			analisis_riesgo=(
				str(diccionario_tarea["analisis_riesgo"])
				if "analisis_riesgo" in diccionario_tarea
				else None
			),
			mitigacion_riesgo=(
				str(diccionario_tarea["mitigacion_riesgo"])
				if "mitigacion_riesgo" in diccionario_tarea
				else None
			),
		)
