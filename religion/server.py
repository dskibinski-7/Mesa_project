from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from .model import ReligionModel
from .agents import MissionaryAgent, UnbelievingAgent, Temple
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
            portrayal["Color"] = "Black"
        portrayal["Shape"] = "circle"
        portrayal["r"] = 1
        portrayal["Filled"] = True
        
    elif type(agent) is Temple:
        if agent.religion_type == 1:
            portrayal["Color"] = "Red"
        elif agent.religion_type == 2:
            portrayal["Color"] = "Green"
        elif agent.religion_type == 3:
            portrayal["Color"] = "Blue"    
        
        portrayal["Shape"] = "circle"#"rect"
        #portrayal["w"] = 0.1
        #portrayal["h"] = 0.1
        portrayal["r"] = agent.faith
        portrayal["Filled"] = False
        
    
    return portrayal

#bylo 700x700
canvas = SimpleCanvas(agent_draw, 600, 600)

chart = ChartModule(
    [{"Label": "1. Religion", "Color": "Red"}, 
     {"Label": "2. Religion", "Color": "Green"}, 
     {"Label": "3. Religion", "Color": "Blue"},
     {"Label": "Atheists", "Color": "Black"}],
    data_collector_name='datacollector'
)

model_params = {
    "missionaries_N": UserSettableParameter(
        "slider", "Początkowa liczba misjonarzy", 10, 1, 20
    ),
    "unbelieving_N": UserSettableParameter(
        "slider", "Początkowa liczba ateistów", 1500, 500, 3000
    ),
    "give_faith_prob": UserSettableParameter(
        "slider", "Prawdopodobieństwo przekazania wiary [%]", 80, 10, 100,
        description="Prawdopodobieństwo, z jakim misjonarzowi uda się nawrócić inną osobę",
    ),
    "temple": UserSettableParameter(
        "checkbox", "Świątynie", value=False
    ),
    "build_temple_ratio": UserSettableParameter(
        "slider", "Procent wiernych do zbudowania świątyni [%]", 50, 10, 100
    ),
    }

server = ModularServer(ReligionModel,
                       [canvas, chart],
                       "Religion Model",
                       model_params)