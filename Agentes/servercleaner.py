"""
Descripción:
Este código configura un servidor de simulación utilizando la biblioteca Mesa para representar un modelo de limpieza.
Incluye la definición de la visualización de agentes "limpiadores" y "sucios" en una rejilla.

Autores:
Víctor Alejandro Morales García
A01749831
David Sánchez Báez
A01798202
"""

import mesa
from cleaner import *

def agent_portrayal(agent):
    """
    Devuelve una representación visual de un agente para la visualización de la simulación.
    """
    if isinstance(agent, Cleaner):
        portrayal = {
            "Shape": "circle",
            "Filled": "true",
            "Layer": 0,
            "Color": "blue",
            "r": 0.5
        }
    elif isinstance(agent, Dirty):
        portrayal = {
            "Shape": "rect",
            "Filled": "true",
            "Layer": 0,
            "Color": "brown",
            "w": 0.5,
            "h": 0.5
        }
    return portrayal

# Definición de parámetros para la simulación
limpiadores: int = 9  # Número de agentes limpiadores
suciedad: int = 90    # Porcentaje de celdas con agentes "sucios"
w: int = 10           # Ancho de la rejilla
h: int = 10           # Altura de la rejilla

# Configuración de la visualización de la rejilla
grid = mesa.visualization.CanvasGrid(
    agent_portrayal,
    w,
    h,
    500,
    500
)

# Configuración del servidor de la simulación
server = mesa.visualization.ModularServer(
    CleanModel,
    [grid],
    "Clean Model",
    {"N": limpiadores, "d": suciedad, "w": w, "h": h}
)

server.port = 8521  # Puerta para ejecutar el servidor
server.launch()     # Lanza la simulación
