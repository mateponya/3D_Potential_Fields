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

from paths import ffmpeg, parent_dir
import datetime

mpl.rcParams['animation.ffmpeg_path'] = ffmpeg()
#this will primarly increase relative size of text and window
plt.rcParams["figure.figsize"] = (8, 4.5)
plt.rcParams["figure.dpi"] = 200




    
class visual:
    
    def __init__(self, trajectories_planets,
                 trajectories_spaceships,
                 names_planets,
                 names_spaceships,
                 colors_planets,
                 colors_spaceships,
                 r_planets):
        
        self.trajectories_planets = trajectories_planets
        self.trajectories_spaceships = trajectories_spaceships
        self.names_planets = names_planets
        self.names_spaceships = names_spaceships
        self.colors_planets = colors_planets
        self.colors_spaceships = colors_spaceships
        self.r_planets = r_planets
        
        self.fig = plt.figure()
        self.ax = Axes3D(self.fig, proj_type="persp") # alternative is "ortho"
        
        self.ax.set_xlim([-5, 5])
        self.ax.set_ylim([-5, 5])
        self.ax.set_zlim([-5, 5])
        
        self.ax.set_xlabel('X axis')
        self.ax.set_ylabel('Y axis')
        self.ax.set_zlabel('Z axis')
        
        self.show_progressbar = False

    

    def _plot_planets(self, i, quality=8):
        theta = np.linspace(0, 2*np.pi, quality)
        phi = np.linspace(0, np.pi, quality)
        theta, phi = np.meshgrid(theta, phi)
        plots_planets = []
        for j in range(len(self.r_planets)):
            coords = np.array([self.r_planets[j]*np.cos(theta)*np.sin(phi) + self.trajectories_planets[j, 0, i],
                               self.r_planets[j]*np.sin(theta)*np.sin(phi) + self.trajectories_planets[j, 1, i],
                               self.r_planets[j]*np.cos(phi) + self.trajectories_planets[j, 2, i]])


            
            plots_planets.append(self.ax.plot_surface(*coords, color=self.colors_planets[j]))
        return plots_planets
    
            
    def animation(self, quality=8):
        self.plots_planets = self._plot_planets(0, quality=quality)
        self.plots_spaceship = [self.ax.plot(s[0, 0:1], s[1, 0:1], s[2, 0:1], c=self.colors_spaceships[i], alpha=.2)[0] for i, s in enumerate(self.trajectories_spaceships)]
        self.scatters_spaceship = [self.ax.scatter(s[0, 0], s[1, 0], s[2, 0], c=self.colors_spaceships[i]) for i, s in enumerate(self.trajectories_spaceships)]
        self.texts = [self.ax.text(s[0, 0], s[1, 0], s[2, 0], "red", color=self.colors_spaceships[i], horizontalalignment='left', verticalalignment='bottom') for i, s in enumerate(self.trajectories_spaceships)]
        self.plot_timer = self.ax.text2D(0.05, 0.95, "2D Text", transform=self.ax.transAxes)
        self.fig.show()
        self.anim = animation.FuncAnimation(self.fig, self._update_animation,
                                            frames=self.trajectories_spaceships.shape[-1], interval=50, blit=False, repeat=True)
      
        
    def _update_animation(self, i):
        
        if self.show_progressbar:
            self.bar.update(i+1)

        self.number = 20
        start_plot_number = i - self.number
        if start_plot_number < 0 or self.number == -1:
            start_plot_number = 0
        
        self.plot_timer.set_text("Animation frame: {}".format(i))

            

        for plot, s in zip(self.plots_spaceship, self.trajectories_spaceships):
            plot.set_data(s[0, start_plot_number:i+1], s[1, start_plot_number:i+1])
            plot.set_3d_properties(s[2, start_plot_number:i+1])
        # self.ax.clear()
        # self._plot_planets()
        for scatter, s, txt in zip(self.scatters_spaceship, self.trajectories_spaceships, self.texts):
            scatter._offsets3d = [[s[0, i]], [s[1, i]], [s[2, i]]]
            # print(txt)
            # if txt.get_text() == "red":
            txt.set_position([s[0, i], s[1, i]])
            txt.set_3d_properties(s[2, i], zdir=None)
                # txt.remove()
        
        for pp in self.plots_planets:
            pp.remove()
        self.plots_planets = self._plot_planets(i)
            
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
        save_name = "animation_" + datetime.datetime.now().strftime("%y%m%d_%H%M.") + file_type
        self.show_progressbar = True
        self.bar = progressbar(max_value=self.trajectories_spaceships.shape[-1])
        if file_type == "gif":
            writer = animation.PillowWriter(fps=20)
        elif file_type == "mp4":
            writer = animation.FFMpegWriter(fps=20)
            
        self.anim.save(parent_dir() + "\\" + save_name, writer=writer)
        self.show_progressbar = False
        self.bar.finish()
        print("Animation saved as: " + save_name)
        print("In main folder: " + parent_dir())
        
        

if __name__ == "__main__":
    import world_maker
    trajectories_spaceships= world_maker.simple_spaceships()
    colors_spaceships = np.array(["green", "blue"])
    names_spaceships= np.array(["Green1", "Blue2"])
    
    planets_raw = world_maker.mini_solar()
    trajectories_planets = np.array(list(map(lambda e: e["data"].transpose(), planets_raw)))
    r_planets = np.array(list(map(lambda e: e["r"], planets_raw)))
    colors_planets = np.array(list(map(lambda e: e["color"], planets_raw)))
    names_planets = np.array(list(map(lambda e: e["name"], planets_raw)))




    Visual = visual(trajectories_planets,
                    trajectories_spaceships,
                    names_planets,
                    names_spaceships,
                    colors_planets,
                    colors_spaceships,
                    r_planets)
    Visual.animation(8)


    # Visual.save_ani("mp4")
    # Visual.save_ani("gif")


    
    
    

