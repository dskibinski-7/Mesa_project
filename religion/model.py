from mesa import Model
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation
from mesa.space import ContinuousSpace
import random

from .agents import MissionaryAgent, UnbelievingAgent, Temple 

def compute_believers(model):
    religion_believiers = {1:0, 2:0, 3:0}
    all_agents = model.schedule.agents
    for agent in all_agents:
        religion_type_to_add = agent.religion_type
        if religion_type_to_add:
            religion_believiers[religion_type_to_add] += 1
        else:
            continue

    return religion_believiers
    
def get_random_missionair(model, religion_type):
    return random.choice(list(a for a in model.schedule.agents if (a.religion_type is religion_type and type(a) is MissionaryAgent)))
    
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
    def __init__(self, missionaries_N, unbelieving_N, width = 600, height= 600, give_faith_prob = 100, temple = False, build_temple_ratio = 80):
        self.num_missionaries = missionaries_N
        self.num_unbelieving = unbelieving_N
        self.space = ContinuousSpace(width,height,True)
        self.schedule = RandomActivation(self)
        self.running = True
        self.current_id = 0
        self.give_faith_prob = give_faith_prob/100
        self.temple = temple
        #self.temple_counter = {1:0, 2:0, 3:0}
        self.build_temple_ratio = build_temple_ratio/100

        
        # Create missionaries
        for i in range(self.num_missionaries):
            # a = MissionaryAgent(self.next_id(), self)
            # self.schedule.add(a)
            # # Add the agent to a random space place
            # x = self.random.randrange(self.space.width)
            # y = self.random.randrange(self.space.height)
            # self.space.place_agent(a, (x, y))
            
            
            a = MissionaryAgent(self.next_id(), self)
            rel_type = a.religion_type

            
            present_missionaries_with_same_religion = list(a for a in self.schedule.agents if a.religion_type is rel_type)
            self.schedule.add(a)
            
            #pojebane w chuj cos sie dzieje tu 
            # #jezeli ten sam misjonarz - to w miare blisko
            if len(present_missionaries_with_same_religion)>0:
                #print(present_missionaries_with_same_religion)
                x_, y_ = present_missionaries_with_same_religion[0].pos #x pozycja misjonarza (juz na mapie) z ta sama religia #y pozycja misjonarza (juz na mapie) z ta sama religia
                x = self.random.randrange(x_-75, x_+75)
                y = self.random.randrange(y_-75, y_+75)
                self.space.place_agent(a, (x, y))
            else:
                #jezeli nie ma zadnego misjonarza z ta sama religia, wrzuc tego w losowe miejsce
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
        #jezeli opcja ze swiatyniami
        #moze u misjonarza w klasie - skoro to on zaklada swiatynie
        if self.temple:
            believers = compute_believers(self)
            all_agents = self.schedule.get_agent_count()
            for religion_type in believers:
                #jezeli powyzej 40 procent calej populacji
                if believers[religion_type]/all_agents > self.build_temple_ratio:
                    #init swiatyni 
                    #nie moze byc w poblizu tej samej swiatyni
                    
                    
                    #x, y randomowego misjonarza danej religii
                    x, y = get_random_missionair(self, religion_type).pos
                    neighbors = self.space.get_neighbors(
                        (x,y), 
                        radius = 250,
                        include_center = True)
                    
                    place_for_temple= True
                    if neighbors:
                        for neigh in neighbors:
                            #jezeli w poblizu swiatynia tego samego typu to nie zakladaj swiatyni - przerwij petle
                            if type(neigh) is Temple and neigh.religion_type == religion_type:
                                place_for_temple = False
                                break 
                            
                        if place_for_temple:      
                            t = Temple(self.next_id(), self, religion_type)
                            self.schedule.add(t)
                            self.space.place_agent(t, (x, y))  
                    
                    
