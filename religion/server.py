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
        portrayal["Color"] = "Red"
        
    elif type(agent) is UnbelievingAgent:
        if agent.faith > 0:
            portrayal["Color"] = "Red" 
        else:
           portrayal["Color"] = "Blue"  
        portrayal["Shape"] = "circle"
        portrayal["r"] = 1
        portrayal["Filled"] = True
               
    
    
    return portrayal

canvas = SimpleCanvas(agent_draw, 500, 500)

#dodac chart dominacji religii
server = ModularServer(ReligionModel,
                       [canvas],
                       "Religion Model",
                       {"missionaries_N":1, "unbelieving_N":100, "width":500, "height":500})