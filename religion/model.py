from mesa import Model
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation
from mesa.space import ContinuousSpace

from .agents import MissionaryAgent, BelieviengAgent, UnbelievingAgent

# def compute_religion_1(model):
#     religion_believiers = {1:0, 2:0, 3:0, 0:0}
#     all_agents = model.schedule.agents
#     for agent in all_agents:
#         religion_type_to_add = agent.religion_type
#         religion_believiers[religion_type_to_add] += 1

#     return religion_believiers
def compute_religion(model, rel_type):
    return sum(1 for a in model.schedule.agents if a.religion_type is rel_type)

def comp1(model):
    return compute_religion(model, 1)

def comp2(model):
    return compute_religion(model, 2)

def comp3(model):
    return compute_religion(model, 3)

def comp0(model):
    return compute_religion(model, 0)

class ReligionModel(Model):
    """A model with some number of agents."""
    def __init__(self, missionaries_N, unbelieving_N, width, height):
        self.num_missionaries = missionaries_N
        self.num_unbelieving = unbelieving_N
        self.space = ContinuousSpace(width,height,True)
        self.schedule = RandomActivation(self)
        self.running = True
        self.current_id = 0

        
        # Create missionaries
        for i in range(self.num_missionaries):
            a = MissionaryAgent(self.next_id(), self)
            self.schedule.add(a)
            # Add the agent to a random space place
            x = self.random.randrange(self.space.width)
            y = self.random.randrange(self.space.height)
            self.space.place_agent(a, (x, y))
        #create unbelievers
        for i in range(self.num_unbelieving):
            #zwiekszenie unique_id aby sie nie powtarzaly z misjonarzami
            a = UnbelievingAgent(self.next_id(), self)
            self.schedule.add(a)
            # Add the agent to a random space place
            x = self.random.randrange(self.space.width)
            y = self.random.randrange(self.space.height)
            self.space.place_agent(a, (x, y))   
        
        
        #dziala, ale bardzo spowalnia apke 
        #mialem rozwiazanei ze slownikiem ale nie dzialalo (ktore liczylo wszystkich agentow na raz)
        self.datacollector = DataCollector(model_reporters=
            {
                "1. Religion": comp1,
                "2. Religion": comp2,
                "3. Religion": comp3,
                "Atheists": comp0,

            }
        )

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
