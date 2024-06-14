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

import Droplet_Detection_Utility as DDU
import Droplet_Detection_Frame as DDF
import Droplet_Detection_Selection_Frame as DDS
import Droplet_Detection_Intensity_Tracker as DDI
import Droplet_Detection_Grapher as DDG

print('\n\n\n════════════════ *.·:·.✧ ° ❆ ° ✧.·:·.* ════════════════')
print('         Grayscale Ice Nucleation (GIN) software         ')
print('            Originally designed for use with:            ')
print('Vienna Optical Droplet Crystallization Analyzer (VODCA)')
print('              Created by: William Bae (UBC)              ') 
print('                 [www.github.com/wbae03]              ')
print('════════════════ *.·:·.✧ ° ❆ ° ✧.·:·.* ════════════════')

# CUSTOMIZABLE PARAMETERS

size_ratio = 0.25 # Proportionally changes the size of image and video files used in the program.

file_directory = 'Assets/'

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

while not ask_user_calib_ready: # While loop ensures the user prompts are repeated if the user input is invalid (ie not 'y' or 'n')

    ask_user_calib = input('\nDo you require calibration using an image with a known measurement (ie. using a ruler)? \nYou may instead enter a calibration ratio (image pixel length / actual micrometer length) obtained from previous calibrations.\nPress \'Y\' to load an image.\nPress \'N\' to enter a known calibration ratio value.\n\n[USER INPUT] > ')

    if ask_user_calib.lower() == 'y':

        use_calib_image = True

        ask_user_calib_ready = True

        calib_file = str(input('\n📏 Enter the name of the calibration image file:\n\n[USER INPUT] > '))

        calib_file = file_directory + calib_file

        print("\n[SYSTEM] > Does the calibration file exist: ", os.path.exists(calib_file))

    elif ask_user_calib.lower() == 'n':

        use_calib_image = False

        ask_user_calib_ready = True

    else:

        print('\nInvalid input. Please press \'Y\' or \'N\'.\n (Tip: if you do not require a calibration, you can just put in an arbitrary calibration value after press \'N\')')

if use_calib_image == True:

    image = cv2.imread(calib_file) # Program loads the image inputted

    temp_image = image.copy()

    def on_mouse(event, x, y, flags, param): # although flags and param are not used in this function, they must be included in the parameters as the data from mouse clicks feeds into this function and includes these parameters.

        global drawing, sbox, line_coords, temp_image, calib_pixel_length, calib_real_length, calib_user_ready, calibration_ratio, close_calib_window

        x = math.floor(x * 1/size_ratio) # note: resizing the window size DOES NOT scale down the frames system / mouse coordinate system.. must convert the mouse values by applying an opposite scale (ie if the frame is scaled down by 0.5 of original size, then scale mouse coordinates by 1/0.5 aka x2 !!)
        
        y = math.floor(y * 1/size_ratio)

        if event == cv2.EVENT_LBUTTONDOWN:

            print('\nStart Mouse Position: [' + str(x) + ',' + str(y) + ']')

            sbox = [x, y]

            line_coords.append(sbox)

            drawing = True

        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing:
                temp_image = image.copy()  # Reset to the original image
                cv2.line(temp_image, tuple(sbox), (x, y), (0, 0, 255), 4)
                #print('drawing! initial xy:', sbox, 'final xy:', x, y)

        elif event == cv2.EVENT_LBUTTONUP:
            print('End Mouse Position: [' + str(x) + ',' + str(y) + ']')
            ebox = [x, y]
            line_coords.append(ebox)
            drawing = False
            # Draw the final line on the main image
            cv2.line(image, tuple(sbox), tuple(ebox), (0, 0, 255), 5)

            # use pythagorean theorem to find length of line
            x_length = abs(sbox[0] - ebox[0])
            y_length = abs(sbox[1] - ebox[1])
            calib_pixel_length = round(math.sqrt(x_length**2 + y_length*2), 2)
            print('\nCalibration pixel length: [', calib_pixel_length, ']')

            while calib_user_ready == False:
                
                calib_real_length = input('\nPlease enter the actual length [MICROMETERS] of the calibration tool.\n\n[USER INPUT] > ')

                if calib_real_length.isnumeric():

                    calib_user_ready = True
                    calibration_ratio = round(float(calib_pixel_length) / float(calib_real_length), 2) # magnification = image length / actual length
                    print('\nCalibration successful. The calibration ratio is: [', calibration_ratio, ']. \nPlease write down this value if you will be analyzing more video data in the future, so you can enter the calibration ratio.')

                else:
                    print('\nInvalid input. Please enter the actual length [MICROMETERS] of the calibration tool')
           


    # Create a window and set the mouse callback
    cv2.namedWindow('Calibration Window')
    cv2.setMouseCallback('Calibration Window', on_mouse)

    # Keep the window open until a key is pressed
    
    print('\nIn the calibration window, please draw a line parallel to the calibration tool / ruler by holding the left mouse button.\n\n[USER INPUT] > ')

    while close_calib_window == False:
        resized_temp_image = cv2.resize(temp_image, (0,0), fx = size_ratio, fy = size_ratio)
        cv2.setWindowProperty('Calibration Window', cv2.WND_PROP_TOPMOST, 1)
        cv2.moveWindow('Calibration Window',10,50)
        cv2.imshow('Calibration Window', resized_temp_image)
        cv2.startWindowThread()


        if calibration_ratio != 0:
            close_calib_window = True

        if cv2.waitKey(1) & 0xFF == 27:  # Exit on pressing 'ESC'
            break

    


