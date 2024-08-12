#Droplet_Detection_Frame

import cv2 
import numpy as np
import math
import os
import csv
import matplotlib.pyplot as plt
import Droplet_Detection_Utility as DDU

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

def choose_blur(x: int, frame):

    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # grayscale to remove color noise

    # Blur Type aka 2D Convolution (Image Filtering); Select one of the filters below for circle detection.
    gaussianFrame = cv2.GaussianBlur(grayFrame, (17, 17), 0) # blur to lower background noise. 2nd p: both values must be odd. Higher = more blur. Default: 17,17

    averagingFrame = cv2.blur(grayFrame, (5, 5)) # blur to lower background noise. 2nd p: both values must be odd. Higher = more blur. Default: 17,17

    medianFrame = cv2.medianBlur(grayFrame, 5) # blur to lower background noise. 2nd p: both values must be odd. Higher = more blur. Default: 17,17

    bilateralFrame = cv2.bilateralFilter(grayFrame, 9, 75, 75) # blur to lower background noise. 2nd p: both values must be odd. Higher = more blur. Default: 17,17
    
    if x == 1:

        blur = grayFrame

        name = 'cv2.COLOR_BGR2GRAY Grayframe [1]'

    elif x == 2: 

        blur = gaussianFrame

        name = 'Gaussian Blur Grayframe [2]'

    elif x == 3:

        blur = averagingFrame

        name = 'Averaging Blur Grayframe [3]'

    elif x == 4:

        blur = medianFrame

        name = 'Median Blur Grayframe [4]'

    elif x == 5:

        blur = bilateralFrame

        name = 'Bilateral Filtering Grayframe [5]'

    return blur, name

