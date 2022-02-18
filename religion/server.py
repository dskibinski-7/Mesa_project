from mesa.visualization.ModularVisualization import ModularServer

from .model import ReligionModel
from .agents import MissionaryAgent, BelieviengAgent, UnbelievingAgent
from .SimpleContinuousModule import SimpleCanvas

def agent_draw(agent):
    portrayal = {}
    
    if type(agent) is MissionaryAgent:
        portrayal["Shape"] = "circle"
        portrayal["r"] = 25
        portrayal["Filled"] = False
        if agent.religion_type == 1:
            portrayal["Color"] = "Red"
        elif agent.religion_type == 2:
            portrayal["Color"] = "Green"
        elif agent.religion_type == 3:
            portrayal["Color"] = "Blue"
        #portrayal["Color"] = "Red"
        
    elif type(agent) is UnbelievingAgent:
        if agent.religion_type == 1:
            portrayal["Color"] = "Red"
        elif agent.religion_type == 2:
            portrayal["Color"] = "Green"
        elif agent.religion_type == 3:
            portrayal["Color"] = "Blue"
        else:
            portrayal["Color"] = "Grey"
        portrayal["Shape"] = "circle"
        portrayal["r"] = 1
        portrayal["Filled"] = True
               
    
    
    return portrayal

canvas = SimpleCanvas(agent_draw, 500, 500)

#dodac chart dominacji religii
server = ModularServer(ReligionModel,
                       [canvas],
                       "Religion Model",
                       {"missionaries_N":3, "unbelieving_N":1500, "width":500, "height":500})