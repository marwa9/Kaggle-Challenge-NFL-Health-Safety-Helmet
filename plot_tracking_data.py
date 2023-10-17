# -*- coding: utf-8 -*-
"""
@author: Marwa Kechaou

Plot the trajectory of tracking data
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
import argparse

parser = argparse.ArgumentParser(description='Plot tracking curves')
parser.add_argument('--data_path', default="./video_frames/train/57583_000082_Endzone", type=str,help='path of extracted dataframes')
parser.add_argument('--player', default='H50', type=str,help='the player to identify')

    
def plot(x_coordinates,y_coordinates,label):
    plt.scatter(x_coordinates,y_coordinates, color='blue', marker='o')
    plt.xlabel('X-Axis Label')
    plt.ylabel('Y-Axis Label')
    plt.title('Tracking plot of player '+label)
    plt.show()

def main():
    args = parser.parse_args()
    # Load tracking data 
    df_tr = pd.read_csv(os.path.join(args.data_path,'tracking_dataframe_'+args.player+'.csv'))  # Replace with your data
    x_coordinates_tr = list(df_tr['x'])
    y_coordinates_tr = list(df_tr['y'])
    plot(x_coordinates_tr,y_coordinates_tr,args.player)
    
if __name__ =="__main__":
    main()