# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 15:43:10 2021

@author: PawelG
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl
from progressbar.bar import ProgressBar as progressbar

from paths import ffmpeg

mpl.rcParams['animation.ffmpeg_path'] = ffmpeg()
#this will primarly increase relative size of text and window
plt.rcParams["figure.figsize"] = (8, 4.5)
plt.rcParams["figure.dpi"] = 200


class visual:
    
    def __init__(self, planets, spaceships):
        self.planets = planets
        self.spaceships = spaceships
        self.fig = plt.figure()
        # self.ax = self.fig.add_subplot(111, projection="3d")
        # # self.ax = Axes3D(self.fig, proj_type="ortho") # alternative is "persp"
        self.ax = Axes3D(self.fig, proj_type="persp") # alternative is "ortho"
        self.ax.set_xlim([-5, 5])
        self.ax.set_ylim([-5, 5])
        self.ax.set_zlim([-5, 5])
        self.show_progressbar = False

    
    
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


        
    def _update_animation(self, i):
        if self.show_progressbar:
            self.bar.update(i+1)
        for plot, s in zip(self.plots, self.spaceships):
            plot.set_data(s[0, :i], s[1, :i])
            plot.set_3d_properties(s[2, :i])
            
            
    def start(self):
        self.plot_planets()
        self.plots = [self.ax.plot(s[0, 0:2], s[1, 0:2], s[2, 0:2])[0] for s in self.spaceships]
        self.anim = animation.FuncAnimation(self.fig, self._update_animation,
                                            frames=self.spaceships.shape[-1], interval=50, blit=False)
        
        
        
    def save_ani(self, file_type):
        if file_type not in ["gif", "mp4"]:
            print("Give anothet file format")
            return 0
        print("Saving animation in progress...")
        self.show_progressbar = True
        self.bar = progressbar(max_value=self.spaceships.shape[-1]).start()
        if file_type == "gif":
            writer_gif = animation.PillowWriter(fps=30) 
            self.anim.save("asd.mp4", writer=writer_gif)
        elif file_type == "mp4":
            writer_video = animation.FFMpegWriter(fps=60)
            self.anim.save("asd.mp4", writer=writer_video)
            self.show_progressbar = False
            self.bar.finish()
        print("Animation saved as: TBD")
        

if __name__ == "__main__":
    def get_planets_spaceships(no_of_planets):
        x = np.random.normal(scale=1.5, size=no_of_planets)
        y = np.random.normal(scale=1.5, size=no_of_planets)
        z = np.random.normal(scale=1.5, size=no_of_planets)
        r = np.random.uniform(low=0.1, high=.5, size=no_of_planets)
        planets = {'x' : x,
                   'y' : y,
                   'z' : z,
                   "r" : r}
        
        
        z = np.linspace(-4, 4, 100)
        x = np.cos(4*z)
        y = np.sin(4*z)
        
        z1 = np.linspace(-.5, 4.5, 100)
        x1 = np.cos(10*z1)-1
        y1 = z1-.3
        
        spaceships = np.array([[x, y, z], [x1, y1, z1]])
        # spaceship -> coordinate -> time
        return planets, spaceships
    

    [planets, spaceships] = get_planets_spaceships(10)

    Visual = visual(planets, spaceships)
    # Visual.show_plot()
    # Visual.animate_3d()
    Visual.start()
    Visual.save_ani("mp4")
    # plt.show()
    
    
    

