#Droplet_Detection_Frame

import cv2 
import numpy as np
import math


def frame_capture(i: int, cap):
    cap.set(cv2.CAP_PROP_POS_FRAMES, i)

def frame_circles(frame):
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # grayscale to remove color noise
    blurFrame = cv2.GaussianBlur(grayFrame, (17, 17), 0) # blur to lower background noise. 2nd p: both values must be odd. Higher = more blur. Default: 17,17
    #value, thresh = cv2.threshold(blurFrame, 200, 255, cv2.THRESH_BINARY_INV) # pixels below 130 become 0, above become 255 (white)

    circles = cv2.HoughCircles(blurFrame, # documentation: https://docs.opencv.org/4.3.0/d3/de5/tutorial_js_houghcircles.html
                               
                            # PLEASE DO NOT CHANGE THE PARAMETERS OF THIS FIRST SET!! THIS HAS BEEN OPTIMIZED FOR THREE VIDEOS THAT USUALLY NEVER HAVE NICE CIRCLES DETECTED TOGETHER, BUT THIS WORKS!!

                            cv2.HOUGH_GRADIENT, 
                            1.1, # influences whether nearby circles will be merged
                            200, # min distance between two circles' centers
                            param1=10, # sensitivity of circle detection; High = wont find much circles. Default: 42
                            param2=45, # accuracy of circle detection; number of edgepoints to declare there's a circle. High = wont find much circles. Default: 75
                            minRadius=30, # min radius of circles
                            maxRadius=200)  # max radius of circles # note to self: the radii parameters are quite important in selecting correct circles!!
    
    print('\nDetectiion parameters #1 used.')
    
    #print('fdsaadfdasfdsfsdasasfa', circles)
    
    if circles is None: # if above parameters/settings were too demanding and the algorithm could not detect a circle, refer to the below parameters instead. On the other hand, if above settings are too sensitive and cause too many inaccurate circles to be detected, opt for less sensitive parameters below.
        
        circles = cv2.HoughCircles(blurFrame, # documentation: https://docs.opencv.org/4.3.0/d3/de5/tutorial_js_houghcircles.html
                                cv2.HOUGH_GRADIENT, 
                                1.1, # influences whether nearby circles will be merged
                                60, # min distance between two circles
                                param1=20, # sensitivity of circle detection; High = wont find much circles
                                param2=45, # accuracy of circle detection; number of edgepoints to declare there's a circle. High = wont find much circles
                                minRadius=30, # min radius of circles
                                maxRadius=500)  # max radius of circles 
        
        print('\nDetectiion parameters #2 used.')
        
    
        if circles is None: # apply these circle detection parameters instead in the case that the video footage is too noisy/unclear in circles for the algorithm. DO NOT USE THESE SETTINGS FOR MORE DEFINED VIDEOS; MILLIONS OF CIRCLES WILL BE DETECTED OTHERWISE !!!
        
            circles = cv2.HoughCircles(blurFrame, # documentation: https://docs.opencv.org/4.3.0/d3/de5/tutorial_js_houghcircles.html
                                    cv2.HOUGH_GRADIENT, 
                                    1.1, # influences whether nearby circles will be merged
                                    30, # min distance between two circles
                                    param1=15, # sensitivity of circle detection; High = wont find much circles
                                    param2=40, # accuracy of circle detection; number of edgepoints to declare there's a circle. High = wont find much circles
                                    minRadius=30, # min radius of circles
                                    maxRadius=300)  # max radius of circles 
            
            print('\nDetectiion parameters #3 used.')
       
            if circles is None: # apply these circle detection parameters instead in the case that the video footage is too noisy/unclear in circles for the algorithm. DO NOT USE THESE SETTINGS FOR MORE DEFINED VIDEOS; MILLIONS OF CIRCLES WILL BE DETECTED OTHERWISE !!!
        
    
                circles = cv2.HoughCircles(blurFrame, # documentation: https://docs.opencv.org/4.3.0/d3/de5/tutorial_js_houghcircles.html
                                        cv2.HOUGH_GRADIENT, 
                                        1.1, # influences whether nearby circles will be merged
                                        30, # min distance between two circles
                                        param1=15, # sensitivity of circle detection; High = wont find much circles
                                        param2=35, # accuracy of circle detection; number of edgepoints to declare there's a circle. High = wont find much circles
                                        minRadius=30, # min radius of circles
                                        maxRadius=300)  # max radius of circles    
                
                print('\n[WARNING] The least sensitive settings for circle detection was used. Consider using a sample video with clearer circles or optimize the circle detection settings.\n')
    
    
    if circles is not None:
        #print(circles)
        circles = np.uint16(np.around(circles)) #converts the list to numpy array)
        #print(circles)
        #print(circles[0])

        # make sure no part of a circle gets rendered outside the window


        for i in circles[0,:]:

            #print(i[0], i[1], i[2])
            above = i[0] - i[2] # remember, the origin (0,0) is top left corner, and +y goes downwards
            below = i[0] + i[2]
            left = i[1] - i[2]
            right = i[1] + i[2]

            # when an out of bounds circle is generated, usually because the radius ends up generating a circle out of the screen, an overflow occurs in the scalar subtraction
            # This results in a really big positive number. 
            # Thus, screen detected circles for absurd radii

            if above < 20000 and below < 20000 and left < 20000 and right < 20000:
                #x, y, r = i[0], i[1], i[2]
                #print('i circles i: ', i)
                cv2.circle(frame, (i[0], i[1]), i[2], (0,0,255), 6) # circumference
                cv2.circle(frame, (i[0], i[1]), 1, (0,0,255), 2) # center point
            else:
            
                print('\n (Above RuntimeWarning explanation) Detected an out-of-bounds circle (y-pos: ', i[0], 'x-pos: ', i[1], 'pixel radius: ', i[2],'). Deselecting the circle...')
    
    else:
        print('WARNING: Unable to detect circles in the given footage. Please tweak the circle detection parameters, so that circles can be detected in the video.')

    ### print('\nDetected circles [x-pos, y-pos, radius]: \n', circles) # to see the numpyarray of the circles generated in this frame. [y, x, r]
    return circles

