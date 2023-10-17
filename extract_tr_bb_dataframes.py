# -*- coding: utf-8 -*-
"""
@author: Marwa Kechaou

Extracting boudning box and tracking dataframes of each player related to a specific video game
"""

import os
import pandas as pd 
import argparse


parser = argparse.ArgumentParser(description='')
# Benchmark specific args
parser.add_argument('--videos_path', default="./video_frames/train", type=str,help='path of extracted dataframes')
parser.add_argument('--video_name', default='57583_000082_Sideline', type=str,help='Decide if optmizer is Adam or SGD')
parser.add_argument('--game_Key', default=57583, type=int,help='maximum number of frames extracted from the video game')
parser.add_argument('--playID', default=82, type=int,help='frame_name')
parser.add_argument('--dataframes_path', default="./nfl-health-and-safety-helmet-assignment", type=str,help='path of extracted dataframes')
parser.add_argument('--save_path', default="./video_frames/train/57583_000082_Endzone", type=str,help='path of extracted dataframes')

def main():
    args = parser.parse_args()

    """ Extract bounding box dataframes per player"""  
    df1 = pd.read_csv(os.path.join(args.dataframes_path,'train_labels.csv'),index_col=0)
    df_bb = df1[(df1['gameKey'] == args.game_Key) & (df1['playID'] == args.playID)]
    views = list(set(df_bb['view']))
    labels = list(set(df_bb['label']))
    for label in labels:
        for view in views:
            df_label = df_bb[(df_bb['label']==label) & (df_bb['view']==view)]
            df_label = df_label.sort_values(by='frame')
            df_label.to_csv(os.path.join(args.save_path,'bounding_boxes_dataframe_{}_{}.csv'.format(view,label)))
        
    """ Extract tracking dataframes per player"""
    df2 = pd.read_csv(os.path.join(args.dataframes_path,'train_player_tracking.csv'),index_col=0)
    df_tracking = df2[(df2.index == args.game_Key) & (df2['playID'] == args.playID)]
    players = list(set(df_tracking['player']))
    for player in players:
        df_player = df_tracking[df_tracking['player']==player]
        df_player.to_csv(os.path.join(args.save_path,'tracking_dataframe_{}.csv'.format(player)))
        
if __name__ =="__main__":
    main()