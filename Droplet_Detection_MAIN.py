#Droplet_Detection_MAIN

'''
Goals:

1) (done) Load video
2) (done) capture the first frame (or whatever frame id) of video
3) (done) detect circles within the frame
4) (done) display the circle locations on the video, based on that one frame
5) (done) track changes in RGB aka BGR values in those circles. 
        used grayscale instead
6) export max/min of derivative
7) link temperature data to intensity max/min data

Additional goals:
1) radius + circumference + arc auto measurer
2) (done) Numerical ordering of circles based on x-axis positioning
3) (done) Ability to 'deselect' / delete a detected circle via user input, based on the numerical ordering
4) HUD/GUI screen (FPS, Video Length, cool things :) )

Notes:
- Modularize!!
- Try not to nest functions... hard to read :( 


# TODO list
# Make histogram / whisker plot of diff circle sizes
# make heat map 
# export data by organizing by circle size

'''
# PACKAGES AND MODULES

import cv2 
import numpy as np
import time
import os
import pandas as pd
import itertools # for animated loading
import threading # for animated loading
import sys # for animated loading
import matplotlib.pyplot as plt
import numpy as np
import math
import tkinter as tk
from tkinter.filedialog import askopenfilename
import ntpath
from colorama import init

import Droplet_Detection_Utility as DDU
import Droplet_Detection_Frame as DDF
import Droplet_Detection_Selection_Frame as DDS
import Droplet_Detection_Grapher as DDG

init() # related to colorama, to enable ANSI escape codes for color

# Create a single instance of Tk
root = tk.Tk()
# Set the window attributes
root.wm_attributes('-topmost', 1)
# Withdraw the window
root.withdraw()


RED = "\33[91m"
BLUE = "\33[94m"
GREEN = "\033[32m"
YELLOW = "\033[93m"
PURPLE = '\033[0;35m' 
CYAN = "\033[36m"
LBLUE = "\033[94m"
END = "\033[0m"
BOLD = "\033[1m"

#os.system('cls') # clear console

def banner():
    font = fr'''
    {CYAN}
   ___                               _         _____               __            _            _   _             
  / _ \_ __ __ _ _   _ ___  ___ __ _| | ___    \_   \___ ___    /\ \ \_   _  ___| | ___  __ _| |_(_) ___  _ __  
 / /_\/ '__/ _` | | | / __|/ __/ _` | |/ _ \    / /\/ __/ _ \  /  \/ / | | |/ __| |/ _ \/ _` | __| |/ _ \| '_ \ 
/ /_\\| | | (_| | |_| \__ \ (_| (_| | |  __/ /\/ /_| (_|  __/ / /\  /| |_| | (__| |  __/ (_| | |_| | (_) | | | |
\____/|_|  \__,_|\__, |___/\___\__,_|_|\___| \____/ \___\___| \_\ \/  \__,_|\___|_|\___|\__,_|\__|_|\___/|_| |_|
                 |___/                                                                  {BOLD}Version 1.6.0{END}                                              
{END}
    {GREEN}> {END}William Bae | NBD Group @ UBC Chemistry     {GREEN}> {END}www.github.com/wbae03     {GREEN}> {END}LinkedIn: wbae03

              {GREEN}> {END}Known OS Compatibilities: Win10 | Win11          {GREEN}> {END}Created 24/06/14

    '''
    print(font)

banner()

# CUSTOMIZABLE PARAMETERS

size_ratio = 0.25 # Proportionally changes the size of image and video files used in the program.

#file_directory = 'Assets/'

# Asks user if calibration image is required

calib_file = '' #  Variable to store user input of calibration image

use_calib_image = False # Condition that triggers calibration image file input

ask_user_calib_ready = False # A switch to terminate the loop below.

# CALIBRATING CIRCLE SIZES (if calibration with image is required)

# Global variables

drawing = False  # True when mouse is pressed on the image window

sbox = []

line_coords = []

calib_real_length = 0

calib_pixel_length = 0

calib_user_ready = False

calibration_ratio = 0

close_calib_window = False

finished_drawing = False

while not ask_user_calib_ready: # While loop ensures the user prompts are repeated if the user input is invalid (ie not 'y' or 'n')

    ask_user_calib = input(f'\n{RED}[PROGRAM] >{END} Do you require calibration using an image with a known measurement (ie. using a ruler)? \nAlternatively, enter a calibration ratio {YELLOW}(pixel length / micrometer length){END} obtained from previous calibrations.\n\nPress {YELLOW}\'Y\'{END} to load an image.\nPress {YELLOW}\'N\'{END} to enter a known calibration ratio value.\n\n{GREEN}[USER INPUT] > {END}')

    if ask_user_calib.lower() == 'y':

        use_calib_image = True

        ask_user_calib_ready = True

        calib_file = askopenfilename()

        #calib_file = str(input('\n📏 Enter the name of the calibration image file:\n\n[USER INPUT] > '))

        #calib_file = file_directory + calib_file

        print(f"\n{RED}[SYSTEM] >{END} Does the calibration file exist: ", os.path.exists(calib_file))

    elif ask_user_calib.lower() == 'n':

        use_calib_image = False

        ask_user_calib_ready = True

    else:

        print(f'\n{RED}[PROGRAM] >{END} Invalid input. Please press {YELLOW}\'Y\'{END} or {YELLOW}\'N\'{END}.\n (Tip: if you do not require a calibration, you can just put in an arbitrary calibration value after press \'N\'){END}')

