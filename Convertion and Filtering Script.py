'''

Replace file location and file name and run the code
The file should be in CSV format and the initial four rows with openBCI metadata should be removed
The csv file should directly start with column headers
The execution results out in a csv file with a cleaned data
Note: Kindly Adjust the file locations carefully, At file URL 3 make sure you set the location to the directory where the converted csv files are generated

'''

import os
import numpy as np
import pandas as pd
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations

def delete_multiple_lines(original_file, line_numbers):
    """In a file, delete the lines at line number in given list"""
    is_skipped = False
    counter = 0
    # Create name of dummy / temporary file
    dummy_file = original_file + '.bak'
    # Open original file in read only mode and dummy file in write mode
    with open(original_file, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
        # Line by line copy data from original file to dummy file
        for line in read_obj:
            # If current line number exist in list then skip copying that line
            if counter not in line_numbers:
                write_obj.write(line)
            else:
                is_skipped = True
            counter += 1

    # If any line is skipped then rename dummy file as original file
    if is_skipped:
        os.remove(original_file)
        os.rename(dummy_file, original_file)
    else:
        os.remove(dummy_file)

def get_data(file):
    dataset = pd.read_csv(file)
    dataset = dataset.drop(['Sample Index',
                            ' Accel Channel 0',
                            ' Accel Channel 1',
                            ' Accel Channel 2',
                            ' Other',
                            ' Other.1',
                            ' Other.2',
                            ' Other.3',
                            ' Other.4',
                            ' Other.5',
                            ' Other.6',
                            ' Analog Channel 0',
                            ' Analog Channel 1',
                            ' Analog Channel 2'], axis=1)
    dataset[' Timestamp (Formatted)'] = pd.to_datetime(dataset[' Timestamp (Formatted)'])
    return dataset

def process(channel):
    for order in range(3):
        DataFilter.perform_highpass(channel, 250, 0.3, 4, FilterTypes.BUTTERWORTH.value, 0)
    for order in range(3):
        DataFilter.perform_lowpass(channel, 250, 95.0, 5, FilterTypes.CHEBYSHEV_TYPE_1.value, 1)
    channel = channel*0.707
    return channel


L=["A001","A002","A003","A004","A005","G001","G002","G003","G004","G006","G007","H001","H002","H003","H004","H005"]#Replace the values of the list with the names of your files
print("Deleting the first 3 lines from the txt file\n")
for k in L:
    url="C:\\Users\\Mark Wagh\\Desktop\\Test Folder\\Data\\"+k+"\\"+k+".txt"
    
    delete_multiple_lines(url, [0,1,2,3])
print("Deleted\n\n\n")

# readinag given csv file 
# and creating dataframe
print("Converting the txt to csv")
print("****************")
for i in L:
    url="C:\\Users\\Mark Wagh\\Desktop\\Test Folder\\Data\\"+i+"\\"+i+".txt" 
    dataframe1 = pd.read_csv(url) 
      # storing this dataframe in a csv file 
    dataframe1.to_csv(i+".csv",index = None)
    print("*", end='')

print("\nConvertion Completed !\n\n\n")

print("Processing Started...") 
for j in L:
    file_location = "C:\\Users\\Mark Wagh\\Desktop\\Test Folder";             # File URL 3
    file_name = j+".csv";                                          
    file = file_location+"\\"+file_name
    data = get_data(file)

    for i in range(8):
        channel = data[' EXG Channel '+str(i)]
        channel = channel/24
        channel = channel.values
        channel_data = process(channel)
        if i == 0:
            processed_data = pd.DataFrame(data = channel_data, columns = ['Channel 1'])
        else:
            processed_data['Channel '+str(i+1)] = pd.DataFrame(data = channel_data)

    processed_data['Timestamp'] = pd.DataFrame(data = data[' Timestamp (Formatted)'])
    processed_data.to_csv('processed_'+file_name)

print("Completed !")
