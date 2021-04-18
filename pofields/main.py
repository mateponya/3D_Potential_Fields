# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 19:15:03 2021

@author: PawelG
"""
# import numpy as np
# import scenarios
from visual import Visual
# from simulator import Universe, Spacecraft
import scenarios




universe, animation_speed = scenarios.example()
trajectories, names, colors, sizes, goals, colors_goals = universe.simulate()


visual = Visual(trajectories, names, colors, sizes, goals, colors_goals,
                quality=8, save_animation=False, trace_length=-1, speed=animation_speed)
