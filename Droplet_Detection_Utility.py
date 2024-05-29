#Droplet_Detection_Utility

import cv2 
import numpy as np
import datetime
import os
import platform
import time

def make_appropriate_window_size(frame, cap):

        width = int(cap.get(3))
        height = int(cap.get(4))

        target_resolution_x = 960
        target_resolution_y = 540

        ratio_x = width / target_resolution_x
        ratio_y = height / target_resolution_y

        if ratio_x >= 1:
             ratio_x = 1 / ratio_x
        
        if ratio_y >= 1:
             ratio_y = 1 / ratio_y

        if width != 500:
             resized_frame = cv2.resize(frame, (0,0), fx = ratio_x, fy = ratio_y)
                                        
        return resized_frame
    

def show_window(window_name: str, frame, size_ratio, cap, filename):
    #resized_frame = cv2.resize(frame, (0,0), fx = size_ratio, fy = size_ratio)
    resized_frame = make_appropriate_window_size(frame, cap)
    resized_frame = vid_datetime(filename, resized_frame)
    resized_frame = get_frame_id(resized_frame, cap)

    cv2.imshow(window_name, resized_frame)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)
    cv2.moveWindow(window_name,10,50)


def vid_datetime(filename, frame):

    # important note: 
    # file creation refers to when the file was created at a certain location (ie copy pasting will set a new creation date)
    # file modification refers to when the file contents were last modified (ex: when the video was first created as it is)


    font = cv2.FONT_HERSHEY_COMPLEX
    #print('pass')
    # get date and time, then save it inside a variable

    ctime = 0
    if platform.system() == 'Windows':
        ctime = time.ctime(os.path.getmtime(filename))
    else:
        print('NO DATE OR TIME AVAILABLE. Sorry, I did not implement the code for inter-system conversion of date-time properties. It is possible, you just have to implement the code. I have attached a useful link that shows the code to do this where the code for this text exists. Goodluck :)')
        #https://stackoverflow.com/questions/237079/how-do-i-get-file-creation-and-modification-date-times
    
    # dt = str(datetime.datetime.now()) # this gives the current time and date.... not what i want

    # put date time on video frame
    frame = cv2.putText(frame, ctime,
                        (10, 20),
                        font, 0.5,
                        (0, 0, 0),
                        5)
    
    frame = cv2.putText(frame, ctime,
                        (10, 20),
                        font, 0.5,
                        (255, 255, 255),
                        1)
    
    return frame
    
def get_frame_id(frame, cap):

    font = cv2.FONT_HERSHEY_COMPLEX

    frame_id = 'Frame ID: ' + str(cap.get(cv2.CAP_PROP_POS_FRAMES)) # get the current frame ID

    frame = cv2.putText(frame, frame_id,
                        (10, 40),
                        font, 0.5,
                        (0, 0, 0),
                        5,)
    
    frame = cv2.putText(frame, frame_id,
                        (10, 40),
                        font, 0.5,
                        (255, 255, 255),
                        1)

    return frame