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

from locators import ffmpeg_file_location, parent_dir_location
import datetime

mpl.rcParams['animation.ffmpeg_path'] = ffmpeg_file_location()
#this will primarly increase relative size of text and window
plt.rcParams["figure.figsize"] = (8, 4.5)
plt.rcParams["figure.dpi"] = 200
plt.rcParams['axes.axisbelow'] = True




    
class Visual:
    
    def __init__(self, trajectories,
                 names,
                 colors,
                 sizes,
                 goals,
                 colors_goals,
                 quality=8,
                 save_animation=False,
                 trace_length=-1,
                 speed=1):
        
        self.trajectories = trajectories[:, :, ::speed]
        self.names = names
        self.colors = colors
        self.sizes = sizes
        self.quality = quality
        self.goals = goals
        self.colors_goals = colors_goals
        self.trace_length = trace_length
        self.animation_frames = self.trajectories.shape[-1]
        self.show_progressbar = False
        
        if save_animation:
            self.save_ani()

    

    def _plot_objects(self, i):
        theta = np.linspace(0, 2*np.pi, self.quality)
        phi = np.linspace(0, np.pi, self.quality)
        theta, phi = np.meshgrid(theta, phi)
        plots_objects = []
        for j in range(len(self.sizes)):
            coords = np.array([self.sizes[j]*np.cos(theta)*np.sin(phi) + self.trajectories[j, 0, i],
                               self.sizes[j]*np.sin(theta)*np.sin(phi) + self.trajectories[j, 1, i],
                               self.sizes[j]*np.cos(phi) + self.trajectories[j, 2, i]])


            
            plots_objects.append(self.ax.plot_surface(*coords, color=self.colors[j], alpha=.5))
        return plots_objects
    
            
    def animate(self):
        self.fig = plt.figure()
        self.ax = Axes3D(self.fig, proj_type="persp", auto_add_to_figure=False) # "ortho" or "persp"
        # self.ax = plt.axes(projection='3d')
        
        self.fig.add_axes(self.ax)
        self.ax.set_xlim([-5, 5])
        self.ax.set_ylim([-5, 5])
        self.ax.set_zlim([-5, 5])
        limits = self.ax.get_w_lims()
        self.ax.set_box_aspect(aspect=(limits[1]-limits[0], limits[3]-limits[2], limits[5]-limits[4]))
        
        self.ax.set_xlabel('X axis')
        self.ax.set_ylabel('Y axis')
        self.ax.set_zlabel('Z axis')
        
        self.plots_objects = self._plot_objects(0)
        self.plots_trajectories = [self.ax.plot(s[0, 0:1], s[1, 0:1], s[2, 0:1], color=self.colors[i], alpha=.7)[0] for i, s in enumerate(self.trajectories)]
        self.plot_timer = self.ax.text2D(0.05, 0.95, "2D Text", transform=self.ax.transAxes)
        self.texts = [self.ax.text(s[0, 0], s[1, 0], s[2, 0], name,
                                   color=self.colors[i],
                                   transform=self.ax.transData + mpl.transforms.ScaledTranslation(0, r/4, self.fig.dpi_scale_trans),
                                   horizontalalignment='center',
                                   verticalalignment='bottom') for i, (s, r, name) in enumerate(zip(self.trajectories, self.sizes, self.names))]
        self.scatters_goals = [self.ax.scatter(s[0], s[1], s[2], color=self.colors_goals[i], alpha=.7) for i, s in enumerate(self.goals)]
        self.anim = animation.FuncAnimation(self.fig, self._update_animation,
                                            frames=self.trajectories.shape[-1], interval=50, blit=False, repeat=True)
        plt.show()

        
    def _update_animation(self, i):
        
        if self.show_progressbar:
            self.bar.update(i+1)

        
        tail_start_frame = i - self.trace_length
        if tail_start_frame < 0 or self.trace_length == -1:
            tail_start_frame = 0
        
        self.plot_timer.set_text("Animation frame: {}/{}".format(i, self.animation_frames))

            

        for plot, s, txt in zip(self.plots_trajectories, self.trajectories, self.texts):
            plot.set_data(s[0, tail_start_frame:i+1], s[1, tail_start_frame:i+1])
            plot.set_3d_properties(s[2, tail_start_frame:i+1])
            txt.set_position([s[0, i], s[1, i]])
            txt.set_3d_properties(s[2, i], zdir=None)
        
        for pp in self.plots_objects:
            pp.remove()
            

        
        self.plots_objects = self._plot_objects(i)
    
    
    def plot2D(self):
        figure, axes = plt.subplots()
        axes.set_aspect(1)
        axes.set_xlim([-5, 5])
        axes.set_ylim([-5, 5])
        plt.title('Circle')
        plt.xticks(np.arange(-5, 6 , 1))
        plt.yticks(np.arange(-5, 6 , 1))
        axes.grid()

        artists = []
        for i in range(self.trajectories.shape[0]):
            artists.append(plt.Circle(self.trajectories[i, 0:2, -1],
                                      self.sizes[i], color=self.colors[i],
                                      label=self.names[i], alpha=0.5))
            axes.add_artist(artists[i])
            axes.plot(*self.trajectories[i, 0:2, :], color=self.colors[i], alpha=.9, label=self.names[i])
        

        for i in range(self.goals.shape[0]):
            axes.scatter(*self.goals[i, 0:2], color=self.colors_goals[i])

        
        axes.legend(handles=artists, bbox_to_anchor=(1.05, 1), loc='upper left')

    
    def plot3D(self):
        
        self.fig = plt.figure()
        self.ax = Axes3D(self.fig, proj_type="ortho", auto_add_to_figure=False) # "ortho" or "persp"
        self.fig.add_axes(self.ax)
        
        self.ax.set_xlim([-5, 5])
        self.ax.set_ylim([-5, 5])
        self.ax.set_zlim([-5, 5])
        
        self.ax.set_xlabel('X axis')
        self.ax.set_ylabel('Y axis')
        self.ax.set_zlabel('Z axis')
        
        self.plots_objects = self._plot_objects(self.trajectories.shape[-1]-1)
        self.plots_trajectories = [self.ax.plot(s[0], s[1], s[2], color=self.colors[i], alpha=.7)[0] for i, s in enumerate(self.trajectories)]
        self.plot_timer = self.ax.text2D(0.05, 0.95, "2D Text", transform=self.ax.transAxes)
        self.texts = [self.ax.text(s[0, -1], s[1, -1], s[2, -1], name,
                                   color=self.colors[i],
                                   transform=self.ax.transData + mpl.transforms.ScaledTranslation(0, r/4, self.fig.dpi_scale_trans),
                                   horizontalalignment='center',
                                   verticalalignment='bottom') for i, (s, r, name) in enumerate(zip(self.trajectories, self.sizes, self.names))]
        # self.scatters_goals = [self.ax.scatter(s[0], s[1], s[2], color=self.colors_goals[i]) for i, s in enumerate(self.goals)]

  
    def _save_plot(self):
        self.fig.set_size_inches(1, 1)
        self.fig.savefig("lol.tiff", format="tiff")
        
    def save_ani(self, file_type="mp4"):
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
            
        self.anim.save(parent_dir_location() + "\\" + save_name, writer=writer)
        self.show_progressbar = False
        self.bar.finish()
        print("Animation saved as: " + save_name)
        print("In main folder: " + parent_dir_location())
        
        

if __name__ == "__main__":
    import visual_demo

    (trajectories, names, colors, sizes) = visual_demo.solar()
    goals = np.array([[1,1,1], [2,2,2]])
    colors_goals = np.array(["red", "black"])

    visual = Visual(trajectories, # shape: (no_of_objects, 3, no_of_frames)
                    names, # shape: (no_of_objects)
                    colors, # shape: (no_of_objects)
                    sizes, # shape: (no_of_objects)
                    goals, # shape: (no_of_goals, 3)
                    colors_goals, # shape: (no_of_goals)
                    quality=8, # try 8 for low and 20 for high quality spheres
                    save_animation=False,
                    trace_length=-1, # tail length in frames (0 for none and -1 for all)
                    speed=1)
    visual.plot3D()
    # visual.animate()


    plt.show()
                        