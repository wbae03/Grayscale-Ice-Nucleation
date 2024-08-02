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

# related to colorama package, to allow ANSI escape codes for coloured text
init() 

# Create a single instance of Tk
root = tk.Tk()

# Set the window attributes
root.wm_attributes('-topmost', 1)

# Withdraw the window
root.withdraw()

# defining ANSI escape codes for coloured text
RED = "\33[91m"
BLUE = "\33[94m"
GREEN = "\033[32m"
YELLOW = "\033[93m"
PURPLE = '\033[0;35m' 
CYAN = "\033[36m"
LBLUE = "\033[94m"
END = "\033[0m"
BOLD = "\033[1m"

# bootup title
def banner():
    font = fr'''
    {CYAN}
   ___                               _         _____               __            _            _   _             
  / _ \_ __ __ _ _   _ ___  ___ __ _| | ___    \_   \___ ___    /\ \ \_   _  ___| | ___  __ _| |_(_) ___  _ __  
 / /_\/ '__/ _` | | | / __|/ __/ _` | |/ _ \    / /\/ __/ _ \  /  \/ / | | |/ __| |/ _ \/ _` | __| |/ _ \| '_ \ 
/ /_\\| | | (_| | |_| \__ \ (_| (_| | |  __/ /\/ /_| (_|  __/ / /\  /| |_| | (__| |  __/ (_| | |_| | (_) | | | |
\____/|_|  \__,_|\__, |___/\___\__,_|_|\___| \____/ \___\___| \_\ \/  \__,_|\___|_|\___|\__,_|\__|_|\___/|_| |_|
                 |___/                                                                  {BOLD}Version 1.8.2{END}                                              
{END}
    {GREEN}> {END}William Bae | NBD Group @ UBC Chemistry     {GREEN}> {END}www.github.com/wbae03     {GREEN}> {END}LinkedIn: wbae03

              {GREEN}> {END}Known OS Compatibilities: Win10 | Win11          {GREEN}> {END}Created 24/06/14

    '''
    print(font)

# show the title
banner()

# Proportionally change the size of image and video inputs.
size_ratio = 0.3

# stores calibration image
calib_file = ''

# condition to trigger calibration file input
use_calib_image = False 

# switch to terminate loop for calibration section
ask_user_calib_ready = False

#//////////////// Global variables for manipulating calibration image //////////////
#
# true when mouse is pressed on the image
drawing = False
#
sbox = []
#
line_coords = []
#
calib_real_length = 0
#
calib_pixel_length = 0
#
calib_user_ready = False
#
calibration_ratio = 0
#
close_calib_window = False
#
finished_drawing = False
#///////////////////////////////////////////////////////////////////////////////////////

# loop ensures user input is valid before moving on
while not ask_user_calib_ready:

    ask_user_calib = input(f'\n{RED}[PROGRAM] >{END} Do you require calibration using an image with a known measurement (ie. using a ruler)? \nAlternatively, enter a calibration ratio {YELLOW}(pixel length / micrometer length){END} obtained from previous calibrations.\n\nPress {YELLOW}\'Y\'{END} to load an image.\nPress {YELLOW}\'N\'{END} to enter a known calibration ratio value.\n\n{GREEN}[USER INPUT] > {END}')

    if ask_user_calib.lower() == 'y':

        use_calib_image = True

        ask_user_calib_ready = True

        calib_file = askopenfilename()

        print(f"\n{RED}[SYSTEM] >{END} Does the calibration file exist: ", os.path.exists(calib_file))

    elif ask_user_calib.lower() == 'n':

        use_calib_image = False

        ask_user_calib_ready = True

    else:

        print(f'\n{RED}[PROGRAM] >{END} Invalid input. Please press {YELLOW}\'Y\'{END} or {YELLOW}\'N\'{END}.\n (Tip: if you do not require a calibration, you can just put in an arbitrary calibration value after press \'N\'){END}')

