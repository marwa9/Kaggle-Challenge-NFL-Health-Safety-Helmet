# -*- coding: utf-8 -*-
"""
@author: Marwa Kechaou

Extract frames from a given video
"""

import cv2
import os 
import argparse

parser = argparse.ArgumentParser(description='Extract frames')
# Benchmark specific args
parser.add_argument('--video_path', default='./nfl-health-and-safety-helmet-assignment/train/57583_000082_Endzone.mp4', 
                    type=str,help='path of the video')
parser.add_argument('--frames_save_path', default="./video_frames/train/57583_000082_Endzone", type=str,help='path to folder where to save extracted frames')


def main():
    args = parser.parse_args()
    
    cap = cv2.VideoCapture(args.video_path)
    
    # Check if the video file was opened successfully
    if not cap.isOpened():
        print("Error: Could not open video file.")
        exit()
    
    frame_number = 0
    while True:
        # Read a frame from the video
        ret, frame = cap.read()
        # Break the loop if we have reached the end of the video
        if not ret:
            break
        # Save the frame as an image
        frame_filename = f"frame_{frame_number:04d}.jpg"
        cv2.imwrite(os.path.join(args.frames_save_path,frame_filename), frame)
    
        # Increment frame number
        frame_number += 1
    
    # Release the video file and close the window if open
    cap.release()
    cv2.destroyAllWindows()

if __name__ =="__main__":
    main()

