# 2D Driving Simulation  
**Author**: Viet Quoc Tran (Vincent)  

---

## Overview  
This project simulates a 2D self-driving car environment inspired by real-world autonomous driving systems, such as Tesla's Autopilot. The simulation demonstrates the fundamentals of autonomous driving by teaching an AI-powered car to navigate a track, avoid collisions, and complete the course successfully.  

---

## Features  
- **Manual Driving Mode**: Control the car manually to understand its movement and behavior.  
- **AI Self-Driving Mode**: An AI system powered by the NEAT algorithm learns to drive autonomously.  
- **Radar-Based Perception**: The car uses a radar system to detect potential collisions and make informed decisions.  
- **NEAT Implementation**: Efficient and lightweight neural network evolution for reinforcement learning.  

---

## Design Rationale  

### Inspiration  
Every year, a significant number of road accidents occur due to human error. Autonomous vehicles offer a solution to improve safety and reduce accidents. Inspired by Tesla's self-driving technology, this project explores the basics of how AI can learn to navigate and make decisions in a 2D driving environment.  

---

### Problem Statement  
Design and implement an AI system capable of navigating a predefined track without human intervention. The AI must learn to complete the track while avoiding collisions with the borders.  

---

### Step-by-Step Solution  

#### 1. Develop a Basic 2D Environment  
- **Why?**  
   Establish a defined "world" for the car to operate within, laying the groundwork for manual and autonomous driving systems.  
- **How?**  
   A static game window with assets such as a track, finish line, and grass was created to provide visual and physical boundaries.  

#### 2. Implement Manual Control  
- **Why?**  
   Understand the movement dynamics of the car and gain insights into the importance of steering versus speed in navigation.  
- **How?**  
   Keyboard controls were added to allow the player to move the car forward, backward, and steer left or right.  

#### 3. Add a Radar System  
- **Why?**  
   Enable the car to "sense" its surroundings by detecting obstacles at various angles, simulating how autonomous cars perceive the world.  
- **How?**  
   A radar system was designed to calculate distances to obstacles at predefined angles, feeding this data as inputs to the AI system.  

#### 4. Develop the AI System Using NEAT  
- **Why?**  
   NEAT (NeuroEvolution of Augmenting Topologies) is ideal for lightweight and accessible reinforcement learning tasks. It evolves neural networks without the need for complex and resource-intensive models.  
- **How?**  
   NEAT was integrated to train neural networks that control the car's actions, learning from trial and error to optimize navigation and avoid collisions.  

---

## How to Run the Simulation  

1. **Clone the repository**.  
2. **Install the required dependencies**:  
   ```bash
   pip install pygame neat-python
3. **Run the main script**:
   ```bash
   python main.py
4. **Choose a mode**:
    - Manual Driving Mode
    - AI Self-Driving Mode
      
---

## Technologies Used
- Python: Programming language for the simulation.
- Pygame: For rendering the 2D environment and handling inputs.
- NEAT-Python: To implement the neuroevolution algorithm for training the AI.

## Future Improvements
- Add dynamic obstacles to increase difficulty.
- Implement advanced neural network architectures for better learning.
- Include multiple levels with varying track designs.
- Add a scoring system to evaluate AI performance more effectively.
- Run simulation on random generated track

Happy Driving!
