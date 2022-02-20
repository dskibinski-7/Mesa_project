from mesa import Agent
import random
import numpy as np




class MissionaryAgent(Agent):

    def __init__(self, unique_id, model, religion_type = 0):
        super().__init__(unique_id, model)
        prob_age = 120
        while prob_age > 100:
            prob_age = int(np.random.normal(70, 20, 1))    
        self.age = prob_age 
        self.faith = 1 #
        self.temple_bonus = 0
        if religion_type == 0:
            #nie byl zadeklarowany, wybierz losowo
            self.religion_type = random.randint(1, 3)
        else:
            self.religion_type = religion_type     

    def move(self):
        random_walk_options = [(-5,-5), (-5,0), (-5,5), (0,-5), (0,0), (0,5), (5,-5), (5,0), (5,5)]
        #sasiedzi:
        neighbors = self.model.space.get_neighbors(
            self.pos, 
            radius = 45,
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
            
                dx, dy = 0, 0
    
                if neigh_x > missionary_x:
                    dx = 5
                elif neigh_x < missionary_x:
                    dx = -5
                    
                if neigh_y > missionary_y:
                    dy = 5
                elif neigh_y < missionary_y:
                    dy = -5
            else:
                dx, dy = random.choice(random_walk_options)                       
        #jezeli brak sasiadow w promieniu to idz losowo
        else:
            
            dx, dy = random.choice(random_walk_options)


        self.model.space.move_agent(self, (missionary_x+dx, missionary_y+dy))

    def give_faith(self):
        #znajdz sasiadow - przekaz im wiare

        neighbors = self.model.space.get_neighbors(
            self.pos, 
            radius = 25,
            include_center = False)
        if len(neighbors) > 1:
            #zwieksz wiare, ale nie wiecej niz 1 
            for n in neighbors:
                #od jakiej wartosci moze zmienic religie 
                if n.religion_type == 0 or n.faith < 0.3:
                    if random.random() > (1 - (self.model.give_faith_prob + self.temple_bonus)):
                        n.faith += np.random.normal(0.5, 0.1, 1)
                        n.religion_type = self.religion_type
                        if n.faith > 1:
                            n.faith = 1
                            
        
                
            

    def step(self):
        self.move()
        self.give_faith()

        self.age -= 1#0.08#0.04
        
        #death; no offspring
        if self.age < 0:
            self.model.space.remove_agent(self)
            self.model.schedule.remove(self)
        

        
class Temple(Agent):
    def __init__(self, unique_id, model, religion_type):
        super().__init__(unique_id, model)
        self.religion_type = religion_type
        self.faith = 200 #bedzie odpowiadac promieniowi buffa
        
    def give_buff(self):
        #zwieksz prawdopodobienstwo przekazania wiary
        #umacniaj wiare wiernych (jezeli w zasiegu to zyskuja wiare) 
        
        #dla sasiadow w zasiegu swiatyni
        neighbors = self.model.space.get_neighbors(
            self.pos, 
            radius = self.faith,
            include_center = True)
        
        if neighbors:
            for n in neighbors:
                #buff tylko dla tej religii
                if n.religion_type == self.religion_type:
                    if type(n) is MissionaryAgent:
                        #buff dla misjonarza
                        n.temple_bonus = 0.1          
                    elif type(n) is UnbelievingAgent:
                        #buff dla wiernych
                        n.temple_bonus = 1.05
     
    def step(self):
        self.give_buff()



class UnbelievingAgent(Agent):
    def __init__(self, unique_id, model, faith = 0, religion_type = 0):
        super().__init__(unique_id, model)
        prob_age = 120
        while prob_age > 100:
            prob_age = int(np.random.normal(70, 20, 1))    
        self.age = prob_age 
        self.religion_type = religion_type
        self.temple_bonus = 1
        if self.religion_type == 0:
            self.faith = 0
        else:
            self.faith = faith
        
        
    
    def move(self):
        dx = random.uniform(-5, 5)
        dy = random.uniform(-5, 5)        
        x, y = self.pos
        
        #test - zmieniony dx
        self.model.space.move_agent(self, (x+dx, y+dy))

    #strengthen or weaken your faith - depending on the number of neighbors    
    def establish_faith(self):
        neighbors = self.model.space.get_neighbors(
            self.pos, 
            radius = 15,
            include_center = False)        
        
        co_believers = 0
        for n in neighbors:
            if n.religion_type == self.religion_type: #swiatynia tez sie wlicza
                co_believers += 1
                
        if co_believers and self.faith < 0.5:
            self.faith += co_believers*0.1 * self.temple_bonus
        else:
            #SPADEK WIARY
            self.faith -= 0.05
        
        if self.faith > 1:
            self.faith = 1
        elif self.faith <= 0:
            self.religion_type = 0
                
                
    def step(self):
        self.move()
        self.age-= 1#0.08#0.04
        #w zaleznosci od sasiadow - wiara umacnia sie lub oslabia
        if self.religion_type:
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
                    #else:
                        
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
            

        

        
