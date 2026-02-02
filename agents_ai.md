# ============================================================
# AGENT DE DESARROLLO IA
# EXTENSIÓN DEL PROYECTO FLASK – ENTREGABLE 2
# ============================================================
# Este archivo define reglas, objetivos y contratos para
# extender el proyecto Flask (Entregable 1) con endpoints de IA.
#
# IMPORTANTE:
# - Este NO es un proyecto nuevo.
# - DEPENDE del agents_core.md (Entregable 1).
# - No romper el CRUD ya existente.
# - Todas las reglas del core siguen vigentes (español, snake_case,
#   sin abreviaturas, incremental).
# ============================================================


# ============================================================
# 1. DEPENDENCIA DEL PROYECTO BASE (NO NEGOCIABLE)
# ============================================================
# El proyecto base ya implementa CRUD sobre "Tarea" y persiste en JSON.
# Este entregable agrega endpoints /ai/* sin modificar el CRUD.
# ============================================================


# ============================================================
# 2. ALCANCE DEL AGENTE IA
# ============================================================
# Este agente implementa:
# - Extensión del modelo Tarea con nuevos campos
# - Servicio de IA para encapsular llamadas a LLM
# - Endpoints /ai/tareas/*
#
# Este agente NO implementa:
# - UI
# - Autenticación
# - Base de datos
# ============================================================


# ============================================================
# 3. MODELO TAREA (CONTRATO ACTUALIZADO)
# ============================================================
# Campos existentes (ya presentes en el CRUD):
# - identificador
# - titulo
# - descripcion
# - prioridad
# - horas_estimadas
# - estado
# - asignado_a
#
# Campos nuevos (Entregable 2):
# - categoria            (str, opcional)
# - analisis_riesgo      (str, opcional)
# - mitigacion_riesgo    (str, opcional)
#
# Compatibilidad:
# - Las tareas antiguas pueden no incluir estos campos.
# - desde_diccionario() debe usar valores por defecto cuando falten.
# - a_diccionario() debe incluir los nuevos campos (aunque sean None o "").
#
# NOTA:
# - La IA solo "completa" campos; NO persiste automáticamente a menos
#   que explícitamente se decida (por defecto, estos endpoints devuelven
#   la tarea con campos completados y el cliente decide si guarda vía POST/PUT).
# ============================================================


# ============================================================
# 4. CONFIGURACIÓN DE IA (SECRETOS)
# ============================================================
# Se permite OpenAI como proveedor.
# Reglas:
# - Credenciales solo por variables de entorno
# - No hardcodear claves ni endpoints
# - No versionar secretos
#
# Dependencia sugerida (según el documento):
# - pip install openai
# ============================================================


# ============================================================
# 5. ARQUITECTURA RECOMENDADA PARA IA
# ============================================================
# Se recomienda encapsular IA en:
# servicios/servicio_ia.py
#
# Responsabilidad de servicio_ia:
# - Centralizar llamadas al LLM
# - Mantener prompts en funciones dedicadas
# - Retornar resultados ya "limpios" (texto o número)
#
# Los endpoints /ai deben:
# - Validar inputs mínimos
# - Llamar al servicio
# - Devolver JSON con la "tarea" enriquecida
# ============================================================


# ============================================================
# 6. CONTRATOS POR ENDPOINT (ENTRADA/SALIDA/ERRORES/EJEMPLOS)
# ============================================================
# IMPORTANTE:
# - Todos los endpoints /ai reciben JSON con estructura de "tarea".
# - Todos devuelven JSON con la misma tarea, pero con campos completados.
# - No se requiere que el endpoint guarde la tarea en tasks.json, a menos
#   que el usuario lo pida explícitamente. (Por defecto: NO persistir.)
#
# Convención de respuesta sugerida:
# - status 200 si IA completó el campo
# - status 400 si faltan campos necesarios o el JSON es inválido
# - status 500 si falla el proveedor de IA (error controlado)
# ============================================================


# ------------------------------------------------------------
# 6.1 POST /ai/tareas/describe
# ------------------------------------------------------------
# Propósito:
# - Generar "descripcion" con IA cuando llega vacía.
#
# Entrada esperada:
# - JSON de tarea donde "descripcion" sea "" o None.
# - Debe existir al menos "titulo" (y opcionalmente prioridad, categoria, etc.)
#
# Reglas mínimas:
# - Si descripcion ya viene con contenido, devolverla sin cambios
#   (o devolver 400 si se quiere forzar "debe estar vacía"; por defecto: no error).
#
# Campo que completa:
# - descripcion (texto largo coherente con el título y el contexto)
#
# Ejemplo de request:
# {
#   "titulo": "Implementar endpoint de listado",
#   "descripcion": "",
#   "prioridad": "media",
#   "estado": "pendiente",
#   "asignado_a": "Guillermo",
#   "categoria": "Backend"
# }
#
# Ejemplo de response:
# {
#   "titulo": "...",
#   "descripcion": "Descripción generada por IA ...",
#   ...
# }
#
# Prompting recomendado:
# - Pedir una descripción clara, completa, en español, con 2-5 oraciones.
# - No incluir formato markdown.
# ------------------------------------------------------------


