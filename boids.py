from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt 
import math
import random
import numpy as np

# A - B: a vector points from B to A


class Agent:
    
    def __init__(self):
        self.x = random.randint(-boundary,boundary)
        self.y = random.randint(-boundary,boundary)
        angle = random.uniform(0, 2*math.pi)
        # self.vx = math.cos(angle) * 0.1
        # self.vy = math.sin(angle) * 0.1
        self.vx = 0
        self.vy = 0
        self.traits =  np.array([random.randint(0,10) for _ in range(3)], dtype=float)
        self.dominant = False
       
    # boundaries wrap around(uncertain)
    def manage_boundary(self):
        if self.x < -boundary:
            self.x = self.x  % boundary
        if self.x > boundary:
            self.x = (self.x  % boundary) - boundary
            
        if self.y < -boundary:
            self.y = self.y  % boundary
        if self.y > boundary:
            self.y = (self.y  % boundary) - boundary
    
    # returns the neighborhood 
    def my_neighborhood(self, others, neighborhood_range=1):
        neighborhood = [] 
        for other in others:
            if other == self:
                continue
            else:
                if math.hypot(other.x - self.x, other.y - self.y) < neighborhood_range:
                    neighborhood.append(other)        
        return neighborhood    
    
    # the agent that has the highest value for a given trait influences that same trait 
    # across the rest of the group — so that trait increases 
    # for everyone. Then, in return, I calculate the average of
    # all traits across the other agents, and the trait with the highest 
    # average influences the dominant agent back.
    def influence(self, neighborhood): 
        avg_t = np.zeros(len(self.traits), dtype=float)
                        
        if len(neighborhood) > 0:
            neighborhood.append(self)
            dominant_agent = self

            # finding the dominant agent who have the highst single value of all traits
            for neighbor in neighborhood:
                neighbor.dominant = False
                if max(neighbor.traits) > max(dominant_agent.traits):
                    dominant_agent = neighbor             
                avg_t += np.array(neighbor.traits)
            
           # subtracting the dominant agent's traits to get the averages
            avg_t -= np.array(dominant_agent.traits)
            dominant_agent.dominant = True
            
            
            # angle = random.uniform(0, 2*math.pi)
            # dominant_agent.vx = math.cos(angle) 
            # dominant_agent.vy = math.sin(angle) 
            
            if len(neighborhood) > 1:
                avg_t = avg_t / (len(neighborhood) - 1)

                
                max_value = 1000
                
                for agent in neighborhood:
                    #  average 
                    if agent == dominant_agent:
                        agent.traits[np.argmax(avg_t)] *= 1.5
                    else:
                        agent.traits[np.argmax(dominant_agent.traits)] *= 1.5
                          
                    # uncertain because it doesn't retain the momentum                  
                    max_abs = np.max(np.abs(agent.traits))
                    if max_abs > max_value:
                        factor = max_value / max_abs
                        agent.traits *= factor
            return dominant_agent

    # others to follow a certain agent
    # def follow(self, neighborhood, boid, follow_factor):
    #     neighborhood.append(self)
    #     vx = 0
    #     vy = 0
    #     if boid in neighborhood:
    #         vx = (boid.x - self.x) * follow_factor
    #         vy = (boid.y - self.y) * follow_factor
    #     return vx, vy
    
    def follow(self, neighborhood, follow_factor):
        vx = 0
        vy = 0
        for neighbor in neighborhood:
            if neighbor.dominant is True:
                vx = (neighbor.x - self.x) * follow_factor
                vy = (neighbor.y - self.y) * follow_factor
                break
        return vx, vy
                                             
    def alignment(self, others, alignment_factor=1):
        neighborhood = others
        avg_vx = 0 
        avg_vy = 0
        alig_vx = 0
        alig_vy = 0
        
        for neighbor in neighborhood:
            avg_vx += neighbor.vx
            avg_vy += neighbor.vy
            
        if len(neighborhood) > 0:
            avg_vx /= len(neighborhood)
            avg_vy /= len(neighborhood)
            alig_vx += (avg_vx - self.vx) * alignment_factor
            alig_vy += (avg_vy - self.vy) * alignment_factor
        # a - b -> what will take b to reach a  
        return alig_vx, alig_vy
    
    def separation(self, others, collide_range=1, separation_factor=1):
        neighborhood = others
        sep_vx = 0
        sep_vy = 0
        for neighbor in neighborhood:
            if  math.hypot(self.x - neighbor.x, self.y - neighbor.y) < collide_range:
                # points from neighbor to self 
                sep_vx += (self.x - neighbor.x) * separation_factor
                sep_vy += (self.y - neighbor.y) * separation_factor
                
            #why adding directly to the velocity would be problematic, and would be a difference if 
            #multiplied the factor outside the loop instead of inside?
        return sep_vx, sep_vy
        
    def cohesion(self, others, cohesion_factor=1):
        neighborhood = others
        avg_x = 0
        avg_y = 0
        cohesion_vx = 0
        cohesion_vy = 0 
        
        for neighbor in neighborhood:
            avg_x += neighbor.x
            avg_y += neighbor.y
        
        if len(neighborhood) > 0:
            avg_x /= len(neighborhood)
            avg_y /= len(neighborhood)
            cohesion_vx += (avg_x - self.x) * cohesion_factor
            cohesion_vy += (avg_y - self.y) * cohesion_factor
        return cohesion_vx, cohesion_vy
    
    def speed_cap(self, vx, vy, max_speed):
        speed = (vx**2 + vy**2) ** 0.5
        if speed > max_speed:
            scale = max_speed / speed
            vx *= scale
            vy *= scale
        return vx, vy
    
    def move(self, others, neighborhood_range, max_speed=3):
        
        # those who have 
        neighborhood = self.my_neighborhood(others, neighborhood_range)
        
        vx1, vy1 = 0,0
        vx2, vy2 = 0,0
        vx3, vy3 = 0,0
        vx4, vy4 = 0,0
        
        # vx1, vy1 = self.alignment(neighborhood,alignment_factor=1)
        vx2, vy2 = self.separation(neighborhood,collide_range=2, separation_factor=3)
        # vx3, vy3 = self.cohesion(neighborhood, cohesion_factor=1)
        
        self.influence(neighborhood)
            

        # if dominant_agent is not None :
        #     vx4, vy4 = self.follow(neighborhood, dominant_agent, follow_factor=1)
        
        
        # Accumilating is what keeps them moving, if we don't accumilate it will run until one state is reached
        if self.dominant is True:
            angle = random.uniform(0, 2*math.pi)
            self.vx += math.cos(angle) * 1
            self.vy += math.sin(angle) * 1
        else:
            vx4, vy4 = self.follow(neighborhood, follow_factor=1)
            self.vx = vx1 + vx2 + vx3 + vx4
            self.vy = vy1 + vy2 + vy3 + vy4

        
        self.vx, self.vy = self.speed_cap(self.vx, self.vy, max_speed)
        
        self.x += self.vx 
        self.y += self.vy 
        
        self.manage_boundary()
        
        return [self.x, self.y]
 
num_agents = 100
boundary = 100


fig, ax = plt.subplots()
ax.set_xlim(-boundary,boundary)
ax.set_ylim(-boundary,boundary)

agents = [ Agent() for _ in range(num_agents)]
scat = ax.scatter([],[], s=20)


def update(frames):
    for agent in agents:
        agent.move(agents, neighborhood_range=30)
    
    points_to_show = [[agent.x, agent.y] for agent in agents]
    colors = ['red' if agent.dominant else 'blue' for agent in agents]
    scat.set_offsets(points_to_show)
    scat.set_color(colors)

    return scat
     
anim = FuncAnimation(fig, update, frames=5000000, interval=100)

plt.show()

