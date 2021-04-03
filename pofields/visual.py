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
    
    def __init__(self, planets,
                 spaceships,
                 planets_names,
                 spaceship_names,
                 planet_colors,
                 spaceship_colors,
                 planet_size):
        
        self.planets = planets
        self.spaceships = spaceships
        self.planets_names = planets_names
        self.spaceship_names = spaceship_names
        self.planet_colors = planet_colors
        self.spaceship_colors = spaceship_colors
        self.planet_size = planet_size
        
        self.fig = plt.figure()
        self.ax = Axes3D(self.fig, proj_type="persp") # alternative is "ortho"
        
        self.ax.set_xlim([-5, 5])
        self.ax.set_ylim([-5, 5])
        self.ax.set_zlim([-5, 5])
        
        self.ax.set_xlabel('X axis')
        self.ax.set_ylabel('Y axis')
        self.ax.set_zlabel('Z axis')
        
        self.show_progressbar = False

    
    # def just_plot(self):
    #     self._plot_planets()
    #     self._plot_spaceships()
    
    
    # def _plot_spaceships(self):
    #     self._plot_planets()
    #     [self.ax.plot(spaceship[0], spaceship[1], spaceship[2], self.COLOURS[i]) for i, spaceship in enumerate(self.spaceships)]


    def _plot_planets(self, quality=8):
        theta = np.linspace(0, 2*np.pi, quality)
        phi = np.linspace(0, np.pi, quality)
        theta, phi = np.meshgrid(theta, phi)
        plots_planets = []
        for i, planet in enumerate(zip(self.planets["x"], self.planets["y"], self.planets["z"], self.planets["r"])):
            x = planet[3]*np.cos(theta)*np.sin(phi) + planet[0]
            y = planet[3]*np.sin(theta)*np.sin(phi) + planet[1]
            z = planet[3]*np.cos(phi) + planet[2]
            plots_planets.append(self.ax.plot_surface(x, y, z, color=self.planet_colors[i]))
        return plots_planets
    
            
    def animation(self):
        self.plots_planets = self._plot_planets()
        self.plots_spaceship = [self.ax.plot(s[0, 0:1], s[1, 0:1], s[2, 0:1], c=self.spaceship_colors[i], alpha=.2)[0] for i, s in enumerate(self.spaceships)]
        self.scatters_spaceship = [self.ax.scatter(s[0, 0], s[1, 0], s[2, 0], c=self.spaceship_colors[i]) for i, s in enumerate(self.spaceships)]
        self.texts = [self.ax.text(s[0, 0], s[1, 0], s[2, 0], "red", color=self.spaceship_colors[i], horizontalalignment='left', verticalalignment='bottom') for i, s in enumerate(self.spaceships)]
        self.plot_timer = self.ax.text2D(0.05, 0.95, "2D Text", transform=self.ax.transAxes)
        self.fig.show()
        self.anim = animation.FuncAnimation(self.fig, self._update_animation,
                                            frames=self.spaceships.shape[-1], interval=50, blit=False, repeat=True)
      
        
    def _update_animation(self, i):
        
        if self.show_progressbar:
            self.bar.update(i+1)

        self.number = 20
        start_plot_number = i - self.number
        if start_plot_number < 0 or self.number == -1:
            start_plot_number = 0
        
        self.plot_timer.set_text("Animation frame: {}".format(i))

            

        for plot, s in zip(self.plots_spaceship, self.spaceships):
            plot.set_data(s[0, start_plot_number:i+1], s[1, start_plot_number:i+1])
            plot.set_3d_properties(s[2, start_plot_number:i+1])
        # self.ax.clear()
        # self._plot_planets()
        for scatter, s, txt in zip(self.scatters_spaceship, self.spaceships, self.texts):
            scatter._offsets3d = [[s[0, i]], [s[1, i]], [s[2, i]]]
            # print(txt)
            # if txt.get_text() == "red":
            txt.set_position([s[0, i], s[1, i]])
            txt.set_3d_properties(s[2, i], zdir=None)
                # txt.remove()
        
        for pp in self.plots_planets:
            pp.remove()
        self.plots_planets = self._plot_planets()
            
        # for plot in self.plots_planets:
        #     plot.remove()
        #     plot = self.ax.plot_surface(x, y, z, color="lightcoral")
            
        # self.ax.cla()
        # self._plot_planets()
        # return self.scatters_spaceship, self.plots_spaceship

  
        
        
    def save_ani(self, file_type):
        if file_type not in ["gif", "mp4"]:
            print("Give anothet file format")
            return 0
        print("Saving animation in progress...")
        self.show_progressbar = True
        self.bar = progressbar(max_value=self.spaceships.shape[-1])
        if file_type == "gif":
            writer_gif = animation.PillowWriter(fps=30) 
            self.anim.save("asd.gif", writer=writer_gif)
        elif file_type == "mp4":
            writer_video = animation.FFMpegWriter(fps=20)
            self.anim.save("asd.mp4", writer=writer_video)
            self.show_progressbar = False
            self.bar.finish()
        print("Animation saved as: TBD")
        

if __name__ == "__main__":
    # import time
    def get_planets_spaceships(no_of_planets):
        # np.random.seed(0)
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
        x1 = np.cos(10*z1) - 1
        y1 = z1 - .3
        
        spaceships = np.array([[x, y, z], [x1, y1, z1]])
        # spaceship -> coordinate -> time
        return planets, spaceships
    COLOURS = np.array(["blue",
                  "magenta",
                  "cyan",
                  "orange",
                  "lime",
                  "darkgreen",
                  "yellow",
                  "red"])

    [planets, spaceships] = get_planets_spaceships(8)

    Visual = visual(planets, spaceships, COLOURS, COLOURS, COLOURS, COLOURS, [1, 1, 1, 1, 1, 1, 1, 1, 1, 2])
    # Visual.just_plot()
    # Visual.animate_3d()
    Visual.animation()

    # print(1)
    # Visual.save_ani("mp4")
    # Visual.save_ani("gif")
    # plt.show()
    # time.sleep(2)

    
    
    

