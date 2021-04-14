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
    
    def __init__(self, trajectories,
                 names,
                 colors,
                 size,
                 quality=8,
                 save_animation=False):
        
        self.trajectories = trajectories
        self.names = names
        self.colors = colors
        self.size = size
        self.quality = quality
        self.number = 50
        self.animation_frames = self.trajectories.shape[-1]
        
        self.fig = plt.figure()
        self.ax = Axes3D(self.fig, proj_type="persp") # alternative is "ortho"
        
        self.ax.set_xlim([-5, 5])
        self.ax.set_ylim([-5, 5])
        self.ax.set_zlim([-5, 5])
        
        self.ax.set_xlabel('X axis')
        self.ax.set_ylabel('Y axis')
        self.ax.set_zlabel('Z axis')
        
        self.show_progressbar = False
        
        
        self.start_animation()
        if save_animation:
            self.save_ani()

    

    def _plot_planets(self, i):
        theta = np.linspace(0, 2*np.pi, self.quality)
        phi = np.linspace(0, np.pi, self.quality)
        theta, phi = np.meshgrid(theta, phi)
        plots_objects = []
        for j in range(len(self.size)):
            coords = np.array([self.size[j]*np.cos(theta)*np.sin(phi) + self.trajectories[j, 0, i],
                               self.size[j]*np.sin(theta)*np.sin(phi) + self.trajectories[j, 1, i],
                               self.size[j]*np.cos(phi) + self.trajectories[j, 2, i]])


            
            plots_objects.append(self.ax.plot_surface(*coords, color=self.colors[j]))
        return plots_objects
    
            
    def start_animation(self):
        self.plots_objects = self._plot_planets(0)
        self.plots_trajectories = [self.ax.plot(s[0, 0:1], s[1, 0:1], s[2, 0:1], c=self.colors[i], alpha=.2)[0] for i, s in enumerate(self.trajectories)]
        self.plot_timer = self.ax.text2D(0.05, 0.95, "2D Text", transform=self.ax.transAxes)
        self.fig.show()
        self.anim = animation.FuncAnimation(self.fig, self._update_animation,
                                            frames=self.trajectories.shape[-1], interval=50, blit=False, repeat=True)
      
        
    def _update_animation(self, i):
        
        if self.show_progressbar:
            self.bar.update(i+1)

        
        tail_start_frame = i - self.number
        if tail_start_frame < 0 or self.number == -1:
            tail_start_frame = 0
        
        self.plot_timer.set_text("Animation frame: {}/{}".format(i, self.animation_frames))

            

        for plot, s in zip(self.plots_trajectories, self.trajectories):
            plot.set_data(s[0, tail_start_frame:i+1], s[1, tail_start_frame:i+1])
            plot.set_3d_properties(s[2, tail_start_frame:i+1])
        
        for pp in self.plots_objects:
            pp.remove()
        self.plots_objects = self._plot_planets(i)

  
        
        
    def save_ani(self, file_type="gif"):
        if file_type not in ["gif", "mp4"]:
            print("Give anothet file format")
            return 0
        print("Saving animation in progress...")
        save_name = "animation_" + datetime.datetime.now().strftime("%y%m%d_%H%M.") + file_type
        self.show_progressbar = True
        self.bar = progressbar(max_value=self.animation_frames)
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
    import scenarios
    trajectories = scenarios.simple_spaceships()
    colors = np.array(["green", "blue"])
    names = np.array(["Green1", "Blue2"])
    size = np.array([.5, .5])
    
    planets_raw = scenarios.mini_solar()
    trajectories = np.append(trajectories, list(map(lambda e: e["data"].transpose(), planets_raw)), axis=0)
    size = np.append(size, list(map(lambda e: e["r"], planets_raw)))
    colors = np.append(colors, list(map(lambda e: e["color"], planets_raw)))
    names = np.append(names, list(map(lambda e: e["name"], planets_raw)))



    


    Visual = visual(trajectories,
                    names,
                    colors,
                    size)


    # Visual.save_ani("mp4")
    # Visual.save_ani("gif")


    
    
    

