#Droplet_Detection_Grapher

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator

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

    #print('mark')


    for i in range(len(intensity_axes)):
       
        hold_differences = []

        for x in range(len(intensity_axes[i])):
           
            try:
               
               diff = intensity_axes[i][x+1] - intensity_axes[i][x]
               hold_differences.append(diff)

            except:
               
               y = 1 # throwaway variable. There will always be one exception, as the last value does not have a subsequent value to be subtracted from.
      
        intensity_difference_axes.append(hold_differences)

    #print(len(intensity_difference_axes[0]), 'content:', intensity_difference_axes)
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
        axis[0, 0].plot(video_seconds, intensity_axes[i], label = 'Circle #' + str(i+1))
    
    
    axis[0, 0].set_title('Grayscale Intensity Every ' + str(video_seconds[1]) + ' Seconds')
    axis[0, 0].set_xlabel('Seconds')
    axis[0, 0].set_ylabel('Grayscale Intensity')
    axis[0, 0].legend(fontsize='x-small', loc='lower left')

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
    print('working intensity diff', intensity_difference_axes)

    for i in range(len(intensity_difference_axes)):

        #print(len(intensity_difference_axes))
        

        #plt.plot(frame_x, intensity_difference_axes[i], label = 'Circle #' + str(i+1))
        axis[0, 1].plot(seconds_x, intensity_difference_axes[i], label = 'Circle #' + str(i+1))
    
    axis[0, 1].set_title('Grayscale Intensity Difference Every ' + str(video_seconds[1]) + ' Seconds')
    axis[0, 1].set_xlabel('Seconds')
    axis[0, 1].set_ylabel('Grayscale Intensity Difference')
    axis[0, 1].legend(fontsize='x-small', loc='lower left')

    
    #plt.xlabel('Frames')
    #plt.ylabel('d(Grayscale Intensity)/d(Frame)')
    #plt.title('Differential Intensities Over Frames')
    #plt.legend()
    
    
    #plt.show() # show all the figures
    
    return 

def get_temperature_axes(video_seconds, temperature_time, temperature):

    temperature_axes = []
    temperature_time_axes = []

    #print('vid secs', video_seconds, 'temp time', temperature_time)


    int_video_seconds = [round(x,0) for x in video_seconds] # round values to be integers.

    for i in range(len(temperature_time)):
        
        #print('temp df index', temperature_df[2][i], 'video secs', video_seconds)

        if temperature_time[i] in int_video_seconds:

            temperature_axes.append(float(temperature[i])) # add the corresponding temperature data to the axes to be plotted
            temperature_time_axes.append(temperature_time[i])
            #print('temp this', temperature[i], 'temp time this', temperature_time[i], 'vid time this', video_seconds)

    #print('temp axes final', temperature_axes)

    return temperature_axes, temperature_time_axes


def get_correct_temperature_axes(intensity_axes, temperature_axes):

    if len(intensity_axes[0]) < len(temperature_axes): # if the video ran longer than the temperature probe...


        #print('int axes smaller than temp axes!!:', intensity_axes[0], 'adfssadf', temperature_axes)
        temperature_axes = temperature_axes[0 : len(intensity_axes[0])]


    #print('numb 1', temperature_axes)

    return temperature_axes

def get_correct_intensity_axes(intensity_axes, temperature_axes):

    intensity_axes_for_temperature = []

    if len(intensity_axes[0]) > len(temperature_axes): # if the video duration is shorter than the temperature probe data measurement duration...


        #print('int axes larger than temp axes!!:', intensity_axes[0], 'adfssadf', temperature_axes)

        for i in range(len(intensity_axes)):

            hold_intensity_axes_for_temperature = intensity_axes[i][0 : len(temperature_axes)]
            intensity_axes_for_temperature.append(hold_intensity_axes_for_temperature)

    #print('numb 2', hold_intensity_axes_for_temperature)

    return intensity_axes_for_temperature

    



def plot_intensity_vs_temperature(intensity_axes, temperature_axes, axis):
    
    #print('temp axessss:', temperature_axes, 'intensity axessss:', intensity_axes)

    for i in range(len(intensity_axes)):
        #print('temp axessss66666:', temperature_axes, 'intensity axessss66666:', intensity_axes[i])

        #plt.figure()
        #plt.plot(frame_x, intensity_axes[i], label = 'Circle #' + str(i+1))
        axis[1, 0].plot(temperature_axes, intensity_axes[i], label = 'Circle #' + str(i+1))
    
    
    axis[1, 0].set_title('Grayscale Intensity vs Temperature (Celsius)')
    axis[1, 0].set_xlabel('Temperature (C)')
    axis[1, 0].set_ylabel('Grayscale Intensity')
    axis[1, 0].legend(fontsize='x-small', loc='lower left')

    #plt.xlabel('Frames')
    #plt.ylabel('Grayscale Intensity (0 = darkest black)')
    #plt.title('Intensity vs Analyzed Frames')
    #plt.legend()

    #plt.show()
    

    return

#def get_dintensity_matched_to_temperature(intensity_difference_axes, video_seconds, temperature_df):


#im so dumb. literally, just convert the video_seconds axis to a temperature axes.... 

def plot_time_and_dintensity_heatmap(dintensity_axes, video_seconds, temperature_axes, temperature_time_axes, axis):

    # Create heatmap using imshow
    heatmap = axis[0, 2].imshow(dintensity_axes, cmap='jet', aspect='auto', interpolation='none')
    
    # Add colorbar to the heatmap
    cbar = plt.colorbar(heatmap, ax=axis[0, 2])
    cbar.set_label('Grayscale Intensity Difference')
    
    # Generate labels for y-ticks
    circle_label = ['Circle ' + str(i+1) for i in range(len(dintensity_axes))]
    
    # Set y-ticks and labels
    axis[0, 2].set_yticks(range(len(dintensity_axes)))
    axis[0, 2].set_yticklabels(circle_label, fontsize=10)
    
    # Set x-ticks to every 10 units and labels
    #axis[0, 2].xaxis.set_major_locator(MultipleLocator(10))
    axis[0, 2].set_xticks(range(0, len(video_seconds), 10))  # Ensure ticks every 50 units
    axis[0, 2].set_xticklabels(video_seconds[::10], fontsize=7, rotation=45, ha='right')
    # the resulting ticks will be the time of analysis * the step interval defined above

    # Set titles and labels
    axis[0, 2].set_title('')
    axis[0, 2].set_xlabel('Time (seconds)')
    axis[0, 2].set_ylabel('Circles')

    # create a second x-axis above the plot using the twin function which creates an x axis with the same y axis
    ax2 = axis[0, 2].twiny()

    # IF TEMPERATURE DATA EXCEEDS LENGTH OF VIDEO THIS WILL ALLOW GRAPHING:
    #print('before manip,', len(temperature_axes), 'vid secs', len(video_seconds))
    #temperature = temperature[:len(video_seconds)] # get all elements before the length of elements in video secs
    ax2.set_xticks(temperature_time_axes[::20]) # only use every 20th element
    #print('hffjfgghkghg temp lngth', len(temperature_axes))
    ax2.set_xticklabels(temperature_axes[::20], fontsize=10, rotation=45, ha='left')
    ax2.set_xlabel('Temperature (C)', fontsize=12) 

    axis[0,2].spines[:].set_visible(False)

    return