if use_calib_image == True:

    # load the calibration image
    image = cv2.imread(calib_file)

    temp_image = image.copy()

    # defining mouse actions to draw/manipulate the calibration image
    def on_mouse(event, x, y, flags, param): 

        global finished_drawing, drawing, sbox, line_coords, temp_image, calib_pixel_length, calib_real_length, calib_user_ready, calibration_ratio, close_calib_window

        # note: resizing the image file proportionally does not scale down the mouse coordinate system. Must convert the mouse values.
        x = math.floor(x * 1/size_ratio)
        
        y = math.floor(y * 1/size_ratio)

        # left mouse button down event
        if event == cv2.EVENT_LBUTTONDOWN and finished_drawing == False:

            print(f'\n{RED}[PROGRAM] > {END}Start Mouse Position: {YELLOW}[' + str(x) + ',' + str(y) + f']{END}')

            sbox = [x, y]

            line_coords.append(sbox)

            drawing = True

        # mouse movement event
        elif event == cv2.EVENT_MOUSEMOVE and finished_drawing == False:

            if drawing:

                # reset to the original image
                temp_image = image.copy()  # Reset to the original image

                cv2.line(temp_image, tuple(sbox), (x, y), (0, 0, 255), 4)
        
        # left mouse button release event
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

            # dummy variable to pass the except condition.
            dummy = 1

        if calibration_ratio != 0:

            close_calib_window = True

        # exit on pressing 'esc'
        if cv2.waitKey(1) & 0xFF == 27:

            break

elif use_calib_image == False:

    while calib_user_ready == False:

        calibration_ratio = input(f'\n{RED}[PROGRAM] > {END}Please enter a {YELLOW}calibration ratio{END} value. \nThis value may be obtained from previous calibrations or analysis of videos with the same dimensions.\n\n{GREEN}[USER INPUT] > {END}')

        try:

            # checks if the instance is a number
            if isinstance(float(calibration_ratio), float):

                calib_user_ready = True

                print(f'\n{RED}[PROGRAM] > {END}Calibration successful. The calibration ratio value is: {YELLOW}[', calibration_ratio, f']{END}.\n Please write down this value if you will be analyzing more video data in the future, so you can enter the calibration ratio.')

        except:

            print(f'\n{RED}[PROGRAM] > {END}Invalid input. Please enter the calibration ratio. If unknown, please restart the program and use a calibration image.')


print(f'\n{RED}[PROGRAM] > {END} Please provide the file directory of the {YELLOW}video data{END} (Accepted formats: .avi, .mp4, .mkv)')

# Upload the video file
filename = askopenfilename()

# MAKE SAVE DIRECTORY

# gets the basename of the file directory path
csv_name = ntpath.basename(filename)

os.environ["USERPROFILE"]

save_path = os.path.join(os.environ["USERPROFILE"], "Desktop")

folder = 'GIN'

try:

    os.mkdir(save_path + '/GIN/')

    print(f"\n{RED}[PROGRAM] > {END}Directory '% s' created!" % folder)

except FileExistsError:

    print(f"\n{RED}[PROGRAM] > {END}Directory '% s' already exists!" % folder)

try:

    os.mkdir(save_path + '/GIN/' + f'{csv_name}')

    print(f"\n{RED}[PROGRAM] > {END}Directory '% s' created!" % csv_name)

except FileExistsError:

    print(f"\n{RED}[PROGRAM] > {END}Directory '% s' already exists!" % csv_name)

directory = os.path.join(save_path, 'GIN', csv_name)

# prepare different cap 
cap = cv2.VideoCapture(filename)

cap1 = cv2.VideoCapture(filename)

cap2 = cv2.VideoCapture(filename)

cap3 = cv2.VideoCapture(filename)

# total frame count of the video
total_frame_count = cap2.get(cv2.CAP_PROP_FRAME_COUNT)

# fps of video
fps = cap2.get(cv2.CAP_PROP_FPS)

duration = total_frame_count/fps

minutes = int(duration/60)

seconds = duration%60

frame_count = 1

stop_reiterating = False

x = 0

