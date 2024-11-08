"""
Descripción:
Este código implementa un modelo de simulación de agentes utilizando la biblioteca Mesa. Incluye agentes que representan
entidades "sucias" y agentes "limpiadores" que se encargan de limpiar estas entidades dentro de una rejilla. Además,
el modelo rastrea el número de pasos requeridos y el tiempo transcurrido para completar la limpieza.

Autores:
Víctor Alejandro Morales García
A01749831
David Sánchez Báez
A01798202
"""

from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import random
import time

class Dirty(Agent):
    """
    Clase que representa un agente "sucio" en el modelo.
    """
    def __init__(self, unique_id: int, model: Model) -> None:
        """
        Inicializa un agente Dirty.
        """
        super().__init__(unique_id, model)
        self.dirty = True
        
    def step(self) -> None:
        """
        Método que representa la acción que el agente realiza en cada paso. Este agente no realiza ninguna acción.
        """
        pass

class Cleaner(Agent):
    """
    Clase que representa un agente "limpiador" en el modelo.
    """
    def __init__(self, unique_id: int, model: Model) -> None:
        """
        Inicializa un agente Cleaner.
        """
        super().__init__(unique_id, model)
        
    def step(self) -> None:
        """
        Método que representa la acción que el agente realiza en cada paso. Si encuentra un agente Dirty en su
        posición actual, lo elimina y se mueve a una nueva posición válida aleatoria.
        
        Disminuye el contador de agentes "sucios" del modelo al eliminar uno.
        """
        current_position = self.pos
        cellmates = self.model.grid.get_cell_list_contents([current_position])
        for agent in cellmates:
            if isinstance(agent, Dirty):
                self.model.grid.remove_agent(agent)
                self.model.schedule.remove(agent)
                self.model.dirty_count -= 1 
        
        possible = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        valid_moves = [pos for pos in possible if not any(isinstance(a, Cleaner) for a in self.model.grid.get_cell_list_contents([pos]))]
        
        if valid_moves:
            new_position = self.random.choice(valid_moves)
            self.model.grid.move_agent(self, new_position)
        
class CleanModel(Model):
    """
    Clase que representa el modelo de simulación.
    """
    def __init__(self, N: int, d: int, w: int, h: int) -> None:
        """
        Inicializa un modelo de simulación con agentes Cleaner y Dirty.
        """
        self.num_agents = N
        self.grid = MultiGrid(w, h, True)
        self.schedule = RandomActivation(self)
        self.step_count = 0  
        self.start_time = time.time()  
        
        for i in range(self.num_agents):
            agent = Cleaner(i, self)
            self.schedule.add(agent)
            x = 1
            y = 1
            self.grid.place_agent(agent, (x, y))
        
        p = ((w * h) * d) // 100
        self.dirty_count = p  
        
        for i in range(p):
            dirty_agent = Dirty(self.num_agents + i, self)
            self.schedule.add(dirty_agent)
            while True:
                x = random.randrange(self.grid.width)
                y = random.randrange(self.grid.height)
                if self.grid.is_cell_empty((x, y)):
                    self.grid.place_agent(dirty_agent, (x, y))
                    break
        
    def step(self) -> None:
        """
        Método que avanza un paso en la simulación, activando todos los agentes. Si no quedan agentes "sucios",
        la simulación se detiene y se imprime el tiempo total y el número de pasos.
        """
        self.schedule.step()
        self.step_count += 1
        
        if self.dirty_count == 0:
            end_time = time.time()
            print(f"Limpieza completada en {self.step_count} pasos.")
            print(f"Tiempo total: {end_time - self.start_time:.2f} segundos.")
            self.running = False 