elif use_calib_image == False:

    while calib_user_ready == False:
        calibration_ratio = input('\nPlease enter a calibration ratio value. \nThis value may be obtained from previous calibrations or analysis of videos with the same dimensions.\n\n[USER INPUT] > ')

        try:
            if isinstance(float(calibration_ratio), float): # checks if the instance is a number

                calib_user_ready = True
                print('\nCalibration successful. The calibration ratio value is: [', calibration_ratio, '].\n Please write down this value if you will be analyzing more video data in the future, so you can enter the calibration ratio.')

        except:
            print('\nInvalid input. Please enter the calibration ratio. If unknown, please restart the program and use a calibration image.')
    


#calib_length = calc_distance(line_coords)
#print('calib length: ', calib_length)

# LOAD VIDEO

file = str(input('\n🎦 Enter the name of the video:\n\n[USER INPUT] > '))
filename = file_directory + file
#filename = 'Assets/TX100_MineralOil_1to3_Test_v3.mp4'
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
print("\n[SYSTEM] > Does the file exist: ", os.path.exists(filename))

codec_code = cap2.get(cv2.CAP_PROP_FOURCC)
print('\nCodec code of video: ', hex(int(codec_code)))
'''
while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, (1920, 1080))
    if not ret: break

    cv2.imshow('test', frame)
    #print('yes')
'''
#print('no')

while True: # makes sure the video loaded + frames are able to be captured

    # MANIPULATE LOADED VIDEO

    ret, frame = cap.read()

    #print(frame)

    #frame = cv2.resize(frame, (640, 500)) #for teresa's videos

    

    if not ret: break


    if stop_reiterating == False:
        if ret:
            print('\nVideo Loaded Successfully')
            print('\n[Filename: ', filename, ']')
            print('Total frame count of video ----------- [', total_frame_count, ']')
            print('The detected video FPS --------------- [', fps, ']')
            print('Duration of the video: --------------- [', round(duration, 2), ' sec ], or [', str(minutes), ' min', str(round(seconds, 2)), ' sec ]')
            frame_count_input = input('\nPlease enter an integer for the interval of frames to be analyzed. If no input is given, the FPS of the video will be used instead.\n(TIP: to anayze every n seconds of the video, enter the product of FPS * n.) \n\n[USER INPUT] > ')

            if frame_count_input.isnumeric():
                frame_count = float(frame_count_input)
                print('\nThe analysis will occur every [', frame_count,'] frames.')

            else:
                frame_count =  fps # if no int is given, resort to default fps setting of the video
                print('\nNo frame count was given. The analysis will resort to the default video property of [', frame_count,'] FPS.')


            #width = int(cap.get(3))
            #height = int(cap.get(4))




            
            # frame_capture: captures a frame of the video based on frame_id
            
            frame_id = 0
            DDF.frame_capture(frame_id, cap)

            # frame_circles: detects circles within the frame
            
            circles = DDF.frame_circles(frame)

            # frame_overlay_sort: numerically orders circles from left to right, top to bottom, based on x and y axis position.
                # done by assessing the calculated area between width and height. Smaller = closer to 0,0... kind of
                # this fn should order the values of circles consistently within lists!!)

            areas_sorted = DDF.frame_overlay_sort(circles)


            # frame_overlay_label: numerically label the order of circles on frame screen

            DDF.frame_overlay_label(areas_sorted, frame, calibration_ratio)

            n = 'WINDOW 1 /// DETECTED CIRCLES'
            cv2.namedWindow(n)
            DDU.show_window(n, frame, size_ratio, cap, filename)
        
        else:
            print('Video Load Error! File may be corrupted, does not meet the compatible file extensions of .mp4 or .mkv, or the recording dimensions are not suitable for analysis. (requires a fullscreen/large recording).')
        

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