def frame_overlay_sort(circles):
    
    areas_unsorted = []
    areas_sorted = []        
        
    for i in range(len(circles.astype(np.int32)[0])):
    #for i in range(len(circles[0])):

            x, y, r = circles.astype(np.int32)[0][i][0], circles.astype(np.int32)[0][i][1], circles.astype(np.int32)[0][i][2]
            #x, y, r = circles[0][i][0], circles[0][i][1], circles[0][i][2]

            #print(x,y,r)

            above = y - r # remember, the origin (0,0) is top left corner, and +y goes downwards
            below = y + r
            left = x - r
            right = x + r

            # when an out of bounds circle is generated, usually because the radius ends up generating a circle out of the screen
            # this time, however, an overflow is not caused. It is not scalar addition (i think??)
            # This results in a negative number 
            # Thus, screen detected circles for negative values from radii subtraction

            if above >= 0 and below >= 0 and left >= 0 and right >= 0:

                area = x * y
                areas_unsorted.append([x, y, r, area])
                areas_sorted = sorted(areas_unsorted, key = lambda x: x[3],reverse = False) # sorts the x, y, r properties of each circle based on the area formed by x * y

    #print(areas_sorted)

    return areas_sorted

def frame_overlay_label(areas_sorted: list, frame, calibration_ratio):
     for i in range(len(areas_sorted)):
          
        font = cv2.FONT_HERSHEY_COMPLEX
          
        x = areas_sorted[i][0]
        y = areas_sorted[i][1]

        circle_number = i+1
        areas_sorted[i].append(circle_number) # by this point, each circle has 5 associated properties in this order: [xpos, ypos, radius, xy area, circle # ranked by area]
        #print(x, y)

        frame = cv2.putText(frame, '#' + str(i+1), (x-60, y+10), font, 1, (0, 0, 0), 8, cv2.LINE_AA) # text outline
        frame = cv2.putText(frame, '#' + str(i+1), (x-60, y+10), font, 1, (0, 255, 100), 2, cv2.LINE_AA) # i+1 so the first circle isnt labelled as '0'

        # radius label

        r = areas_sorted[i][2] # radius in pixels
        calib_r = round(float(r) / float(calibration_ratio), 2) # radius in micrometer length

        frame = cv2.line(frame, (x,y), (x+r, y), (0,0,255), 6)

        frame = cv2.putText(frame, 'r=' + str(calib_r), (x+5, y-15), font, 1, (0, 0, 0), 8, cv2.LINE_AA) # text outline
        frame = cv2.putText(frame, 'r=' + str(calib_r), (x+5, y-15), font, 1, (0, 255, 100), 2, cv2.LINE_AA)

        # circumference, as a measure of curvature (its an opened and straightened out arc length). C = 2pir

        circumference = round(2 * math.pi * calib_r, 2)

        frame = cv2.putText(frame, 'C=' + str(circumference), (x+5, y+35), font, 1, (0, 0, 0), 8, cv2.LINE_AA) # text outline
        frame = cv2.putText(frame, 'C=' + str(circumference), (x+5, y+35), font, 1, (0, 255, 100), 2, cv2.LINE_AA) 







