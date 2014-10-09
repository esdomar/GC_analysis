from os import sep
import numpy as np
from os import listdir, path, makedirs
from open_find_write import find_files, write_file, as_string
from gaze_data_functions import dtype_sdk_gazedata, find_timestamp, num_samples, per_valid_et_data, per_valid_et_data_both_eyes_found
import time
'''
    Saves a txt file per participant containing the number of trials that have been seen with different ET validity data
    percentages 40%, 60% 80% and 90% the files are taken from the participant data, the one that contains the onset of every
    ERP stimulus and the raw ET data used to estimate the number of trials with valid data per infant and decide on the
    quality of the data.
'''

if __name__ == '__main__':

    #Define variables
    baseline_time_ms = 1000
    stimulus_time_ms = 1000
    cross_time_ms = 1000
    sampling_rate = 120

    main_path = 'C:\GC data\Participant_data'
    results_path = "C:\GC data\Results"
    #if not path.exists(results_path):
    #    makedirs(results_path)

    #Open a file to write the results to a txt file
    f = open(results_path + sep + 'number_of_trials_per_percentage.txt', 'w')
    folders = listdir(main_path)
    part_name = []

    for folder in folders:

        part_name.append(folder[1:])

    #Variable where the number of trials that have at least a percentage of valid data are stored:
    #0 - Participant
    #1-5:  40, 60, 80, 90
    #Number of trials with more than: 40, 60, 80 and 90% of valid samples.
    number_trials_valid_data = np.zeros((len(part_name), 5), dtype=float)

    for j, participant in enumerate(folders):
        print "participant", participant
        part_path = main_path + sep + participant
        onset_file_name = find_files(part_path, 'onset_stimuli')
        gaze_data_name = find_files(part_path, 'GazeData')

        #Raise exception and continue with the next participant if the file is not in the folder
        if onset_file_name == '':
            print "the participant " + participant + "does not have the onset_video file required"
            number_trials_valid_data[j] = -1
            continue

        if gaze_data_name == '':
            print "the participant " + participant + "does not have the gaze_data file required"
            number_trials_valid_data[j] = -1
            continue

        if len(onset_file_name) > 1:
            print 'More than one onset file for participant ' + str(participant)

        if len(gaze_data_name) > 1:
            print 'More than one gaze data file for participant ' + str(participant)

        #Create a folder to save the data if it does not exist yet:
        #if not path.exists(results_path + sep + participant):
        #    makedirs(results_path + sep + participant)
        #Open the txt necessary to store the information of each participant
        f_perc_data = open(part_path + sep + participant +  '_percentage_of_valid_data.txt', 'w')
        f_onset = open(part_path + sep + participant + 'et_data_indexes_every_stimulus_onset.txt', 'w')

        #import pdb; pdb.set_trace()
        #Open files
        #Onset of every stimulus
        onset_data = np.loadtxt(part_path + sep + onset_file_name[0], dtype=([('Trial', np.int), ('Cond', np.int),
                                                                              ('Time', np.float_)]), delimiter="\t", skiprows=1, ndmin=1)
        #Gaze data
        start = time.time()
        dt_gaze_data = dtype_sdk_gazedata()
        gaze_data = np.loadtxt(part_path + sep + gaze_data_name[0], dtype=dt_gaze_data,  delimiter="\t", skiprows=1, ndmin=1)
        end = time.time()
        print 'Time to open gaze data = ' + str(end - start)

        #Calculate the closest timestamp in the ET data that corresponds to every onset time
        indexes = []
        starting_index = 0
        start = time.time()
        for onset in onset_data:
            line = []
            line.append(onset['Trial'])
            line.append(starting_index + find_timestamp(gaze_data['Local_timestamp'][starting_index:], onset['Time']*1000000))
            indexes.append(line)
            starting_index = line[-1]
        end = time.time()
        print 'Time to open calculate indexes = ' + str(end - start)

        #Percentage_et_data: 0 -part_number, 1 - percentage valid samples, 2 - Percentage valid samples only
        # both eyes valid
        percentage_et_data = np.zeros((len(indexes), 3), dtype=float)

        #First, calculate percentage of valid data per trial
        start = time.time()
        for i, timestamp in enumerate(indexes):
            initial_sample = timestamp[1]
            final_sample = initial_sample + num_samples(sampling_rate, stimulus_time_ms)

            percentage_et_data[i][0] = part_name[j]
            percentage_et_data[i][1] = per_valid_et_data(gaze_data['Right']['Validity'][initial_sample:final_sample],
                                                                    gaze_data['Left']['Validity'][initial_sample:final_sample])

            percentage_et_data[i][2] = per_valid_et_data_both_eyes_found(gaze_data['Right']['Validity'][initial_sample:final_sample],
                                                                    gaze_data['Left']['Validity'][initial_sample:final_sample])
        #import pdb; pdb.set_trace()
        #Second, calculate the number of valid trials for different percentages
        number_trials_valid_data[j][0] = part_name[j]
        number_trials_valid_data[j][1] = str(len([number for i, number in enumerate(percentage_et_data[:, 1]) if number > 40]))
        number_trials_valid_data[j][2] = str(len([number for i, number in enumerate(percentage_et_data[:, 1]) if number > 60]))
        number_trials_valid_data[j][3] = str(len([number for i, number in enumerate(percentage_et_data[:, 1]) if number > 80]))
        number_trials_valid_data[j][4] = str(len([number for i, number in enumerate(percentage_et_data[:, 1]) if number > 90]))
        end = time.time()
        print 'Time to calculate percentage = ' + str(end - start)

        start = time.time()
        #Save the percentage of valid data per trial for each participant
        write_file(f_perc_data, percentage_et_data)
        f_perc_data.close()
        #Save the ET data onset indexes
        #indexes_str = []

        #indexes_str = as_string(indexes)
        write_file(f_onset, indexes)
        f_onset.close()
        end = time.time()
        print 'Time to save files = ' + str(end - start)

    #Save the summary of how many trials per participant had more then a percentage of valid data (40,60, 80,90...)
    write_file(f, number_trials_valid_data)
    f.close()