while True:

    ret, selection_frame = cap1.read()
    #selection_frame = cv2.resize(frame, (640, 500)) for teresa's videos

    if not ret: break

    # frame_overlay_select: selects a circle(s) and its associated data via its index position within the data lists.
        # could try deleting circles and reshowing screen?
    
    if stop_reiterating == False:
        deselection_input_list = DDS.frame_overlay_select()

        # make_selection_list: makes a list containing the circles that will be analyzed. This fn removes the data for deselected circles.

        selection_list = DDS.make_selection_list(areas_sorted, deselection_input_list, selection_frame)
        #print('selection list:', selection_list)
        # selected_circles_on_frame: places only the selected circles and corresponding numerical identity on a new still frame.


        selection_frame, calib_r_list = DDS.selected_circles_on_frame_and_label(selection_list, selection_frame, calibration_ratio)


        n = 'WINDOW 2 /// SELECTED CIRCLES FOR ANALYSIS'
        cv2.namedWindow(n)
        DDU.show_window(n, selection_frame, size_ratio, cap1, filename)
        

    if stop_reiterating == True:
        i = input('\nThe deselected circles have been removed. \nPress [R or ENTER] to begin analysis of the change in intensity within each circle.\n\n[USER INPUT] > ')
        if i in 'Rr':
            break
    else:
        stop_reiterating = True # will set stop_reinterating to true after the first loop

    if cv2.waitKey(1) == ord('r'): #27: # Escape key ASCII is 27. If R is pressed on video instead of console.
        break



while True:
    stop_reiterating = False
    print('\n---------\nTo cancel the analysis, please close the program as it will not terminate properly within the client.\n') #press \'Esc\' on the video window, or input Ctrl + C in console.\n')
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

        for c in itertools.cycle([' ·      ', ' ⊹  .   ', ' ❅  ..  ', ' ❆  ... ']): 
            if done:
                break
            sys.stdout.write('\rCompletion: ' + str(round(cap2.get(cv2.CAP_PROP_POS_FRAMES)/total_frame_count*100, 2)) + '%' + c) #+ str(round(cap2.get(cv2.CAP_PROP_POS_FRAMES)/total_frame_count*100, 2)) + '%' + c)
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

ask_user_temperature_ready = False

while True: # it seems that after video analysis, the data is stored in memory :))) 
    frame_id = int(cap2.get(cv2.CAP_PROP_POS_FRAMES)) # for some reason, this doesnt start from 1 and go to the final frame, even while looping; it gives the final total frame count right away!! I suspect its because the video was alraedy read in the prev loop (data stored in memory?)

    intensity_axes = DDG.get_intensity_axes(video_BGR_data)
    intensity_difference_axes = DDG.get_intensity_difference_axes(intensity_axes)
    #print('checkpoint 1', intensity_difference_axes)

    end_time = time.time()
    elapsed_time = round(end_time - start_time, 2)
    print('\nThe analysis took: ', elapsed_time, ' seconds to complete (Efficiency: ', round(elapsed_time/duration*100, 2), ' % of time relative to the video duration)')

    print('\nTotal frames analyzed: ', frame_id)

    while not ask_user_temperature_ready:

        ask_user_temperature = input('Would you like to upload an excel file containing the temperature data? (Temperature data should correspond to elapsed experiment/video time in seconds).\n\n[USER INPUT] > ')
        
        if ask_user_temperature.lower() == 'y':

            temperature_file = str(input('\n🌡️ Enter the name of the temperature file:\n\n[USER INPUT] > '))

            temperature_file = file_directory + temperature_file

            use_temperature_file = True

            ask_user_temperature_ready = True

            print("\n[SYSTEM] > Does the temperature file exist: ", os.path.exists(temperature_file))

        elif ask_user_temperature.lower() == 'n':

            use_temperature_file = False

            ask_user_temperature_ready = True

        else:

            print('\nInvalid input. Please press \'Y\' or \'N\'.\n')

    if use_temperature_file == True:

        temperature_df = pd.read_csv(temperature_file)



        temperature_df = temperature_df.iloc[:,0].str.split(';', expand = True) # iloc method allows us to pass the column's index position

        # gets the time associated with each temperature

        temperature_time = list(temperature_df.iloc[:,2].values)

        temperature_time = [round(float(x), 0) for x in temperature_time] # convert list of strings to list of integers

        # gets the real temperature data

        temperature = list(temperature_df.iloc[:,1].values)

        temperature = [float(x) for x in temperature] # convert list of strings to list of integers

        #temperature_df.columns = ['Target Temperature', 'Real Temperature', 'Time']

        #temperature_df[2] = temperature_df.round({'Time': 0})
        
        print('temperature time df check 1', temperature_time, 'temperature check', temperature)
        



    
    x = input('\nTo save the data as a .csv file and to show the plotted intensity vs frame or time graphs, press [R or ENTER].\n\n[USER INPUT] > ')
    if x in 'Rr':
        break



    if cv2.waitKey(1) == ord('r'): #27: # Escape key ASCII is 27. If R is pressed on video instead of console.
        break

    


