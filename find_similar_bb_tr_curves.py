# -*- coding: utf-8 -*-
"""
@author: Marwa Kechaou

This script is to explain the intuition behind the strategy I followed. 

We assume that we already identified the followed curve of each Helmet bounding box center.
We check if the curve of a certain Helmet is similar to the tracking curve of the same player.
If so, we can associate similar curves using distance metrics that conserve the geometrical properties of curves
This helps identify player ID of helmet.
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
import argparse
from distances import Hausdorff_distance, Wasserstein, Discrete_frechet, Fastdtw_distance


parser = argparse.ArgumentParser(description='Associate bounding box and tracking curves')
# Benchmark specific args
parser.add_argument('--data_path', default="./video_frames/train/57583_000082_Endzone", type=str,help='path of extracted dataframes')
parser.add_argument('--number_frames', default=472, type=int,help='maximum number of frames extracted from the video game')
parser.add_argument('--prefix', default="57583_000082_Endzone_", type=str,help='frame_name')
parser.add_argument('--label', default='H99', type=str,help='Decide if optmizer is Adam or SGD')
parser.add_argument('--players', default=['V5','V13','V15','V34','V68','V72','V73','V74','V79','V86','V87',
                                          'H22','H27','H30','H36','H50','H56','H59','H90','H96','H97','H99'], type=list,help='list of player IDs')


def center_coordinate(row):
    if len(row) != 0:
        return row['left'].iloc[0]+row['width'].iloc[0]/2,row['top'].iloc[0]+row['height'].iloc[0]/2
    else:
        return 0,0
    
def plot(x_coordinates,y_coordinates, label,data_type):
    plt.scatter(x_coordinates,y_coordinates, color='blue', marker='o')
    plt.xlabel('X-Axis Label')
    plt.ylabel('Y-Axis Label')
    plt.title(data_type+ 'plot of player '+label)
    plt.show()


def scaling(input_list):
    min_value = min(input_list)
    max_value = max(input_list)
    scaled_list = [2 * (x - min_value) / (max_value - min_value) - 1 for x in input_list]
    return scaled_list

def curve(x_coordinates,y_coordinates):
    curve = []
    for i in range(len(x_coordinates)):
        curve.append([x_coordinates[i],y_coordinates[i]])
    return np.array(curve)

def downsample_vector(vector, target_length):
    if len(vector) <= target_length:
        return vector
    # Calculate the step size for subsampling
    step = len(vector) // target_length
    # Subsample the vector
    downsampled_vector = vector[::step]
    return downsampled_vector

def oversample_vector(vector, target_length):
    if len(vector) >= target_length:
        return vector
    # Calculate the number of times to replicate the data
    num_replications = target_length // len(vector)
    # Calculate the remaining data needed to reach the target length
    remaining_length = target_length - (len(vector) * num_replications)
    # Replicate the data and add the remaining data if needed
    oversampled_vector = np.tile(vector, (num_replications, 1))
    # Add the remaining data, if any
    if remaining_length > 0:
        oversampled_vector = np.vstack((oversampled_vector, vector[:remaining_length]))
    return oversampled_vector


def predicted_player(distances_list,players):
    min_value = min(distances_list)
    min_index = distances_list.index(min_value)
    return players[min_index]

def main():
    args = parser.parse_args()
    
    hausdorff_distances = []
    frechet_distances = []
    wasserstein_distances = []
    fastdtw_distances = []
    
    # Load your tracking data 
    df_tr = pd.read_csv(os.path.join(args.data_path,'tracking_dataframe_'+args.label+'.csv'))  # Replace with your data
    # Scale values between -1 and 1
    x_coordinates_tr = scaling(list(df_tr['x']))
    y_coordinates_tr = scaling(list(df_tr['y']))
    plot(x_coordinates_tr,y_coordinates_tr,args.label,"tracking")
    curve_tr = curve(x_coordinates_tr,y_coordinates_tr)
    
    # Load your tracking data 
    for player in args.players:
        print(" check distance for player "+player)
        df_bb = pd.read_csv(os.path.join(args.data_path,'bounding_boxes_dataframe_'+player+'.csv'))
        x_coordinates_bb = []
        y_coordinates_bb = []
        for i in range(1,args.number_frames):
            x,y = center_coordinate(df_bb[df_bb["video_frame"]==args.prefix+str(i)])
            if x==0 and y==0:
                if len(x_coordinates_bb) == 0:
                    x_coordinates_bb.append(x)
                    y_coordinates_bb.append(y)
                else:
                    x_coordinates_bb.append(x_coordinates_bb[-1])
                    y_coordinates_bb.append(y_coordinates_bb[-1])
            else:
                x_coordinates_bb.append(x)
                y_coordinates_bb.append(y)
    
        # Scale values between -1 and 1
        x_coordinates_bb = scaling(x_coordinates_bb)
        y_coordinates_bb = scaling(y_coordinates_bb)
        
        # Adjust the number of points in bb curve to get same number of points in both curves
        if len(x_coordinates_bb)>len(x_coordinates_tr):
            x_coordinates_bb = downsample_vector(x_coordinates_bb, len(x_coordinates_tr))
            y_coordinates_bb = downsample_vector(y_coordinates_bb, len(y_coordinates_tr))
        else:
            x_coordinates_bb = oversample_vector(x_coordinates_bb, len(x_coordinates_bb))
            y_coordinates_bb = oversample_vector(y_coordinates_bb, len(y_coordinates_bb))
            
        plot(x_coordinates_bb,y_coordinates_bb,player," Bounding box center")
        curve_bb = curve(x_coordinates_bb,y_coordinates_bb)
        
        # Calculate the distance between curves representing sequential coordinates of bounding boxes and tracking data 
        hausdorff_distances.append(Hausdorff_distance(curve_tr,curve_bb))
        frechet_distances.append(Discrete_frechet(curve_tr, curve_bb))
        wasserstein_distances.append(Wasserstein(x_coordinates_tr, y_coordinates_tr,x_coordinates_bb, y_coordinates_bb))
        fastdtw_distances.append(Fastdtw_distance(curve_tr, curve_bb))
        
    # Display predicted players based on curves comparison
    print("The ID player: ",args.label)
    print("Predicted player using hausdorff distance: ",predicted_player(hausdorff_distances,args.players))
    print("Predicted player using frechet distance: ",predicted_player(frechet_distances,args.players))
    print("Predicted player using wasserstein distance: ",predicted_player(wasserstein_distances,args.players))
    print("Predicted player using fastdtw distance: ",predicted_player(fastdtw_distances,args.players))
    
if __name__ =="__main__":
    main()