from os import listdir, sep
from open_GC_files import open_file_summary
import numpy as np
'''
    Open file per participant and save in a txt number of trials watched
    the files are taken from the participant data, the one that contains the onset of every ERP stimulus
    used to estimate the number of trials watched per infant and decide if the number of trials were enough
'''
def find_files(path, name):
    nfile = ''
    for item in listdir(path):
        if item.startswith(name):
            nfile = item
    return nfile


main_path = 'C:\GC data\Participant_data'
#Open a file to write the results to a txt file
f = open('C:\Users\edz\OneDrive @ Tobii Technology AB\PhD\Chapter 2 - Gaze Contingency\Analysis\Results\partial results/number_of_trials_watched.txt', 'w')
f.write('Participant' + '\t' + 'Included GC' + '\t' + 'GC' + '\t' + 'Number of trials' + '\n')

file_summary = open_file_summary()

number_of_trials = []

for participant in listdir(main_path):
    part_path = main_path + sep + participant
    onset_file_name = find_files(part_path, 'onset_stimuli')

    #Raise exception and continue with the next participant if the file is not in the folder
    if onset_file_name == '':
        text = ["the participant " + participant + "does not have the onset_video file required"]
        f.write(participant + "\t" + "-1")
        raise ValueError(text)
        continue

    #import pdb; pdb.set_trace()
    onset_data = np.loadtxt(part_path + sep + onset_file_name, dtype=int,  delimiter="\t", skiprows=1)

    number_of_trials.append(len(onset_data))
    print participant, onset_file_name, len(onset_data)

    participant_row = [row for row in file_summary if row[1] == int(participant[1:])][0]

    #write it to a file
    f.write(participant[1:] + "\t" + str(participant_row[3]) + "\t" + str(participant_row[4]) + "\t" + str(number_of_trials[-1]) + "\n")
        
f.close()