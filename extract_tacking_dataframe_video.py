# -*- coding: utf-8 -*-
"""
@author: Marwa Kechaou

Extract the rows of tracking dataframe corresponding to a given video
"""

import argparse
import os
import pandas as pd
import cv2
import sys
from datetime import datetime, timedelta

parser = argparse.ArgumentParser(description='Draw bounding boxes')
# Benchmark specific args
parser.add_argument('--data_path', default="./video_frames/train/57786_003085", type=str,help='path of extracted frames and dataframes')
parser.add_argument('--video_path', default="./nfl-health-and-safety-helmet-assignment/train/57786_003085_Sideline.mp4", 
                    type=str,help='path of the video corresponding to the tracking data')
parser.add_argument('--fps', default=59.94, type=float,help='path of extracted frames and dataframes')
parser.add_argument('--view', default="Sideline", type=str,help='precise the side if Endzone or Sideline')

def video_duration(video_path,fps):
    video_capture = cv2.VideoCapture(video_path)
    # Check if the video file was successfully opened
    if not video_capture.isOpened():
        print("Error: Could not open the video file.")
        sys.exit()
    # Get the total number of frames in the video
    total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    # Calculate the duration in seconds
    video_duration_seconds = total_frames / fps
    print(f"Video duration: {video_duration_seconds:.2f} seconds")
    # Release the video capture object
    video_capture.release()
    return video_duration_seconds

def end_time(original_time_str,duration):
    # Parse the original time string
    original_time = datetime.strptime(original_time_str, "%H:%M:%S.%f")
    # Add duration seconds
    new_time = original_time + timedelta(seconds=duration)
    # Format the result back into the desired time format
    result_time_str = new_time.strftime("%H:%M:%S.%f")[:-3]
    return result_time_str

def final_row(df,start_time,final_time,final_duration):
    start_time = datetime.strptime(start_time, "%H:%M:%S.%f")
    final_time = datetime.strptime(final_time, "%H:%M:%S.%f")
    row_achieved = 0
    for index, row in df.iterrows():
        current_time_str = row['time'].split('T')[1].split('Z')[0]
        current_time = datetime.strptime(current_time_str, "%H:%M:%S.%f")
        # Calculate the elapsed time
        elapsed_time = current_time - start_time
        # Check if the elapsed time exceeds the final duration
        if elapsed_time.total_seconds() >= final_duration:
            row_achieved = index
            break  # Exit the loop once the duration is achieved)
    return row_achieved

def add_x_y_columns(df):
    x =[]
    y = []
    for i in range(len(df)):
        x.append(df['left'][i]+df['width'][i]/2)
        y.append(df['top'][i]+df['height'][i]/2)
    df['x'] = x
    df['y'] = y
    return df
    
def main():
    args = parser.parse_args()
    players = pd.read_csv(os.path.join(args.data_path,'players.csv'),index_col=0)
    players = list(players['player'])
    for p in players:
        tr_data = pd.read_csv(os.path.join(args.data_path,'tracking_dataframe_{}.csv'.format(p)))
        # Identify rows in tracking dataframe corresponding to the video
        # The first row corresponds to "ball_snap" event
        ball_snap_df = tr_data[tr_data['event'] == 'ball_snap']
        index_ball_snap = (ball_snap_df.index)[0]
        # The last row depens on video duration
        time_ball_snap = ball_snap_df['time'].iloc[0].split('T')[1].split('Z')[0]
        duration = video_duration(args.video_path,args.fps)
        end_time_video = end_time(time_ball_snap,duration)
        index_end_video = final_row(tr_data[index_ball_snap:],time_ball_snap,end_time_video,duration)
        if index_end_video<index_ball_snap:
            index_end_video = len(tr_data)
        # Get the tracking dataframe corresponding to the video
        tr_data_video = tr_data[index_ball_snap:index_end_video+1]
        # Save the new tracking dataframe
        tr_data_video = tr_data_video.reset_index(drop=True)
        tr_data_video.to_csv(os.path.join(args.data_path,'tracking_dataframe_video_{}.csv'.format(p)))     
        
if __name__ =="__main__":
    main()