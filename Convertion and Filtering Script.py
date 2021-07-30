'''

Replace path and file name and run the code
Note: The file needs to be in .csv or .txt format containing the output of 8 channel OpenBCI Ultracortex Mark IV

'''

path = "C:\\Users\\Mohammad Asad Shaikh\\Desktop"
file_name = "OpenBCI-RAW-2020-12-08_19-24-02.txt"
file = path+"\\"+file_name

import os
import numpy as np
import pandas as pd
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations

def delete_multiple_lines(original_file, line_numbers):
    """In a file, delete the lines at line number in given list"""
    is_skipped = False
    counter = 0
    dummy_file = original_file + '.bak'
    with open(original_file, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
        for line in read_obj:
            if counter not in line_numbers:
                write_obj.write(line)
            else:
                is_skipped = True
            counter += 1
            
    if is_skipped:
        os.remove(original_file)
        os.rename(dummy_file, original_file)
    else:
        os.remove(dummy_file)
    print("Lines Deleted!")

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
    channel_data = channel/24
    channel_data = channel_data.values
    for order in range(3):
        DataFilter.perform_highpass(channel_data, 250, 0.3, 4, FilterTypes.BUTTERWORTH.value, 0)
    for order in range(3):
        DataFilter.perform_lowpass(channel_data, 250, 95.0, 5, FilterTypes.CHEBYSHEV_TYPE_1.value, 1)
    channel_data = channel_data*0.707
    print('.')
    return channel_data

delete_multiple_lines(file, range(4))
data = get_data(file)

print("Processing Started...")

for i in range(8):
    channel = data[' EXG Channel '+str(i)]
    channel = process(channel)
    if i == 0:
        processed_data = pd.DataFrame(data = channel, columns = ['Channel 1'])
    else:
        processed_data['Channel '+str(i+1)] = pd.DataFrame(data = channel)

processed_data['Timestamp'] = pd.DataFrame(data = data[' Timestamp (Formatted)'])
processed_data.to_csv('processed_'+file_name)

print("Completed !")
