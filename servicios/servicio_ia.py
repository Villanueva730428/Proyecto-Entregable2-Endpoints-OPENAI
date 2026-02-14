"""Servicio: IA (OpenAI).

Este módulo encapsula funcionalidades de IA generativa para el Entregable 2.

Reglas obligatorias de este paso:
- Usar el SDK oficial de OpenAI.
- Credenciales solo por variables de entorno.
- No hardcodear claves ni imprimirlas.
- Mantener los contratos ya usados por los endpoints /ai (sin modificar rutas).
"""

from __future__ import annotations

import os
import re
from typing import Any

try:
	from openai import OpenAI
except Exception:  # pragma: no cover
	OpenAI = None  # type: ignore[assignment]


CATEGORIAS_PERMITIDAS = [
	"Frontend",
	"Backend",
	"Testing",
	"Infra",
	"DevOps",
	"Documentación",
	"Seguridad",
	"Datos",
	"Otro",
]


NOMBRE_MODELO_POR_DEFECTO = "gpt-4o-mini"


def _obtener_configuracion_openai() -> tuple[str, str]:
	api_key = os.getenv("OPENAI_API_KEY")
	nombre_modelo = os.getenv("OPENAI_MODEL", NOMBRE_MODELO_POR_DEFECTO)

	if api_key is None or api_key.strip() == "":
		raise ValueError("Falta configurar OPENAI_API_KEY")

	return api_key, nombre_modelo


def _obtener_cliente_openai() -> Any:
	if OpenAI is None:
		raise RuntimeError("Falta instalar la dependencia 'openai'")

	api_key, _nombre_modelo = _obtener_configuracion_openai()
	return OpenAI(api_key=api_key)


def _consultar_openai(texto_sistema: str, texto_usuario: str, temperatura: float = 0.2) -> str:
	"""Consulta OpenAI y devuelve texto plano.

	- Usa Responses API si está disponible.
	- Fallback a Chat Completions en versiones antiguas.
	"""
	_cliente = _obtener_cliente_openai()
	_api_key, nombre_modelo = _obtener_configuracion_openai()
	try:
		if hasattr(_cliente, "responses"):
			respuesta = _cliente.responses.create(
				model=nombre_modelo,
				input=[
					{"role": "system", "content": texto_sistema},
					{"role": "user", "content": texto_usuario},
				],
				temperature=temperatura,
			)
			texto = getattr(respuesta, "output_text", None)
			if isinstance(texto, str) and texto.strip() != "":
				return texto.strip()

		if hasattr(_cliente, "chat") and hasattr(_cliente.chat, "completions"):
			respuesta = _cliente.chat.completions.create(
				model=nombre_modelo,
				messages=[
					{"role": "system", "content": texto_sistema},
					{"role": "user", "content": texto_usuario},
				],
				temperature=temperatura,
			)
			contenido = respuesta.choices[0].message.content
			return (contenido or "").strip()

		raise RuntimeError("El SDK de OpenAI no expone un método compatible")
	except ValueError:
		raise
	except Exception as excepcion:
		status_code = getattr(excepcion, "status_code", None)
		codigo = getattr(excepcion, "code", None)
		mensaje_extra = ""
		if status_code == 401:
			mensaje_extra = " (401: autenticación fallida; revisa OPENAI_API_KEY)"
		elif status_code == 404:
			mensaje_extra = " (404: modelo no encontrado; revisa OPENAI_MODEL)"
		elif status_code == 429:
			mensaje_extra = " (429: rate limit/cuota; revisa límites y facturación)"
		elif isinstance(codigo, str) and codigo.strip() != "":
			mensaje_extra = f" (código: {codigo.strip()})"

		raise RuntimeError(f"Error al consultar el proveedor de IA{mensaje_extra}") from excepcion


def _normalizar_categoria(texto: str, categorias_permitidas: list[str]) -> str:
	texto_normalizado = (texto or "").strip().strip('"').strip("'").strip()
	texto_normalizado = texto_normalizado.rstrip(".:")
	if texto_normalizado == "":
		return "Otro"

	# Coincidencia exacta (ignorando mayúsculas/minúsculas).
	for categoria in categorias_permitidas:
		if texto_normalizado.casefold() == categoria.casefold():
			return categoria

	# Si viene texto adicional, intentamos encontrar una categoría contenida.
	for categoria in categorias_permitidas:
		if categoria.casefold() in texto_normalizado.casefold():
			return categoria

	# Permitir variantes sin acentos para "Documentación".
	if texto_normalizado.casefold() == "documentacion":
		return "Documentación"

	return "Otro"