if use_calib_image == True:

    image = cv2.imread(calib_file) # Program loads the image inputted

    temp_image = image.copy()

    def on_mouse(event, x, y, flags, param): # although flags and param are not used in this function, they must be included in the parameters as the data from mouse clicks feeds into this function and includes these parameters.

        global finished_drawing, drawing, sbox, line_coords, temp_image, calib_pixel_length, calib_real_length, calib_user_ready, calibration_ratio, close_calib_window

        x = math.floor(x * 1/size_ratio) # note: resizing the window size DOES NOT scale down the frames system / mouse coordinate system.. must convert the mouse values by applying an opposite scale (ie if the frame is scaled down by 0.5 of original size, then scale mouse coordinates by 1/0.5 aka x2 !!)
        
        y = math.floor(y * 1/size_ratio)
        

        if event == cv2.EVENT_LBUTTONDOWN and finished_drawing == False:

            print(f'\n{RED}[PROGRAM] > {END}Start Mouse Position: {YELLOW}[' + str(x) + ',' + str(y) + f']{END}')

            sbox = [x, y]

            line_coords.append(sbox)

            drawing = True

        elif event == cv2.EVENT_MOUSEMOVE and finished_drawing == False:
            if drawing:
                temp_image = image.copy()  # Reset to the original image
                cv2.line(temp_image, tuple(sbox), (x, y), (0, 0, 255), 4)
                #print('drawing! initial xy:', sbox, 'final xy:', x, y)

        elif event == cv2.EVENT_LBUTTONUP and finished_drawing == False:
            
            finished_drawing = True
            
            print(f'\n{RED}[PROGRAM] > {END}End Mouse Position: {YELLOW}[' + str(x) + ',' + str(y) + f']{END}')
            ebox = [x, y]
            line_coords.append(ebox)
            drawing = False
            # Draw the final line on the main image
            cv2.line(image, tuple(sbox), tuple(ebox), (0, 0, 255), 5)

            # use pythagorean theorem to find length of line
            x_length = abs(sbox[0] - ebox[0])
            y_length = abs(sbox[1] - ebox[1])
            calib_pixel_length = round(math.sqrt(x_length**2 + y_length*2), 2)
            print(f'\n{RED}[PROGRAM] > {END}Calibration pixel length: {YELLOW}[', calib_pixel_length, f']{END}')


            while calib_user_ready == False:
                
                calib_real_length = input(f'\n{RED}[PROGRAM] > {END}Please enter the actual length {YELLOW}[MICROMETERS]{END} of the calibration tool.\n\n{GREEN}[USER INPUT] > {END}')

                if calib_real_length.isnumeric():

                    calib_user_ready = True
                    calibration_ratio = round(float(calib_pixel_length) / float(calib_real_length), 2) # magnification = image length / actual length
                    print(f'\n{RED}[PROGRAM] > {END}Calibration successful. The calibration ratio is: {YELLOW}[', calibration_ratio, f']{END}. \nPlease write down this value if you will be analyzing more video data in the future, so you can enter the calibration ratio.')
                    cv2.destroyWindow('Calibration Window')

                else:
                    print(f'\n{RED}[PROGRAM] > {END}Invalid input. Please enter the actual length {YELLOW}[MICROMETERS]{END} of the calibration tool')
           


    # Create a window and set the mouse callback
    cv2.namedWindow('Calibration Window')
    if finished_drawing == False:
        cv2.setMouseCallback('Calibration Window', on_mouse)

    # Keep the window open until a key is pressed
    
    print(f'\n{RED}[PROGRAM] > {END}In the calibration window, please draw a line parallel to the calibration tool / ruler by holding the left mouse button.\n\n{GREEN}[USER INPUT] > {END}')

    while close_calib_window == False:

        try:
            resized_temp_image = cv2.resize(temp_image, (0,0), fx = size_ratio, fy = size_ratio)
            cv2.setWindowProperty('Calibration Window', cv2.WND_PROP_TOPMOST, 1)
            cv2.moveWindow('Calibration Window',10,50)
            cv2.imshow('Calibration Window', resized_temp_image)
            cv2.startWindowThread()
        except:
            dummy = 1

        if calibration_ratio != 0:
            close_calib_window = True

        if cv2.waitKey(1) & 0xFF == 27:  # Exit on pressing 'ESC'
            break

    


