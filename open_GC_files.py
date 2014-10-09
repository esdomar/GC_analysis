import numpy as np
from os import listdir, sep


def open_file_summary():
    #Opens the file summary file
    fname = 'C://GC data//Results//Files_summary.txt'
    dt = np.dtype(
    [('Comments', np.str, 20), ('Participants', np.int), ('Included_ERP', np.int), ('Included_GC', np.int), ('GC', np.int),
     ('Files', [('Video', np.int), ('EEG', np.int), ('Calibration', np.int),
                ('Gaze', np.int), ('Onset_V', np.int), ('Onset_P', np.int), ('Matlab_F', np.int)]), ('Trials', np.int),
     ('Trials_40p', np.int), ('Trials_60p', np.int), ('Trials_80p', np.int), ('Trials_90p', np.int)])

    return np.loadtxt(fname, dtype=dt, delimiter="\t", skiprows=1)


def open_video_onset_file(path):
    #Opens the video onset file specified in the path. Assumes that there is only one onset_video file per folder
    files = listdir(path)
    for file in files:
        if file.startswith('onset_video_P'):
            return np.loadtxt(path + sep + file, dtype=([('Video', np.int), ('Time', np.float_)]), delimiter="\t", skiprows=1)
    return 'This participant has no onset video file'


def open_erp_onset_file(path):
    files = listdir(path)

    for file in files:
        if file.startswith('onset_stimuli'):
            return np.loadtxt(path + sep + file, dtype=([('Trial', np.int), ('Cond', np.int), ('Time', np.float_)]), delimiter="\t", skiprows=1)
    return 'This participant has no onset erp file'


def available_parts(path):
    return listdir(path)