def frame_circles(frame, n, name, save_path, folder):

    global first_pass, last_stored_sens_selection

    sens_selection_ready = False

    user_circle_detection_ready_input = False # to be returned to decide if main loop continues or terminates

    while sens_selection_ready == False:

        print(f'''\n{RED}PROGRAM] > {END}Please select (or re-select) an option for the {YELLOW}circle detection sensitivity{END}. 
Choosing the wrong sensitivity may lead to overwhelming or underwhelming false-positive circles. 
If you are satisfied with the sensitivity, press {YELLOW}[ ENTER ]{END}.

                {CYAN}Sensitivity Option        Use if the Video Footage Contains:{END}
                        {YELLOW}(1){END} ............. [BLURFRAME] High Clarity, Distinct Circles
                        {YELLOW}(2){END} ............. [BLURFRAME] Moderate Clarity
                        {YELLOW}(3){END} ............. [BLURFRAME] Average Clarity
                        {YELLOW}(4){END} ............. [BLURFRAME] Low Clarity
                        {YELLOW}(5){END} ............. [GRAYFRAME] High Clarity
                        {YELLOW}(6){END} ............. [GRAYFRAME] Average Clarity
                        {YELLOW}(7){END} ............. [GRAYFRAME] Low Clarity

                        * BLURFRAME blurs the input video, reducing the noise of shapes to give more accurate circle detection.
                        * If BLURFRAME is not giving the best results, try using GRAYFRAME which only grayscales the video.

                ''')
        
        sens_selection = input(f'\n{GREEN}[USER INPUT] > {END}')

        try:
                
            with open(os.path.join(save_path, folder, '_GIN_Properties.txt')) as f:
                    
                reader = csv.reader(f, delimiter=',')

                rows = list(reader)

                # Ensure there are enough rows before accessing
                size_ratio = rows[0][1].strip()

                inner_radius_factor = float(rows[2][1].strip())

                outer_radius_factor = float(rows[4][1].strip())

                hough1 = [float(rows[10][1].strip()), float(rows[10][2].strip()), float(rows[10][3].strip()), float(rows[10][4].strip()), int(rows[10][5].strip()), int(rows[10][6].strip()), int(rows[10][7].strip())]

                hough2 = [float(rows[12][1].strip()), float(rows[12][2].strip()), float(rows[12][3].strip()), float(rows[12][4].strip()), int(rows[12][5].strip()), int(rows[12][6].strip()), int(rows[12][7].strip())]

                hough3 = [float(rows[14][1].strip()), float(rows[14][2].strip()), float(rows[14][3].strip()), float(rows[14][4].strip()), int(rows[14][5].strip()), int(rows[14][6].strip()), int(rows[14][7].strip())]

                hough4 = [float(rows[16][1].strip()), float(rows[16][2].strip()), float(rows[16][3].strip()), float(rows[16][4].strip()), int(rows[16][5].strip()), int(rows[16][6].strip()), int(rows[16][7].strip())]

                hough5 = [float(rows[18][1].strip()), float(rows[18][2].strip()), float(rows[18][3].strip()), float(rows[18][4].strip()), int(rows[18][5].strip()), int(rows[18][6].strip()), int(rows[18][7].strip())]

                hough6 = [float(rows[20][1].strip()), float(rows[20][2].strip()), float(rows[20][3].strip()), float(rows[20][4].strip()), int(rows[20][5].strip()), int(rows[20][6].strip()), int(rows[20][7].strip())]

                hough7 = [float(rows[22][1].strip()), float(rows[22][2].strip()), float(rows[22][3].strip()), float(rows[22][4].strip()), int(rows[22][5].strip()), int(rows[22][6].strip()), int(rows[22][7].strip())]

        except FileNotFoundError: 

            print("No '_GIN_PROPERTIES.txt' file exists. Please obtain the file by following the README.txt and downloading from Github.")

        try: 
            if isinstance(int(sens_selection), int):
                if int(sens_selection) in (1,2,3,4,5,6,7):
                    sens_selection_ready = True
                    sens_selection = int(sens_selection)
                    last_stored_sens_selection = sens_selection

                    if first_pass == True:
        
                        cv2.destroyWindow(n)

                        cv2.destroyWindow(name)

                    else: 
                        first_pass = True
        
                    n = f'WINDOW 1 /// DETECTED CIRCLES /// PARAMETER OPTION #{sens_selection}'

        except:

            if first_pass == True: # or enter

                if sens_selection == '':

                    user_circle_detection_ready_input = True
                    sens_selection_ready = True
                    sens_selection = last_stored_sens_selection

            else:
                print(f'\n{RED}[PROGRAM] > {END}Invalid input. Please enter an integer value from the provided options.')

    # obtain the blur filter based on the input in the _GIN_PROPERTIES.txt

    if sens_selection == 1:

        blur, name = choose_blur(hough1[6], frame)

        circles = cv2.HoughCircles(blur, # documentation: https://docs.opencv.org/4.3.0/d3/de5/tutorial_js_houghcircles.html
                                cv2.HOUGH_GRADIENT, 
                                hough1[0], # influences whether nearby circles will be merged
                                hough1[1], # min distance between two circles' centers
                                param1=hough1[2], # sensitivity of circle detection; High = wont find much circles. Default: 42
                                param2=hough1[3], # accuracy of circle detection; number of edgepoints to declare there's a circle. High = wont find much circles. Default: 75
                                minRadius=hough1[4], # min radius of circles
                                maxRadius=hough1[5])  # max radius of circles # note to self: the radii parameters are quite important in selecting correct circles!!

        print(f'\n{RED}[PROGRAM] > {END}Detection parameters {YELLOW}(1){END} used by the program.')

    elif sens_selection == 2:

        blur, name = choose_blur(hough2[6], frame)

        circles = cv2.HoughCircles(blur, # documentation: https://docs.opencv.org/4.3.0/d3/de5/tutorial_js_houghcircles.html
                                cv2.HOUGH_GRADIENT, 
                                hough2[0], # influences whether nearby circles will be merged
                                hough2[1], # min distance between two circles' centers
                                param1=hough2[2], # sensitivity of circle detection; High = wont find much circles. Default: 42
                                param2=hough2[3], # accuracy of circle detection; number of edgepoints to declare there's a circle. High = wont find much circles. Default: 75
                                minRadius=hough2[4], # min radius of circles
                                maxRadius=hough2[5])  # max radius of circles # note to self: the radii parameters are quite important in selecting correct circles!!

        print(f'\n{RED}[PROGRAM] > {END}Detection parameters {YELLOW}(2){END} used by the program.')


    elif sens_selection == 3:

        blur, name = choose_blur(hough3[6], frame)
            
        circles = cv2.HoughCircles(blur, # documentation: https://docs.opencv.org/4.3.0/d3/de5/tutorial_js_houghcircles.html
                                cv2.HOUGH_GRADIENT, 
                                hough3[0], # influences whether nearby circles will be merged
                                hough3[1], # min distance between two circles' centers
                                param1=hough3[2], # sensitivity of circle detection; High = wont find much circles. Default: 42
                                param2=hough3[3], # accuracy of circle detection; number of edgepoints to declare there's a circle. High = wont find much circles. Default: 75
                                minRadius=hough3[4], # min radius of circles
                                maxRadius=hough3[5])  # max radius of circles # note to self: the radii parameters are quite important in selecting correct circles!!
        
        print(f'\n{RED}[PROGRAM] > {END}Detection parameters {YELLOW}(3){END} used by the program.')


    elif sens_selection == 4:

        blur, name = choose_blur(hough4[6], frame)

        circles = cv2.HoughCircles(blur, # documentation: https://docs.opencv.org/4.3.0/d3/de5/tutorial_js_houghcircles.html
                                cv2.HOUGH_GRADIENT, 
                                hough4[0], # influences whether nearby circles will be merged
                                hough4[1], # min distance between two circles' centers
                                param1=hough4[2], # sensitivity of circle detection; High = wont find much circles. Default: 42
                                param2=hough4[3], # accuracy of circle detection; number of edgepoints to declare there's a circle. High = wont find much circles. Default: 75
                                minRadius=hough4[4], # min radius of circles
                                maxRadius=hough4[5])  # max radius of circles # note to self: the radii parameters are quite important in selecting correct circles!!
        
        print(f'\n{RED}[PROGRAM] > {END}Detection parameters {YELLOW}(4){END} used by the program.')


    elif sens_selection == 5:

        blur, name = choose_blur(hough5[6], frame)

        circles = cv2.HoughCircles(blur, # documentation: https://docs.opencv.org/4.3.0/d3/de5/tutorial_js_houghcircles.html
                                cv2.HOUGH_GRADIENT, 
                                hough5[0], # influences whether nearby circles will be merged
                                hough5[1], # min distance between two circles' centers
                                param1=hough5[2], # sensitivity of circle detection; High = wont find much circles. Default: 42
                                param2=hough5[3], # accuracy of circle detection; number of edgepoints to declare there's a circle. High = wont find much circles. Default: 75
                                minRadius=hough5[4], # min radius of circles
                                maxRadius=hough5[5])  # max radius of circles # note to self: the radii parameters are quite important in selecting correct circles!!
        
        print(f'\n{RED}[PROGRAM] > {END}Detection parameters {YELLOW}(5){END} used by the program.')    
                
    elif sens_selection == 6:

        blur, name = choose_blur(hough6[6], frame)

        circles = cv2.HoughCircles(blur, # documentation: https://docs.opencv.org/4.3.0/d3/de5/tutorial_js_houghcircles.html
                                cv2.HOUGH_GRADIENT, 
                                hough6[0], # influences whether nearby circles will be merged
                                hough6[1], # min distance between two circles' centers
                                param1=hough6[2], # sensitivity of circle detection; High = wont find much circles. Default: 42
                                param2=hough6[3], # accuracy of circle detection; number of edgepoints to declare there's a circle. High = wont find much circles. Default: 75
                                minRadius=hough6[4], # min radius of circles
                                maxRadius=hough6[5])  # max radius of circles # note to self: the radii parameters are quite important in selecting correct circles!!
        
        print(f'\n{RED}[PROGRAM] > {END}Detection parameters {YELLOW}(6){END} used by the program.') 

    elif sens_selection == 7:

        blur, name = choose_blur(hough7[6], frame)

        circles = cv2.HoughCircles(blur, # documentation: https://docs.opencv.org/4.3.0/d3/de5/tutorial_js_houghcircles.html
                                cv2.HOUGH_GRADIENT, 
                                hough7[0], # influences whether nearby circles will be merged
                                hough7[1], # min distance between two circles' centers
                                param1=hough7[2], # sensitivity of circle detection; High = wont find much circles. Default: 42
                                param2=hough7[3], # accuracy of circle detection; number of edgepoints to declare there's a circle. High = wont find much circles. Default: 75
                                minRadius=hough7[4], # min radius of circles
                                maxRadius=hough7[5])  # max radius of circles # note to self: the radii parameters are quite important in selecting correct circles!!
        
        print(f'\n{RED}[PROGRAM] > {END}Detection parameters {YELLOW}(7){END} used by the program.') 

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

            # Set the values for the inner and outer radius for analysis. The ROI will be the ring formed by the 2 circles. 
            inner_radius = int(round(i[2] * inner_radius_factor, 0))

            outer_radius = int(round(i[2] * outer_radius_factor, 0))

            # when an out of bounds circle is generated, usually because the radius ends up generating a circle out of the screen, an overflow occurs in the scalar subtraction
            # This results in a really big positive number. 
            # Thus, screen detected circles for absurd radii

            if above < 20000 and below < 20000 and left < 20000 and right < 20000:

                # Detected Circle
                cv2.circle(frame, (i[0], i[1]), i[2], (255,0,29), 6) # circumference

                cv2.circle(frame, (i[0], i[1]), 1, (255,0,29), 2) # center point

                # RINGs
                cv2.circle(frame, (i[0], i[1]), inner_radius, (107,0,178), 6) # inner ring

                cv2.circle(frame, (i[0], i[1]), outer_radius, (152,0,255), 2) # outer ring

            else:
            
                print(f'\n {RED}[PROGRAM] > {END}(Above RuntimeWarning explanation) Detected an out-of-bounds circle (y-pos: ', i[0], 'x-pos: ', i[1], 'pixel radius: ', i[2],f'). {YELLOW}Deselecting the circle...{END}')
    
    else:
        
        user_circle_detection_ready_input = False # to be returned to decide if main loop continues or terminates

    ### print('\nDetected circles [x-pos, y-pos, radius]: \n', circles) # to see the numpyarray of the circles generated in this frame. [y, x, r]
    return n, circles, user_circle_detection_ready_input, blur, name, size_ratio

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

