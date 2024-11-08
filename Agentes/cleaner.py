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
        super().__init__(unique_id, model)
        self.dirty = True

    def step(self) -> None:
        pass

class Cleaner(Agent):
    """
    Clase que representa un agente "limpiador" en el modelo.
    """
    def __init__(self, unique_id: int, model: Model) -> None:
        super().__init__(unique_id, model)
    
    def step(self) -> None:
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
        self.num_agents = N
        self.grid = MultiGrid(w, h, True)
        self.schedule = RandomActivation(self)
        self.step_count = 0  
        self.start_time = time.time()  
        
        # Agregar agentes Cleaner
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
        Método que avanza un paso en la simulación, activando todos los agentes.
        """
        self.schedule.step()
        self.step_count += 1
        
        if self.dirty_count == 0:
            end_time = time.time()
            print(f"Limpieza completada en {self.step_count} pasos.")
            print(f"Tiempo total: {end_time - self.start_time:.2f} segundos.")
            self.running = False  # Detener la simulación
