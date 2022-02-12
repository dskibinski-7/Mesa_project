from mesa.visualization.ModularVisualization import ModularServer

from .model import ReligionModel
from .agents import MissionaryAgent, BelieviengAgent, UnbelievingAgent
from .SimpleContinuousModule import SimpleCanvas

def agent_draw(agent):
    portrayal = {}
    
    if type(agent) is MissionaryAgent:
        portrayal["Shape"] = "circle"
        portrayal["r"] = 1
        portrayal["Filled"] = "true"
        portrayal["Color"] = "Red"
        
    elif type(agent) is UnbelievingAgent:
        portrayal["Shape"] = "circle"
        portrayal["r"] = 1
        portrayal["Filled"] = "true"
        portrayal["Color"] = "Blue"        
    
    
    return portrayal

canvas = SimpleCanvas(agent_draw, 250, 250)


server = ModularServer(ReligionModel,
                       [canvas],
                       "Religion Model",
                       {"missionaries_N":2, "unbelieving_N":10, "width":250, "height":250})