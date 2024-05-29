#Droplet_Detection_Grapher

import matplotlib.pyplot as plt
import numpy as np

def get_intensity_axes(video_BGR_data):
    
    video_BGR_data = np.int32(np.around(video_BGR_data)) #note: uint32 = unsignt int32 = signed!!
    
    intensity_axes = []

    for i in range(len(video_BGR_data[0])): # gets the amount of circles analyzed based on 'video_BGR_data'

        x = video_BGR_data[:,i] # creates a separate list, within a overall list, containing intensity values across frames for each circle. 
        intensity_axes.append(x)

    
    #print('intensity axes: ', intensity_axes)
    #print(' first circle y axis test: ', intensity_axes[0], 'second circley axis: ', intensity_axes[1])
    return intensity_axes

def plot_intensity_vs_frames(intensity_axes, frame_axes, axis, frame_count):

    #plt.figure()
    
    for i in range(len(intensity_axes)):
        #plt.figure()
        #plt.plot(frame_x, intensity_axes[i], label = 'Circle #' + str(i+1))
        axis[0, 0].plot(frame_axes, intensity_axes[i], label = 'Circle #' + str(i+1))
    
    
    axis[0, 0].set_title('Grayscale Intensity Every ' + str(frame_count) + ' Frames')
    axis[0, 0].set_xlabel('Frames')
    axis[0, 0].set_ylabel('Grayscale Intensity')
    axis[0, 0].legend(fontsize='x-small')

    #plt.xlabel('Frames')
    #plt.ylabel('Grayscale Intensity (0 = darkest black)')
    #plt.title('Intensity vs Analyzed Frames')
    #plt.legend()

    #plt.show()
    

    return

def get_intensity_difference_axes(intensity_axes):

    intensity_difference_axes = []




    for i in range(len(intensity_axes)):
       
        hold_differences = []

        for x in range(len(intensity_axes[i])):
           
            try:
               
               diff = intensity_axes[i][x+1] - intensity_axes[i][x]
               hold_differences.append(diff)

            except:
               
               print('ah')
      
        intensity_difference_axes.append(hold_differences)

    print(len(intensity_difference_axes[0]))
    return intensity_difference_axes

    

def plot_dintensity_vs_dframes(intensity_difference_axes, frame_axes, axis, frame_count): # intensity axes should look like [[circle 1 data],[circle 2],[etc...]]

    frame_x = frame_axes[0: -1] # get entire list except for the last element (must match amount of elements in frame axis to agree with difference axis)

    #plt.figure()
    
    for i in range(len(intensity_difference_axes)):

        #print(len(intensity_difference_axes))
        

        #plt.plot(frame_x, intensity_difference_axes[i], label = 'Circle #' + str(i+1))
        axis[1, 0].plot(frame_x, intensity_difference_axes[i], label = 'Circle #' + str(i+1))
    
    axis[1, 0].set_title('Grayscale Intensity Difference Every ' + str(frame_count) + ' Frames')
    axis[1, 0].set_xlabel('Frames')
    axis[1, 0].set_ylabel('Grayscale Intensity Difference')
    axis[1, 0].legend(fontsize='x-small')

    '''
    plt.xlabel('Frames')
    plt.ylabel('d(Grayscale Intensity)/d(Frame)')
    plt.title('Differential Intensities Over Frames')
    plt.legend()
    '''
    
    #plt.show() # show all the figures
    
    return 


def plot_intensity_vs_seconds(intensity_axes, video_seconds, axis):

    #plt.figure()
    
    for i in range(len(intensity_axes)):
        #plt.figure()
        #plt.plot(frame_x, intensity_axes[i], label = 'Circle #' + str(i+1))
        axis[0, 1].plot(video_seconds, intensity_axes[i], label = 'Circle #' + str(i+1))
    
    
    axis[0, 1].set_title('Grayscale Intensity Every ' + str(video_seconds[1]) + ' Seconds')
    axis[0, 1].set_xlabel('Seconds')
    axis[0, 1].set_ylabel('Grayscale Intensity')
    axis[0, 1].legend(fontsize='x-small')

    #plt.xlabel('Frames')
    #plt.ylabel('Grayscale Intensity (0 = darkest black)')
    #plt.title('Intensity vs Analyzed Frames')
    #plt.legend()

    #plt.show()
    

    return

def plot_dintensity_vs_seconds(intensity_difference_axes, video_seconds, axis): # intensity axes should look like [[circle 1 data],[circle 2],[etc...]]

    seconds_x = video_seconds[0: -1] # get entire list except for the last element (must match amount of elements in frame axis to agree with difference axis)

    #print('len seconds', len(seconds_x), 'len int diff', len(intensity_difference_axes))
    #plt.figure()
    
    for i in range(len(intensity_difference_axes)):

        #print(len(intensity_difference_axes))
        

        #plt.plot(frame_x, intensity_difference_axes[i], label = 'Circle #' + str(i+1))
        axis[1, 1].plot(seconds_x, intensity_difference_axes[i], label = 'Circle #' + str(i+1))
    
    axis[1, 1].set_title('Grayscale Intensity Difference Every ' + str(video_seconds[1]) + ' Seconds')
    axis[1, 1].set_xlabel('Seconds')
    axis[1, 1].set_ylabel('Grayscale Intensity Difference')
    axis[1, 1].legend(fontsize='x-small')

    '''
    plt.xlabel('Frames')
    plt.ylabel('d(Grayscale Intensity)/d(Frame)')
    plt.title('Differential Intensities Over Frames')
    plt.legend()
    '''
    
    #plt.show() # show all the figures
    
    return 