elif use_calib_image == False:

    while calib_user_ready == False:
        calibration_ratio = input(f'\n{RED}[PROGRAM] > {END}Please enter a {YELLOW}calibration ratio{END} value. \nThis value may be obtained from previous calibrations or analysis of videos with the same dimensions.\n\n{GREEN}[USER INPUT] > {END}')

        try:
            if isinstance(float(calibration_ratio), float): # checks if the instance is a number

                calib_user_ready = True
                print(f'\n{RED}[PROGRAM] > {END}Calibration successful. The calibration ratio value is: {YELLOW}[', calibration_ratio, f']{END}.\n Please write down this value if you will be analyzing more video data in the future, so you can enter the calibration ratio.')

        except:
            print(f'\n{RED}[PROGRAM] > {END}Invalid input. Please enter the calibration ratio. If unknown, please restart the program and use a calibration image.')
    


#calib_length = calc_distance(line_coords)
#print('calib length: ', calib_length)

# LOAD VIDEO

print(f'\n{RED}[PROGRAM] > {END} Please provide the file directory of the {YELLOW}video data{END} (Accepted formats: .avi, .mp4, .mkv)')
#time.sleep(1)
filename = askopenfilename()

cap = cv2.VideoCapture(filename)
cap1 = cv2.VideoCapture(filename)
cap2 = cv2.VideoCapture(filename)

total_frame_count = cap2.get(cv2.CAP_PROP_FRAME_COUNT)
fps = cap2.get(cv2.CAP_PROP_FPS)
duration = total_frame_count/fps
minutes = int(duration/60)
seconds = duration%60




frame_count = 1

######################
####### SCRIPT #######
######################

stop_reiterating = False
x = 0
print(f"\n{RED}[SYSTEM] > {END}Does the file exist: ", os.path.exists(filename))

codec_code = cap2.get(cv2.CAP_PROP_FOURCC)
#print('\nCodec code of video: ', hex(int(codec_code)))
sens_selection = []
user_circle_detection_ready = False
#print('no')

while True: # makes sure the video loaded + frames are able to be captured

    # MANIPULATE LOADED VIDEO

    ret, frame = cap.read()


    #print(frame)

    #frame = cv2.resize(frame, (640, 500)) #for teresa's videos

    

    if not ret: break


    if stop_reiterating == False:
        if ret:
            print(f'\n{RED}[SYSTEM] > {END}\n') 
            print(f'Selected file: {YELLOW}', filename, f'{END}')
            print(f'\n{CYAN}    Video Property                       Value{END}')
            print(f'Total frame count of video ----------- {YELLOW}[', total_frame_count, f']{END}')
            print(f'The detected video FPS --------------- {YELLOW}[', fps, f']{END}')
            print(f'Duration of the video: --------------- {YELLOW}[', round(duration, 2), f' sec ]{END}, or {YELLOW}[', str(minutes), f' min', str(round(seconds, 2)), f' sec ]{END}')
            frame_count_input = input(f'\nPlease enter an {YELLOW}integer for the interval of frames to be analyzed{END}. If no input is given, the FPS of the video will be used instead.\n({YELLOW}TIP:{END} to anayze every n seconds of the video, enter the product of FPS * n.) \n\n{GREEN}[USER INPUT] > {END}')

            if frame_count_input.isnumeric():
                frame_count = float(frame_count_input)
                print(f'\n{RED}[PROGRAM] > {END}The analysis will occur every {YELLOW}[', frame_count,f'] frames{END}.')

            else:
                frame_count =  fps # if no int is given, resort to default fps setting of the video as the frame interval
                print(f'\n{RED}[PROGRAM] > {END}No frame count was given. The analysis will resort to analyzing every {YELLOW}[', frame_count,f'] frames{END}.')


            #width = int(cap.get(3))
            #height = int(cap.get(4))




            
            # frame_capture: captures a frame of the video based on frame_id
            
            frame_id = 0
            DDF.frame_capture(frame_id, cap)

            # frame_circles: detects circles within the frame
            


            while user_circle_detection_ready == False:
                n = 'WINDOW 1 /// DETECTED CIRCLES'
                
                frame_copy = frame.copy()

                #circles = [] # resets with each loop
                circles, user_circle_detection_ready_input = DDF.frame_circles(frame_copy, n)

                if circles is not None:
                    # frame_overlay_sort: numerically orders circles from left to right, top to bottom, based on x and y axis position.
                        # done by assessing the calculated area between width and height. Smaller = closer to 0,0... kind of
                        # this fn should order the values of circles consistently within lists!!)

                    areas_sorted = DDF.frame_overlay_sort(circles)


                    # frame_overlay_label: numerically label the order of circles on frame screen

                    DDF.frame_overlay_label(areas_sorted, frame_copy, calibration_ratio)

                    
                    cv2.namedWindow(n)
                    cv2.setWindowProperty(n, cv2.WND_PROP_TOPMOST, 1)
                    cv2.moveWindow(n,10,50)
                    DDU.show_window(n, frame_copy, size_ratio, cap, filename)

                    #user_circle_detection_ready_input = input(f'\n{RED}[PROGRAM] > {END}To switch the circle detection sensitivity, please re-select an option. \nOtherwise, please press {YELLOW}[ENTER]{END} to proceed with the analysis. \n\n{GREEN}[USER INPUT] > {END}')
            
                    if user_circle_detection_ready_input == True:

                        user_circle_detection_ready = True
                    
                    '''
                    elif user_circle_detection_ready_input == False:
                        print('tat')
                        if int(user_circle_detection_ready_input) in range(6):
                            print('bab')
                            cv2.destroyWindow(n)
                    '''
                
                else:
                    
                    print(f'\n{RED}[PROGRAM] > {END}Unable to detect circles with the given circle detection option. Please {YELLOW}reselect.{END}')


        else:
            print(f'{RED}[PROGRAM] > {END}Video Load Error! File may be corrupted, does not meet the compatible file extensions.')
        

    if stop_reiterating == True: # breaks loop after 1 cycle
        break
        #i = input('\n---------\nOn the screen are the circles detected in the first frame of the video. \nIf you are unsatisfied with the detection, try changing the detection parameters in the code. \nPress [R or ENTER] to continue to the next step of analysis.')
        #if i in 'Rr':
        #    break
    else:
        stop_reiterating = True # will set stop_reinterating to true after the first loop

    if cv2.waitKey(1) == ord('r'): #27: # Escape key ASCII is 27. If R is pressed on video instead of console.
        break