print(f"\n{RED}[SYSTEM] > {END}Does the file exist: ", os.path.exists(filename))

codec_code = cap2.get(cv2.CAP_PROP_FOURCC)

sens_selection = []

user_circle_detection_ready = False

# makes sure the video is loaded + frames are able to be captured
while True:

    ret, frame = cap.read()

    # stop the loop if the video is unable to be loaded
    if not ret: break

    # first iteration condition
    if stop_reiterating == False:

        if ret:

            print(f'\n{RED}[SYSTEM] > {END}\n') 
            print(f'{CYAN}Selected File:{END} {YELLOW}', filename, f'{END}')
            print(f'\n{CYAN}    Video Property                       Value{END}')
            print(f'Total frame count of video ----------- {YELLOW}[', total_frame_count, f']{END}')
            print(f'The detected video FPS --------------- {YELLOW}[', fps, f']{END}')
            print(f'Duration of the video: --------------- {YELLOW}[', round(duration, 2), f' sec ]{END}, or {YELLOW}[', str(minutes), f' min', str(round(seconds, 2)), f' sec ]{END}')

            analysis_start_time = input(f'\n{RED}[PROGRAM] > {END}Enter the {YELLOW}starting time{END} of the video you wish to analyze, in integer seconds.\n\n{GREEN}[USER INPUT] > {END}')

            try:

                if isinstance(int(analysis_start_time), int):

                    analysis_start_time = float(analysis_start_time)

                    print(f'\n{RED}[PROGRAM] > {END}The analysis will start from {YELLOW}[', analysis_start_time,f'] seconds{END}.')

            except:

                # if no int is given, resort to default fps setting of the video 
                analysis_start_time =  0

                print(f'\n{RED}[PROGRAM] > {END}No start time was given. The analysis will begin at {YELLOW}0 seconds{END}.')

            analysis_end_time = input(f'\n{RED}[PROGRAM] > {END}Enter the {YELLOW}final time{END} of the video you wish to analyze, in integer seconds.\n\n{GREEN}[USER INPUT] > {END}')

            try: 

                if isinstance(int(analysis_end_time), int):

                    analysis_end_time = float(analysis_end_time)

                    print(f'\n{RED}[PROGRAM] > {END}The analysis will end when the video is at {YELLOW}[', analysis_end_time,f'] seconds{END}.')

            except:

                # if no int is given, resort to default video duration as the end time.
                analysis_end_time = round(duration, 2)

                print(f'\n{RED}[PROGRAM] > {END}No end time was given. The analysis will end at {YELLOW}{analysis_end_time} seconds{END}.')

            frame_count_input = input(f'\nPlease enter an {YELLOW}integer for the interval of frames to be analyzed{END}. If no input is given, the FPS of the video will be used instead.\n({YELLOW}TIP:{END} to anayze every n seconds of the video, enter the product of FPS * n.) \n\n{GREEN}[USER INPUT] > {END}')

            try:

                if isinstance(int(frame_count_input), int):

                    frame_count = int(frame_count_input)

                    print(f'\n{RED}[PROGRAM] > {END}The analysis will occur every {YELLOW}[', frame_count,f'] frames{END}.')

            except:

                # if no int is given, resort to default fps to set as the frame interval
                frame_count =  round(fps,0)

                print(f'\n{RED}[PROGRAM] > {END}No frame count was given. The analysis will resort to analyzing every {YELLOW}[', frame_count,f'] frames{END}.')
            
            frame_id = 0

            DDF.frame_capture(frame_id, cap)

            while user_circle_detection_ready == False:

                n = 'WINDOW 1 /// DETECTED CIRCLES'
                
                frame_copy = frame.copy()

                circles, user_circle_detection_ready_input = DDF.frame_circles(frame_copy, n)

                # condition if circles are detected
                if circles is not None:

                    areas_sorted = DDF.frame_overlay_sort(circles)

                    DDF.frame_overlay_label(areas_sorted, frame_copy, calibration_ratio)

                    cv2.namedWindow(n)

                    cv2.setWindowProperty(n, cv2.WND_PROP_TOPMOST, 1)

                    cv2.moveWindow(n,10,50)

                    DDU.show_window(n, frame_copy, size_ratio, cap, filename)

                    cv2.imwrite(os.path.join(directory, f'{csv_name}_Image_of_Detected_Circles.jpg'), frame_copy)
            
                    if user_circle_detection_ready_input == True:

                        user_circle_detection_ready = True
                
                # condition if no circles are detected
                else:
                    
                    print(f'\n{RED}[PROGRAM] > {END}Unable to detect circles with the given circle detection option. Please {YELLOW}reselect.{END}')

        else:

            print(f'{RED}[PROGRAM] > {END}Video Load Error! File may be corrupted, does not meet the compatible file extensions.')  

    # breaks the loop after 1 iteration
    if stop_reiterating == True:

        break
      
    else:

        stop_reiterating = True

    if cv2.waitKey(1) == ord('r'):

        break

