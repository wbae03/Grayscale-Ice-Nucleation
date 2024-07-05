#Droplet_Detection_Grapher

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import MultipleLocator

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

    ax = axis[0,0]
    
    for i in range(len(intensity_axes)):
        #plt.figure()
        #plt.plot(frame_x, intensity_axes[i], label = 'Circle #' + str(i+1))
        ax.plot(frame_axes, intensity_axes[i], label = 'Circle #' + str(i+1))
    
    
    ax.set_title('Grayscale Intensity Every ' + str(frame_count) + ' Frames')
    ax.set_xlabel('Frames')
    ax.set_ylabel('Grayscale Intensity')
    ax.legend(fontsize='x-small')

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
               
               y = 1 # throwaway variable. There will always be one exception, as the last value does not have a subsequent value to be subtracted from.
      
        intensity_difference_axes.append(hold_differences)

    #print(len(intensity_difference_axes[0]), 'content:', intensity_difference_axes)
    return intensity_difference_axes

    

def plot_dintensity_vs_dframes(intensity_difference_axes, frame_axes, axis, frame_count): # intensity axes should look like [[circle 1 data],[circle 2],[etc...]]

    frame_x = frame_axes[0: -1] # get entire list except for the last element (must match amount of elements in frame axis to agree with difference axis)

    ax = axis[1,0]
    
    for i in range(len(intensity_difference_axes)):

        #print(len(intensity_difference_axes))
        

        #plt.plot(frame_x, intensity_difference_axes[i], label = 'Circle #' + str(i+1))
        ax.plot(frame_x, intensity_difference_axes[i], label = 'Circle #' + str(i+1))
    
    ax.set_title('Grayscale Intensity Difference Every ' + str(frame_count) + ' Frames')
    ax.set_xlabel('Frames')
    ax.set_ylabel('Grayscale Intensity Difference')
    ax.legend(fontsize='x-small')

    '''
    plt.xlabel('Frames')
    plt.ylabel('d(Grayscale Intensity)/d(Frame)')
    plt.title('Differential Intensities Over Frames')
    plt.legend()
    '''
    
    #plt.show() # show all the figures
    
    return 



def plot_intensity_vs_seconds(intensity_axes, video_seconds, axis):

    ax = axis[0,0]
    
    for i in range(len(intensity_axes)):
        #plt.figure()
        #plt.plot(frame_x, intensity_axes[i], label = 'Circle #' + str(i+1))
        ax.plot(video_seconds, intensity_axes[i], label = 'Circle #' + str(i+1))
    
    
    ax.set_title('Grayscale Intensity Every ' + str(video_seconds[1]) + ' Seconds')
    ax.set_xlabel('Seconds')
    ax.set_ylabel('Grayscale Intensity')
    ax.legend(fontsize='x-small', loc='lower left')

    #plt.xlabel('Frames')
    #plt.ylabel('Grayscale Intensity (0 = darkest black)')
    #plt.title('Intensity vs Analyzed Frames')
    #plt.legend()

    #plt.show()
    

    return

def plot_dintensity_vs_seconds(intensity_difference_axes, video_seconds, axis): # intensity axes should look like [[circle 1 data],[circle 2],[etc...]]

    seconds_x = video_seconds[0: -1] # get entire list except for the last element (must match amount of elements in frame axis to agree with difference axis)

    ax = axis[1,0]

    for i in range(len(intensity_difference_axes)):

        #print(len(intensity_difference_axes))
        

        #plt.plot(frame_x, intensity_difference_axes[i], label = 'Circle #' + str(i+1))
        ax.plot(seconds_x, intensity_difference_axes[i], label = 'Circle #' + str(i+1))
    
    ax.set_title('Grayscale Intensity Difference Every ' + str(video_seconds[1]) + ' Seconds')
    ax.set_xlabel('Seconds')
    ax.set_ylabel('Grayscale Intensity Difference')
    ax.legend(fontsize='x-small', loc='lower left')

    
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

    for i in range(len(int_video_seconds)):
        
        #print('temp df index', temperature_df[2][i], 'video secs', video_seconds)
        '''
        if temperature_time[i] in int_video_seconds:

            temperature_axes.append(float(temperature[i])) # add the corresponding temperature data to the axes to be plotted
            temperature_time_axes.append(float(temperature_time[i]))
            #print('temp this', temperature[i], 'temp time this', temperature_time[i], 'vid time this', video_seconds)

        '''

        for t in range(len(temperature_time)):

            try: # try takes care for if one of the lists (temperature time, or int vid secs, is longer than the other and thus lacks t+1)

                if int_video_seconds[i] >= temperature_time[t] and int_video_seconds[i] < temperature_time[t+1]: # locating the two temperature time values that the video time value of the change in intensity lies between

                    mid_point_of_tempperature_values = (temperature_time[t+1] - temperature_time[t]) / 2 # find mid point so I can round the vid time to the nearest temperature time data point

                    if int_video_seconds[i] <= temperature_time[t] + mid_point_of_tempperature_values: # if vid time is closer to the left most boundary of temp time datas
                        
                        temperature_axes.append(float(temperature[t])) # add the corresponding temperature data to the axes to be plotted

                        temperature_time_axes.append(float(temperature_time[t]))

                    elif int_video_seconds[i] > temperature_time[t] + mid_point_of_tempperature_values: 

                        temperature_axes.append(float(temperature[t+1])) # add the corresponding temperature data to the axes to be plotted

                        temperature_time_axes.append(float(temperature_time[t+1]))
            
            except:
                dummy = 1


    return temperature_axes, temperature_time_axes


