import mesa
from cleaner import *

def agent_portrayal(agent):
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

limpiadores: int = 9
suciedad: int = 90
w: int = 10
h: int = 10

grid = mesa.visualization.CanvasGrid(
    agent_portrayal,
    w,
    h,
    500,
    500
)

server = mesa.visualization.ModularServer(
    CleanModel,
    [grid],
    "Clean Model",
    {"N": limpiadores, "d": suciedad, "w": w, "h": h}
)

server.port = 8521
server.launch()