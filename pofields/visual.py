# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 15:43:10 2021

@author: PawelG
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

#this will primarly increase relative size of text and window
plt.rcParams["figure.figsize"] = (8, 4.5)
plt.rcParams["figure.dpi"] = 200


class visual:
    
    def __init__(self, planets, spaceships):
        self.planets = planets
        self.spaceships = spaceships
        # self.fig = plt.figure()
        # # self.ax = Axes3D(self.fig, proj_type="ortho") # alternative is "persp"
        # self.ax = Axes3D(self.fig, proj_type="persp") # alternative is "ortho"
        # self.ax.set_xlim([-5, 5])
        # self.ax.set_ylim([-5, 5])
        # self.ax.set_zlim([-5, 5])

    
    
    def show_plot(self):
        self.plot_planets()
        self.plot_spaceships()
        

    def plot_planets(self):
        theta = np.linspace(0, 2*np.pi, 10)
        phi = np.linspace(0, np.pi, 10)
        theta, phi = np.meshgrid(theta, phi)

        for planet in zip(self.planets["x"], self.planets["y"], self.planets["z"], self.planets["r"]):
            x = planet[3]*np.cos(theta)*np.sin(phi) + planet[0]
            y = planet[3]*np.sin(theta)*np.sin(phi) + planet[1]
            z = planet[3]*np.cos(phi) + planet[2]
            self.ax.plot_surface(x, y, z, color="red")
    
    
    
    def plot_spaceships(self):
        self.plot_planets()
        # self.ax.scatter(spaceships["x"], spaceships["y"], spaceships["z"], c="green", s=40)
        [self.ax.plot(spaceship[0], spaceship[1], spaceship[2]) for spaceship in self.spaceships]

    def animate_3d(self):
        def update_animation(num, trajectories, plots):
            print(num)
            for plot, trajectory in zip(plots, trajectories):
                plot.set_data(trajectory[0:2, :num])
                plot.set_3d_properties(trajectory[2, :num])    

        # line_ani = animation.FuncAnimation(fig, func, frames=numDataPoints, fargs=(dataSet,line), interval=50)
        plots = [self.ax.plot(spaceship[0], spaceship[1], spaceship[2])[0] for spaceship in self.spaceships]
        # ani = animation.FuncAnimation(self.fig, update_animation, frames=self.spaceships.shape[2], fargs=(self.spaceships, plots), interval=50, blit=False)
        animation.FuncAnimation(self.fig, update_animation, frames=10, fargs=(self.spaceships, plots), interval=50)


    def d3(self):
        def func(num, dataSe, lin):
            print(num)
            for line, dataSet in zip(lin, dataSe):
                # NOTE: there is no .set_data() for 3 dim data...
                line.set_data(dataSet[0:2, :num])    
                line.set_3d_properties(dataSet[2, :num])    
        fig = plt.figure()
        ax = Axes3D(fig)
        line = [plt.plot(tst[0], tst[1], tst[2], c='g')[0] for tst in self.spaceships] # For line plot
        line_ani = animation.FuncAnimation(fig, func, frames=100, fargs=(self.spaceships, line), interval=50)

        
if __name__ == "__main__":
    no_of_planets = 10
    x = np.random.normal(scale=1.5, size=no_of_planets)
    y = np.random.normal(scale=1.5, size=no_of_planets)
    z = np.random.normal(scale=1.5, size=no_of_planets)
    r = np.random.uniform(low=0.1, high=.5, size=no_of_planets)
    planets = {'x' : x,
               'y' : y,
               'z' : z,
               "r" : r}
    
    # no_of_spaceships = 10
    # x = np.random.normal(scale=1.5, size=no_of_spaceships)
    # y = np.random.normal(scale=1.5, size=no_of_spaceships)
    # z = np.random.normal(scale=1.5, size=no_of_spaceships)
    
    z = np.linspace(-4, 4, 100)
    x = np.cos(4*z)
    y = np.sin(4*z)
    
    z1 = np.linspace(-.5, 4.5, 100)
    x1 = np.cos(10*z1)-1
    y1 = z1-.3
    
    spaceships = np.array([[x, y, z], [x1, y1, z1]])
    # spaceship -> coordinate -> time
    
    # tst = np.array([x, y, z])
    # spaceships = {'x' : x,
    #               'y' : y,
    #               'z' : z}
    # def func(num, dataSe, lin):
    #     print(num)
    #     for line, dataSet in zip(lin, dataSe):
    #         # NOTE: there is no .set_data() for 3 dim data...
    #         line.set_data(dataSet[0:2, :num])    
    #         line.set_3d_properties(dataSet[2, :num])    
    #     return line
    Visual = visual(planets, spaceships)
    # Visual.show_plot()
    # Visual.animate_3d()
    Visual.d3()
    # fig = plt.figure()
    # ax = Axes3D(fig)
    # line = [plt.plot(tst[0], tst[1], tst[2], c='g')[0] for tst in spaceships] # For line plot
    # line_ani = animation.FuncAnimation(fig, func, frames=100, fargs=(spaceships, line), interval=50)