# reset for use in the next loop
stop_reiterating = False

# list is initially empty. When below loop occurs, deselected circles are appended.
deselection_input_list = []

while True:

    ret, selection_frame = cap1.read()

    if not ret: break

    if stop_reiterating == False:

        deselection_input_list, user_ready = DDS.frame_overlay_select(deselection_input_list)

        selection_list = DDS.make_selection_list(areas_sorted, deselection_input_list, selection_frame)

        selection_frame, calib_r_list = DDS.selected_circles_on_frame_and_label(selection_list, selection_frame, calibration_ratio)

        m = 'WINDOW 2 /// SELECTED CIRCLES FOR ANALYSIS'

        cv2.namedWindow(m)

        cv2.setWindowProperty(m, cv2.WND_PROP_TOPMOST, 1)

        cv2.moveWindow(m,10,50)

        DDU.show_window(m, selection_frame, size_ratio, cap1, filename)

        cv2.imwrite(os.path.join(directory, f'{csv_name}_Image_of_Selected_Circles.jpg'), selection_frame)

    if stop_reiterating == True:

        break # breaks loop and begins analysis

    elif user_ready == True:

        stop_reiterating = True 

    if cv2.waitKey(1) == ord('r'): #27: # Escape key ASCII is 27. If R is pressed on video instead of console.

        break

cv2.destroyWindow(n)

cv2.destroyWindow(m)

# add space before the loading loop. 
print('\n') 


# loop for animated loading screen
while True:

    stop_reiterating = False

    video_BGR_data = []

    # temporal resolution of processing
    previous = time.time()

    delta = 0

    # timer for the entire processing time
    start_time = time.time()

    done = False

    analysis_start_frame = analysis_start_time * fps

    analysis_end_frame = analysis_end_time * fps

    frame_range = analysis_end_frame - analysis_start_frame

    # animated loading screen !!
    def animate():

        for c in itertools.cycle([' ·      ', 
                                  ' ⊹  .   ',
                                  ' ❅  ..  ', 
                                  ' ❆  ... ']): 
            
            if done:

                break

            sys.stdout.write(f'\r{RED}[PROGRAM] > {END}Loading... ' + str(round((cap2.get(cv2.CAP_PROP_POS_FRAMES) - analysis_start_frame)/frame_range*100, 2)) + f'%{CYAN}' + c + f'{END}') #+ str(round(cap2.get(cv2.CAP_PROP_POS_FRAMES)/total_frame_count*100, 2)) + '%' + c)
            
            sys.stdout.flush()
            
            time.sleep(0.5)

    t = threading.Thread(target=animate)

    t.start()

    break

video_milliseconds = []

frame_axes = []

frame_count_change = analysis_start_frame

cap2.set(cv2.CAP_PROP_POS_FRAMES, analysis_start_frame)

