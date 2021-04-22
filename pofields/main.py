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




# universe, animation_speed = scenarios.example()
# universe, animation_speed = scenarios.spaceships2_collinear()
# universe, animation_speed = scenarios.spaceships2_cross()
# universe, animation_speed = scenarios.spaceships3_hex1()
# universe, animation_speed = scenarios.spaceships3_hex2()
# universe, animation_speed = scenarios.spaceships2_collinear()
# universe, animation_speed = scenarios.spaceships2_collinear()
universe, animation_speed = scenarios.spaceships4_stell_octa()



trajectories, names, colors, sizes, goals, colors_goals = universe.simulate()
visual = Visual(trajectories, names, colors, sizes, goals, colors_goals,
                quality=8, save_animation=False, trace_length=-1, speed=animation_speed)
# visual.animate()
# visual.plot2D()
visual.plot3D()