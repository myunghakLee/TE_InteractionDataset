# -*- coding: utf-8 -*-
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

length = 50 * 1000
stride = 25 * 1000
minimum_length = 7 * 1000


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
#"dataset/INTERACTION-Dataset-TC-v1_0/recorded_trackfiles/TC_BGR_Intersection_VA/"


paths.reverse()

for path in paths: # file root
    print(path)
    config = {
        'datapath': path,
        'index': ['id', 'x', 'y'],
        'savepath': path + "/TE/"
    }
    os.makedirs(config['savepath'], exist_ok=True)
    files = glob.glob(path + "vehicle*.csv")
    for f_i, f in enumerate(files): # select file
        scenario = f
        print(f)
        data = utill.preprocessing(scenario)
        data_arr = sorted([data['agent'][k] for k in data['agent'].keys()], key = lambda a : a['time'][0])


        scene_attendent = {}  # 각 scene별 참석자번호
        for i, d in enumerate(data_arr): # 모든 데이터에 대해 scene_attendent구하자
            time = length
            while(True):
                if (d['time'][0] < time < d['time'][-1] and time - d['time'][0] >= minimum_length) or \
                (time - length < d['time'][0] and d['time'][-1] < time and d['time'][-1] - d['time'][0] >= minimum_length) or \
                (d['time'][0] < time - length < d['time'][-1] and d['time'][-1] - (time - length)  >= minimum_length) or\
                (d['time'][0] < time - length and time < d['time'][-1]):
                    try:
                        scene_attendent[f"{time-length}_{time}"]["id"].append(i)
                    except:
                        scene_attendent[f"{time-length}_{time}"] = {}
                        scene_attendent[f"{time-length}_{time}"]["id"] = [i]
                elif d['time'][-1] < time-length:
                    break

                time += stride


        for implement in tqdm(range(10)):
            write_dict = {}
            write_dict["data"] = data_arr
            write_dict["scene_attendent"] = scene_attendent
            write_dict["TEmatrix"] = {}



            if (os.path.isfile(config["savepath"] + f.split('/')[-1].split('.')[0] + "_" + str(implement).zfill(3) +".json")):
                print("SKIP, File is exist")
                continue

            for scene in tqdm(scene_attendent.keys()):
                attendent_num = len(scene_attendent[scene]['id'])
                write_dict["TEmatrix"][scene] = [[0.0] * attendent_num for i in range(attendent_num)]
                too_short = 0
                for i in (range(attendent_num)):
                    for j in range(i+1, attendent_num):
                        source = data_arr[scene_attendent[scene]['id'][i]]
                        desc = data_arr[scene_attendent[scene]['id'][j]]
                        if source["time"][0] > desc["time"][-1] - minimum_length or desc["time"][0] > source["time"][-1] - minimum_length:
                            too_short += 1
                            continue

                        start, end = max(source["time"][0] , desc["time"][0]), min(source["time"][-1] , desc["time"][-1])
                        try:
                            write_dict["TEmatrix"][scene][i][j] , write_dict["TEmatrix"][scene][j][i] = TE.computeTE(source["xy"][source["time"].index(start) : source["time"].index(end)], desc["xy"][desc["time"].index(start) : desc["time"].index(end)])
                        except utill.java.lang.Exception:
                            write_dict["TEmatrix"][scene][i][j] , write_dict["TEmatrix"][scene][j][i] = 0.0,0.0
                            too_short += 1
#                         print(write_dict["TEmatrix"][scene][i][j] , write_dict["TEmatrix"][scene][j][i])
            print("save " + config["savepath"] + f.split('/')[-1].split('.')[0] + "_" + str(implement).zfill(3) +".json")
            with open(config["savepath"] + f.split('/')[-1].split('.')[0] + "_" + str(implement).zfill(3) +".json", "w") as j:
                json.dump(write_dict, j)
#         if f_i > 3:
#             break


# +

if (visualize):
    for k in ["100000_200000","150000_250000"]:
        minTE = min(np.array(write_dict["TEmatrix"][k]).flatten())
        maxTE = max(np.array(write_dict["TEmatrix"][k]).flatten())

        for i in range(40):
            df = [write_dict["TEmatrix"][k][i]]
            plt.figure(figsize=(8, 1))

            plt.pcolor(df, vmin=minTE, vmax=maxTE)

    #         plt.xlim(20,60)
    #         plt.ylim(20,60)

            plt.title(k + " / agent:" + str(i), fontsize=20)
            plt.xlabel('Agent', fontsize=14)
            plt.ylabel('Agent', fontsize=14)

            plt.colorbar()
            plt.show()
        break
# +

# with open(config["datapath"] + file_name.split('.')[0] + ".json", "r") as j:
#     data = json.load(j)
