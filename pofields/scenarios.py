# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 23:00:15 2021

@author: PawelG
"""
import numpy as np
# from simulator import Universe, Spacecraft, Planet, Meteorite
from simulator2 import Universe, Spacecraft, Planet, Meteorite






def example():
    
    # Spaceship needs arguments: name, start, goal, radius, vmax
    # Planet needs arguments: name, loc, radius
    # Meteorite needs arguments: name, start, goal, radius, vmax

    # uncomment spaceships to add them
    ship1 = Spacecraft("S1", [-1.5,-1.5,-1.5], [1,0,0], .2, 0.5)
    # ship2 = Spacecraft("S2", [1.75,1.75,1.75], [0,0,0], .1, 1)
    # ship3 = Spacecraft("S3", [-0.5,1.25, 0.75], [0.5,-1.5,-0.5], .15, 0.75)
    ship4 = Spacecraft("S4", [-1.5,-0.1, -1], [1.25,-0.5, 0.5], .3, 0.3)
    ship5 = Spacecraft("S5", [-1.5,0, 0], [0.5,0, 0], .2, 0.5)
    ship6 = Spacecraft("S6", [1.5,0, 0], [-1.75,-0, 0], .1, 0.5)
    # ship7 = Spacecraft("S7", [1,0.5, -0.25], [-1,-1,1.75], .3, 0.5)
    planet1 = Planet("P1", [1,1,1], 1.)
    meteorite1 = Meteorite("M1", [2,2,1.5], [-2,-2,1.75], .1, 1.5)
    universe = Universe()
    
    speed = 8
    
    return universe, speed



def spaceships2_collinear():
    Spacecraft("S1", [-3, 0, 0], [3, 0, 0], .5, 0.5)
    Spacecraft("S2", [3, 0, 0], [-3, 0, 0], 1.5, 0.5)
    universe = Universe()
    speed = 16
    return universe, speed



def spaceships2_cross():
    Spacecraft("S1", [-3, -3, 0], [3, 3, 0], .5, 0.5)
    Spacecraft("S2", [3, -3, 0], [-3, 3, 0], 1.5, 0.5)
    universe = Universe()
    speed = 16
    return universe, speed



def spaceships3_hex1():
    Spacecraft("S1", 2*np.array([-1, 0, 0]), 2*np.array([1, 0, 0]), .5, 0.5)
    Spacecraft("S2", 2*np.array([np.cos(2*np.pi/3), np.sin(2*np.pi/3), 0]),
               2*np.array([-np.cos(2*np.pi/3), -np.sin(2*np.pi/3), 0]), .5, 0.5)
    Spacecraft("S3", 2*np.array([np.cos(np.pi/3), np.sin(np.pi/3), 0]),
               2*np.array([-np.cos(np.pi/3), -np.sin(np.pi/3), 0]), .5, 0.5)
    universe = Universe()
    speed = 8
    return universe, speed



def spaceships3_hex2():
    [a1, a2, a3] = np.pi*np.array([0, 1/3, 2/3])
    da = np.pi*60/180
    radius = 3
    Spacecraft("S1", radius*np.array([np.cos(a1), np.sin(a1), 0]),
               radius*np.array([-np.cos(a1+da), -np.sin(a1+da), 0]), .5, 0.5)
    Spacecraft("S2", radius*np.array([np.cos(a2), np.sin(a2), 0]),
               radius*np.array([-np.cos(a2+da), -np.sin(a2+da), 0]), .5, 0.5)
    Spacecraft("S3", radius*np.array([np.cos(a3), np.sin(a3), 0]),
               radius*np.array([-np.cos(a3+da), -np.sin(a3+da), 0]), .5, 0.5)


    # da=0
    # Spacecraft("S1", radius*np.array([np.cos(a1), np.sin(a1), 0]),
    #            radius*np.array([-np.cos(a1+da), -np.sin(a1+da), 0]), .5, 0.5)
    # Spacecraft("S2", radius*np.array([np.cos(a2), np.sin(a2), 0]),
    #            radius*np.array([-np.cos(a2+da), -np.sin(a2+da), 0]), .5, 0.5)
    # Spacecraft("S3", radius*np.array([np.cos(a3), np.sin(a3), 0]),
    #            radius*np.array([-np.cos(a3+da), -np.sin(a3+da), 0]), .5, 0.5)
    
    universe = Universe()
    speed = 8
    return universe, speed

def spaceships4_stell_octa():
    "4 spaceships in a tetrahedral arrangement, each going through the centre"
    magnitude = 8
    Spacecraft("S1", magnitude*np.array([0, 0,   np.sqrt(2/3) - 1/(2*np.sqrt(6))]),
                     magnitude*np.array([0, 0, -(np.sqrt(2/3) - 1/(2*np.sqrt(6)))]), 0.3, 0.5)
    Spacecraft("S2", magnitude*np.array([-1/(2*np.sqrt(3)), -1/2, -1/(2*np.sqrt(6))]),
                     magnitude*np.array([ 1/(2*np.sqrt(3)),  1/2,  1/(2*np.sqrt(6))]), 0.5, 0.5)
    Spacecraft("S3", magnitude*np.array([-1/(2*np.sqrt(3)),  1/2, -1/(2*np.sqrt(6))]),
                     magnitude*np.array([ 1/(2*np.sqrt(3)), -1/2,  1/(2*np.sqrt(6))]), 1.0, 0.5)
    Spacecraft("S4", magnitude*np.array([ 1/np.sqrt(3), 0, -1/(2*np.sqrt(6))]),
                     magnitude*np.array([-1/np.sqrt(3), 0,  1/(2*np.sqrt(6))]), 1.25, 0.5)
    
    universe = Universe()
    speed = 25
    
    return universe, speed

def planets_in_line():
    Spacecraft("S1", np.array([4, 0, 0]), np.array([-4, 0, 0]), 0.3, 0.5)
    Planet("P1", [2.5, 0, 0], 1.)
    Planet("P2", [0, 0, 0], 1.)
    Planet("P3", [-2.5, 0, 0], 1.)
    
    universe = Universe()
    speed = 16
    
    return universe, speed

def planets_in_line_zigzag():
    Spacecraft("S1", np.array([4.5, 0, 0]), np.array([-4.5, 0, 0]), 0.3, 0.5)
    Planet("P1", [2.5, 0, 0], 1.)
    Planet("P2", [1, 3, 0], 1.25)
    Planet("P3", [0, 0, 3], 1.)
    Planet("P4", [0, 0, -3], 1.5)
    Planet("P5", [0, -3, 0], 1.)
    Planet("P6", [-1, 2, 2.1], 1.3)
    Planet("P7", [-1, -2, 2.1], 1.5)
    Planet("P8", [-1, 2.1, -2], 1.25)
    Planet("P9", [-1, -2.1, -2], 1.)
    Planet("P10", [0, 0, 0], 1.2)
    Planet("P11", [-2.5, 0, 0], 1.5)
    
    universe = Universe()
    speed = 16
    
    return universe, speed

def multi_meteor_line():
    ship1 = Spacecraft("S1", np.array([4.5, 0, 0]), np.array([-4.5, 0, 0]), 0.3, 0.5)
    for n in range(5):
        pos = np.random.uniform(-6.0, 6.0, 3)
        # heading = (ship1.start+(ship1.goal-ship1.start)*np.random.rand())-pos
        heading = (ship1.start+(ship1.goal-ship1.start)/2)-pos
        # dir1 = np.random.rand(3)
        # dir1 -= dir1.dot(heading) * heading
        dir1 = np.cross(heading, np.array([1,0,0]))
        dir1 /= np.linalg.norm(dir1)
        dir2 = np.cross(dir1, heading)
        dir2 /= np.linalg.norm(dir2)
        for i in range(5):
            rand_heading = pos + 10*heading + 50*(np.random.uniform(-1,1)*dir1 + np.random.uniform(-1,1)*dir2)
            Meteorite("M"+str(n+i), pos, rand_heading, 0.1, np.random.rand()*2+0.5)
    universe = Universe()
    speed = 25
    
    return universe, speed