def get_correct_temperature_axes(intensity_axes, temperature_axes):

    if len(intensity_axes[0]) < len(temperature_axes): # if the video ran longer than the temperature probe...


        #print('int axes smaller than temp axes!!:', intensity_axes[0], 'adfssadf', temperature_axes)
        temperature_axes = temperature_axes[0 : len(intensity_axes[0])]


    #print('numb 1', temperature_axes)

    return temperature_axes

def get_correct_intensity_axes(intensity_axes, modified_temperature_axes):

    intensity_axes_for_temperature = []

    if len(intensity_axes[0]) > len(modified_temperature_axes): # if the video duration is shorter than the temperature probe data measurement duration...


        #print('int axes larger than temp axes!!:', intensity_axes[0], 'adfssadf', temperature_axes)

        for i in range(len(intensity_axes)):

            hold_intensity_axes_for_temperature = intensity_axes[i][0 : len(modified_temperature_axes)]
            intensity_axes_for_temperature.append(hold_intensity_axes_for_temperature)

    #print('numb 2', hold_intensity_axes_for_temperature)

    return intensity_axes_for_temperature

    


'''
def plot_intensity_vs_temperature(intensity_axes_for_temperature, modified_temperature_axes, axis):
    
    #print('temp axessss:', temperature_axes, 'intensity axessss:', intensity_axes)

    ax = [0,1]

    for i in range(len(intensity_axes_for_temperature)):
        #print('temp axessss66666:', temperature_axes, 'intensity axessss66666:', intensity_axes[i])

        #plt.figure()
        #plt.plot(frame_x, intensity_axes[i], label = 'Circle #' + str(i+1))
        ax.plot(modified_temperature_axes, intensity_axes_for_temperature[i], label = 'Circle #' + str(i+1))
    
    
    ax.set_title('Grayscale Intensity vs Temperature (Celsius)')
    ax.set_xlabel('Temperature (C)')
    ax.set_ylabel('Grayscale Intensity')
    ax.legend(fontsize='x-small', loc='lower left')

    #plt.xlabel('Frames')
    #plt.ylabel('Grayscale Intensity (0 = darkest black)')
    #plt.title('Intensity vs Analyzed Frames')
    #plt.legend()

    #plt.show()
    

    return

#def get_dintensity_matched_to_temperature(intensity_difference_axes, video_seconds, temperature_df):


#im so dumb. literally, just convert the video_seconds axis to a temperature axes.... 
'''
def plot_time_and_dintensity_heatmap(dintensity_axes, video_seconds, temperature_axes, temperature_time_axes, axis):

    ax = axis[0,1]
    # Create heatmap using imshow
    heatmap = ax.imshow(dintensity_axes, cmap='jet', aspect='auto', interpolation='none')
    
    # Add colorbar to the heatmap
    cbar = plt.colorbar(heatmap, ax=ax)
    cbar.set_label('Grayscale Intensity Difference')
    
    # Generate labels for y-ticks
    circle_label = ['Circle ' + str(i+1) for i in range(len(dintensity_axes))]
    
    # Set y-ticks and labels
    ax.set_yticks(range(len(dintensity_axes)))
    ax.set_yticklabels(circle_label, fontsize=10)
    
    # Set x-ticks to every 10 units and labels
    #axis[0, 2].xaxis.set_major_locator(MultipleLocator(10))
    rounded_video_seconds = [round(x, 2) for x in video_seconds]
    ax.set_xticks(range(0, len(rounded_video_seconds), 10))  # Ensure ticks every 50 units
    ax.set_xticklabels(rounded_video_seconds[::10], fontsize=7, rotation=45, ha='right')
    # the resulting ticks will be the time of analysis * the step interval defined above

    # Set titles and labels
    ax.set_title('')
    ax.set_xlabel('Analyzed Time Points (seconds)')
    ax.set_ylabel('Circles')

    # create a second x-axis above the plot using the twin function which creates an x axis with the same y axis
    ax2 = axis[0,1].twiny()

    # customizable values

    temp_interval = 3

    # IF TEMPERATURE DATA EXCEEDS LENGTH OF VIDEO THIS WILL ALLOW GRAPHING:
    #print('before manip,', len(temperature_axes), 'vid secs', len(video_seconds))
    #temperature = temperature[:len(video_seconds)] # get all elements before the length of elements in video secs
    ax2.set_xticks(temperature_time_axes[::temp_interval]) # only use every 20th element
    #print('hffjfgghkghg temp lngth', len(temperature_axes))
    ax2.set_xticklabels(temperature_axes[::temp_interval], fontsize=10, rotation=45, ha='left')
    ax2.set_xlabel('Temperature (C)', fontsize=12) 

    return

