import numpy as np
from os import sep

# Open file summary file .csv
''' File structure:
    0 - General_comments: H = No Horita ; V = Only videos ; N = No EEG
    1 - Participant
    From now on: 1 = Yes ; 0 = No
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
'''
working_path = 'C:\Users\edz\OneDrive @ Tobii Technology AB\PhD\Chapter 2 - Gaze Contingency\Analysis'

#Create numpy data type according to the data
dt = np.dtype(
    [('Comments', np.str, 20), ('Participants', np.int), ('Included_ERP', np.int), ('GC', np.int), ('Test', np.int),
     ('Files', [('Video', np.int), ('EEG', np.int), ('Calibration', np.int),
                ('Gaze', np.int), ('Onset_V', np.int), ('Onset_P', np.int), ('Matlab_F', np.int)])])
fname = '../Files Summarytxt.txt'

results_summary = np.loadtxt(fname, dtype=dt, delimiter="\t", skiprows=1)

#Include the number of stimulus that each participant watched
'''
   The number of trials that each participant watched was calculated using the script "compute_number_trials_watched.py"
'''
trials_watched_path = working_path + sep + 'number_of_trials_watched.txt'
trials_watched = np.loadtxt(trials_watched_path, dtype=np.dtype([('participant', np.str, 4), ('trials', np.int)]))

for i, item in enumerate(trials_watched):
    results_summary['Test'][i] = item[1]

#Include the number of trials that have more than 40, 60, and 80% of the data
#Open the txt file created with the script compute_percentage_etdata.py
fname = working_path + sep + 'Results' + sep + "number_of_trials_per_percentage.txt"
percentage_et_data = np.loadtxt(fname, dtype=np.float64, delimiter="\t", skiprows=0)


#File summary statistics
'''
    compute simple statistics on how many participants we have:
    On each condition:
    with / without webcam
    with / without EEG
    with/ without matlab file
'''




