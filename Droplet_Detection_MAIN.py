#Droplet_Detection_MAIN

# TO DO: frame_circles() fn may benefit from using thresholds to detect circles based on dark circumference

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

'''
# PACKAGES AND MODULES

#PLEASE REMEMBER TO RUN/SAVE EDITS TO MODULES; CODE WILL NOT WORK OTHERWISE.
import cv2 
import numpy as np
import time
import os
import pandas as pd
import itertools # for animated loading :)
import threading # for animated loading :D
import sys # also for loading :0
import matplotlib.pyplot as plt
import numpy as np

import Droplet_Detection_Utility as DDU
import Droplet_Detection_Frame as DDF
import Droplet_Detection_Selection_Frame as DDS
import Droplet_Detection_Intensity_Tracker as DDI
import Droplet_Detection_Grapher as DDG

# LOAD VIDEO

file = str(input('\n\n\n─── ∘°❉°∘ ──── ∘°❉°∘ ──── ∘°❉°∘ ──── ∘°❉°∘ ───\nEnter the name of the video: '))
filename = 'Assets/' + file
#filename = 'Assets/TX100_MineralOil_1to3_Test_v3.mp4'
cap = cv2.VideoCapture(filename)
cap1 = cv2.VideoCapture(filename)
cap2 = cv2.VideoCapture(filename)

total_frame_count = cap2.get(cv2.CAP_PROP_FRAME_COUNT)
fps = cap2.get(cv2.CAP_PROP_FPS)
duration = total_frame_count/fps
minutes = int(duration/60)
seconds = duration%60


#size_ratio = float(input('Enter a value to scale the video by: '))
size_ratio = 0.5

frame_count = 1

######################
####### SCRIPT #######
######################

stop_reiterating = False
x = 0
print("Does the file exist: ", os.path.exists(filename))

codec_code = cap2.get(cv2.CAP_PROP_FOURCC)
print('Codec code of video: ', hex(int(codec_code)))
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
            print('\n---------\nVideo Loaded Successfully')
            print('Total frame count of video ----------- [', total_frame_count, ']')
            print('The detected video FPS --------------- [', fps, ']')
            print('Duration of the video: --------------- [', round(duration, 2), ' sec ], or [', str(minutes), ' min', str(round(seconds, 2)), ' sec ]')
            frame_count_input = input('\nPlease enter an integer for the interval of frames to be analyzed. If no input is given, the FPS of the video will be used instead.\n(TIP: to anayze every n seconds of the video, enter the product of FPS * n.)\n\n')

            if frame_count_input.isnumeric():
                frame_count = float(frame_count_input)
                print('\nThe analysis will occur every [', frame_count,'] frames.\n')

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

            DDF.frame_overlay_label(areas_sorted, frame)

            n = 'WINDOW 1 /// DETECTED CIRCLES'
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


        selection_frame = DDS.selected_circles_on_frame(selection_list, selection_frame)


        n = 'WINDOW 2 /// SELECTED CIRCLES FOR ANALYSIS'
        DDU.show_window(n, selection_frame, size_ratio, cap1, filename)
        

    if stop_reiterating == True:
        i = input('\n---------\nThe deselected circles have been removed. \nPress [R or ENTER] to begin analysis of the change in intensity within each circle.')
        if i in 'Rr':
            break
    else:
        stop_reiterating = True # will set stop_reinterating to true after the first loop

    if cv2.waitKey(1) == ord('r'): #27: # Escape key ASCII is 27. If R is pressed on video instead of console.
        break



while True:
    stop_reiterating = False
    print('\n---------\nTo cancel the program, please close the program.\n') #press \'Esc\' on the video window, or input Ctrl + C in console.\n')
    cv2.destroyAllWindows
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

while True: # it seems that after video analysis, the data is stored in memory :))) 
    frame_id = int(cap2.get(cv2.CAP_PROP_POS_FRAMES)) # for some reason, this doesnt start from 1 and go to the final frame, even while looping; it gives the final total frame count right away!! I suspect its because the video was alraedy read in the prev loop (data stored in memory?)

    intensity_axes = DDG.get_intensity_axes(video_BGR_data)
    intensity_difference_axes = DDG.get_intensity_difference_axes(intensity_axes)
    #print('checkpoint 1')


    end_time = time.time()
    elapsed_time = round(end_time - start_time, 2)
    print('\n---------\nThe analysis took: ', elapsed_time, ' seconds to complete (Efficiency: ', round(elapsed_time/duration*100, 2), ' % of time relative to the video duration)')

    print('\nTotal frames analyzed: ', frame_id)
    
    x = input('\nTo save the data as a .csv file and to show the plotted intensity vs frame or time graphs, press [R or ENTER].')
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

video_seconds = []

for i in video_milliseconds:
    video_seconds.append(i/1000)

d = {'Frame Time (milliseconds)': video_seconds, 'Frames Axes': frame_axes}
#print(len(frame_axes), len(intensity_axes))
export_intensity_differences = pd.DataFrame(d)

for i in range(len(intensity_axes)):
    export_intensity_differences['Avg Grayscale Intensity of Circle' + str(i+1)] = intensity_axes[i]

export_intensity_differences.to_csv('Saved_data/' + csv_name + '.csv')

cap.release()
cv2.destroyAllWindows

figure, axis = plt.subplots(2, 2, figsize=(15,9)) # width, height

DDG.plot_intensity_vs_frames(intensity_axes, frame_axes, axis, frame_count)
DDG.plot_dintensity_vs_dframes(intensity_difference_axes, frame_axes, axis, frame_count)
DDG.plot_intensity_vs_seconds(intensity_axes, video_seconds, axis)
DDG.plot_dintensity_vs_seconds(intensity_difference_axes, video_seconds, axis)

print('To conclude the script, please close the graph window.')
plt.show()