'''
def frame_overlay_select(areas_sorted: list, frame_circle_sel):

    user_ready = False
    selection_input_list = []
    selection_list = []


    while user_ready == False:
        
        #print('The deselected circles will be: ', selection_list)
        
        print('\nPlease enter an integer representing the circle # that you wish to deselect. \nCurrently, the deselected circle(s) entered are: ', selection_input_list, '\nOtherwise, enter 99 to confirm the chosen deselected circles.\n')
        user_input = input()

        if user_input.isnumeric():


            selection_input_list.append(int(user_input))
            if 99 in selection_input_list:
                user_ready = True
                print(user_ready)

        else:
            print('================\nInvalid input. Please enter a single integer value.\n================')
        
        
    if areas_sorted is not None:
        areas_sorted_np = np.uint16(np.around(areas_sorted)) #converts the list to numpy array)

        for i in areas_sorted_np:
            print('i value:', i)
            if i[4] in selection_input_list:
                #print('i value thats detected in the selection list: ', i)
                continue
            
            else:
                for m in areas_sorted:
                    # add the selected circles into a new list for downstream analysis
                    print('list is:', selection_list)
                    print(m)
                    selection_list.append([m]) # by this point, each circle has 5 associated properties in this order: [xpos, ypos, radius, xy area, circle # ranked by area]
                
                #print('I VALUE IS : ', i)
                #print('selection list is: ', selection_list)

                #print('i values that are not in selection list: ', i)
                # note x, y, r = i[0], i[1], i[2]
                cv2.circle(frame_circle_sel, (i[0], i[1]), i[2], (0,0,255), 4) # circumference
                cv2.circle(frame_circle_sel, (i[0], i[1]), 1, (0,0,255), 2)
                
                font = cv2.FONT_HERSHEY_COMPLEX
                
                x = i[0]
                y = i[1]

                frame_circle_sel = cv2.putText(frame_circle_sel, str(i[4]), (x-10, y+10), font, 1, (0, 0, 0), 8, cv2.LINE_AA) # text outline
                frame_circle_sel = cv2.putText(frame_circle_sel, str(i[4]), (x-10, y+10), font, 1, (0, 255, 100), 2, cv2.LINE_AA) # i+1 so the first circle isnt labelled as '0'

        
        #return True # true return will end the 
'''
'''
def show_window(window_name: str, frame, size_ratio):
    resized_frame = cv2.resize(frame, (0,0), fx = size_ratio, fy = size_ratio)
    cv2.imshow(window_name, resized_frame)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)
    cv2.moveWindow(window_name,10,50)
'''