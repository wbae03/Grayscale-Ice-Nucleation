#Droplet_Detection_GOALS

'''
Goals:

1) (done) Load video
2) capture the first frame (or whatever frame id) of video
3) detect circles within the frame
4) display the circle locations on the video, based on that one frame
5) track changes in RGB aka BGR values in those circles

Additional goals:
1) radius + circumference + arc auto measurer
2) Numerical ordering of circles based on x-axis positioning
3) Ability to 'deselect' / delete a detected circle via user input, based on the numerical ordering
4) HUD screen (FPS, Video Length, cool things :) )

Notes:
- Modularize!!
- Try not to nest functions... hard to read :( 

'''
# PACKAGES AND MODULES

import cv2 
import numpy as np

# LOAD VIDEO

# filename = str(input('Enter the name of the video: '))
filename = 'Assets/TX100_MineralOil_1to3_Test_v2.wmv'
cap = cv2.VideoCapture(filename)

while True: # makes sure the video loaded + frames are able to be captured

    # MANIPULATE LOADED VIDEO

    # frame_capture: captures a frame of the video based on frame_id

    # frame_circles: detects circles within the frame
    
    # frame_overlay_sort: numerically orders circles from left to right, top down, based on x and y axis position.
        # this fn should order the values of circles consistently within lists!!)

    # frame_overlay_label: numerically label the order of circles on video screen

    # frame_overlay_delete: deletes a circle and its associated data by deleting its index position within the data lists
        
    ### up to this point, freeze subsequent code. Once user has assessed the initial frame and deleted necessary circles, begin the video analysis
    
    # load video

    # frame_overlay: applies an overlay of circles based on the frame_id upon the video. This is more for user knowledge of what circles were detected and does not serve any other function.

    # BGR_change: keep track of BGR sum per frame for each circle, stored in an ordered list

    # BGR_max: find the maximum of the derivative/change in BGR for each circle === freezing event

    # auto_sizer: measures size, radius, cirumference, arc of circles based on a user input using calibration caliper