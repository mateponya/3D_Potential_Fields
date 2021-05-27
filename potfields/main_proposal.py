# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 10:53:33 2021

@author: Mate
"""


import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import matplotlib.animation as animation
# import matplotlib as mpl 
# mpl.rcParams['animation.ffmpeg_path'] = r"C:\\Users\\Mate\\Desktop\\ffmpeg.exe"
from paths import ffmpeg
import matplotlib as mpl
mpl.rcParams['animation.ffmpeg_path'] = ffmpeg()
import time

WALL_OFFSET = 2.
dt = 0.01
T = 10

class Object:
    """The basic unit in the space"""
    
    obj_type = ""
    
    def __init__(self, name, start, goal, radius, vmax):
        self.name = name
        self.start = np.array(start)
        self.goal = np.array(goal)
        self.position = np.array([start])
        self.next = np.array(start)
        self.radius = radius
        self.vmax = vmax
        Universe.objects.append(self)
        
    def velocity(self, position):
        pass
        
    def velocity_to_goal(self, position):
        pass
    
    def velocity_from_obstacles(self, position):
        pass
    
    def potfield(self):
        pass
    
    def update(self):
        pass
    
    def move(self):
        pass
    
    def __str__(self):
        return ("Name:\t{}\nType:\t{}\nStart:\t{}\nGoal:\t{}\nRad:\t{}\nVmax:\t{}\n"
                .format(self.name, self.obj_type, self.start, self.goal, self.radius,
                        self.vmax))
        
class Spacecraft(Object):
    """A spacecraft going in space from start to goal. Derived from Object class"""
    
    obj_type = 'Spacecraft'
    
    def __init__(self, name, start, goal, radius, vmax):
        super().__init__(name, start, goal, radius, vmax)
    
    def velocity(self, position):
        v_goal = self.velocity_to_goal(position)
        v_obst = self.velocity_from_obstacles(position)
        v = v_goal + v_obst
        
        def cap(v):
            n = np.linalg.norm(v)
            if n > self.vmax:
                return v / n * self.vmax
            return v
        
        return cap(v)
        
    def velocity_to_goal(self, position):
        dist = np.linalg.norm(self.goal - position)
        return self.vmax * (self.goal - position)/dist

    
    def velocity_from_obstacles(self, position):
        v = np.zeros(2)
        current = self.position.shape[0]-1
        for obst in (obj for obj in Universe.objects if obj is not self):
        # for obst in Universe.objects if obj is not self:
            dist = np.linalg.norm(obst.position[current] - position)
            # scale = norm.pdf(dist, loc=0, scale=obst.radius*self.vmax) / norm.pdf(0, loc=0, scale=obst.radius*self.vmax)
            scale = norm.pdf(dist, loc=0, scale=np.sum((self.radius, obst.radius)))
            v += scale * (position - obst.position[current])/dist
        return v
        
    def potfield(self):
        x = y = np.linspace(-WALL_OFFSET, WALL_OFFSET, 25)
        # matrices each with the x and y coordinates of the corresponding point
        X, Y = np.meshgrid(x,y)
        
        # matrix of vectors containing the coordinates of the corresponding point
        XY = np.stack((X,Y), axis=2)
        
        # initialise the vector field
        Field = np.zeros_like(XY)
        
        # FIELD FROM OBSTACLES
        # for obst in Universe.object if obst is not self:
        for obst in (obj for obj in Universe.objects if obj is not self):
            
            # matrix of vectors containing the vector from the obstacle
            # to the corresponding point
            D = XY - obst.position[-1]
            
            # matrix containing the absolute values of the above vectors
            # i.e. the distance of the corresponding point from the obstacle
            Abs = np.linalg.norm(D, axis=2)
            
            # unit vectors from the obstacle to the corresponding point
            # note: the stack operation is needed as Abs in (n,n) and D is (n,n,2)
            # hence we need to copy (or extend) Abs into one more dimension (hence the stacking)
            # Unit = D / np.stack((Abs, Abs), axis=2) # only for understanding
            
            # the above can however be done in the following manner as well
            Unit = D / Abs[:,:,None]
            
            # at the location of the obstacle we divide by zero (as the distance from itself is zero)
            # this results 'nan' values which can now be set to zero (the plot in this case will show a dot there)
            # Unit[np.isnan(Unit)] = 0 # not necessary
            
            # scale the unit vectors by the Gaussian of the distance of the corresponding points
            # from the obstacle
            # note: we use the same logic here to broadcast a (n,n) matrix to multiply it with a (n,n,2) matrix
            Field += Unit * norm.pdf(Abs, loc=0, scale=np.sum((self.radius, obst.radius)))[:,:,None]
            
        # FIELD FROM GOAL
        # matrix of vectors containing the vector to the goal
        # from the corresponding point
        D = self.goal - XY
        
        # matrix containing the absolute values of the above vectors
        # i.e. the distance of the corresponding point from the goal
        Abs = np.linalg.norm(D, axis=2)
        
        # unit vectors to the goal from the corresponding point
        # note: the stack operation is needed as Abs in (n,n) and D is (n,n,2)
        # hence we need to copy (or extend) Abs into one more dimension (hence the stacking)
        # Unit = D / np.stack((Abs, Abs), axis=2) # only for understanding
        
        # the above can however be done in the following manner as well
        Unit = D / Abs[:,:,None]
        
        # at the location of the goal we divide by zero (as the distance from itself is zero)
        # this results 'nan' values which can now be set to zero (the plot in this case will show a dot there)
        # Unit[np.isnan(Unit)] = 0 # not necessary
        
        # scale the unit vectors by a constant
        # note: we use the same logic here to broadcast a (n,n) matrix to multiply it with a (n,n,2) matrix
        Field += Unit * self.vmax
        
        # GENERATE U,V FIELDS
        # U and V are the x and y coordinates of the unit vectors in Field
        U = Field[:,:,0]
        V = Field[:,:,1]
        
        return X,Y,U,V
            
    
    def update(self, method="euler"):
        # if near goal, return goal
        if np.linalg.norm(self.position[-1]-self.goal) < 0.01:
            self.next = self.goal
            return
        
        # update the next position from the current
        if method == "euler":
            v = self.velocity(self.position[-1])
            self.next = self.position[-1] + dt*v
        else:
            pass
        
    def move(self):
        # move from current position to the next
        self.position = np.vstack((self.position, self.next))

class Universe:
    
    objects = list()
    
    def __init__(self):
        pass
    
    def list_objects(self, mode="tabular"):
        if mode == "linear":
            for obj in Universe.objects:
                print(obj)
        elif mode == "tabular":
                
            def get_pretty_table(iterable, header):
                max_len = [len(x) for x in header]
                for row in iterable:
                    row = [row] if type(row) not in (list, tuple) else row
                    for index, col in enumerate(row):
                        if max_len[index] < len(str(col)):
                            max_len[index] = len(str(col))
                # output = '-' * (sum(max_len) + 1) + '\n'
                output = '|' + ''.join(['-'*len(h) + '-' * (l - len(h)) + '-' for h, l in zip(header, max_len)])[:-1] + '|' + '\n'
                output += '|' + ''.join([h + ' ' * (l - len(h)) + '|' for h, l in zip(header, max_len)]) + '\n'
                # output += '-' * (sum(max_len) + 1) + '\n'
                output += '|' + ''.join(['-'*len(h) + '-' * (l - len(h)) + '-' for h, l in zip(header, max_len)])[:-1] + '|' + '\n'
                for row in iterable:
                    row = [row] if type(row) not in (list, tuple) else row
                    output += '|' + ''.join([str(c) + ' ' * (l - len(str(c))) + '|' for c, l in zip(row, max_len)]) + '\n'
                # output += '-' * (sum(max_len) + 1) + '\n'
                output += '|' + ''.join(['-'*len(h) + '-' * (l - len(h)) + '-' for h, l in zip(header, max_len)])[:-1] + '|' + '\n'
                return output
            
            header = ["Name", "Type", "Start", "Goal", "Radius", "V_max"]
            iterable = list()
            for obj in Universe.objects:
                iterable.append([obj.name, obj.obj_type, obj.start, obj.goal, obj.radius, obj.vmax])
            print(get_pretty_table(iterable, header))
        
    def animate(self, mode="all", save=False):
        if mode == "all":
            # show all objects on the same plot
            pass
            
        elif mode == "individual":
            ncols = min(len(Universe.objects), 3)
            nrows = int(np.ceil(len(Universe.objects)/ncols))
            fig = plt.figure(figsize=(4*ncols, 4*nrows))
            cmap = plt.cm.get_cmap('Paired')
            N = len(Universe.objects)-1
            
            fields = list()
            trajectories = list()
            markers = list()
            obst_markers = list()
            obst_texts = list()
            
            # create subplots
            for n,obj in enumerate(Universe.objects):
                ax = fig.add_subplot(nrows, ncols, n+1)
                ax.set_xlim(-WALL_OFFSET, WALL_OFFSET)
                ax.set_ylim(-WALL_OFFSET, WALL_OFFSET)
                ax.set_title(obj.name)
                ax.set_aspect('equal')
                ax.scatter(obj.goal[0], obj.goal[1], marker='+', color=cmap(n/N))
                X,Y,U,V = obj.potfield()
                Qu = ax.quiver(X, Y, U, V, units='width')
                Tr = ax.plot([], [], color=cmap(n/N))[0]
                Ma = ax.plot([], [], color=cmap(n/N))[0]
                OMa = list(ax.plot([], [], color='dimgray')[0] for other in Universe.objects if other is not obj)
                OTe = list(ax.text([], [], "", va='center', ha='center') for other in Universe.objects if other is not obj)
                fields.append(Qu)
                trajectories.append(Tr)
                markers.append(Ma)
                obst_markers.append(OMa)
                obst_texts.append(OTe)
            
            def anim_update(i):
                # print("update")
                for obj, field, traj, mark, omark, otext in zip(Universe.objects, fields, trajectories, markers, obst_markers, obst_texts):
                    obj.update()
                    X,Y,U,V = obj.potfield()
                    field.set_UVC(U,V)
                    traj.set_data(obj.position[0:i+1,0], obj.position[0:i+1,1])
                    theta = np.linspace(0,2*np.pi,20)
                    mark.set_data(obj.position[i,0]+obj.radius*np.cos(theta),
                                  obj.position[i,1]+obj.radius*np.sin(theta))
                    for other_obj_marker, other_obj_text, other_obj in zip(omark, otext, list(other for other in Universe.objects if other is not obj)):
                        other_obj_marker.set_data(other_obj.position[i,0]+other_obj.radius*np.cos(theta),
                                                  other_obj.position[i,1]+other_obj.radius*np.sin(theta))
                        other_obj_text.set_text(other_obj.name)
                        other_obj_text.set_position((other_obj.position[i,0], other_obj.position[i,1]))
                    obj.move()
                    
            self.anim = animation.FuncAnimation(fig, anim_update,
                                                # frames=Universe.objects[0].position.shape[0],
                                                frames=int(T/dt),
                                                interval=3,
                                                repeat=False)
            plt.show()
            if save == True:
                # writergif = animation.PillowWriter(fps=2)
                # self.anim.save("sim_"+time.strftime("%Y_%m_%d-%H_%M_%S")+".gif", writer=writergif)
                writervideo = animation.FFMpegWriter(fps=25) 
                self.anim.save("sim_"+time.strftime("%Y_%m_%d-%H_%M_%S")+".mp4", writer=writervideo)
                

if __name__ == '__main__':
    
    # uncomment spaceships to add them
    ship1 = Spacecraft("S1", [-1.5,-1.5], [1,0], .2, 0.5)
    ship2 = Spacecraft("S2", [1.75,1.75], [0,0], .1, 1)
    ship3 = Spacecraft("S3", [-0.5,1.25], [0.5,-1.5], .15, 0.75)
    # ship4 = Spacecraft("S4", [-1.5,-0.1], [1.25,-0.5], .3, 0.3)
    # ship5 = Spacecraft("S5", [0,0.5], [1,1.5], .2, 0.5)
    # ship6 = Spacecraft("S6", [0,-1], [1,-1], .1, 0.5)
    # ship7 = Spacecraft("S7", [1,0.5], [-1,-1], .3, 0.5)
    
    universe = Universe()
    # list all objects in the system
    universe.list_objects("tabular")
    # animate system
    universe.animate(mode="individual", save=False)
    # to run this line download ffmpeg first and set the path to the .exe at the top
    # universe.animate(mode="individual", save=True)
    pass