def generar_respuesta_prueba(texto_entrada: str) -> str:
	"""Genera una respuesta de IA a partir de un texto de entrada.

	Parámetros:
	- texto_entrada: texto de entrada que normalmente se enviaría a un modelo.

	Retorna:
	- Texto generado por IA.
	"""
	if not isinstance(texto_entrada, str):
		raise TypeError("texto_entrada debe ser una cadena")

	texto_normalizado = texto_entrada.strip()
	if texto_normalizado == "":
		return ""

	texto_sistema = (
		"Eres un asistente que responde en español. "
		"No uses markdown. Responde solo con texto plano."
	)
	return _consultar_openai(texto_sistema=texto_sistema, texto_usuario=texto_normalizado)


def obtener_categoria_simulada(titulo: str, descripcion: str | None = None) -> str:
	"""Clasifica una tarea en una categoría permitida usando IA.

	Reglas:
	- Siempre devuelve una categoría dentro de `CATEGORIAS_PERMITIDAS`.
	"""
	if not isinstance(titulo, str):
		raise TypeError("titulo debe ser una cadena")
	if descripcion is not None and not isinstance(descripcion, str):
		raise TypeError("descripcion debe ser una cadena o None")

	texto_sistema = (
		"Eres un clasificador de tareas. "
		"Devuelve SOLO una categoría EXACTA de la lista proporcionada. "
		"No agregues explicaciones."
	)
	texto_usuario = (
		"Categorías permitidas: "
		+ ", ".join(CATEGORIAS_PERMITIDAS)
		+ "\n\n"
		+ "Título: "
		+ titulo.strip()
	)
	if descripcion is not None and descripcion.strip() != "":
		texto_usuario += "\nDescripción: " + descripcion.strip()

	respuesta = _consultar_openai(texto_sistema=texto_sistema, texto_usuario=texto_usuario)
	return _normalizar_categoria(respuesta, CATEGORIAS_PERMITIDAS)


def obtener_estimacion_simulada(titulo: str, descripcion: str | None = None) -> str:
	"""Devuelve una estimación de horas para una tarea usando IA.

	Reglas:
	- Retorna texto; el endpoint hará parsing del primer número a float.
	"""
	if not isinstance(titulo, str):
		raise TypeError("titulo debe ser una cadena")
	if descripcion is not None and not isinstance(descripcion, str):
		raise TypeError("descripcion debe ser una cadena o None")

	texto_sistema = (
		"Eres un estimador de esfuerzo. "
		"Devuelve SOLO un número en formato decimal con punto (por ejemplo 2.5). "
		"No incluyas unidades, palabras ni símbolos adicionales."
	)
	texto_usuario = "Título: " + titulo.strip()
	if descripcion is not None and descripcion.strip() != "":
		texto_usuario += "\nDescripción: " + descripcion.strip()

	return _consultar_openai(texto_sistema=texto_sistema, texto_usuario=texto_usuario)


def extraer_primer_numero_como_float(texto: str) -> float | None:
	"""Extrae el primer número (entero o decimal) y lo convierte a float.

	Ejemplos aceptados:
	- "2" -> 2.0
	- "2.5" -> 2.5
	- "2,5 horas" -> 2.5

	Retorna:
	- float si se pudo interpretar.
	- None si no se encontró un número.
	"""
	if not isinstance(texto, str):
		raise TypeError("texto debe ser una cadena")

	coincidencia = re.search(r"(\d+(?:[\.,]\d+)?)", texto)
	if coincidencia is None:
		return None

	numero_texto = coincidencia.group(1).replace(",", ".")
	try:
		return float(numero_texto)
	except ValueError:
		return None


def generar_analisis_riesgo(tarea: dict[str, Any]) -> str:
	"""Genera un análisis de riesgo para una tarea usando IA."""
	if not isinstance(tarea, dict):
		raise TypeError("tarea debe ser un diccionario")

	titulo = str(tarea.get("titulo", "")).strip()
	descripcion = str(tarea.get("descripcion", "")).strip()
	prioridad = str(tarea.get("prioridad", "")).strip()
	categoria = str(tarea.get("categoria", "")).strip()

	texto_sistema = (
		"Eres un asistente de gestión de proyectos. "
		"Genera un análisis de riesgo breve y útil en español (2 a 4 oraciones). "
		"No uses markdown."
	)
	texto_usuario = "Título: " + titulo
	if descripcion != "":
		texto_usuario += "\nDescripción: " + descripcion
	if prioridad != "":
		texto_usuario += "\nPrioridad: " + prioridad
	if categoria != "":
		texto_usuario += "\nCategoría: " + categoria

	return _consultar_openai(texto_sistema=texto_sistema, texto_usuario=texto_usuario)


