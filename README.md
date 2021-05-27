# 3D Potential Fields Navigation
A simulation environment for dynamic heterogeneous multi-agent potential field navigation.

## Overview
The project is space-themed meaning that our agents are spaceships that have to navigate through space to reach their goal location while avoiding collisions with any other objects. The universe consits of the following types of objects:
- **Spaceships**: They are starting from a given position and heading towards a goal location. They have a maximum speed which limits their movement. Every spaceship has a safe zone around it with a given radius. The aim is not to let any other object intrude into this safe zone.
- **Planets**:  These objects are stationary and usually have  a large radius. Planets serve the purpose of an obstacle and have to be avoided by spaceships.
- **Meteorites**: They are another type of obstacles to be avoided by spaceships. However, they have a much smaller radius and a significantly larger speed.
Planets and meteorites do not change their position, heading or velocity if they come in the vicinity of any other obejct. Hence, spaceships have to do all the work avoiding obstacles as well as other spaceships while ensuring they reach their goal. The method for path planning is potential field navigation where the spaceships are guided by the attractive and repulsive forces. Two new approaches have been elaborated to make navigation even smoother.

## Setting up the environment

- `potfields/simulator.py and simulator2.py` contain the two navigation algorithms.
- `potfields/simulator.py and simulator2.py` contains the scenarios with the locations, goals etc. of all objects in space. The navigation algorithm can be set in the header.
- `potfields/simulator.py and main.py` runs the simulation of a selected scenrio and plots the result. These plots range from the final result showing the trajectories of each of the objects to an `.mp4` video showing the whole process.
- `potfields/visual.py` does the job of showing the results in the desired form.



## Notes
The project uses the **progressbar2** library to visually display the completeness of lengthy simulations. This module can be installed by:
`pip install progressbar2`