stop_reiterating = False # reset this to prepare for use in the next loop
deselection_input_list = [] # this list is initially empty. When the loop below occurs, deselected circles are appended.


while True:

    ret, selection_frame = cap1.read()
    #selection_frame = cv2.resize(frame, (640, 500)) for teresa's videos

    if not ret: break

    # frame_overlay_select: selects a circle(s) and its associated data via its index position within the data lists.
        # could try deleting circles and reshowing screen?
    
    if stop_reiterating == False:
        deselection_input_list, user_ready = DDS.frame_overlay_select(deselection_input_list)

        # make_selection_list: makes a list containing the circles that will be analyzed. This fn removes the data for deselected circles.

        selection_list = DDS.make_selection_list(areas_sorted, deselection_input_list, selection_frame)
        #print('selection list:', selection_list)
        # selected_circles_on_frame: places only the selected circles and corresponding numerical identity on a new still frame.


        selection_frame, calib_r_list = DDS.selected_circles_on_frame_and_label(selection_list, selection_frame, calibration_ratio)


        m = 'WINDOW 2 /// SELECTED CIRCLES FOR ANALYSIS'
        cv2.namedWindow(m)
        cv2.setWindowProperty(m, cv2.WND_PROP_TOPMOST, 1)
        cv2.moveWindow(m,10,50)
        DDU.show_window(m, selection_frame, size_ratio, cap1, filename)
        
        

    if stop_reiterating == True:
        #i = input(f'\n{RED}[PROGRAM] > {END}The deselected circles have been removed. \n\n{RED}[PROGRAM] > {END}Press {YELLOW}[ENTER]{END} to begin analysis of the change in intensity within each circle.\n')
        #if i in 'Rr':
        #    break
        break # breaks loop and begins analysis

    elif user_ready == True:

        stop_reiterating = True 

    if cv2.waitKey(1) == ord('r'): #27: # Escape key ASCII is 27. If R is pressed on video instead of console.
        break

cv2.destroyWindow(n)
cv2.destroyWindow(m)
print('\n') # give space before loading loop... cant add space to loading loop or else it will bug out.

while True:
    stop_reiterating = False
    #print('\n---------\nTo cancel the analysis, please close the program as it will not terminate properly within the client.\n') #press \'Esc\' on the video window, or input Ctrl + C in console.\n')
    #cv2.destroyAllWindows
    video_BGR_data = []
    previous = time.time() # temporal resolution of processing
    delta = 0 # temporal resolution of processing
    start_time = time.time() # timer for entire processing time
    


    #==========================
    # animated loading screen !!
    done = False
    #here is the animation
    def animate():

        for c in itertools.cycle([' ·      ', 
                                  ' ⊹  .   ',
                                  ' ❅  ..  ', 
                                  ' ❆  ... ']): 
            if done:
                break
            sys.stdout.write(f'\r{RED}[PROGRAM] > {END}Loading... ' + str(round(cap2.get(cv2.CAP_PROP_POS_FRAMES)/total_frame_count*100, 2)) + f'%{CYAN}' + c + f'{END}') #+ str(round(cap2.get(cv2.CAP_PROP_POS_FRAMES)/total_frame_count*100, 2)) + '%' + c)
            sys.stdout.flush()
            time.sleep(0.5)
        #sys.stdout.write('\rDone!     ')

    t = threading.Thread(target=animate)
    t.start()
    
    break
    #===========================


