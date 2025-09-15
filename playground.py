import numpy as np
import matplotlib.pyplot as plt

class Agent:
    def __init__(self, position, speed):
        self.position = position
        self.speed = speed

    def move(self, angle):
        dx = self.speed * np.cos(angle)
        dy = self.speed * np.sin(angle)
        self.position = (self.position[0] + dx, self.position[1] + dy)
        

# 3ayez abda2 el simulation hena
if __name__ == "__main__":
    # Create two agents with different starting positions
    agent1 = Agent(position=(0, 0), speed=0.1)
    agent2 = Agent(position=(1, 1), speed=0.1)  # Different starting position
    
    positions1 = [agent1.position]
    positions2 = [agent2.position]

    for _ in range(100):
        # Move both agents with random angles
        agent1.move(angle=np.deg2rad(np.random.randint(0, 360)))
        agent2.move(angle=np.deg2rad(np.random.randint(0, 360)))
        
        positions1.append(agent1.position)
        positions2.append(agent2.position)

    positions1 = np.array(positions1)
    positions2 = np.array(positions2)
    
    # --- PLOTTING CODE FOR TWO AGENTS ---
    plt.figure(figsize=(10, 6))
    
    # Plot first agent (blue)
    plt.plot(positions1[:, 0], positions1[:, 1], 
             linestyle='-', 
             linewidth=1.5, 
             marker='', 
             color='blue',
             alpha=0.8,
             label='Agent 1 Path')
    
    # Plot second agent (red)
    plt.plot(positions2[:, 0], positions2[:, 1], 
             linestyle='-', 
             linewidth=1.5, 
             marker='', 
             color='red',
             alpha=0.8,
             label='Agent 2 Path')
    
    # Mark the start and end points for Agent 1
    plt.plot(positions1[0, 0], positions1[0, 1], 'go', markersize=8, label='Agent 1 Start')
    plt.plot(positions1[-1, 0], positions1[-1, 1], 'bo', markersize=8, label='Agent 1 End')
    
    # Mark the start and end points for Agent 2
    plt.plot(positions2[0, 0], positions2[0, 1], 'yo', markersize=8, label='Agent 2 Start')  # Yellow
    plt.plot(positions2[-1, 0], positions2[-1, 1], 'ro', markersize=8, label='Agent 2 End')   # Red
    
    plt.title("Dual Agent Random Walk Simulation")
    plt.xlabel("X Position")
    plt.ylabel("Y Position")
    plt.axis('equal')  # Important for proper scaling
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.show()
