# -*- coding: utf-8 -*-
"""
@author: Marwa Kechaou

Identify the helmets corresponding to the bounding box data based on the tracking data.
We assume we know each helmet's team.
Step 1: Calculate the distance matrix between the helmets using the tracking data and the bounding box data.
Second step: Identify the closest players of both teams on the basis of the distance matrices.
=> One player is identified per team
Third step: Iterative process: For a player on team A, find the player closest to him on the same team. 
At each stage, players already identified are removed from the team.

"""

import argparse
import os
import pandas as pd
import numpy as np

parser = argparse.ArgumentParser(description='Draw bounding boxes')
# Benchmark specific args
parser.add_argument('--data_path', default="./video_frames/train/57583_000082", type=str,help='path of extracted frames and dataframes')
parser.add_argument('--view', default="Sideline", type=str,help='precise the side if Endzone or Sideline')
parser.add_argument('--snap_ball_index', default=0, type=int,help='precise the index of snap ball event')

def points(x_coordinates,y_coordinates):
    points_list = []
    for i in range(len(x_coordinates)):
        points_list.append((x_coordinates[i],y_coordinates[i]))
    return np.array(points_list)

def dist_matrix(points):
    num_points = len(points)
    # Initialize a square distance matrix with zeros
    distance_matrix = np.zeros((num_points, num_points))   
    # Calculate distances and fill in the matrix
    for i in range(num_points):
        for j in range(num_points):
            x1, y1 = points[i]
            x2, y2 = points[j]
            distance = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            distance_matrix[i, j] = distance
    return distance_matrix
    
def team(c,players):
    team_c = []
    for p in players:
        if c in p:
            team_c.append(p)
    return team_c
        
def second_min_index(liste):
    index_min_value = liste.index(min(liste))
    liste[index_min_value] = max(liste) + 1
    return liste.index(min(liste))

def closest_players_couples(players,dist_matrix):
    couples_players = []
    couples_distances = []
    for i in range(len(players)):
        index_closest_player = second_min_index(list(dist_matrix[i,:]))
        if players[i][0] != players[index_closest_player][0]:
            if players[i][0]=='V':
                couple = (players[i],players[index_closest_player]) 
            else:
                couple = (players[index_closest_player],players[i])
            if not(couple in couples_players):
                couples_players.append(couple)
                couples_distances.append(dist_matrix[i,index_closest_player])
    return couples_players,couples_distances

def identify_first_players(couples_players_bb,couples_distances_bb,couples_players_tr,couples_distances_tr):
    Vbb,Hbb = couples_players_bb[couples_distances_bb.index(min(couples_distances_bb))]
    Vtr,Htr = couples_players_tr[couples_distances_tr.index(min(couples_distances_tr))]
    return Vbb,Vtr,Hbb,Htr

def identify_remained_players(prefix,team,players,players_bb_unknown,dist_matrix_tr,dist_matrix_bb,Ptr,Pbb):
    associated_players = ['']*len(team)
    associated_players[players_bb_unknown.index(Pbb)-prefix] = Ptr
    counter = 0
    index_players_tr = []
    index_players_bb = []
    while counter<=len(team)-2:
        Ptr_index = players.index(Ptr)
        index_players_tr.append(Ptr_index-prefix)
        distances_p_tr = list(dist_matrix_tr[Ptr_index,:][prefix:prefix+len(team)])
        for i in index_players_tr:
            distances_p_tr[i] = max(distances_p_tr)+1
        
        Pbb_index = players_bb_unknown.index(Pbb)
        index_players_bb.append(Pbb_index-prefix)
        distances_p_bb = list(dist_matrix_bb[Pbb_index,:][prefix:prefix+len(team)])
        for i in index_players_bb:
            distances_p_bb[i] = max(distances_p_bb)+1
            
        Ptr = players[distances_p_tr.index(min(distances_p_tr))+prefix]
        Pbb = players_bb_unknown[distances_p_bb.index(min (distances_p_bb))+prefix]
        associated_players[players_bb_unknown.index(Pbb)-prefix] = Ptr
        
        counter +=1
        
    return associated_players

def main():
    args = parser.parse_args()
    players = pd.read_csv(os.path.join(args.data_path,'players.csv'),index_col=0)
    players = list(players['player'])  
    teamV = team('V',players)
    teamH = team('H',players)
    players = teamV+teamH
    
    # Bounding Box data
    x_bb_coordinates = []
    y_bb_coordinates = []
    for p in players:
        bb_data = pd.read_csv(os.path.join(args.data_path,'bounding_boxes_dataframe_{}_{}.csv'.format(args.view,p)))
        x_bb_coordinates.append(bb_data['left'][args.snap_ball_index]+bb_data['width'][args.snap_ball_index]/2)
        y_bb_coordinates.append(bb_data['top'][args.snap_ball_index]+bb_data['height'][args.snap_ball_index]/2)  
    dist_matrix_bb = dist_matrix(points(x_bb_coordinates,y_bb_coordinates))  
    # Replace players by unknown IDs (imitate the real case)
    players_bb_unknown = ['V'+str(i) for i in range(11)] + ['H'+str(i) for i in range(11,22)]
    # Identify couples of players from different teams
    # For a player of team A, the closest player should be from team B
    couples_players_bb,couples_distances_bb = closest_players_couples(players_bb_unknown,dist_matrix_bb)
    
    # Tracking data
    x_tr_coordinates = []
    y_tr_coordinates = []
    for p in players:
        tr_data = pd.read_csv(os.path.join(args.data_path,'tracking_dataframe_video_{}.csv'.format(p)))
        x_tr_coordinates.append(tr_data['x'][args.snap_ball_index])
        y_tr_coordinates.append(tr_data['y'][args.snap_ball_index])      
    dist_matrix_tr = dist_matrix(points(x_tr_coordinates,y_tr_coordinates))
    # Identify couples of players from different teams
    # For a player of team A, the closest player should be from team B
    couples_players_tr,couples_distances_tr = closest_players_couples(players,dist_matrix_tr)
    
    Vbb,Vtr,Hbb,Htr = identify_first_players(couples_players_bb,couples_distances_bb,couples_players_tr,couples_distances_tr)
    
    print(Vbb,' : ',Vtr)
    print(Hbb,' : ',Htr)
    
    associated_players_V = identify_remained_players(0,teamV,players,players_bb_unknown,dist_matrix_tr,dist_matrix_bb,Vtr,Vbb)
    associated_players_H = identify_remained_players(len(teamH),teamH,players,players_bb_unknown,dist_matrix_tr,dist_matrix_bb,Htr,Hbb)
        
    print("teamV                : ",teamV)
    print("associated_players_V : ",associated_players_V)
    
    print("teamH                : ",teamH)
    print("associated_players_H : ",associated_players_H)
    
    return players,dist_matrix_tr,couples_players_tr,couples_distances_tr,dist_matrix_bb,couples_players_bb,couples_distances_bb
    
if __name__ =="__main__":
    players,dist_matrix_tr,couples_players_tr,couples_distances_tr,dist_matrix_bb,couples_players_bb,couples_distances_bb= main()