timestr = time.strftime("%Y%m%d_%H%M%S")
#print(timestr)
csv_name = timestr + '_' + file
'''
frame_time = []
for i in frame_axes:
    ctime = 0
    if platform.system() == 'Windows':
        ctime = time.ctime(os.path.getmtime(filename))
        frame_time.append(ctime)
    else:
        print('NO DATE OR TIME AVAILABLE. Sorry, I did not implement the code for inter-system conversion of date-time properties. It is possible, you just have to implement the code. I have attached a useful link that shows the code to do this where the code for this text exists. Goodluck :)')
        #https://stackoverflow.com/questions/237079/how-do-i-get-file-creation-and-modification-date-times
'''

# if no temperature data is available, the frame vs change in intensity plots will be given.
# if temperature data is given, plots temperature vs change in intensity



video_seconds = []

for i in video_milliseconds:
    video_seconds.append(i/1000)

# gets time associated with each measured temperature
#temperature_seconds = temperature_df.iloc[:,2]
#print('temp', temperature_seconds)

# gets temperature associated with each time


d = {'Frame Time (seconds)': video_seconds, 'Frames Axes': frame_axes}
#print(len(frame_axes), len(intensity_axes))
export_intensity_differences = pd.DataFrame(d)

for i in range(len(intensity_axes)):
    export_intensity_differences['Avg Grayscale Intensity of Circle' + str(i+1)] = intensity_axes[i]

export_intensity_differences.to_csv('Saved_data/' + csv_name + '.csv')

cap.release()
cv2.destroyAllWindows

figure, axis = plt.subplots(2, 3, figsize=(12,6)) # width, height

if use_temperature_file == True:
    

    temperature_axes, temperature_time_axes = DDG.get_temperature_axes(video_seconds, temperature_time, temperature)
    modified_temperature_axes = DDG.get_correct_temperature_axes(intensity_axes, temperature_axes)
    intensity_axes_for_temperature = DDG.get_correct_intensity_axes(intensity_axes, modified_temperature_axes)
    DDG.plot_intensity_vs_temperature(intensity_axes_for_temperature, modified_temperature_axes, axis)

    DDG.plot_time_and_dintensity_heatmap(intensity_difference_axes, video_seconds, modified_temperature_axes, temperature_time_axes, axis)

    min_intensity_all_temperatures = DDG.get_freezing_temperature(intensity_difference_axes, video_seconds, temperature_axes, temperature_time_axes)

    bin_data_list, bin_edges, label_names = DDG.get_boxplot_data_by_radii(calib_r_list, min_intensity_all_temperatures)

    DDG.plot_boxplot(bin_data_list, bin_edges, label_names, axis)

    # only plot points if the time data between temperature csv file and the video time data match.
    #paired_intensity_difference_to_temperature = DDG.get_dintensity_matched_to_temperature(intensity_difference_axes, video_seconds, temperature_df)
    #DDG.plot_dintensity_vs_temperature(paired_intensity_difference_to_temperature, axis)

#if use_temperature_file == False:

    
    #DDG.plot_intensity_vs_frames(intensity_axes, frame_axes, axis, frame_count)
    #DDG.plot_dintensity_vs_dframes(intensity_difference_axes, frame_axes, axis, frame_count)

DDG.plot_intensity_vs_seconds(intensity_axes, video_seconds, axis)
DDG.plot_dintensity_vs_seconds(intensity_difference_axes, video_seconds, axis)

print('\nTo conclude the script, please close the graph window or press [Ctrl + C].')
plt.show()

