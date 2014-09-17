from open_write_functions import open_csv
import numpy as np
import csv

# Open file summary file .csv
''' File structure:
    0 - General_comments
    1 - Participant
    2 - Included_ERP
    3 - GC
    4 - Test
    5 - Video
    6 - EEG
    7 -Cal
    8 - Gaze
    9 - Onset_V
    10 - Onset_P
    11 - MatlabF
    12 - Other comments
'''
working_path = 'C:\Users\edz\OneDrive @ Tobii Technology AB\PhD\Chapter 2 - Gaze Contingency\Analysis'

#Create numpy data type according to the data
dt = np.dtype(
    [('Comments', np.str_, 20), ('Participants', np.int_), ('Included_ERP', np.int_), ('GC', np.int_), ('Test', np.int_),
     ('Files', [('Video', np.int_), ('EEG', np.int_), ('Calibration', np.int_),
                ('Gaze', np.int_), ('Onset_V', np.int_), ('Onset_P', np.int_), ('Matlab_F', np.int_)])])
fname = '../Files Summarytxt.txt'

db = np.loadtxt(fname, dtype=dt, delimiter="\t", skiprows=1)

#Compute the number of stimulus that each participant watched


#File summary statistics
'''
    compute simple statistics on how many participants we have:
    On each condition:
    with / without webcam
    with / without EEG
    with/ without matlab file
'''



