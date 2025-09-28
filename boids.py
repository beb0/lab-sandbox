from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt 
import math
import random

class Agent:
    
    def __init__(self):
        self.x = random.randint(-boundary,boundary)
        self.y = random.randint(-boundary,boundary)
        angle = random.uniform(0, 2*math.pi)
        self.vx = math.cos(angle) * 0.5
        self.vy = math.sin(angle) * 0.5
        self.t1 = random.randint(0,10)
        self.t2 = random.randint(0,10)
        self.t2 = random.randint(0,10)
       
    def manage_boundary(self):
        if self.x < -boundary:
            self.x = self.x  % boundary
        if self.x > boundary:
            self.x = (self.x  % boundary) - boundary
            
        if self.y < -boundary:
            self.y = self.y  % boundary
        if self.y > boundary:
            self.y = (self.y  % boundary) - boundary
    
    # to implement
    def follow(self, other):
        pass
    
    def my_neighborhood(self, others):
        neighborhood = [] 
        for other in others:
            if other == self:
                continue
            else:
                if math.hypot(other.x - self.x, other.y - self.y) < neighborhood_range:
                    neighborhood.append(other)        
        return neighborhood
    
    # opposite of separation, if close touch
    # def collide(self, others):
    #     neighborhood = self.my_neighborhood(others)
    #     for neighbor in neighborhood:
    #         if  math.hypot(self.x - neighbor.x, self.y - neighbor.y) < collide_range:
    #             self.vx += self.x + neighbor.x
    #             self.vy += self.y + neighbor.y
    
    # collision to be simulated
    def separation(self, others):
        neighborhood = self.my_neighborhood(others)
        for neighbor in neighborhood:
            if  math.hypot(self.x - neighbor.x, self.y - neighbor.y) < collide_range:
                self.vx += self.x - neighbor.x
                self.vy += self.y - neighbor.y

    
    def alignment(self, others):
        # pass
        neighborhood = self.my_neighborhood(others)
        avg_vx = 0 
        avg_vy = 0
        for neighbor in neighborhood:
            avg_vx += neighbor.vx
            avg_vy += neighbor.vy
            
        if len(neighborhood) > 0:
            avg_vx /= len(neighborhood)
            avg_vy /= len(neighborhood)
        # a - b -> what will take b to reach a  
        self.vx += (avg_vx - self.vx) 
        self.vy += (avg_vy - self.vy) 
        
    
    def cohesion(self, others):
        neighborhood = self.my_neighborhood(others)
        avg_x = 0
        avg_y = 0
        
        for neighbor in neighborhood:
            avg_x += neighbor.x
            avg_y += neighbor.y
        
        if len(neighborhood) > 0:
            avg_x /= len(neighborhood)
            avg_y /= len(neighborhood)
        
        self.vx += (avg_x - self.x)
        self.vy += (avg_y - self.y) 
      
    def boids(self):
        pass
        # calculate the new vector 
    
    def move(self, others, speed=1):
        
        # if abs(self.x - others[0].x) < 2:
        #     self.follow(others[0])             
        # else:
        #     orientation = random.uniform(0,2*math.pi)
                
        #     self.x += math.cos(orientation) * speed
        #     self.y += math.sin(orientation) * speed
        
        # orientation = random.uniform(0,2*math.pi)          
        # self.x += math.cos(orientation) * speed
        # self.y += math.sin(orientation) * speed
        
        self.alignment(others)
        self.separation(others)
        self.cohesion(others)
        
        self.x += self.vx * steering_factor
        self.y += self.vy * steering_factor
        
        self.manage_boundary()
        
        
        return [self.x, self.y]
 
num_agents = 100
neighborhood_range = 5
collide_range = 3
steering_factor = 0.01
boundary = 50


fig, ax = plt.subplots()
ax.set_xlim(-boundary,boundary)
ax.set_ylim(-boundary,boundary)

agents = [ Agent() for _ in range(num_agents)]
scat = ax.scatter([],[], s=20)


def update(frame):
    for agent in agents:
        agent.move(agents, speed=0.5)
    
    points_to_show = [[agent.x, agent.y] for agent in agents]
    scat.set_offsets(points_to_show)

    return scat
        
anim = FuncAnimation(fig, update, frames=2000, interval=100,  repeat=True)

plt.show()