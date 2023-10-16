This repo contains the code base for the technical exercice for the Skillcorner interview.

Main tasks are :

1. Visualize helmets detection and plot tracking data

2. Think / implement a solution to identify helmet detections based on tracking data

Two approaches: 

1. Create visual representations of the graphs for helmet positions using bounding box and tracking data at the same time.
   Map points on both graphs to identify Helmet IDs.

2. Identify the followed curve of each Helmet bounding box center.
   Check the closest curve to the Helmet box center among the tracking curves of players for identification.

