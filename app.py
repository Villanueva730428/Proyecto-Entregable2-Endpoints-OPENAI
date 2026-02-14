"""Aplicación principal (punto de entrada).

Reglas de este paso (según agents.md):
- Iniciar Flask e implementar SOLO el endpoint GET /tareas (en el Blueprint).
- No implementar otros endpoints todavía.

Este archivo:
- Crea la aplicación Flask.
- Registra el Blueprint de tareas.
- (Opcional) expone una ruta raíz "/" para verificación rápida.
"""

from flask import Flask, jsonify

from rutas.rutas_ai import plano_rutas_ai
from rutas.rutas_tareas import plano_rutas_tareas


def crear_aplicacion() -> Flask:
	"""Crea y configura la aplicación Flask.

	Se expone como factory para permitir tests con `pytest` sin necesidad de
	levantar un servidor real.
	"""
	aplicacion = Flask(__name__)

	# Registro del Blueprint que contiene endpoints CRUD.
	aplicacion.register_blueprint(plano_rutas_tareas)

	# Registro del Blueprint de IA (Entregable 2).
	aplicacion.register_blueprint(plano_rutas_ai)

	@aplicacion.get("/")
	def inicio():
		"""Ruta raíz opcional para verificar que la app está levantada."""
		return jsonify({"estado": "aplicacion_en_ejecucion"}), 200

	return aplicacion


# Instancia principal de la aplicación Flask (compatibilidad con ejecución directa).
aplicacion = crear_aplicacion()


if __name__ == "__main__":
	# Ejecuta el servidor de desarrollo.
	# debug=True permite recarga automática y mensajes de error útiles.
	aplicacion.run(debug=True)
