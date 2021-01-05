# -*- coding: utf-8 -*-
import os


# +
# # !pip install jpype1
# -

from sys import platform
import glob
import numpy as np
# from src.utils import *
import pickle
import matplotlib.pyplot as plt
import pandas as pd

import csv
from tqdm import tqdm

import random
import math
import utill

minimum_length = 3000
TE = utill.calc_TE()
visualize = True

paths = ["dataset/INTERACTION-Dataset-DR-v1_1/recorded_trackfiles/DR_CHN_Merging_ZS/",
"dataset/INTERACTION-Dataset-DR-v1_1/recorded_trackfiles/DR_CHN_Roundabout_LN/",
"dataset/INTERACTION-Dataset-DR-v1_1/recorded_trackfiles/DR_DEU_Merging_MT/",
"dataset/INTERACTION-Dataset-DR-v1_1/recorded_trackfiles/DR_DEU_Roundabout_OF/",
"dataset/INTERACTION-Dataset-DR-v1_1/recorded_trackfiles/DR_USA_Intersection_EP0/",
"dataset/INTERACTION-Dataset-DR-v1_1/recorded_trackfiles/DR_USA_Intersection_EP1/",
"dataset/INTERACTION-Dataset-DR-v1_1/recorded_trackfiles/DR_USA_Intersection_GL/",
"dataset/INTERACTION-Dataset-DR-v1_1/recorded_trackfiles/DR_USA_Intersection_MA/",
"dataset/INTERACTION-Dataset-DR-v1_1/recorded_trackfiles/DR_USA_Roundabout_EP/",
"dataset/INTERACTION-Dataset-DR-v1_1/recorded_trackfiles/DR_USA_Roundabout_FT/",
"dataset/INTERACTION-Dataset-DR-v1_1/recorded_trackfiles/DR_USA_Roundabout_SR/",
"dataset/INTERACTION-Dataset-TC-v1_0/recorded_trackfiles/TC_BGR_Intersection_VA/"]


for path in paths:
    # vehicle to vehicle
    config = {
        'datapath': path,
        'index': ['id', 'x', 'y'],
        'savepath': f'./te/DR_CHN_Merging_ZS/te/'
    }
    files = os.listdir(config["datapath"])
    
    for f in files:
        file_name = f
    
        scenario = config["datapath"] + file_name
        data = utill.preprocessing(scenario)
        data_arr = sorted([data['agent'][k] for k in data['agent'].keys()], key = lambda a : a['time'][0])
        
        for i in tqdm(range(10)):
            agent_num = len(data_arr)
            minimum_length = 3500
            TE_matrix = [[0] * agent_num for i in range(agent_num)]

            JAVA_EXCEPTION_NUM = 0
            ac_arr = []
            for i in tqdm(range(agent_num)):
                if data_arr[i]['time'][-1] - data_arr[i]['time'][0]  < minimum_length:
                    continue

                ac = 0
                source = data_arr[i]
                for j in range(i+1, agent_num):
                    desc = data_arr[j]
                    start, end = max(source["time"][0] , desc["time"][0]), min(source["time"][-1] , desc["time"][-1])
                    if source["time"][0] > desc["time"][-1] - minimum_length or desc["time"][0] > source["time"][-1] - minimum_length:

                        continue
                    if end - start > minimum_length and start < end:
                        try:
                            ac +=1
                            TE_matrix[source["id"]][desc["id"]] , TE_matrix[desc["id"]][source["id"]] = TE.computeTE(source["xy"][source["time"].index(start) : source["time"].index(end)], 
                                                                                                                     desc["xy"][desc["time"].index(start) : desc["time"].index(end)])

                        except utill.java.lang.Exception:
                            JAVA_EXCEPTION_NUM +=1
                            ac -= 1

            #             except:
            #                 print(source["xy"][source["time"].index(start) : source["time"].index(end)])
            #                 print(desc["xy"][desc["time"].index(start) : desc["time"].index(end)])
            #                 assert False, "DDD"            
                ac_arr.append(ac)




            agent_num = len(data_arr)
            minimum_length = 3500
            TE_matrix = [[0] * agent_num for i in range(agent_num)]

            JAVA_EXCEPTION_NUM = 0
            ac_arr = []
            for i in tqdm(range(agent_num)):
                if data_arr[i]['time'][-1] - data_arr[i]['time'][0]  < minimum_length:
                    continue

                ac = 0
                source = data_arr[i]
                for j in range(i+1, agent_num):
                    desc = data_arr[j]
                    start, end = max(source["time"][0] , desc["time"][0]), min(source["time"][-1] , desc["time"][-1])
                    if source["time"][0] > desc["time"][-1] - minimum_length or desc["time"][0] > source["time"][-1] - minimum_length:

                        continue
                    if end - start > minimum_length and start < end:
                        try:
                            ac +=1
                            TE_matrix[source["id"]][desc["id"]] , TE_matrix[desc["id"]][source["id"]] = TE.computeTE(source["xy"][source["time"].index(start) : source["time"].index(end)], 
                                                                                                                     desc["xy"][desc["time"].index(start) : desc["time"].index(end)])

                        except utill.java.lang.Exception:
                            JAVA_EXCEPTION_NUM +=1
                            ac -= 1

            #             except:
            #                 print(source["xy"][source["time"].index(start) : source["time"].index(end)])
            #                 print(desc["xy"][desc["time"].index(start) : desc["time"].index(end)])
            #                 assert False, "DDD"            
                ac_arr.append(ac)


# +
# visualize = True
# if (visualize):
#     df = TE_matrix
#     plt.figure(figsize=(8, 8))

#     plt.pcolor(df)


#     plt.xlim(520,550)
#     plt.ylim(520,550)


#     plt.title("TE", fontsize=20)
#     plt.xlabel('Agent(source)', fontsize=14)
#     plt.ylabel('Agent(desc)', fontsize=14)

#     plt.colorbar()
#     plt.show()

# -