frame_count_change = 0
video_milliseconds = []
frame_axes = []

while True: # this analyzes the video. IMPORTANT: MINIMIZE FUNCTIONS IN THIS LOOP TO SPEED UP ANALYSIS.

    ret, video = cap2.read()
    if not ret: 
        done = True
        break



    frame_intensity_sum_hold = [] # reset this var every loop. Holds on to values, so that I can store values together as a list into another variable.

    video = cv2.cvtColor(video, cv2.COLOR_BGR2GRAY) # grayscale to remove color noise


    if selection_list is not None:
        #selection_list = np.uint16(np.around(selection_list))

        #print('selection list np:', selection_list)
        for i in range(len(selection_list)):


            #print('sel list length', len(selection_list))
            #print('sel list', selection_list)
            #x, y, r = i[0], i[1], i[2]
            #cv2.circle(video, (i[0], i[1]), i[2], (0,255,0), 2) # circumference
            #cv2.circle(video, (i[0], i[1]), 1, (0,0,255), 2) #center point of circle

            # applying masking to measure BGR
            #x, y, r = selection_list.astype(np.int32)[0][0][0], selection_list.astype(np.int32)[0][0][1], selection_list.astype(np.int32)[0][0][2]
            #print('selecction list', selection_list)
            # line doesnt work: x, y, r = selection_list.astype(np.int32)[i][0], selection_list.astype(np.int32)[i][1], selection_list.astype(np.int32)[i][2]
            x, y, r = selection_list[i][0], selection_list[i][1], selection_list[i][2]

            #.astype(np.int32)[i] #0 is indexing the first circle entry
            #print(circles[0].astype(np.int32)) #np.int32 calls for the 1st bracket within [[[x, y, r], [x2,y2,r2]]]
            #https://www.youtube.com/watch?v=1p1lUyLGB2E&ab_channel=CodesofInterest
            #https://stackoverflow.com/questions/62944745/how-to-find-the-average-rgb-value-of-a-circle-in-an-image-with-python

            #print(x,y,r)
            #print('video', video)

            #print('sub', y-r)
            #print('vidtest', video[10:11, 10:11], 'length', len(video[10:11, 10:11]))

            #roi = video[9+1:11, 10:11] # height, width
 
            #print('y-r', y-r, 'y+r', y+r, 'x-r', x-r, 'x+r', x+r)
            #roi = video[y-r: y+r, x-r: x+r] # height, width
            #print('roi', roi)

            # Circular Region of interest (ROI) in original image
            roi = np.zeros(video.shape[:2], np.uint8)
            roi = cv2.circle(roi, (x, y), r, 255, cv2.FILLED)
            #cv2.imshow('roi', roi)

            #print('roi: ', roi, 'roi length:, ', len(roi))

            # Target image; white background
            mask = np.ones_like(video) * 255
            #cv2.imshow('mask before operation', mask)

            # Copy ROI from original image to target blank canvas
            mask = cv2.bitwise_and(mask, video, mask=roi) + cv2.bitwise_and(mask, mask, mask=~roi)
            #cv2.imshow('mask after operation', mask)

            roi_analyze = mask[y-r: y+r, x-r: x+r]

            # note to self: both these lines produce similar valuse, but cv.countNonZero better since it sprob more accurate.
            non_zero_pixels = cv2.countNonZero(roi)
            # print('non zero pixs:', non_zero_pixels)
            # print('p r 2: ', math.pi * r**2)

            #print('mask [0] length', len(mask[0]), 'mask length', len(mask))
            #print('mask [0] sum avg:', sum(), 'mask sum sum avg:', sum(sum(mask))/len(mask))
            #print('mask sum', sum(mask), 'mask len: ', len(mask), 'mask[0] sum: ', sum(mask[0]), 'len mask[0]:', len(mask[0]))
            #print('roi:  ', roi)
            sum1 = [sum(i) for i in zip(*roi_analyze)]
            #print('roi sum1: ', sum1)
            sum2 = sum(sum1)
            #print('roi sum2: ', sum2)
            frame_intensity_sum = sum2/(2*r*2*r) # 4*r^2 is the area of analysis (two radii wide, two radii high) sum(sum(mask))/len(mask[0])
            #print('frame int sum: ', frame_intensity_sum)
            #print('area with pi', )
            #print('summed mask', sum(sum(mask))/len(mask[0]))
            frame_intensity_sum_hold.append(int(frame_intensity_sum))



            #print('current frame of video being analyzed: ', cap2.get(cv2.CAP_PROP_POS_FRAMES), 'total frames:', total_frame_count, '%:', cap2.get(cv2.CAP_PROP_POS_FRAMES)/total_frame_count*100)

            
            #print('framesum', frame_intensity_sum)
        #print('frame intensity hold', frame_intensity_sum_hold)
        #cv2.imshow('mask after operation', mask)
        
        #sys.stdout.write('Completion: ' + str(round(cap2.get(cv2.CAP_PROP_POS_FRAMES)/total_frame_count*100, 2)) + '%')
        #sys.stdout.flush()
        
        # SETTINGS FOR ANALYSIS OF WHICH FRAMES (HIGHER = FASTER ANALYSIS)

        video_millisecond_position = cap2.get(cv2.CAP_PROP_POS_MSEC)
        video_milliseconds.append(video_millisecond_position)


        frame_axes.append(frame_count_change) # forms the axes of frames analyzed for plotting purposes
        #print('frame axes list: ', frame_axes)

        frame_count_change += float(frame_count) # advances at 30 frames. Ex: if video is 30 FPS, advances 1 second.
        ###print('fraame ciount change:', frame_count_change)
        cap2.set(cv2.CAP_PROP_POS_FRAMES, frame_count_change)
        ###print('current frame', cv2.CAP_PROP_POS_FRAMES)

        video_BGR_data.append(frame_intensity_sum_hold)

        #video_BGR_data.append(round(sum(frame_BGR_data)/len(frame_BGR_data))) #I used calculator to confirm; this is the average of BGR... presumably for each circle!
        #print('video BGR', video_BGR_data, 'length:', len(video_BGR_data))
                
        #video_BGR_data.append(round(sum(frame_BGR_data)/len(frame_BGR_data))) #I used calculator to confirm; this is the average of BGR... presumably for each circle!
        #print('BGR data total:', video_BGR_data, '\nlength', len(video_BGR_data)) 
        #if KeyboardInterrupt:
            #done = True # stops system writing


