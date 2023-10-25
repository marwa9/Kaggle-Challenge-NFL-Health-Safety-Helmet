# -*- coding: utf-8 -*-
"""
@author: Marwa Kechaou 

Identify the team of each Helmet
"""

import argparse
import cv2
import os
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

parser = argparse.ArgumentParser(description='Draw bounding boxes')
# Benchmark specific args
parser.add_argument('--data_path', default="./video_frames/train/57584_000336", type=str,help='path of extracted frames and dataframes')
parser.add_argument('--frame', default='frame_0000.jpg', type=str,help='frame name file')
parser.add_argument('--view', default="Sideline", type=str,help='precise the side if Endzone or Sideline')


def clustering(feature_matrix,n_clusters,helmets):
    # Apply K-means clustering
    kmeans = KMeans(n_clusters=n_clusters)
    labels = kmeans.fit_predict(feature_matrix)
    # Assuming labels 0 and 1 represent the two teams
    team1_indices = np.where(labels == 0)[0]
    team2_indices = np.where(labels == 1)[0]
    # Extract helmets belonging to each team based on indices
    team1_helmets = [helmets[i] for i in team1_indices]
    team2_helmets = [helmets[i] for i in team2_indices]
    return team1_helmets,team2_helmets

def extract_features(roi):
    return roi.flatten()

def main():
    args = parser.parse_args()
    
    players = pd.read_csv(os.path.join(args.data_path,'players.csv'),index_col=0)
    players = list(players['player'])
    
    # Load extracted frame 
    frame = cv2.imread(os.path.join(args.data_path,'frames'+'_'+args.view,args.frame))
    target_size = (16,16)
    
    helmet_rois = []
    for p in players:
        bb_data = pd.read_csv(os.path.join(args.data_path,'bounding_boxes_dataframe_{}_{}.csv'.format(args.view,p)))
        # Define the coordinates of the bounding box
        x1, y1 = bb_data['left'][0],bb_data['top'][0]   # Top-left corner
        x2, y2 = x1+bb_data['width'][0],y1+bb_data['height'][0] # Bottom-right corner
        helmet_roi = frame[y1:y2, x1:x2]
        helmet_roi = cv2.resize(helmet_roi, target_size)
        helmet_rois.append(helmet_roi)

    # Extract features from helmet ROIs
    feature_matrix = np.array([extract_features(roi) for roi in helmet_rois])
    # Apply clustering
    team1_helmets,team2_helmets = clustering(feature_matrix,2,players)
        
    return team1_helmets,team2_helmets
    
if __name__ =="__main__":
    team1_helmets,team2_helmets = main()