from mesa import Model
from mesa.time import RandomActivation
from mesa.space import ContinuousSpace

from .agents import MissionaryAgent, BelieviengAgent, UnbelievingAgent

class ReligionModel(Model):
    """A model with some number of agents."""
    def __init__(self, missionaries_N, unbelieving_N, width, height):
        self.num_missionaries = missionaries_N
        self.num_unbelieving = unbelieving_N
        self.space = ContinuousSpace(width,height,True)
        self.schedule = RandomActivation(self)
        self.running = True
        
        
        # Create missionaries
        for i in range(self.num_missionaries):
            a = MissionaryAgent(i, self)
            self.schedule.add(a)
            # Add the agent to a random space place
            x = self.random.randrange(self.space.width)
            y = self.random.randrange(self.space.height)
            self.space.place_agent(a, (x, y))
        for i in range(self.num_unbelieving):
            #zwiekszenie unique_id aby sie nie powtarzaly z misjonarzami
            a = UnbelievingAgent(i + self.num_missionaries, self)
            self.schedule.add(a)
            # Add the agent to a random space place
            x = self.random.randrange(self.space.width)
            y = self.random.randrange(self.space.height)
            self.space.place_agent(a, (x, y))            

    def step(self):
        self.schedule.step()