done = True # ends the animated loading screen
###print('frame count', frame_count)
###print('frame count input', frame_count_input)

use_temperature_file = False

use_temperature_ramp = False

ask_user_temperature_ready = False


while True: # it seems that after video analysis, the data is stored in memory :))) 
    frame_id = int(cap2.get(cv2.CAP_PROP_POS_FRAMES)) # for some reason, this doesnt start from 1 and go to the final frame, even while looping; it gives the final total frame count right away!! I suspect its because the video was alraedy read in the prev loop (data stored in memory?)

    intensity_axes = DDG.get_intensity_axes(video_BGR_data)
    intensity_difference_axes = DDG.get_intensity_difference_axes(intensity_axes)
    #print('checkpoint 1', intensity_difference_axes)

    end_time = time.time()
    elapsed_time = round(end_time - start_time, 2)
    print(f'\n\n{RED}[PROGRAM] > {END}The analysis took: {YELLOW}', elapsed_time, f'{END} seconds to complete \n({YELLOW}', round(elapsed_time/duration*100, 2), f' %{END} of time relative to the video duration)')

    print(f'\n{RED}[PROGRAM] > {END}Total frames analyzed: ', frame_id)

    while not ask_user_temperature_ready:

        print(f'\n{RED}[PROGRAM] > {END}Would you like to attach temperature data to the analyzed circles? Please choose an option below.')
        print(f'''

        {CYAN}Options                                                            Description{END}
           {YELLOW}(1) Yes. Upload a {YELLOW}.csv File{END} ------------------------------ File must contain a {YELLOW}\'Temperature\' and a \'Seconds\' column{END}, in {YELLOW}degrees C° and seconds{END} (recommended to use integer values, but not necessary).
           {YELLOW}(2) Yes. Input a {YELLOW}Temperature Ramp{END} ----------- Input a value to represent the {YELLOW} decreasing change in degrees C° / second{END}, assuming the ramp begins at the {YELLOW}start of the video{END}. {RED}(+/- signs matter!){END}))
           {YELLOW}(3) No. -------------------------------------------------- No temperature plots will be given. Only the intensity plots vs time will be shown.

        ''')
        ask_user_temperature = input(f'\n\n{GREEN}[USER INPUT] > {END}')
        
        if ask_user_temperature == '1':

            temperature_file = print(f'\n{RED}[PROGRAM] > {END}Please provide the {YELLOW}temperature data{END} file (Accepted format: .csv). \nFile must contain the words {YELLOW}\'Temperature\' and a \'Time\'{END} in two separate column headers, in {YELLOW}degrees C° and seconds{END}. The position of the columns, or if there are other words attached to the header, does not matter. (Recommended to use integer values, but not necessary).')

            temperature_file = askopenfilename()

            use_temperature_file = True

            ask_user_temperature_ready = True

            print(f"\n{RED}[SYSTEM] > {END}Does the temperature file exist: ", os.path.exists(temperature_file))
        
        elif ask_user_temperature == '2':

            use_temperature_ramp = True

            #print(f'\nPlease input a value to represent the {YELLOW} decreasing change in degrees C° / second{END}, assuming the ramp begins at the {YELLOW}start of the video.{END} {RED}(+/- signs matter!){END})

            input_valid = False

            while input_valid == False:
            
                ramp = input(f'\nPlease input a single value to represent the {YELLOW} decreasing change in degrees C° / second{END}, assuming the ramp begins at the {YELLOW}start of the video.{END} {RED}(+/- signs matter!){END})\n\n{GREEN}[USER INPUT] > {END}')

                try:
                    if isinstance(float(ramp), float):

                        input_valid = True

                        ramp = float(ramp)
                
                except:

                    print(f'{RED}[PROGRAM] > {END}Invalid input. Please provide a float or integer value.')

            input_valid = False

            while input_valid == False:
            
                ramp_initial = input(f'\nPlease input the {YELLOW}initial temperature of the ramp in degrees C°{END} {RED}(+/- signs matter!){END}.\n\n{GREEN}[USER INPUT] > {END}')

                try:
                    if isinstance(float(ramp_initial), float):

                        input_valid = True

                        ramp_initial = float(ramp_initial)
                
                except:

                    print(f'{RED}[PROGRAM] > {END}Invalid input. Please provide a float or integer value.')
                    

            ask_user_temperature_ready = True


        elif ask_user_temperature == '3':

            #use_temperature_file = False

            ask_user_temperature_ready = True

        else:

            print(f'\n{RED}[PROGRAM] > {END}Invalid input. Please select an option (1-3).\n')

    
    x = input(f'\n{RED}[PROGRAM] > {END}To save the data as a .csv file and to show the plotted graphs, press {YELLOW}[ENTER]{END}.\n\n{GREEN}[USER INPUT] > {END}')
    if x in 'Rr':
        break



    if cv2.waitKey(1) == ord('r'): #27: # Escape key ASCII is 27. If R is pressed on video instead of console.
        break



