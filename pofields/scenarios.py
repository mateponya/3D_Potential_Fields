# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 23:00:15 2021

@author: PawelG
"""
import numpy as np
from simulator import Universe, Spacecraft, Planet, Meteorite






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





















# def spaceship_planet_sideways():
#     """One spaceship and one planet in its way, not collinear"""
#     spaceships = np.array([[-2, -2, -2]])
#     spaceships_sizes = np.array([.2])
#     goals = np.array([[2, 2, 2]])
    
#     planets = np.array([[0, 0, 0.1]])
#     planets_sizes = np.array([1])


# def spaceship_planet_collinear():
#     """One spaceship and one planet in its way, collinear"""
#     spaceships = np.array([[-2, -2, -2]])
#     spaceships_sizes = np.array([.2])
#     goals = np.array([[2, 2, 2]])
    
#     planets = np.array([[0, 0, 0]])
#     planets_sizes = np.array([1])


# def spaceships2_line():
#     """2 spaceships on coliding course, collinear"""
#     spaceships = np.array([[-2, -2, -2]])
#     spaceships_sizes = np.array([.2])
#     goals = np.array([[2, 2, 2]])


# def spaceships2_cross():
#     """2 spaceships on coliding course, not collinear"""
#     spaceships = np.array([[-2, -2, -2], [-2, -2, 2]])
#     spaceships_sizes = np.array([.2])
#     goals = np.array([[1, 1, 1], [1, 1, -1]])


# def spaceships_meteroid():
#     """Spaceship on collision course with meteroid"""
#     spaceships = np.array([[-2, 0, 0]])
#     spaceships_sizes = np.array([.2])
#     goals = np.array([[1, 0, 0]])
    
#     meteroids = np.array([3, 0, 0])
#     meteroids_velocities = np.array([-1, 0, 0])

    
