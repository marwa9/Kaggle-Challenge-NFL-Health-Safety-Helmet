# -*- coding: utf-8 -*-
"""
@author: Marwa Kechaou

Display the positions of players based on tracking and bouding box data
corresponding to either first event (snap ball) or end of the video
"""

import argparse
import matplotlib.pyplot as plt
import os
import pandas as pd

parser = argparse.ArgumentParser(description='Draw bounding boxes')
# Benchmark specific args
# parser.add_argument('--data_path', default="./video_frames/train/57786_003085", type=str,help='path of extracted frames and dataframes')
parser.add_argument('--data_path', default="./video_frames/train/57583_000082", type=str,help='path of extracted frames and dataframes')
parser.add_argument('--view', default="Sideline", type=str,help='precise the side if Endzone or Sideline')
parser.add_argument('--index_event_plot', default="first", type=str,
                    help='precise the synchronized event to display (snap ball: first) or last (end of video)')
      
def plot(x_coordinates,y_coordinates,players,description):
    plt.scatter(x_coordinates,y_coordinates, label= players,color='blue', marker='o')
    # Add player labels next to the points
    for i in range(len(x_coordinates)):
        plt.annotate(players[i], (x_coordinates[i], y_coordinates[i]), textcoords="offset points", xytext=(5,5), ha='center')
    plt.xlabel('X-Axis Label')
    plt.ylabel('Y-Axis Label')
    plt.title(description+' plot')
    plt.show() 
    
def main():
    args = parser.parse_args()
    players = pd.read_csv(os.path.join(args.data_path,'players.csv'),index_col=0)
    players = list(players['player'])
    x_bb_coordinates = []
    y_bb_coordinates = []
    x_tr_coordinates = []
    y_tr_coordinates = []
    
    if args.index_event_plot == 'first':
        l=0
        m=0
    
    for p in players:
        # Bounding Box data 
        bb_data = pd.read_csv(os.path.join(args.data_path,'bounding_boxes_dataframe_{}_{}.csv'.format(args.view,p)))
        if args.index_event_plot != 'first':
            l = len(bb_data)-1
        x_bb_coordinates.append(bb_data['left'][l]+bb_data['width'][l]/2)
        y_bb_coordinates.append(bb_data['top'][l]+bb_data['height'][l]/2)
        # Tracking data
        tr_data = pd.read_csv(os.path.join(args.data_path,'tracking_dataframe_video_{}.csv'.format(p)))
        if args.index_event_plot != 'first':
            m = len(tr_data)-1
        x_tr_coordinates.append(tr_data['x'][m])
        y_tr_coordinates.append(tr_data['y'][m])
    
    # Display plots
    plot(x_bb_coordinates,y_bb_coordinates,players,'Bouding box')      
    plot(x_tr_coordinates,y_tr_coordinates,players,'Tracking')
    
    
if __name__ =="__main__":
    main()