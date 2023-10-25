# -*- coding: utf-8 -*-
"""
@author: Marwa Kechaou

Draw Helmet bounding boxes of a given frame
"""

import argparse
import cv2
import os
import pandas as pd

parser = argparse.ArgumentParser(description='Draw bounding boxes')
# Benchmark specific args
parser.add_argument('--data_path', default="./video_frames/train/57584_000336", type=str,help='path of extracted frames and dataframes')
parser.add_argument('--frame', default='frame_0000.jpg', type=str,help='frame name file')
parser.add_argument('--view', default="Sideline", type=str,help='precise the side if Endzone or Sideline')

def main():
    args = parser.parse_args()
    
    players = pd.read_csv(os.path.join(args.data_path,'players.csv'),index_col=0)
    players = list(players['player'])
    
    # Load extracted frame 
    frame = cv2.imread(os.path.join(args.data_path,'frames'+'_'+args.view,args.frame))
    # Draw a bounding box on the frame
    color = (0, 255, 0)  # Green color (BGR format)
    thickness = 2  # Thickness of the bounding box lines
        
    for p in players:
        bb_data = pd.read_csv(os.path.join(args.data_path,'bounding_boxes_dataframe_{}_{}.csv'.format(args.view,p)))
        # Define the coordinates of the bounding box
        x1, y1 = bb_data['left'][0],bb_data['top'][0]   # Top-left corner
        x2, y2 = x1+bb_data['width'][0],y1+bb_data['height'][0] # Bottom-right corner
        # Use the cv2.rectangle function to draw the bounding box
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)
    
    # Display the frame with the bounding box
    cv2.imshow('Frame with Bounding Box', frame)
    cv2.imwrite('bb_image_sideline.jpg', frame)
    
    # Wait for a key press and then close the window
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
if __name__ =="__main__":
    main()