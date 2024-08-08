#Droplet_Detection_Selection_Frame
import cv2 
import numpy as np
import math

RED = "\33[91m"
BLUE = "\33[94m"
GREEN = "\033[32m"
YELLOW = "\033[93m"
PURPLE = '\033[0;35m' 
CYAN = "\033[36m"
LBLUE = "\033[94m"
END = "\033[0m"
BOLD = "\033[1m"
LGREEN = "\033[92m"
LRED = "\033[91m"

def frame_overlay_select(deselection_input_list):

    circle_was_selected = False
    deselection_input_list = deselection_input_list
    user_ready = False

    while circle_was_selected == False:
        
        #print('The deselected circles will be: ', selection_list)
        
        print(f'\n{RED}[PROGRAM] > {END}Please enter an integer representing the circle # that you wish to deselect. \nCurrently, the {YELLOW}deselected circle(s){END} entered are: {YELLOW}{BOLD}', deselection_input_list, f'{END}\nOtherwise, press {YELLOW}[ENTER]{END} to begin analysis of the change in intensity within each circle.\n\n{GREEN}[USER INPUT] > {END}')
        user_input = input()

        if user_input.isnumeric():

            deselection_input_list.append(int(user_input))
            circle_was_selected = True

        elif user_input == 'r' or 'R': # or enter
            circle_was_selected = True
            user_ready = True

        else:
            print(f'{RED}[PROGRAM] > {END}\nInvalid input. Please enter a single integer value at a time.\n')
    
    return deselection_input_list, user_ready

def make_selection_list(areas_sorted: list, deselection_input_list, selection_frame):

    selection_list = []

    if areas_sorted is not None:
        #areas_sorted_np = np.uint16(np.around(areas_sorted)) #converts the list to numpy array)

        for i in areas_sorted:
            #print('i value:', i, type(i))
            if i[4] in deselection_input_list: # is the circle identity a part of the deselection list made by the user?
                print(f'{RED}Circle #', i[4], f' --- Deselection successful!{END}')
                continue
            
            else:

                selection_list.append(i)
                
                #print('sel list:', selection_list)

                #print('i values that are not in selection list: ', i)
                # note x, y, r = i[0], i[1], i[2]
                #cv2.circle(selection_frame, (i[0], i[1]), i[2], (0,0,255), 4) # circumference
                #cv2.circle(selection_frame, (i[0], i[1]), 1, (0,0,255), 2)
                
                #font = cv2.FONT_HERSHEY_COMPLEX
                
                #x = i[0]
                #y = i[1]

                #selection_frame = cv2.putText(selection_frame, str(i[4]), (x-10, y+10), font, 1, (0, 0, 0), 8, cv2.LINE_AA) # text outline
                #selection_frame = cv2.putText(selection_frame, str(i[4]), (x-10, y+10), font, 1, (0, 255, 100), 2, cv2.LINE_AA) # i+1 so the first circle isnt labelled as '0'


    else:
        return(print(f'{RED}[PROGRAM] > {END}Error: The list for areas_sorted is empty!!'))
    
    return selection_list

def selected_circles_on_frame_and_label(selection_list: list, selection_frame, cap1, inner_radius_factor, outer_radius_factor, calibration_ratio):

    calib_r_list = []

    half_width = int(cap1.get(3)) / 2

    font = cv2.FONT_HERSHEY_PLAIN

    for i in selection_list:

        # note x, y, r = i[0], i[1], i[2]

        x = i[0]

        y = i[1]

        r = i[2]

        r_rounded = round(i[2], 0)

        calib_r = round(float(r) / float(calibration_ratio), 2) # radius in micrometer length

        calib_r_list.append(calib_r)

        inner_radius = int(round(r * inner_radius_factor, 0))

        outer_radius = int(round(r * outer_radius_factor, 0))
        

        # Detected Circle
        cv2.circle(selection_frame, (x, y), r, (255,0,29), 6) # circumference

        cv2.circle(selection_frame, (x, y), 1, (255,0,29), 2)
            
        # RINGs
        cv2.circle(selection_frame, (x, y), inner_radius, (107,0,178), 6) # inner ring

        cv2.circle(selection_frame, (x, y), outer_radius, (152,0,255), 2) # outer ring

        # draw the labels
        if x <= half_width:

            selection_frame = cv2.line(selection_frame, (x,y), (x+r_rounded, y), (0, 0, 0), 10, cv2.LINE_AA)

            selection_frame = cv2.putText(selection_frame, '#' + str(i[4]), (x+r_rounded, y+20), font, 4, (0, 204, 255), 20, cv2.LINE_AA) # text outline

            selection_frame = cv2.putText(selection_frame, '#' + str(i[4]), (x+r_rounded, y+20), font, 4, (0, 0, 255), 4, cv2.LINE_AA) # i+1 so the first circle isnt labelled as '0'

        if x > half_width:

            selection_frame = cv2.line(selection_frame, (x,y), (x-r_rounded-15, y), (0, 0, 0), 10, cv2.LINE_AA)

            selection_frame = cv2.putText(selection_frame, '#' + str(i[4]), (x-r_rounded-120, y+20), font, 4, (0, 204, 255), 20, cv2.LINE_AA) # text outline

            selection_frame = cv2.putText(selection_frame, '#' + str(i[4]), (x-r_rounded-120, y+20), font, 4, (0, 0, 255), 4, cv2.LINE_AA) # i+1 so the first circle isnt labelled as '0'



        '''
        selection_frame = cv2.putText(selection_frame, '#' + str(i[4]), (x-70, y+10), font, 1.5, (0, 0, 0), 10, cv2.LINE_AA) # text outline
        selection_frame = cv2.putText(selection_frame, '#' + str(i[4]), (x-70, y+10), font, 1.5, (0, 255, 100), 2, cv2.LINE_AA) # i+1 so the first circle isnt labelled as '0'

        # radius label

        r = i[2] #radius in pixels
        calib_r = round(float(r) / float(calibration_ratio), 2) # radius in micrometer length
        calib_r_list.append(calib_r)

        selection_frame = cv2.line(selection_frame, (x,y), (x+r, y), (0,0,255), 6)

        selection_frame = cv2.putText(selection_frame, 'r=' + str(calib_r), (x+5, y-10), font, 1, (0, 0, 0), 8, cv2.LINE_AA) # text outline
        selection_frame = cv2.putText(selection_frame, 'r=' + str(calib_r), (x+5, y-10), font, 1, (0, 255, 100), 2, cv2.LINE_AA)
        '''
        # circumference, as a measure of curvature (its an opened and straightened out arc length). C = 2pir

        #circumference = round(2 * math.pi * calib_r, 2)

        #selection_frame = cv2.putText(selection_frame, 'C=' + str(circumference), (x+5, y+35), font, 1, (0, 0, 0), 8, cv2.LINE_AA) # text outline
        #selection_frame = cv2.putText(selection_frame, 'C=' + str(circumference), (x+5, y+35), font, 1, (0, 255, 100), 2, cv2.LINE_AA) 

        print(f'{LGREEN}Circle #', i[4], f' --- Selection successful!{END}')
        
    return selection_frame, calib_r_list