# ------------------------------------------------------------
# 6.2 POST /ai/tareas/categorize
# ------------------------------------------------------------
# Propósito:
# - Clasificar la tarea bajo una categoría (Frontend, Backend, Testing, Infra, etc.)
#
# Entrada esperada:
# - JSON de tarea donde "categoria" sea "" o None.
# - Deben existir "titulo" y preferentemente "descripcion" (si no hay descripcion,
#   categorizar solo con titulo y prioridad).
#
# Campo que completa:
# - categoria (string)
#
# Reglas mínimas:
# - Definir una lista controlada de categorías para reducir ambigüedad.
#   Ejemplo: ["Frontend","Backend","Testing","Infra","DevOps","Documentación","Seguridad","Datos","Otro"]
# - El LLM debe devolver SOLO una de esas categorías.
#
# Ejemplo de request:
# {
#   "titulo": "Crear pruebas unitarias de GestorTareas",
#   "descripcion": "Agregar pruebas para carga/guardado de JSON...",
#   "categoria": ""
# }
#
# Ejemplo de response:
# {
#   "categoria": "Testing",
#   ...
# }
#
# Prompting recomendado:
# - "Devuelve solo una palabra exactamente igual a una categoría permitida."
# ------------------------------------------------------------


# ------------------------------------------------------------
# 6.3 POST /ai/tareas/estimate
# ------------------------------------------------------------
# Propósito:
# - Estimar el esfuerzo en horas (horas_estimadas) con IA.
#
# Entrada esperada:
# - JSON de tarea donde "horas_estimadas" sea null/""/ausente.
# - Debe existir "titulo".
# - Debe existir "descripcion" y "categoria" idealmente.
#
# Campo que completa:
# - horas_estimadas (NUMÉRICO, float)
#
# Reglas críticas:
# - La salida del LLM debe parsearse a float.
# - El prompt debe forzar salida numérica (sin texto adicional).
# - Si el parse falla:
#   - retornar 400 con mensaje claro, o
#   - reintentar con un prompt de corrección (opcional; por defecto: sin reintento).
#
# Ejemplo de request:
# {
#   "titulo": "Implementar endpoint POST /tareas",
#   "descripcion": "Crear endpoint para crear tarea, validar campos mínimos...",
#   "categoria": "Backend",
#   "horas_estimadas": null
# }
#
# Ejemplo de response:
# {
#   "horas_estimadas": 2.5,
#   ...
# }
#
# Prompting recomendado:
# - "Devuelve solo un número decimal (ej: 2.5). Sin unidades. Sin texto."
# - Considerar rango razonable (0.5 a 80, por ejemplo) solo si se desea.
# ------------------------------------------------------------


# ------------------------------------------------------------
# 6.4 POST /ai/tareas/audit
# ------------------------------------------------------------
# Propósito:
# - Generar:
#   1) analisis_riesgo: riesgos potenciales de la tarea
#   2) mitigacion_riesgo: plan de mitigación basado en la tarea y el análisis
#
# Entrada esperada:
# - Tarea con campos completos, excepto:
#   - analisis_riesgo vacío
#   - mitigacion_riesgo vacío
#
# Campos que completa:
# - analisis_riesgo (texto)
# - mitigacion_riesgo (texto)
#
# Reglas del flujo:
# - Se realizan DOS llamadas al LLM:
#   1) Llamada 1: genera analisis_riesgo usando los datos de la tarea
#   2) Llamada 2: genera mitigacion_riesgo usando:
#      - datos de la tarea
#      - analisis_riesgo generado
#
# Ejemplo de request:
# {
#   "titulo": "Migrar persistencia a almacenamiento robusto",
#   "descripcion": "Evaluar riesgos de concurrencia y corrupción de archivo JSON...",
#   "prioridad": "alta",
#   "horas_estimadas": 6.0,
#   "estado": "pendiente",
#   "asignado_a": "Guillermo",
#   "categoria": "Backend",
#   "analisis_riesgo": "",
#   "mitigacion_riesgo": ""
# }
#
# Ejemplo de response:
# {
#   "analisis_riesgo": "Riesgos: ...",
#   "mitigacion_riesgo": "Mitigación: ...",
#   ...
# }
#
# Prompting recomendado:
# - Analisis: 5-10 bullets en español, sin markdown si se quiere texto plano
# - Mitigación: acciones concretas, priorizadas, relacionadas a los riesgos listados
# ------------------------------------------------------------


# ============================================================
# 7. VALIDACIONES BÁSICAS (SIN SOBREINGENIERÍA)
# ============================================================
# Los endpoints /ai deben validar:
# - Que el body sea JSON
# - Que existan campos mínimos para la operación
# - Que horas_estimadas sea numérica al final (en estimate)
#
# Evitar:
# - Catálogos complejos
# - Reglas de negocio avanzadas
# - Persistencia automática sin decisión explícita
# ============================================================


# ============================================================
# 8. DESARROLLO INCREMENTAL (ORDEN RECOMENDADO)
# ============================================================
# 1) Extender modelo Tarea (nuevos campos + serialización)
# 2) Crear servicio_ia.py con una función mínima (ping o respuesta fija)
# 3) Implementar /ai/tareas/describe y probar
# 4) Implementar /ai/tareas/categorize y probar
# 5) Implementar /ai/tareas/estimate y probar (parsing crítico)
# 6) Implementar /ai/tareas/audit y probar (2 llamadas)
# ============================================================


# ============================================================
# 9. PRUEBAS (POSTMAN)
# ============================================================
# El agente debe proveer para cada endpoint:
# - JSON de ejemplo (request)
# - JSON esperado (response)
# - Escenarios de error (400/500)
# - Recordatorio: NO incluir credenciales en la entrega
# ============================================================


# ============================================================
# FIN DEL ARCHIVO agents_ai.md (AMPLIADO)
# ============================================================
