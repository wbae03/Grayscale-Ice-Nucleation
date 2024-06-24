#Droplet_Detection_Frame

import cv2 
import numpy as np
import math
import os

RED = "\33[91m"
BLUE = "\33[94m"
GREEN = "\033[32m"
YELLOW = "\033[93m"
PURPLE = '\033[0;35m' 
CYAN = "\033[36m"
LBLUE = "\033[94m"
END = "\033[0m"
BOLD = "\033[1m"

first_pass = False

last_stored_sens_selection = 0

def frame_capture(i: int, cap):
    cap.set(cv2.CAP_PROP_POS_FRAMES, i)

def frame_circles(frame, n):
    global first_pass, last_stored_sens_selection

  

    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # grayscale to remove color noise
    blurFrame = cv2.GaussianBlur(grayFrame, (17, 17), 0) # blur to lower background noise. 2nd p: both values must be odd. Higher = more blur. Default: 17,17
    #value, thresh = cv2.threshold(blurFrame, 200, 255, cv2.THRESH_BINARY_INV) # pixels below 130 become 0, above become 255 (white)

    sens_selection_ready = False

    
    
    user_circle_detection_ready_input = False # to be returned to decide if main loop continues or terminates

    while sens_selection_ready == False:

        print(f'''\n{RED}PROGRAM] > {END}Please select (or re-select) an option for the {YELLOW}circle detection sensitivity{END}. 
Choosing the wrong sensitivity may lead to overwhelming or underwhelming false-positive circles. 
If you are satisfied with the sensitivity, press {YELLOW}[ ENTER ]{END}.

                {CYAN}Sensitivity Option        Use if the Video Footage Contains:{END}
                        {YELLOW}(1){END} ............. High Clarity, Distinct & Perfect Circles
                        {YELLOW}(2){END} ............. Moderate Clarity, Some Background Noise
                        {YELLOW}(3){END} ............. Average Clarity, Minor Distortion
                        {YELLOW}(4){END} ............. Low Clarity, Faded Circles
                        {YELLOW}(5){END} ............. Questionable & Blurry Circles {RED}[EXPERIMENTAL! MAY CRASH COMPUTER!]{END}
                ''')
        
        sens_selection = input(f'\n{GREEN}[USER INPUT] > {END}')

        try: 
            if isinstance(int(sens_selection), int):
                if int(sens_selection) in (1,2,3,4,5):
                    sens_selection_ready = True
                    sens_selection = int(sens_selection)
                    last_stored_sens_selection = sens_selection
                    

                    if first_pass == True:
        
                        cv2.destroyWindow(n)

                    else: 
                        first_pass = True


        
        except:

            if first_pass == True: # or enter

                if sens_selection == '':

                    user_circle_detection_ready_input = True
                    sens_selection_ready = True
                    sens_selection = last_stored_sens_selection

            else:
                print(f'\n{RED}[PROGRAM] > {END}Invalid input. Please enter an integer value from the provided options.')



    if sens_selection == 1:

        circles = cv2.HoughCircles(blurFrame, # documentation: https://docs.opencv.org/4.3.0/d3/de5/tutorial_js_houghcircles.html
                                cv2.HOUGH_GRADIENT, 
                                1.1, # influences whether nearby circles will be merged
                                50, # min distance between two circles' centers
                                param1=42, # sensitivity of circle detection; High = wont find much circles. Default: 42
                                param2=75, # accuracy of circle detection; number of edgepoints to declare there's a circle. High = wont find much circles. Default: 75
                                minRadius=20, # min radius of circles
                                maxRadius=200)  # max radius of circles # note to self: the radii parameters are quite important in selecting correct circles!!
        
        print(f'\n{RED}[PROGRAM] > {END}Detection parameters {YELLOW}(1){END} used by the program.')


    elif sens_selection == 2:

        circles = cv2.HoughCircles(blurFrame, # documentation: https://docs.opencv.org/4.3.0/d3/de5/tutorial_js_houghcircles.html
                                cv2.HOUGH_GRADIENT, 
                                1.1, # influences whether nearby circles will be merged
                                100, # min distance between two circles' centers
                                param1=30, # sensitivity of circle detection; High = wont find much circles. Default: 42
                                param2=50, # accuracy of circle detection; number of edgepoints to declare there's a circle. High = wont find much circles. Default: 75
                                minRadius=20, # min radius of circles
                                maxRadius=200)  # max radius of circles # note to self: the radii parameters are quite important in selecting correct circles!!
        
        print(f'\n{RED}[PROGRAM] > {END}Detection parameters {YELLOW}(2){END} used by the program.')


    elif sens_selection == 3:

            
        circles = cv2.HoughCircles(blurFrame, # documentation: https://docs.opencv.org/4.3.0/d3/de5/tutorial_js_houghcircles.html
                                cv2.HOUGH_GRADIENT, 
                                1.1, # influences whether nearby circles will be merged
                                100, # min distance between two circles
                                param1=20, # sensitivity of circle detection; High = wont find much circles
                                param2=35, # accuracy of circle detection; number of edgepoints to declare there's a circle. High = wont find much circles
                                minRadius=20, # min radius of circles
                                maxRadius=200)  # max radius of circles 
        
        print(f'\n{RED}[PROGRAM] > {END}Detection parameters {YELLOW}(3){END} used by the program.')


    elif sens_selection == 4:

        circles = cv2.HoughCircles(blurFrame, # documentation: https://docs.opencv.org/4.3.0/d3/de5/tutorial_js_houghcircles.html
                                cv2.HOUGH_GRADIENT, 
                                1.1, # influences whether nearby circles will be merged
                                100, # min distance between two circles
                                param1=12, # sensitivity of circle detection; High = wont find much circles
                                param2=25, # accuracy of circle detection; number of edgepoints to declare there's a circle. High = wont find much circles
                                minRadius=20, # min radius of circles
                                maxRadius=200)  # max radius of circles 
        
        print(f'\n{RED}[PROGRAM] > {END}Detection parameters {YELLOW}(4){END} used by the program.')


    elif sens_selection == 5:

        circles = cv2.HoughCircles(blurFrame, # documentation: https://docs.opencv.org/4.3.0/d3/de5/tutorial_js_houghcircles.html
                                cv2.HOUGH_GRADIENT, 
                                1.1, # influences whether nearby circles will be merged
                                150, # min distance between two circles
                                param1=10, # sensitivity of circle detection; High = wont find much circles
                                param2=20, # accuracy of circle detection; number of edgepoints to declare there's a circle. High = wont find much circles
                                minRadius=10, # min radius of circles
                                maxRadius=200)  # max radius of circles    
        
        print(f'\n{RED}[PROGRAM] > {END}Detection parameters {YELLOW}(5){END} used by the program.')    
                
    
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
            
                print(f'\n {RED}[PROGRAM] > {END}(Above RuntimeWarning explanation) Detected an out-of-bounds circle (y-pos: ', i[0], 'x-pos: ', i[1], 'pixel radius: ', i[2],f'). {YELLOW}Deselecting the circle...{END}')
    
    else:
        
        user_circle_detection_ready_input = False # to be returned to decide if main loop continues or terminates


    ### print('\nDetected circles [x-pos, y-pos, radius]: \n', circles) # to see the numpyarray of the circles generated in this frame. [y, x, r]
    return circles, user_circle_detection_ready_input

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

        #circumference = round(2 * math.pi * calib_r, 2)

        #frame = cv2.putText(frame, 'C=' + str(circumference), (x+5, y+35), font, 1, (0, 0, 0), 8, cv2.LINE_AA) # text outline
        #frame = cv2.putText(frame, 'C=' + str(circumference), (x+5, y+35), font, 1, (0, 255, 100), 2, cv2.LINE_AA) 