def get_freezing_temperature(intensity_difference_axes, video_seconds, temperature_axes, temperature_time_axes):  # global min of derivative is the largest change towards a black colour = freezing event

    min_intensity_all_temperatures = []

    for i in range(len(intensity_difference_axes)):

        min_value = min(intensity_difference_axes[i])

        #print('MIN VALUE:', min_value)
        min_intensity_index = intensity_difference_axes[i].index(min_value)
        min_intensity_video_time = round(video_seconds[min_intensity_index])

        ###

        #print('temp axes2', temperature_axes, len(temperature_axes), 'temp time axes2', temperature_time_axes, len(temperature_time_axes))
        #print('min int vid time', min_intensity_video_time, 'temp time axes', temperature_time_axes)
        for t in range(len(temperature_time_axes)):

            if min_intensity_video_time >= temperature_time_axes[t] and min_intensity_video_time < temperature_time_axes[t+1]: # locating the two temperature time values that the video time value of the change in intensity lies between
                #print('first', min_intensity_video_time - temperature_time_axes[t], 'second', min_intensity_video_time - temperature_time_axes[t+1])

                #print('hit')
                mid_point_of_tempperature_values = (temperature_time_axes[t+1] - temperature_time_axes[t]) / 2 # find mid point so I can round the vid time to the nearest temperature time data point

                if min_intensity_video_time <= temperature_time_axes[t] + mid_point_of_tempperature_values: # if vid time is closer to the left most boundary of temp time datas
                    #print(' L hit')
                    # self note: whatever the index of the closest temperature time axis value is, the corresponding temperature axis value will have the same index. 
                    
                    min_intensity_temperature = temperature_axes[t]

                    min_intensity_all_temperatures.append(min_intensity_temperature)

                elif min_intensity_video_time > temperature_time_axes[t] + mid_point_of_tempperature_values: 
                    #print('R hit')
                    min_intensity_temperature = temperature_axes[t+1]

                    min_intensity_all_temperatures.append(min_intensity_temperature)
            

            # in the case that the most significant minimum int change occurs outside of the temperature data time range 
            # ex: min int change given as 0 seconds in video due to false-positive circle in an area that does not go through much grayscale change, but temperature data begins recording at 1 second
            # ex 2: min int change occurs at 10 seconds, but temperature data only goes up to 5 seconds
            elif min_intensity_video_time < temperature_time_axes[0] or min_intensity_video_time > temperature_time_axes[-1]: 
                print(f'\n\n{RED}[PROGRAM] > {END}{YELLOW}WARNING! There is an issue with the provided video and temperature data{END}. The min_intensity_video_time (time when greatest grayscale int change to darkness occurs) of a circle is either smaller or larger than the range of the temperature time data. \nPossible solutions: Add a header to the temperature data (the 1st row is ignored), or obtain a wider range of temperature data.')
                '''
                {CYAN} Diagnostic Data {END})
                print(f'{YELLOW}Element Length of Video Time (Varies with Chosen Frame Interval Analysis){END} ---', len(video_seconds))
                print(f'{YELLOW}First Element of Video Time{END} -------------------------------------------------', video_seconds[0])
                print(f'{YELLOW}Last Element of Video Time{END} --------------------------------------------------', video_seconds[-1])
                print(f'{YELLOW}Minimum Intensity in Video Time{END} ---------------------------------------------', min_intensity_video_time)

                print(f'\n{YELLOW}Element Length of Temperature Time{END} ------------------------------------------', len(temperature_time_axes))
                print(f'{YELLOW}First Element of Temperature Time{END} -------------------------------------------', temperature_time_axes[0])
                print(f'{YELLOW}Last Element of Temperature Time{END} --------------------------------------------', temperature_time_axes[-1])
                
                print(f'\n{YELLOW}Full List of min_intensity_video_time:{END} This will be an incomplete list. Must put a print function outside of this else condition.')
                print(f'\n{YELLOW}Full List of temperature_time_axes:{END}', temperature_time_axes)

                print(f'\n{YELLOW}The minimum intensity in video time{END} {RED} should not {END}{YELLOW}be be smaller than he first element of temperature time, or larger than the last element. \nIt may also be very useful to investigate the length of the calib_r_list and the min_intensity_all_temperatures list in the get_boxplot_data_by_radii function. The lengths should match. \n{END}{GREEN}Possible solution:{END}{YELLOW} Acquire or edit the raw data to fix this.{END}')
                '''

        #print('min int vid time', min_intensity_video_time, 'temp time axes', temperature_time_axes

    
    #print('get temp min int all temp', min_intensity_all_temperatures)
    return min_intensity_all_temperatures

