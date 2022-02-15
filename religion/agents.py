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
        random_walk_options = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,0), (0,1), (1,-1), (1,0), (1,1)]
        #ruch na podstawie innych agentów - moze niewierzacych, ale to potem
        #sasiedzi:
        neighbors = self.model.space.get_neighbors(
            self.pos, 
            radius = 25,
            include_center = False)
        
        #wspolrzedne misjonarza
        missionary_x, missionary_y = self.pos
        
        if len(neighbors) > 1:
            #idz w strone najblizszego  w promieniu
            distances_between_missionair_neigh = {}
            for neigh in neighbors:
                if type(neigh) is MissionaryAgent or neigh.faith > 0.2:
                    continue
                else:
                    dist = self.model.space.get_distance(self.pos, neigh.pos)
                    distances_between_missionair_neigh[neigh] = dist
            
            #jezeli znaleziono kogos w poblizu
            if distances_between_missionair_neigh:
                closest = min(distances_between_missionair_neigh, key=distances_between_missionair_neigh.get)
                neigh_x, neigh_y = closest.pos
                #print("Misjonarz nr: " + str(self.unique_id) + "pozycja: " + str(self.pos) + "najblizszy siasiad ma numer " + str(closest.unique_id) + "jego pozycja: " + str(closest.pos))                                               
                dx, dy = 0, 0
    
                if neigh_x > missionary_x:
                    dx = 3
                elif neigh_x < missionary_x:
                    dx = -3
                    
                if neigh_y > missionary_y:
                    dy = 3
                elif neigh_y < missionary_y:
                    dy = -3
            else:
                dx, dy = random.choice(random_walk_options)                       
        #jezeli brak sasiadow w promieniu to idz losowo
        else:
            #random walk tak
            dx, dy = random.choice(random_walk_options)


        self.model.space.move_agent(self, (missionary_x+dx, missionary_y+dy))

    def give_faith(self):
        #znajdz sasiadow - przekaz im wiare
        #tylko type of niewierzacy?
        neighbors = self.model.space.get_neighbors(
            self.pos, 
            radius = 25,
            include_center = False)
        if len(neighbors) > 1:
            #zwieksz wiare, ale nie wiecej niz 1 (jezeli wiecej niz jeden to moze misjonarz?)
            for n in neighbors:
                n.faith += np.random.normal(0.5, 0.1, 1)
                if n.faith > 1:
                    n.faith = 1
            #test
            #print("pozycja sasiadow (pod nimi pozycja misjonarza)")
            #for n in neighbors:
            #    print(n.pos)

        #print("misjonarz pozycja" +str(self.pos))
            

    def step(self):
        self.move()
        self.give_faith()
        self.age -= 0.01
        
        
class BelieviengAgent(Agent):
    pass
    # def __init__(self, unique_id, model):
    #     super().__init__(unique_id, model)
    #     prob_age = 120
    #     while prob_age > 100:
    #         prob_age = int(np.random.normal(70, 20, 1))    
    #     self.age = prob_age 
    #     self.faith = 0 #  
        
    
    # def move(self):
    #     dx = random.uniform(-1, 1)
    #     dy = random.uniform(-1, 1)        
    #     x, y = self.pos
    #     self.model.space.move_agent(self, (x+dx, y+dy))
        
    # def step(self):
    #     self.move()
    #     self.age-= 1


class UnbelievingAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        prob_age = 120
        while prob_age > 100:
            prob_age = int(np.random.normal(70, 20, 1))    
        self.age = prob_age 
        self.faith = 0 #  
        
    
    def move(self):
        dx = random.uniform(-1, 1)
        dy = random.uniform(-1, 1)        
        x, y = self.pos
        
        #test - zmieniony dx
        self.model.space.move_agent(self, (x+dx, y+dy))
        #print("niewierzacy pozycja" + str(self.pos))
        
    def step(self):
        self.move()
        self.age-= 1