# ANALYSIS LOOP. Minimize operations within this loop to speed up analysis
while True: 

    ret, video = cap2.read()

    if not ret or cap2.get(cv2.CAP_PROP_POS_FRAMES) >= total_frame_count or cap2.get(cv2.CAP_PROP_POS_FRAMES) >= analysis_end_frame: 
        
        done = True
        
        break

    # list gets reset every iteration. Purpose is to hold on to values temporarily, to send to another list
    frame_intensity_sum_hold = []

    # grayscale to remove colour noise
    video = cv2.cvtColor(video, cv2.COLOR_BGR2GRAY)

    if selection_list is not None:
        
        for i in range(len(selection_list)):

            x, y, r = selection_list[i][0], selection_list[i][1], selection_list[i][2]

            roi = np.zeros(video.shape[:2], np.uint8)

            roi = cv2.circle(roi, (x, y), r, 255, cv2.FILLED)
            
            # Target image; white background
            mask = np.ones_like(video) * 255

            # Copy ROI from original image to target blank canvas
            mask = cv2.bitwise_and(mask, video, mask=roi) + cv2.bitwise_and(mask, mask, mask=~roi)

            roi_analyze = mask[y-r: y+r, x-r: x+r]

            # note to self: both these lines produce similar valuse, but cv.countNonZero better since it sprob more accurate.
            non_zero_pixels = cv2.countNonZero(roi)
            # print('non zero pixs:', non_zero_pixels)
            # print('p r 2: ', math.pi * r**2)

            sum1 = [sum(i) for i in zip(*roi_analyze)]

            sum2 = sum(sum1)

            # 4*r^2 is the square-shaped area of analysis (2 radii wide, 2 radii high, hence 2 * r * 2 * r)
            frame_intensity_sum = sum2/(2*r*2*r)

            frame_intensity_sum_hold.append(int(frame_intensity_sum))
        
        video_millisecond_position = cap2.get(cv2.CAP_PROP_POS_MSEC)

        video_milliseconds.append(video_millisecond_position)

        # forms the axes of frames analyzed for plotting purposes
        frame_axes.append(frame_count_change)

        # advances the frame of analysis by [frame_count]. If fps is 30 and frame_count = 30, then analysis occurs every 1 video second
        frame_count_change += float(frame_count)

        cap2.set(cv2.CAP_PROP_POS_FRAMES, frame_count_change)

        video_BGR_data.append(frame_intensity_sum_hold)

done = True # ends the animated loading screen

use_temperature_file = False

use_temperature_ramp = False

ask_user_temperature_ready = False