def plot_radii_vs_temperatures(calib_r_list, min_intensity_all_temperatures, axis):

    boxp = axis[1,1]

    calib_r_list_sorted, min_intensity_all_temperatures_sorted = (list(t) for t in zip(*sorted(zip(calib_r_list, min_intensity_all_temperatures))))

    boxp.scatter(calib_r_list_sorted, min_intensity_all_temperatures_sorted)
    boxp.set_xlabel('Radius (um)')
    boxp.set_ylabel('Freezing Temperature (ºC)')
    boxp.set_title(f'Freezing Activity Based on Droplet Radii (n={len(min_intensity_all_temperatures)})')

    return calib_r_list_sorted, min_intensity_all_temperatures_sorted


def get_boxplot_data_by_radii(calib_r_list, min_intensity_all_temperatures):


    #Customizable things:
    #label_names = ['A', 'B', 'C']
    label_names = ['A']

    amt_of_equal_sized_bins = 1

    # DIAGNOSTIC PURPOSES 
    # print('calib r list', len(calib_r_list), calib_r_list, 'min intensity all temp', len(min_intensity_all_temperatures), min_intensity_all_temperatures)

    # Create a DataFrame from the input list
    df = pd.DataFrame({'radii': calib_r_list, 'min_intensity_temperatures': min_intensity_all_temperatures})
    
    # Use pd.cut to bin the data into 3 categories labeled 'A', 'B', 'C'
    df['bins'], bin_edges = pd.cut(df['radii'], amt_of_equal_sized_bins, labels=label_names, retbins=True)
    
    # Print the original list and the bin edges
    #print("Original list:")
    #print(calib_r_list)
    #print("\nBin edges:")
    #print(bin_edges)
    

    # Group by the 'bins' column
    grouped = df.groupby('bins', observed=True)
    
    bin_data_list = []

    # Access values in each bin and print them
    for bin_label in label_names:
        #print(f"\nValues in bin '{bin_label}':")
        bin_data = grouped.get_group(bin_label)
        #print(bin_data)
    
        bin_data_list.append(bin_data[['radii', 'min_intensity_temperatures']].values.tolist())

    
    #print('bin data list', bin_data_list)
    return bin_data_list, bin_edges, label_names # bin data list contains the data sorted by radii with their associated freezing temperature

#def convert_to_boxplot_data_by_temperature(bin_data_list)

def plot_boxplot(bin_data_list, bin_edges, label_names, axis):

    boxp = axis[1,1]

    freezing_temperatures = []

    for i in range(len(bin_data_list)):

        freezing_temperature_per_bin = []

        for t in range(len(bin_data_list[i])):

            #print('freezing temp per bin', bin_data_list[i][t][1])
            freezing_temperature_per_bin.append(bin_data_list[i][t][1])

        freezing_temperatures.append(freezing_temperature_per_bin)
    
    #print('freezing temps', freezing_temperatures)



    # rename labels to include the bin edges
    new_label_names = []

    for i in range(len(label_names)): 
        label_names_hold = [str(round(bin_edges[i],1)), 'um to ', str(round(bin_edges[i+1],1)), 'um']
        new_label_names.append(label_names_hold)

    label_names = new_label_names
    #print(label_names)



    boxp.boxplot(freezing_temperatures, showmeans=True)
    boxp.set_xticklabels(label_names)
    boxp.set_xlabel('Bins')
    boxp.set_ylabel('Freezing Temperature (ºC)')
    boxp.set_title('Boxplots of Freezing Activity Based on Radius')

def get_frozen_fraction_data(min_intensity_all_temperatures):

    y = []

    for i in range(len(min_intensity_all_temperatures)):

        y.append((i+1)/len(min_intensity_all_temperatures))

    x = sorted(min_intensity_all_temperatures, reverse=True)

    return x, y
    
