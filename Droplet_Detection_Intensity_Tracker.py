#Droplet_Detection_Intensity_Tracker

import cv2 
import numpy as np
import pandas as pd


def change_in_intensityx(video_BGR_data):

    video_BGR_data = np.uint16(np.around(video_BGR_data)) # converts the list of frames, each frame containing the intensity avg for each circle, into an array
    # arrays make analysis much easier since we can now make use of columns in the array to access, for instance, all values for the first circle at once.

    intensity_differences = []

    for f in range(len(video_BGR_data[0])):

        single_circle_intensities = video_BGR_data[:,f] # extract the column of intensity data, which represents each circle

        intensity_differences_of_a_circle = []

        for i in range(len(single_circle_intensities)):
                
            try:

                diff = (single_circle_intensities.astype(int)[i+1] - single_circle_intensities.astype(int)[i]) / 1 # change in intensity divided by change in frame (1 frame between intensity)]

                if diff < 0:
                    diff = diff * -1
                
                #print('first number', single_circle_intensities.astype(int)[i+1], 'second number', )
                intensity_differences_of_a_circle.append(diff)

            except:

                print('\nCircle ', f, 'completed differential analysis of grayscale intensities between frames.')


        intensity_differences.append(intensity_differences_of_a_circle)
    intensity_differences = np.uint32(np.around(intensity_differences))


    single_intensity_chunks = [single_circle_intensities[x:x+4] for x in range(0, len(single_circle_intensities), 4)]
    export_single_circle_intensities = pd.DataFrame(single_intensity_chunks)
    export_single_circle_intensities.to_csv('Saved_data/' + 'single_chunks' + '.csv')


    print('Grayscale intensity differences of each circle per analyzed frame: \n', intensity_differences)

    return intensity_differences

'''
def load_screen(frame, cap):
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    frame_id = int(cap.get(cv2.CAP_PROP_POS_FRAMES)) # get the current frame ID

    progress_percent = str(frame_id / total_frames * 100)

    print('frame id', frame_id)
    print('frame total', total_frames)

    font = cv2.FONT_HERSHEY_COMPLEX

    frame = cv2.putText(frame, progress_percent,
                        (10, 90),
                        font, 2,
                        (0, 0, 0),
                        5,)
    
    frame = cv2.putText(frame, progress_percent,
                        (10, 90),
                        font, 2,
                        (255, 255, 255),
                        1)

    return frame
'''
'''
def BGR_sum(selection_list, video):
        #if circles is not None:
        #selection_list = np.uint16(np.around(circles)) #converts the list to numpy array)

        #chosen = None
        for i in selection_list:
            #x, y, r = i[0], i[1], i[2]
            cv2.circle(video, (i[0], i[1]), i[2], (0,255,0), 2) # circumference
            cv2.circle(video, (i[0], i[1]), 1, (0,0,255), 2) #center point of circle

            # applying masking to measure BGR
            #x, y, r = selection_list.astype(np.int32)[0][0][0], selection_list.astype(np.int32)[0][0][1], selection_list.astype(np.int32)[0][0][2]
            print(selection_list)
            x, y, r = selection_list[0][0], selection_list[0][1], selection_list[0][2]


            #.astype(np.int32)[i] #0 is indexing the first circle entry
            #print(circles[0].astype(np.int32)) #np.int32 calls for the 1st bracket within [[[x, y, r], [x2,y2,r2]]]
            #https://www.youtube.com/watch?v=1p1lUyLGB2E&ab_channel=CodesofInterest
            #https://stackoverflow.com/questions/62944745/how-to-find-the-average-rgb-value-of-a-circle-in-an-image-with-python

            #print(x,y,r)

            roi = video[y-r: y+r, x-r: x+r] # height, width

            width, height = roi.shape[:2] #excluding parameter 2... so only 0,1 (height/width)
            mask = np.zeros((width, height, 3), roi.dtype) # make new array with width and height and colour space/channels = 3 for BGR or RGB
            cv2.circle(mask, (int(width / 2), int(height / 2)), r, (255, 255, 255), -1)

            dst = cv2.bitwise_and(roi, mask) #form the mask i think?

            frame_BGR_data = []
            for i in range(3):
                channel = dst[:, :, i]
                indices = np.where(channel != 0)[0]
                color = np.mean(channel[indices]) #access the ith position in channel for RGB or BGR... average B/G/R value of all the pixels in the circle's area??
                frame_BGR_data.append(int(color))
                
        video_BGR_data.append(round(sum(frame_BGR_data)/len(frame_BGR_data))) #I used calculator to confirm; this is the average of BGR... presumably for each circle!
        print(video_BGR_data)  
        '''