def generar_mitigacion_riesgo(tarea: dict[str, Any], analisis_riesgo: str) -> str:
	"""Genera una mitigación de riesgo para una tarea usando IA.

	Usa `analisis_riesgo` como contexto (segunda llamada).
	"""
	if not isinstance(tarea, dict):
		raise TypeError("tarea debe ser un diccionario")
	if not isinstance(analisis_riesgo, str):
		raise TypeError("analisis_riesgo debe ser una cadena")

	titulo = str(tarea.get("titulo", "")).strip()
	descripcion = str(tarea.get("descripcion", "")).strip()

	texto_sistema = (
		"Eres un asistente de gestión de proyectos. "
		"Propón mitigaciones concretas y accionables en español. "
		"Devuelve de 3 a 6 acciones en una sola línea separadas por punto y coma. "
		"No uses markdown."
	)
	texto_usuario = "Título: " + titulo
	if descripcion != "":
		texto_usuario += "\nDescripción: " + descripcion
	texto_usuario += "\nAnálisis de riesgo: " + analisis_riesgo.strip()

	return _consultar_openai(texto_sistema=texto_sistema, texto_usuario=texto_usuario)


def generar_descripcion_tarea(tarea: dict[str, Any]) -> str:
	"""Genera la descripción de una tarea usando IA."""
	if not isinstance(tarea, dict):
		raise TypeError("tarea debe ser un diccionario")

	titulo = str(tarea.get("titulo", "")).strip()
	prioridad = str(tarea.get("prioridad", "")).strip()
	estado = str(tarea.get("estado", "")).strip()
	asignado_a = str(tarea.get("asignado_a", "")).strip()
	categoria = str(tarea.get("categoria", "")).strip()

	texto_sistema = (
		"Eres un asistente que redacta descripciones de tareas. "
		"Escribe en español, sin markdown, en 2 a 5 oraciones."
	)
	texto_usuario = "Título: " + titulo
	if prioridad != "":
		texto_usuario += "\nPrioridad: " + prioridad
	if estado != "":
		texto_usuario += "\nEstado: " + estado
	if asignado_a != "":
		texto_usuario += "\nAsignado a: " + asignado_a
	if categoria != "":
		texto_usuario += "\nCategoría: " + categoria

	return _consultar_openai(texto_sistema=texto_sistema, texto_usuario=texto_usuario)


def generar_categoria_tarea(tarea: dict[str, Any], categorias_permitidas: list[str]) -> str:
	"""Genera una categoría (controlada) para una tarea usando IA."""
	if not isinstance(tarea, dict):
		raise TypeError("tarea debe ser un diccionario")
	if not isinstance(categorias_permitidas, list) or any(
		not isinstance(categoria, str) for categoria in categorias_permitidas
	):
		raise TypeError("categorias_permitidas debe ser una lista de cadenas")

	titulo = str(tarea.get("titulo", "")).strip()
	descripcion = str(tarea.get("descripcion", "")).strip()

	texto_sistema = (
		"Eres un clasificador de tareas. "
		"Devuelve SOLO una categoría EXACTA de la lista proporcionada. "
		"No agregues explicaciones."
	)
	texto_usuario = "Categorías permitidas: " + ", ".join(categorias_permitidas)
	texto_usuario += "\nTítulo: " + titulo
	if descripcion != "":
		texto_usuario += "\nDescripción: " + descripcion

	respuesta = _consultar_openai(texto_sistema=texto_sistema, texto_usuario=texto_usuario)
	return _normalizar_categoria(respuesta, categorias_permitidas)


def generar_estimacion_horas(tarea: dict[str, Any]) -> str:
	"""Genera una estimación de horas (como texto) para una tarea usando IA."""
	if not isinstance(tarea, dict):
		raise TypeError("tarea debe ser un diccionario")

	titulo = str(tarea.get("titulo", "")).strip()
	descripcion = str(tarea.get("descripcion", "")).strip()
	prioridad = str(tarea.get("prioridad", "")).strip()

	texto_sistema = (
		"Eres un estimador de esfuerzo. "
		"Devuelve SOLO un número en formato decimal con punto (por ejemplo 2.5). "
		"No incluyas unidades, palabras ni símbolos adicionales."
	)
	texto_usuario = "Título: " + titulo
	if descripcion != "":
		texto_usuario += "\nDescripción: " + descripcion
	if prioridad != "":
		texto_usuario += "\nPrioridad: " + prioridad

	return _consultar_openai(texto_sistema=texto_sistema, texto_usuario=texto_usuario)
