# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 12:04:38 2021

@author: Mate
"""

import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import matplotlib as mpl
from locators import ffmpeg_file_location
mpl.rcParams['animation.ffmpeg_path'] = ffmpeg_file_location()
import time

WALL_OFFSET = 2.
dt = 0.01
T = 15

class Object:
    """The basic unit in the space"""
    
    obj_type = ""
    
    def __init__(self, name, start, goal, radius, vmax):
        self.name = name
        self.start = np.array(start)
        self.goal = np.array(goal)
        self.position = np.array([start])
        self.next = np.array(start)
        self.radius = radius
        self.vmax = vmax
        Universe.objects.append(self)
        
    def velocity(self, position):
        pass
        
    def velocity_to_goal(self, position):
        pass
    
    def velocity_from_obstacles(self, position):
        pass
    
    def potfield(self):
        pass
    
    def update(self):
        pass
    
    def move(self):
        pass
    
    def __str__(self):
        return ("Name:\t{}\nType:\t{}\nStart:\t{}\nGoal:\t{}\nRad:\t{}\nVmax:\t{}\n"
                .format(self.name, self.obj_type, self.start, self.goal, self.radius,
                        self.vmax))
        
class Spacecraft(Object):
    """A spacecraft going in space from start to goal. Derived from Object class"""
    
    obj_type = 'Spacecraft'
    
    def __init__(self, name, start, goal, radius, vmax):
        super().__init__(name, start, goal, radius, vmax)
    
    def velocity(self, position):
        v_goal = self.velocity_to_goal(position)
        v_obst = self.velocity_from_obstacles(position)
        v = v_goal + v_obst
        v += np.random.rand(3) * self.vmax / 3
        
        def cap(v):
            n = np.linalg.norm(v)
            if n > self.vmax:
                return v / n * self.vmax
            return v
        
        return cap(v)
        
    def velocity_to_goal(self, position, mode="uniform"):
        dist = np.linalg.norm(self.goal - position)
        if mode == "uniform":
            v = self.vmax * (self.goal - position)/dist
        elif mode == "parabolic":
            v = dist**2 * (self.goal - position)/dist
        return v
    
    def velocity_from_obstacles(self, position):
        v = np.zeros(3)
        for obst in (obj for obj in Universe.objects if obj is not self):
            dist = np.linalg.norm(obst.position[-1] - position)
            spread = np.mean((self.vmax, obst.vmax)) * np.sum((self.radius, obst.radius))
            scale = norm.pdf(dist, loc=0, scale=spread) * self.vmax / norm.pdf(sum((self.radius,obst.radius)), loc=0, scale=spread)
            v += scale * (position - obst.position[-1])/dist
            d_goal = self.goal - position
            d_obst = obst.position[-1] - position
            perp = d_obst - np.dot(d_obst,d_goal)/np.dot(d_goal,d_goal)*d_goal
            if np.linalg.norm(perp) > 0:
                u_perp = perp / np.linalg.norm(perp)
                v += - u_perp * 1/dist / 4
        return v
            
    
    def update(self, method="euler"):
        # if near goal, return goal
        if np.linalg.norm(self.position[-1]-self.goal) < 0.01:
            self.next = self.goal
            return
        
        # update the next position from the current
        if method == "euler":
            v = self.velocity(self.position[-1])
            self.next = self.position[-1] + dt*v
        else:
            pass
        
    def move(self):
        # move from current position to the next
        self.position = np.vstack((self.position, self.next))
        
class Planet(Object):
    """A stationary planet in space. Derived from Object class"""
    
    obj_type = 'Planet'
    
    def __init__(self, name, loc, radius):
        super().__init__(name, loc, [], radius, [])            
    
    def update(self, method="euler"):
        # planet does not move, it stays at the same location
        if method == "euler":
            self.next = self.position[-1]
        else:
            pass
        
    def move(self):
        # move from current position to the next
        self.position = np.vstack((self.position, self.next))
        
class Meteorite(Object):
    """A meteorite going in space on a straight line, undisturbed. Derived from Object class"""
    
    obj_type = 'Meteorite'
    
    def __init__(self, name, start, goal, radius, vmax):
        super().__init__(name, start, goal, radius, vmax)
    
    def velocity(self, position):
        direction = self.goal - self.start
        return self.vmax * direction/np.linalg.norm(direction)       
    
    def update(self, method="euler"):
        # if near goal, return goal
        if np.linalg.norm(self.position[-1]-self.goal) < 0.01:
            self.next = self.goal
            return
        
        # update the next position from the current
        if method == "euler":
            v = self.velocity(self.position[-1])
            self.next = self.position[-1] + dt*v
        else:
            pass
        
    def move(self):
        # move from current position to the next
        self.position = np.vstack((self.position, self.next))

class Universe:
    
    objects = list()
    
    def __init__(self):
        pass
    
    def list_objects(self, mode="tabular"):
        if mode == "linear":
            for obj in Universe.objects:
                print(obj)
        elif mode == "tabular":
                
            def get_pretty_table(iterable, header):
                max_len = [len(x) for x in header]
                for row in iterable:
                    row = [row] if type(row) not in (list, tuple) else row
                    for index, col in enumerate(row):
                        if max_len[index] < len(str(col)):
                            max_len[index] = len(str(col))
                # output = '-' * (sum(max_len) + 1) + '\n'
                output = '|' + ''.join(['-'*len(h) + '-' * (l - len(h)) + '-' for h, l in zip(header, max_len)])[:-1] + '|' + '\n'
                output += '|' + ''.join([h + ' ' * (l - len(h)) + '|' for h, l in zip(header, max_len)]) + '\n'
                # output += '-' * (sum(max_len) + 1) + '\n'
                output += '|' + ''.join(['-'*len(h) + '-' * (l - len(h)) + '-' for h, l in zip(header, max_len)])[:-1] + '|' + '\n'
                for row in iterable:
                    row = [row] if type(row) not in (list, tuple) else row
                    output += '|' + ''.join([str(c) + ' ' * (l - len(str(c))) + '|' for c, l in zip(row, max_len)]) + '\n'
                # output += '-' * (sum(max_len) + 1) + '\n'
                output += '|' + ''.join(['-'*len(h) + '-' * (l - len(h)) + '-' for h, l in zip(header, max_len)])[:-1] + '|' + '\n'
                return output
            
            header = ["Name", "Type", "Start", "Goal", "Radius", "V_max"]
            iterable = list()
            for obj in Universe.objects:
                iterable.append([obj.name, obj.obj_type, obj.start, obj.goal, obj.radius, obj.vmax])
            print(get_pretty_table(iterable, header))
        
    def simulate(self):
        for iter in range(int(T/dt)):
            for obj in Universe.objects:
                obj.update()
            for obj in Universe.objects:
                obj.move()
        
        trajectories = np.dstack(list(obj.position for obj in Universe.objects)).T
        names = list(obj.name for obj in Universe.objects)
        cmap = plt.cm.get_cmap('Paired')
        N = len(Universe.objects)-1
        colors = list(cmap(n/N) for n in range(N+1))
        sizes = list(obj.radius for obj in Universe.objects)
        goals = np.vstack(list(obj.goal for obj in Universe.objects))
        colors_goals = colors.copy()
        
        return trajectories, names, colors, sizes, goals, colors_goals
        
if __name__ == '__main__':
    
    # uncomment spaceships to add them
    ship1 = Spacecraft("S1", [-1.5,-1.5,-1.5], [1,0,0], .2, 0.5)
    # ship2 = Spacecraft("S2", [1.75,1.75,1.75], [0,0,0], .1, 1)
    # ship3 = Spacecraft("S3", [-0.5,1.25, 0.75], [0.5,-1.5,-0.5], .15, 0.75)
    ship4 = Spacecraft("S4", [-1.5,-0.1, -1], [1.25,-0.5, 0.5], .3, 0.3)
    ship5 = Spacecraft("S5", [-1.5,0, 0], [0.5,0, 0], .2, 0.5)
    ship6 = Spacecraft("S6", [1.5,0, 0], [-1.75,-0, 0], .1, 0.5)
    # ship7 = Spacecraft("S7", [1,0.5, -0.25], [-1,-1,1.75], .3, 0.5)
    
    universe = Universe()
    # list all objects in the system
    universe.list_objects("tabular")
    # animate system
    trajectories, names, colors, sizes, goals, colors_goals = universe.simulate()
    pass