timestr = time.strftime("%Y%m%d_%H%M%S")

csv_name = timestr + '_' + ntpath.basename(filename) # get base name of file directory path

video_seconds = []

for i in video_milliseconds:

    video_seconds.append(i/1000)

cap.release()

cv2.destroyAllWindows


figure, axis = plt.subplots(2, 2, figsize=(30,15)) # width, height

DDG.plot_intensity_vs_seconds(intensity_axes, video_seconds, axis)

DDG.plot_dintensity_vs_seconds(intensity_difference_axes, video_seconds, axis)


circle_radii = []
circle_freezing_temperatures = []
os.environ["USERPROFILE"]
save_path = os.path.join(os.environ["USERPROFILE"], "Desktop")

if use_temperature_file == True:
    
    df = pd.read_csv(temperature_file)

    #temperature_df = temperature_df.iloc[:,0].str.split(';', expand = True) # iloc method allows us to pass the column's index position

    # gets the time associated with each temperature

    temperature_time = []

    for col in df.columns:

        if 'time' in col.lower():

            print(f'\n{RED}[PROGRAM] > {END}Time column successfully detected in the provided file!')

            temperature_time = df[col].values

            #temperature_time = [round(float(x), 2) for x in temperature_time]

            print(temperature_time)

            break # only take the first instance 

    #temperature_time = list(temperature_df.iloc[:,2].values)

    #temperature_time = [round(float(x), 0) for x in temperature_time] # convert list of strings to list of integers

    # gets the real temperature data

    temperature = []

    for col in df.columns:

        if 'temperature' in col.lower() or 'temp' in col.lower():

            print(f'\n{RED}[PROGRAM] > {END}Temperature column successfully detected in the provided file!')

            temperature = df[col].values

            temperature = [round(float(x), 2) for x in temperature]

            print(temperature)

            break # only take the first instance

    if len(temperature_time) == 0:
        print(f'\n{RED}[PROGRAM] > {END}[ERROR] > Time column not found in the provided file!')

    if len(temperature) == 0:
        print(f'\n{RED}[PROGRAM] > {END}[ERROR] > Temperature column not found in the provided file!')


    #temperature = list(temperature_df.iloc[:,1].values)

    #temperature = [float(x) for x in temperature] # convert list of strings to list of integers



    temperature_axes, temperature_time_axes = DDG.get_temperature_axes(video_seconds, temperature_time, temperature)
    modified_temperature_axes = DDG.get_correct_temperature_axes(intensity_axes, temperature_axes)
    intensity_axes_for_temperature = DDG.get_correct_intensity_axes(intensity_axes, modified_temperature_axes)
    #DDG.plot_intensity_vs_temperature(intensity_axes_for_temperature, modified_temperature_axes, axis)

    DDG.plot_time_and_dintensity_heatmap(intensity_difference_axes, video_seconds, modified_temperature_axes, temperature_time_axes, axis)

    min_intensity_all_temperatures = DDG.get_freezing_temperature(intensity_difference_axes, video_seconds, temperature_axes, temperature_time_axes)

    bin_data_list, bin_edges, label_names = DDG.get_boxplot_data_by_radii(calib_r_list, min_intensity_all_temperatures)

    DDG.plot_boxplot(bin_data_list, bin_edges, label_names, axis)

    # only plot points if the time data between temperature csv file and the video time data match.
    #paired_intensity_difference_to_temperature = DDG.get_dintensity_matched_to_temperature(intensity_difference_axes, video_seconds, temperature_df)
    #DDG.plot_dintensity_vs_temperature(paired_intensity_difference_to_temperature, axis)
    for i in range(len(bin_data_list)):

        for t in range(len(bin_data_list[i])):

            circle_radii.append(bin_data_list[i][t][0])
            circle_freezing_temperatures.append(bin_data_list[i][t][1])

    c = {'Radii (um)': circle_radii, 'Freezing Temperature (C)': circle_freezing_temperatures}

    export_radii_freezing = pd.DataFrame(c)

    export_radii_freezing.to_csv(save_path + '/GIN/' + csv_name + '_radii_freezing_(CSV_INPUT).csv')

