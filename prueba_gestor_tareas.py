from modelos.tarea import Tarea
from servicios.gestor_tareas import GestorTareas

tarea = Tarea(
    identificador=1,
    titulo="Prueba persistencia",
    descripcion="Validar guardar y cargar JSON",
    prioridad="media",
    horas_estimadas=1.5,
    estado="pendiente",
    asignado_a="Guillermo"
)

GestorTareas.guardar_tareas([tarea])
tareas_cargadas = GestorTareas.cargar_tareas()

print([t.a_diccionario() for t in tareas_cargadas])
