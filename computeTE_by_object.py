import os
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
import json
import copy

# +
visualize = False
minimum_length = 5000
TE = utill.calc_TE('6')

repeat = 10
length = 50 * 1000
stride = 25 * 1000
minimum_length = 7 * 1000
minimum_time_thresh_hold =  50*100
# -

paths = ["dataset/INTERACTION-Dataset-DR-v1_1/recorded_trackfiles/DR_USA_Intersection_EP0/",
"dataset/INTERACTION-Dataset-DR-v1_1/recorded_trackfiles/DR_USA_Intersection_EP1/",
"dataset/INTERACTION-Dataset-DR-v1_1/recorded_trackfiles/DR_CHN_Merging_ZS/",
"dataset/INTERACTION-Dataset-DR-v1_1/recorded_trackfiles/DR_CHN_Roundabout_LN/",
"dataset/INTERACTION-Dataset-DR-v1_1/recorded_trackfiles/DR_DEU_Merging_MT/",
"dataset/INTERACTION-Dataset-DR-v1_1/recorded_trackfiles/DR_DEU_Roundabout_OF/",
"dataset/INTERACTION-Dataset-DR-v1_1/recorded_trackfiles/DR_USA_Intersection_GL/",
"dataset/INTERACTION-Dataset-DR-v1_1/recorded_trackfiles/DR_USA_Intersection_MA/",
"dataset/INTERACTION-Dataset-DR-v1_1/recorded_trackfiles/DR_USA_Roundabout_EP/",
"dataset/INTERACTION-Dataset-DR-v1_1/recorded_trackfiles/DR_USA_Roundabout_FT/",
"dataset/INTERACTION-Dataset-DR-v1_1/recorded_trackfiles/DR_USA_Roundabout_SR/"]
# "dataset/INTERACTION-Dataset-TC-v1_0/recorded_trackfiles/TC_BGR_Intersection_VA/"]
paths.reverse()

# +
for path in paths: # file root
    print(path)
    config = {
        'datapath': path,
        'index': ['id', 'x', 'y'],
        'savepath': path + "/TE_by_object/"
    }
    os.makedirs(config['savepath'], exist_ok=True)
    files = sorted(glob.glob(path + "vehicle*.csv"), key = lambda f : int(f.split('/')[-1].split('.')[0].split('_')[-1]))
    for f in tqdm(files): # select file
        print(f)
        scenario = f
        scenario_name = scenario.split("/")[-1].split(".")[0]
        data = utill.preprocessing(scenario)
        data_arr = sorted([data["agent"][k] for k in data["agent"].keys()], key = lambda a : a["time"][0])
        
        agent_list = list(data["agent"].keys())
        for i in tqdm(range(len(data_arr[:-1]))):  # select actor
            agent = data_arr[i]
            save_file_name = config["savepath"] + scenario_name + "_" + str(agent["id"]) + ".json"
            if os.path.isfile(save_file_name):
                continue
            
            write_dict = {}
            write_dict["normalize_xy"] = data["normalize_xy"]
            write_dict["agent"] = {}
            write_dict["social"] = []
            
            write_dict["agent"] = {}
            write_dict["agent"]["xy"] =agent["xy"]
            write_dict["agent"]["id"] = agent["id"]
            write_dict["agent"]["type"] = agent["type"]
            write_dict["agent"]["time"] = agent["time"]
            write_dict["TE"] = [0.0]
            others_idx = i+1
            others = data_arr[others_idx]
            while(agent["time"][-1] - others["time"][0] > minimum_time_thresh_hold and others_idx < len(data_arr)):
                
                others = data_arr[others_idx]
                start = others["time"][0]
                end = min(others["time"][-1], agent["time"][-1])

                
                if end - start >= minimum_time_thresh_hold:
                    info = {}
                    info["xy"] = others["xy"][:others["time"].index(end) + 1]
                    info["id"] = others["id"]
                    info["type"] = others["type"]
                    info["time"] = others["time"]

                    trans_entropy = sum([max(TE.computeTE_a2b(info["xy"],
                                        agent["xy"][agent["time"].index(start): agent["time"].index(end) + 1]), 
                                             0.0) for i in range(repeat)]
                                       ) / repeat

#                     trans_entropy = max(TE.computeTE_a2b(info["xy"], agent["xy"][agent["time"].index(start): agent["time"].index(end) + 1]), 0.0)

                    write_dict["TE"].append(trans_entropy)
                    write_dict["social"].append(info)
                others_idx +=1

            if len(write_dict["TE"]) > 2:
                with open(config["savepath"] + scenario_name + "_" + str(agent["id"]) + ".json", "w") as json_data:
                    json.dump(write_dict, json_data)


# -