if use_temperature_ramp == True:

    ramp_temperatures = []


    int_video_seconds = [round(x,0) for x in video_seconds] # round values to be integers.

    for i in int_video_seconds:
        
        ramp_temperatures.append(round(ramp_initial + ramp * i, 5))

    ramp_time = int_video_seconds

    #for i in ramp_temperatures:

    #    ramp_time.append((i - ramp_temperatures[0]) / ramp) # subtract from target_temperatures[0] to get 0 seconds at the initial temperature


    # sort through this!
    temperature_axes, temperature_time_axes = DDG.get_temperature_axes(video_seconds, ramp_time, ramp_temperatures)
    modified_temperature_axes = DDG.get_correct_temperature_axes(intensity_axes, temperature_axes)
    intensity_axes_for_temperature = DDG.get_correct_intensity_axes(intensity_axes, modified_temperature_axes)

    DDG.plot_time_and_dintensity_heatmap(intensity_difference_axes, video_seconds, modified_temperature_axes, temperature_time_axes, axis)

    min_intensity_all_temperatures = DDG.get_freezing_temperature(intensity_difference_axes, video_seconds, temperature_axes, temperature_time_axes)

    bin_data_list, bin_edges, label_names = DDG.get_boxplot_data_by_radii(calib_r_list, min_intensity_all_temperatures)

    DDG.plot_boxplot(bin_data_list, bin_edges, label_names, axis)

    # only plot points if the time data between temperature csv file and the video time data match.
    for i in range(len(bin_data_list)):

        for t in range(len(bin_data_list[i])):

            circle_radii.append(bin_data_list[i][t][0])
            circle_freezing_temperatures.append(bin_data_list[i][t][1])

    c = {'Radii (um)': circle_radii, 'Freezing Temperature (C)': circle_freezing_temperatures}

    export_radii_freezing = pd.DataFrame(c)

    export_radii_freezing.to_csv(save_path + '/GIN/' + csv_name + '_radii_freezing_(RAMP_INPUT).csv')







d = {'Frame Time (seconds)': video_seconds, 'Frames Axes': frame_axes}

export_intensity_differences = pd.DataFrame(d)

for i in range(len(intensity_axes)):

    export_intensity_differences['Avg Grayscale Intensity of Circle' + str(i+1)] = intensity_axes[i]

export_intensity_differences.to_csv(save_path + '/GIN/' + csv_name + '_intensity_change.csv')

plt.savefig(save_path + '/GIN/' + csv_name + '_all_plots.png')

end_banner = f'''\n
{CYAN}
                ░▄░█░░░▄▀▀▀▀▀▄░░░█░▄░
                ▄▄▀▄░░░█─▀─▀─█░░░▄▀▄▄
                ░░░░▀▄▒▒▒▒▒▒▒▒▒▄▀░░░░
                ░░░░░█────▀────█░░░░░
                ░░░░░█────▀────█░░░░░

                   END OF PROGRAM! 
{END}
'''
print(end_banner)
plt.show()
root.destroy() # destroy tkinter windows

