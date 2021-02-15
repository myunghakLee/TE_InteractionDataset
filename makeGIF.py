# -*- coding: utf-8 -*-
import imageio
import numpy as np 
import matplotlib.pyplot as plt


class makeGIF:
    def __init__(self, title,axis, fontsize = 15, figsize = (5,5)):
        self.figure = []
        self.axis = axis
        self.figsize = figsize
        self.title = title
        self.fontsize = fontsize
        pass

    def figure_to_array(self,fig):
        fig.canvas.draw()
        return np.array(fig.canvas.renderer._renderer)
    
    def add_plot(self,map_xy, agent_xy, agent_time,social_xy, social_time,social_TE, time):
        f = plt.figure(figsize = self.figsize)
        plt.title(self.title,fontsize= self.fontsize)
        plt.axis(self.axis)
        for j, w in enumerate(map_xy[0][0]):
            xy = np.array(w['node'])
            plt.plot(xy[:,0]-950,xy[:,1]-950, color='gray',linewidth=1)

        plt.plot(agent_xy[:,0][:time+1],agent_xy[:,1][:time+1], color = "blue", zorder = 3)
        plt.scatter(agent_xy[:,0][time],agent_xy[:,1][time], color = "blue", zorder = 3)
        end = agent_time[time]  #몇 frame에서 끝나는지 정함
        
        for i, xy in enumerate(social_xy):
            if  social_time[i][0] < end and social_time[i][-1] > agent_time[0]:
                start = max(agent_time[0], social_time[i][0]) # 몇 frame에서 시작할지 정함
                start_idx = 0  # 애초에 dataset만들때 이렇게 정함
                end_idx = np.where(social_time[i] <= end)[0][-1]
                plt.plot(xy[:,0][:end_idx],xy[:,1][:end_idx], color = "black")
                plt.scatter(xy[:,0][end_idx],xy[:,1][end_idx], color = "black")
                plt.scatter(xy[:,0][end_idx],xy[:,1][end_idx], color = "orange", alpha = social_TE[i], linewidths = 3, zorder = 4)            
        plt.close()
        self.figure.append(self.figure_to_array(f))
    
    def make_gif(self,file_name, fps = 10):
        imageio.mimsave(f'{file_name}.gif', self.figure, fps=fps)#     print("=" * 100)
