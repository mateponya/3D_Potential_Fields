# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 23:00:15 2021

@author: PawelG
"""
import numpy as np

def spaceship_planet_sideways():
    """One spaceship and one planet in its way, not collinear"""
    spaceships = np.array([[-2, -2, -2]]))
    spaceships_sizes = np.array([.2])
    goals = np.array([[2, 2, 2]])
    
    planets = np.array([[0, 0, 0.1]])
    planets_sizes = np.array([1])


def spaceship_planet_collinear():
    """One spaceship and one planet in its way, collinear"""
    spaceships = np.array([[-2, -2, -2]]))
    spaceships_sizes = np.array([.2])
    goals = np.array([[2, 2, 2]])
    
    planets = np.array([[0, 0, 0]])
    planets_sizes = np.array([1])


def spaceships2_line():
    """2 spaceships on coliding course, collinear"""
    spaceships = np.array([[-2, -2, -2]]))
    spaceships_sizes = np.array([.2])
    goals = np.array([[2, 2, 2]])


def spaceships2_cross():
    """2 spaceships on coliding course, not collinear"""
    spaceships = np.array([[-2, -2, -2], [-2, -2, 2]]))
    spaceships_sizes = np.array([.2])
    goals = np.array([[1, 1, 1], [1, 1, -1])


def spaceships_meteroid():
    """Spaceship on collision course with meteroid"""
    spaceships = np.array([[-2, 0, 0]]))
    spaceships_sizes = np.array([.2])
    goals = np.array([[1, 0, 0])
    
    meteroids = np.array([3, 0, 0])
    meteroids_velocities = np.array([-1, 0, 0])

    
    
    
    
    
    
    
    