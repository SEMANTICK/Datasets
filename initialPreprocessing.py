'''

Replace file location and file name and run the code
The file should be in CSV format and the initial four rows with openBCI metadata should be removed
The csv file should directly start with column headers
The execution results out in a csv file with a cleaned data

'''

import numpy as np
import pandas as pd
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations

file_location = 'C:\\Users\\Mohammad Asad Shaikh\\Desktop';             # File URL
file_name = 'sample_data.csv';                                          # File name
file = file_location+'\\'+file_name

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
