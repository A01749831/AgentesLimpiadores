from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import random

class dirty(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.dirty = True 
        
    def step(self):
        pass
    
class cleaner(Agent):
    def __init__(self, unique_id: int, model: Model) -> None:
        super().__init__(unique_id, model)
        
    def step(self):
        current_position = self.pos
        cellmates = self.model.grid.get_cell_list_contents([current_position])
        for agent in cellmates:
            if isinstance(agent, dirty):
                self.model.grid.remove_agent(agent)
                self.model.schedule.remove(agent)
                print(f"Agente {self.unique_id} limpió la posición {current_position}")
        
        possible = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = self.random.choice(possible)
        self.model.grid.move_agent(self, new_position)
        
class cleanModel(Model):
    def __init__(self, N, d, w, h):
        self.num_agents = N
        self.grid = MultiGrid(w, h, True)
        self.schedule = RandomActivation(self)
        
        for i in range(self.num_agents):
            agent = cleaner(i, self)
            self.schedule.add(agent)
            
            x = 1
            y = 1
            self.grid.place_agent(agent, (x, y))
            
        p = ((w * h) * d) // 100
            
        for i in range(p):
            dirty_agent = dirty(self.num_agents + i, self)
            self.schedule.add(dirty_agent)
            while True:
                x = random.randrange(self.grid.width)
                y = random.randrange(self.grid.height)
                if self.grid.is_cell_empty((x, y)):
                    self.grid.place_agent(dirty_agent, (x, y))
                    break
    
    
    def step(self):
        self.schedule.step()

        