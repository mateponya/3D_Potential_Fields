# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 17:30:17 2021

@author: PawelG
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from time import sleep


def planet_data(r):
    t = np.linspace(0, 2*np.pi, 100)
    [start, start2] = 2*np.pi*np.random.rand(2)
    elevation = .7*np.random.rand()
    p_data = r*np.array([np.cos(start + t),
              np.sin(start + t),
              elevation*np.cos(start2 + t)])
    return p_data.transpose()


def planet_data2(r, r2=0):
    if r==0:
        w=0
    else:
        w = .1*(r**(-1.5))
    if r2==0:
        w2=0
    else:
        w2 = .2*(r2**(-1.5))
    
    
    t = np.linspace(0, 20, 100)
    [start, start2] = 2*np.pi*np.random.rand(2)
    elevation = .5*np.random.rand()
    p_data = r*np.array([np.cos(start + w*t),
              np.sin(start + w*t),
              elevation*np.cos(start2 + w*t)]) + r2*np.array([np.cos(start + w2*t),
              np.sin(start + w2*t),
              elevation*np.cos(start2 + w2*t)])
    return p_data.transpose()

# from mpl_toolkits.mplot3d import Axes3D
# fig = plt.figure()
# ax = Axes3D(fig, proj_type="persp") # alternative is "ortho"
# a=planet_data(.7)
# b=planet_data(1)
# c=planet_data2(1.5, .3)
# d=planet_data(1.7)
# # print(a.shape)
# ax.scatter(*a.transpose())
# ax.scatter(*b.transpose())
# ax.scatter(*c.transpose())
# ax.scatter(*d.transpose())

# import sys
# sys.exit()

def mini_solar():
    planets = []
    
    sun = {}
    sun["name"] = "Sun"
    sun["data"] = planet_data2(0)
    sun["color"] = "yellow"
    sun["r"] = .7
    planets.append(sun)
    
    mercury = {}
    mercury["name"] = "Mercury"
    mercury["data"] = planet_data2(.95)
    mercury["color"] = "tomato"
    mercury["r"] = .2
    planets.append(mercury)
    
    # return planets

    venus = {}
    venus["name"] = "Venus"
    venus["data"] = planet_data2(1.3)
    venus["color"] = "gold"
    venus["r"] = .24
    planets.append(venus)
    
    earth = {}
    earth["name"] = "Earth"
    earth["data"] = planet_data2(1.6)
    earth["color"] = "green"
    earth["r"] = .28
    planets.append(earth)
    
    mars = {}
    mars["name"] = "Mars"
    mars["data"] = planet_data2(1.9)
    mars["color"] = "peru"
    mars["r"] = .2
    planets.append(mars)
    
    jupiter = {}
    jupiter["name"] = "Jupiter"
    jupiter["data"] = planet_data2(2.7)
    jupiter["color"] = "sandybrown"
    jupiter["r"] = .54
    planets.append(jupiter)
    
    saturn = {}
    saturn["name"] = "Saturn"
    saturn["data"] = planet_data2(3.1)
    saturn["color"] = "sienna"
    saturn["r"] = .46
    planets.append(saturn)
    
    uranus = {}
    uranus["name"] = "Uranus"
    uranus["data"] = planet_data2(4.5)
    uranus["color"] = "aqua"
    uranus["r"] = .36
    planets.append(uranus)
    
    neptune = {}
    neptune["name"] = "Neptune"
    neptune["data"] = planet_data2(4.8)
    neptune["color"] = "deepskyblue"
    neptune["r"] = .32
    planets.append(neptune)

    return planets


# fig, ax = plt.subplots()
# for planet in planets:
#     # c = plt.Circle([np.linalg.norm(planet["data"][0]), 0],
#     #             planet["r"],
#     #           color=planet["color"])

#     c = plt.Circle(planet["data"][0],
#                 planet["r"],
#               color=planet["color"])

#     ax.add_patch(c)


# ax.set_xlim([-5, 5])
# ax.set_ylim([-5, 5])
# ax.set_aspect(1)
# plt.show()



# plt.scatter(list(map(lambda e: np.linalg.norm(e["data"][0]), planets)),
#             np.zeros(len(planets)),
#             s=np.array(list(map(lambda e: e["r"], planets)))**2*4000,
#             c=list(map(lambda e: e["color"], planets)))





def simple_spaceships(): 
    z = np.linspace(-4, 4, 100)
    x = np.cos(4*z)
    y = np.sin(4*z)
    
    z1 = np.linspace(-.5, 4.5, 100)
    x1 = np.cos(10*z1) - 1
    y1 = z1 - .3
    
    spaceships = np.array([[x, y, z], [x1, y1, z1]])

    return spaceships





    # COLOURS = np.array(["blue",
    #               "magenta",
    #               "cyan",
    #               "orange",
    #               "lime",
    #               "darkgreen",
    #               "yellow",
    #               "red"])















