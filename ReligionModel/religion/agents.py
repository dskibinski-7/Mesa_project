from mesa import Agent
import random
import numpy as np

class MissionaryAgent(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        prob_age = 120
        while prob_age > 100:
            prob_age = int(np.random.normal(70, 20, 1))    
        self.age = prob_age 
        self.faith = 1 #
        

    def move(self):
        #ruch na podstawie innych agentów - moze niewierzacych, ale to potem
        #sasiedzi:
        neighbors = self.model.space.get_neighbors(
            self.pos, 
            radius = 4,
            include_center = False)
        
        #wspolrzedne misjonarza
        missionary_x, missionary_y = self.pos
        
        if len(neighbors) > 0:
            #idz w strone najblizszego  w promieniu
            distances_between_missionair_neigh = {}
            for neigh in neighbors:
                dist = self.model.space.get_distance(self.pos, neigh.pos)
                distances_between_missionair_neigh[neigh] = dist
            
            closest = min(distances_between_missionair_neigh, key=distances_between_missionair_neigh.get)
            neigh_x, neigh_y = closest.pos
            dx, dy = 0, 0
            #ruch może być do poprawki
            if neigh_x > missionary_x:
                dx = 1
            elif neigh_x < missionary_x:
                dx = -1
            if neigh_y > missionary_y:
                dy = 1
            elif neigh_y < missionary_y:
                dy = -1                       
        #jezeli brak sasiadow w promieniu to idz losowo
        else:
            dx = random.uniform(-1, 1)
            dy = random.uniform(-1, 1)

        self.model.space.move_agent(self, (missionary_x+dx, missionary_y+dy))

    def give_faith(self):
        #znajdz sasiadow - przekaz im wiare
        #tylko type of niewierzacy?
        neighbors = self.model.space.get_neighbors(
            self.pos, 
            radius = 2,
            include_center = False)
        if len(neighbors) > 1:
            print("PRZEKAZANIE WIARY")
            #test
            print("pozycja sasiadow (pod nimi pozycja misjonarza)")
            for n in neighbors:
                print(n.pos)
        else:
            print("pusty obszar")
        print("misjonarz pozycja" +str(self.pos))
            

    def step(self):
        self.move()
        self.give_faith()
        
class BelieviengAgent(Agent):
    #agent ktory przyjal wiare - moze ona spadac
    pass

class UnbelievingAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        prob_age = 120
        while prob_age > 100:
            prob_age = int(np.random.normal(70, 20, 1))    
        self.age = prob_age 
        self.faith = 0 #  
        
    
    def move(self):
        dx = 40 #random.uniform(-1, 1)
        dy = 40 #random.uniform(-1, 1)        
        x, y = self.pos
        
        #test - zmieniony dx
        self.model.space.move_agent(self, (x+dx, y+dy))
        print("niewierzacy pozycja" + str(self.pos))
        
    def step(self):
        self.move()
