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
parser.add_argument('--data_path', default="./video_frames/train/57583_000082_Endzone", type=str,help='path of extracted frames and dataframes')
parser.add_argument('--frame', default='frame_0000.jpg', type=str,help='frame name file')
parser.add_argument('--players', default=['V5','V13','V15','V34','V68','V72','V73','V74','V79','V86','V87',
                                          'H22','H27','H30','H36','H50','H56','H59','H90','H96','H97','H99'], type=list,help='list of player IDs')

def main():
    args = parser.parse_args()
    # Load extracted frame 
    frame = cv2.imread(os.path.join(args.data_path,'frames',args.frame))
    # Draw a bounding box on the frame
    color = (0, 255, 0)  # Green color (BGR format)
    thickness = 2  # Thickness of the bounding box lines
        
    for p in args.players:
        bb_data = pd.read_csv(os.path.join(args.data_path,'bounding_boxes_dataframe_{}.csv'.format(p)))
        # Define the coordinates of the bounding box
        x1, y1 = bb_data['left'][0],bb_data['top'][0]   # Top-left corner
        x2, y2 = x1+bb_data['width'][0],y1+bb_data['height'][0] # Bottom-right corner
        # Use the cv2.rectangle function to draw the bounding box
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)
    
    # Display the frame with the bounding box
    cv2.imshow('Frame with Bounding Box', frame)
    
    # Wait for a key press and then close the window
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
if __name__ =="__main__":
    main()