def frame_overlay_label(areas_sorted: list, frame, cap, calibration_ratio):

    half_width = int(cap.get(3)) / 2
    
    #half_height = int(cap.get(4)) / 2

    font = cv2.FONT_HERSHEY_PLAIN

    for i in range(len(areas_sorted)):
          
        x = areas_sorted[i][0]

        y = areas_sorted[i][1]

        r = round(areas_sorted[i][2], 0)

        circle_number = i+1

        # by this point, each circle has 5 associated properties in this order: [xpos, ypos, radius, xy area, circle # ranked by area]
        areas_sorted[i].append(circle_number)

        if x <= half_width:

            frame = cv2.line(frame, (x,y), (x+r, y), (0, 0, 0), 10, cv2.LINE_AA)

            frame = cv2.putText(frame, '#' + str(i+1), (x+r, y+20), font, 4, (0, 204, 255), 20, cv2.LINE_AA) # text outline

            frame = cv2.putText(frame, '#' + str(i+1), (x+r, y+20), font, 4, (0, 0, 255), 4, cv2.LINE_AA) # i+1 so the first circle isnt labelled as '0'

        if x > half_width:

            frame = cv2.line(frame, (x,y), (x-r-15, y), (0, 0, 0), 10, cv2.LINE_AA)

            frame = cv2.putText(frame, '#' + str(i+1), (x-r-120, y+20), font, 4, (0, 204, 255), 20, cv2.LINE_AA) # text outline

            frame = cv2.putText(frame, '#' + str(i+1), (x-r-120, y+20), font, 4, (0, 0, 255), 4, cv2.LINE_AA) # i+1 so the first circle isnt labelled as '0'

        # Radius Label
        #r = areas_sorted[i][2] # radius in pixels

        #calib_r = round(float(r) / float(calibration_ratio), 2) # radius in micrometer length

        #frame = cv2.line(frame, (x,y), (x+r, y), (0,0,255), 6)

        #frame = cv2.putText(frame, 'r=' + str(calib_r), (x+5, y-15), font, 1, (0, 0, 0), 8, cv2.LINE_AA) # text outline

        #frame = cv2.putText(frame, 'r=' + str(calib_r), (x+5, y-15), font, 1, (0, 255, 100), 2, cv2.LINE_AA)

        # Circumference, as a measure of curvature (its an opened and straightened out arc length). C = 2pir

        #circumference = round(2 * math.pi * calib_r, 2)

        #frame = cv2.putText(frame, 'C=' + str(circumference), (x+5, y+35), font, 1, (0, 0, 0), 8, cv2.LINE_AA) # text outline
        #frame = cv2.putText(frame, 'C=' + str(circumference), (x+5, y+35), font, 1, (0, 255, 100), 2, cv2.LINE_AA) 