while True:

    # for some reason, this doesnt start from 1 and go to the final frame, even while looping; it gives the final total frame count right away!! I suspect its because the video was alraedy read in the prev loop (data stored in memory?)
    frame_id = int(cap2.get(cv2.CAP_PROP_POS_FRAMES)) 

    intensity_axes = DDG.get_intensity_axes(video_BGR_data)

    intensity_difference_axes = DDG.get_intensity_difference_axes(intensity_axes)

    # Save jpg of frame when very last droplet freezes (the very last maximal change in intensity across all circles)

    # get the entire list except for the last element, because you must match the amount of elements in frame axis to agree with difference axis
    # get entire list except for the last element (must match amount of elements in frame axis to agree with difference axis)
    frame_x = frame_axes[0: -1] 

    min_dintensity_values = [sublist.index(min(sublist)) for sublist in intensity_difference_axes]

    max_of_min_index = max(min_dintensity_values)

    try:

        # try to get the next frame after all is frozen, to ensure the frame contains everything frozen. This is especially useful when analyzing videos in huge frame intervals.
        frozen_frame_number = frame_x[max_of_min_index+1] 
    
    except:

        frozen_frame_number = frame_x[max_of_min_index] 
     
    cap3.set(cv2.CAP_PROP_POS_FRAMES, frozen_frame_number)

    ret, frozen_frame = cap3.read()

    if not ret: break

    frozen_frame, calib_r_list = DDS.selected_circles_on_frame_and_label(selection_list, frozen_frame, calibration_ratio)

    frozen_frame = DDU.get_frame_id(frozen_frame, cap3)

    cv2.imwrite(os.path.join(directory, f'{csv_name}_Image_of_Last_Frozen_Circle.jpg'), frozen_frame)

    end_time = time.time()

    elapsed_time = round(end_time - start_time, 2)

    print(f'\n\n{RED}[PROGRAM] > {END}The analysis took: {YELLOW}', elapsed_time, f'{END} seconds to complete \n({YELLOW}', round(elapsed_time/duration*100, 2), f' %{END} of time relative to the video duration)')

    print(f'\n{RED}[PROGRAM] > {END}Total frames analyzed: ', frame_id)

    while not ask_user_temperature_ready:

        print(f'\n{RED}[PROGRAM] > {END}Would you like to attach temperature data to the analyzed circles? Please choose an option below.')

        print(f'\n{CYAN}Previously Selected Video File:{END} {YELLOW}', filename, f'{END}')

        print(f'''
        {CYAN}Options                                                            Description{END}
           {YELLOW}(1) Yes. Upload .csv File{END} ----------- File must contain a {YELLOW}\'Temperature\' (C) and a \'Seconds\' column{END}.
           {YELLOW}(2) Yes. Input a Temperature Ramp{END} ----- Input the {YELLOW}change in degrees C° / second{END} beginning at the video start {RED}(+/- signs matter!).{END}))
           {YELLOW}(3) No. {END}------------------------------- No temperature-related plots will be given. Only the intensity plots vs time will be shown.

        ''')

        ask_user_temperature = input(f'\n\n{GREEN}[USER INPUT] > {END}')
        
        if ask_user_temperature == '1':

            temperature_file = print(f'\n{RED}[PROGRAM] > {END}Please provide the {YELLOW}temperature data{END} file (Accepted format: .csv). \nFile must contain the words {YELLOW}\'Temperature\' and a \'Time\'{END} in two separate column headers, in {YELLOW}degrees C° and seconds{END}. \nThe position of the columns, or if there are other words attached to the header, does not matter. \n(Recommended to use integer values, but not necessary).')

            temperature_file = askopenfilename()

            use_temperature_file = True

            ask_user_temperature_ready = True

            print(f"\n{RED}[SYSTEM] > {END}Does the temperature file exist: ", os.path.exists(temperature_file))
        
        elif ask_user_temperature == '2':

            use_temperature_ramp = True

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




video_seconds = []

for i in video_milliseconds:

    video_seconds.append(i/1000)

cap.release()

cv2.destroyAllWindows


fig1, axis = plt.subplots(2, 2, figsize=(30,15)) # width, height

DDG.plot_intensity_vs_seconds(intensity_axes, video_seconds, axis)

DDG.plot_dintensity_vs_seconds(intensity_difference_axes, video_seconds, axis)



circle_radii = []

circle_freezing_temperatures = []
# Create or use a directory to store the GIN data.



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

            #print(temperature_time)

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

            #print(temperature)

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

    #print('min int all temp', min_intensity_all_temperatures, 'calib r list', calib_r_list)



    # IF I WANT BOXPLOTS USE THE CODE BELOW 
    # ------
    '''
    bin_data_list, bin_edges, label_names = DDG.get_boxplot_data_by_radii(calib_r_list, min_intensity_all_temperatures)

    DDG.plot_boxplot(bin_data_list, bin_edges, label_names, axis)


    for i in range(len(bin_data_list)):

        for t in range(len(bin_data_list[i])):

            circle_radii.append(bin_data_list[i][t][0])
            circle_freezing_temperatures.append(bin_data_list[i][t][1])


    c = {'Radii (um)': circle_radii, 'Freezing Temperature (C)': circle_freezing_temperatures}

    export_radii_freezing = pd.DataFrame(c)

    export_radii_freezing.to_csv(os.path.join(directory, f'{csv_name}_radii_freezing_(CSV_INPUT).csv')) # use os.path.join() to properly concatenate paths and filenames.

    '''
    # --------
    # OTHERWISE USE RADII VS TEMP PLOT
    
    calib_r_list_sorted, min_intensity_all_temperatures_sorted = DDG.plot_radii_vs_temperatures(calib_r_list, min_intensity_all_temperatures, axis)

    c = {'Radii (um)': calib_r_list_sorted, 'Freezing Temperature (C)': min_intensity_all_temperatures_sorted}

    export_radii_freezing = pd.DataFrame(c)

    export_radii_freezing.to_csv(os.path.join(directory, f'{csv_name}_radii_freezing_(CSV_INPUT).csv')) # use os.path.join() to properly concatenate paths and filenames.


