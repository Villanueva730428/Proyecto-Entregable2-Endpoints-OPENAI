# ============================================================
# AGENT DE DESARROLLO FLASK – ENTREGABLE 1
# ============================================================
# Este archivo define las reglas, el comportamiento y la forma
# de trabajo del agente de IA que asistirá en el desarrollo
# del proyecto Flask de gestión de tareas.
#
# IMPORTANTE:
# - Este archivo se lee como guía operativa.
# - Los comentarios explican QUÉ debe hacerse y POR QUÉ.
# - El código se desarrolla paso a paso y se prueba en cada fase.
# ============================================================


# ============================================================
# 1. REGLAS DE NOMBRADO (OBLIGATORIAS)
# ============================================================
# Todas las variables, funciones, clases y métodos del proyecto
# deben cumplir estas reglas SIN EXCEPCIÓN.
#
# Estas reglas existen para:
# - Facilitar la comprensión del código
# - Mejorar el aprendizaje
# - Permitir comparar intención vs implementación
#
# REGLAS:
#
# 1. TODO debe estar en español
#    Aplica a:
#    - Variables
#    - Funciones
#    - Métodos
#    - Clases
#    - Parámetros
#
#    Ejemplo correcto:
#       gestor_tareas
#       crear_tarea
#       descripcion_tarea
#
#    Ejemplo incorrecto:
#       task_manager
#       create_task
#       task_description
#
# 2. Usar snake_case en todo momento
#
#    Correcto:
#       horas_estimadas
#       estado_tarea
#
#    Incorrecto:
#       horasEstimadas
#       estadoTarea
#
# 3. No usar abreviaturas
#
#    Correcto:
#       descripcion
#       identificador_tarea
#
#    Incorrecto:
#       desc
#       id_t
#
# 4. Los nombres deben reflejar INTENCIÓN
#    El nombre debe permitir entender su propósito
#    sin necesidad de leer la implementación.
#
# 5. Preferir claridad sobre brevedad
#
# El agente debe:
# - Respetar estrictamente estas reglas
# - Corregir cualquier violación detectada
# - Señalar inconsistencias si aparecen
# ============================================================


# ============================================================
# 2. CONTEXTO DE EJECUCIÓN
# ============================================================
# Sistema operativo: Windows
# Editor: Visual Studio Code
# Asistente: GitHub Copilot + este agente
# Lenguaje: Python 3.12.0
# Framework: Flask
#
# El agente debe asumir ejecución desde:
# - PowerShell
# - Terminal integrada de VS Code
#
# ENTORNO VIRTUAL:
# - Se debe usar un entorno virtual (venv) para el proyecto
# - El entorno virtual debe crearse en la raíz del proyecto
# - El agente debe asumir que el entorno virtual está activado
#   antes de ejecutar cualquier comando o script
#
# Ejemplo de activación en Windows:
#   venv\Scripts\activate
#
# El agente NO debe:
# - Instalar dependencias fuera del entorno virtual
#
# El agente SÍ debe:
# - Recordar activar el entorno virtual al iniciar el proyecto
# ============================================================


# ============================================================
# 3. OBJETIVO DEL PROYECTO
# ============================================================
# Construir una API REST en Flask para la gestión de tareas
# asignadas a usuarios, usando un archivo JSON como almacenamiento.
#
# Este entregable es la BASE del proyecto para módulos futuros.
# ============================================================


# ============================================================
# 4. FILOSOFÍA DE DESARROLLO
# ============================================================
# El desarrollo debe ser INCREMENTAL.
#
# Regla principal:
# - No avanzar al siguiente paso sin que el actual:
#   - esté implementado
#   - esté ejecutándose
#   - haya sido probado
#
# Cada bloque de código debe:
# - Tener comentarios que expliquen la funcionalidad
# - Poder compararse fácilmente con la implementación
#
# El agente debe:
# - Explicar qué se va a hacer ANTES de escribir código
# - Evitar complejidad innecesaria
# ============================================================


# ============================================================
# 5. ARQUITECTURA DEL PROYECTO (OBJETIVO FINAL)
# ============================================================
# Estructura esperada:
#
# proyecto/
# ├── app.py
# ├── rutas/
# │   └── rutas_tareas.py
# ├── modelos/
# │   └── tarea.py
# ├── servicios/
# │   └── gestor_tareas.py
# ├── datos/
# │   └── tareas.json
# ├── venv/
# ├── requirements.txt
#
# El agente debe construir esta estructura PASO A PASO.
# ============================================================


# ============================================================
# 6. MODELO DE DATOS: CLASE TAREA
# ============================================================
# Representa una tarea del sistema.
#
# Campos:
# - identificador
# - titulo
# - descripcion
# - prioridad
# - horas_estimadas
# - estado
# - asignado_a
#
# Métodos:
# - a_diccionario(): convierte el objeto en dict
# - desde_diccionario(): crea una tarea desde un dict
#
# El agente debe:
# - Implementar esta clase primero
# - Probarla de forma aislada
# ============================================================


# ============================================================
# 7. GESTIÓN DE DATOS: GESTOR_TAREAS
# ============================================================
# Responsable de leer y escribir tareas en un archivo JSON.
#
# Métodos estáticos:
# - cargar_tareas()
# - guardar_tareas(lista_tareas)
#
# Reglas:
# - Si el archivo no existe, debe crearse
# - No usar base de datos en este entregable
#
# El agente debe:
# - Probar esta clase sin Flask
# ============================================================


# ============================================================
# 8. API FLASK – ENDPOINTS
# ============================================================
# Endpoints requeridos:
#
# POST   /tareas
# GET    /tareas
# GET    /tareas/<identificador>
# PUT    /tareas/<identificador>
# DELETE /tareas/<identificador>
#
# Reglas:
# - Respuestas en JSON
# - Manejo básico de errores
#
# El agente debe:
# - Implementar primero GET /tareas
# - Avanzar endpoint por endpoint
# ============================================================


# ============================================================
# 9. REGLAS DE COMPORTAMIENTO DEL AGENTE
# ============================================================
# El agente NO debe:
# - Saltar pasos
# - Introducir patrones avanzados innecesarios
#
# El agente SÍ debe:
# - Detenerse si algo falla
# - Explicar errores
# - Corregir antes de avanzar
# ============================================================


# ============================================================
# 10. CRITERIO DE ÉXITO
# ============================================================
# El entregable es correcto cuando:
# - Flask levanta sin errores
# - Todos los endpoints funcionan
# - Las tareas se guardan en JSON
# - La arquitectura coincide con lo definido
# ============================================================


# ============================================================
# FIN DEL ARCHIVO agents.md
# ============================================================

