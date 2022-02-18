from mesa import Agent
import random
import numpy as np


#oba agenty moglyby dziedziczyc po jednym typie 

class MissionaryAgent(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, unique_id, model, religion_type = random.choice([1,2,3])):
        super().__init__(unique_id, model)
        prob_age = 120
        while prob_age > 100:
            prob_age = int(np.random.normal(70, 20, 1))    
        self.age = prob_age 
        self.faith = 1 #
        self.religion_type = religion_type
        

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
                #od jakiej wartosci moze zmienic religie (n.faith < 0.3)
                if n.religion_type == 0 or n.faith < 0.3:
                    n.faith += np.random.normal(0.5, 0.1, 1)
                    n.religion_type = self.religion_type
                    if n.faith > 1:
                        n.faith = 1
                
            

    def step(self):
        self.move()
        self.give_faith()
        #stazenie sie - w tym przypadku osonik (ok. 70) bedzie zyc 1750 stepow
        self.age -= 0.04
        
        #death; no offspring
        if self.age < 0:
            self.model.space.remove_agent(self)
            self.model.schedule.remove(self)
        
        
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
    def __init__(self, unique_id, model, faith = 0, religion_type = 0):
        super().__init__(unique_id, model)
        prob_age = 120
        while prob_age > 100:
            prob_age = int(np.random.normal(70, 20, 1))    
        self.age = prob_age 
        self.religion_type = religion_type
        if self.religion_type == 0:
            self.faith = 0
        else:
            self.faith = faith
        
        
    
    def move(self):
        dx = random.uniform(-1, 1)
        dy = random.uniform(-1, 1)        
        x, y = self.pos
        
        #test - zmieniony dx
        self.model.space.move_agent(self, (x+dx, y+dy))

    #strengthen or weaken your faith - depending on the number of neighbors    
    def establish_faith(self):
        neighbors = self.model.space.get_neighbors(
            self.pos, 
            radius = 10,
            include_center = False)        
        
        co_believers = 0
        for n in neighbors:
            if n.religion_type == self.religion_type:
                co_believers += 1
                
        if co_believers:
            self.faith += co_believers*0.01
        else:
            self.faith -= 0.05
        
        if self.faith > 1:
            self.faith = 1
        elif self.faith <= 0:
            self.religion_type = 0
                
                
    def step(self):
        self.move()
        self.age-= 0.04
        #w zaleznosci od sasiadow - wiara umacnia sie lub oslabia
        #potem update z kosciolem?
        self.establish_faith()
        
        #death and birth /next pop
        if self.age < 0:
            #birth of the offspring
            num_of_childs = np.random.choice([0,1,2])
            for child in range(num_of_childs):
                shuffle_faith = np.random.normal(self.faith, 0.1, 1)
                if shuffle_faith >= 1:
                    #misjonarz
                    a = MissionaryAgent(self.model.next_id(), self.model, religion_type=self.religion_type)
                    self.model.schedule.add(a)
                    self.model.space.place_agent(a, self.pos)
                elif shuffle_faith <= 0.5:
                    #normalagent
                    #moze zmienic wiare
                    a = UnbelievingAgent(self.model.next_id(), self.model, faith = shuffle_faith, religion_type = random.choice([0,1,2,3]))
                    self.model.schedule.add(a)
                    # Add the agent to a random space place
                    self.model.space.place_agent(a, self.pos)
                else:
                    #normal agent, ta sama wiare
                    a = UnbelievingAgent(self.model.next_id(), self.model, faith = shuffle_faith, religion_type = self.religion_type)
                    self.model.schedule.add(a)
                    # Add the agent to a random space place
                    self.model.space.place_agent(a, self.pos)
                
            
            #death
            self.model.space.remove_agent(self)
            self.model.schedule.remove(self)
            

        

        