if use_temperature_ramp == True:

    ramp_temperatures = []



    int_video_seconds = [round(x,0) for x in video_seconds] # round values to be integers. +1 so ramp_temperatures has extra temp value to prevent error

    int_video_seconds.append(int_video_seconds[-1] + (int_video_seconds[-1] - int_video_seconds[-2]))
    
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


    '''
    bin_data_list, bin_edges, label_names = DDG.get_boxplot_data_by_radii(calib_r_list, min_intensity_all_temperatures)

    DDG.plot_boxplot(bin_data_list, bin_edges, label_names, axis)

    # only plot points if the time data between temperature csv file and the video time data match.
    for i in range(len(bin_data_list)):

        for t in range(len(bin_data_list[i])):

            circle_radii.append(bin_data_list[i][t][0])
            circle_freezing_temperatures.append(bin_data_list[i][t][1])

    c = {'Radii (um)': circle_radii, 'Freezing Temperature (C)': circle_freezing_temperatures}

    export_radii_freezing = pd.DataFrame(c)

    export_radii_freezing.to_csv(os.path.join(directory, f'{csv_name}_radii_freezing_(RAMP_INPUT).csv'))
    '''

    calib_r_list_sorted, min_intensity_all_temperatures_sorted = DDG.plot_radii_vs_temperatures(calib_r_list, min_intensity_all_temperatures, axis)

    c = {'Radii (um)': calib_r_list_sorted, 'Freezing Temperature (C)': min_intensity_all_temperatures_sorted}

    export_radii_freezing = pd.DataFrame(c)

    export_radii_freezing.to_csv(os.path.join(directory, f'{csv_name}_radii_freezing_(CSV_INPUT).csv')) # use os.path.join() to properly concatenate paths and filenames.



d = {'Frame Time (seconds)': video_seconds, 'Frames Axes': frame_axes}

export_intensity_differences = pd.DataFrame(d)

for i in range(len(intensity_axes)):

    export_intensity_differences['Avg Grayscale Intensity of Circle' + str(i+1)] = intensity_axes[i]

export_intensity_differences.to_csv(os.path.join(directory, f'{csv_name}_intensity_change.csv'))

fig1.savefig(os.path.join(directory, f'{csv_name}_Intensity_Plots.png'))

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


x, y = DDG.get_frozen_fraction_data(min_intensity_all_temperatures)

fig2, axis2 = plt.subplots(1, 1, figsize=(15, 10))

# Customizing the scatter plot with marker and color options
# 'c' sets the color, 'marker' sets the marker style, and 's' sets the marker size
f1 = axis2.scatter(x, y, c='#219fe4', marker='o', s=100)

axis2.set_title(f'Frozen Fraction Plot of {csv_name}')
axis2.grid(linestyle='--', alpha=0.3)
axis2.tick_params(axis='x', labelsize=18)
axis2.tick_params(axis='y', labelsize=18)
axis2.set_xlabel('Temperature (ºC)', fontsize=18)
axis2.set_ylabel(f'Frozen Fraction (n={len(min_intensity_all_temperatures)})', fontsize=18)

fig2.savefig(os.path.join(directory, f'{csv_name}_Frozen_Fraction.png'))


z = {'Frozen Fraction)': y, 'Freezing Temperature (ºC)': x}

export_frozen_fraction = pd.DataFrame(z)

export_frozen_fraction.to_csv(os.path.join(directory, f'{csv_name}_Frozen_Fraction.csv'))


print(end_banner)
plt.show()
root.destroy() # destroy tkinter windows

