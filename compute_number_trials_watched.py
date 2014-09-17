from os import listdir
from os import sep
import numpy as np
#Open file per participant and save in a txt number of trials watched

def find_files(path, name):
    nfile = ''
    for item in listdir(path):
        if item.startswith(name):
            nfile = item
    return nfile


main_path = 'G:\Claire Project\Data\Participants'
#Open a file to write the results to a txt file
f = open('number_of_trials_watched.txt', 'w')

number_of_trials = []

for participant in listdir(main_path):
    part_path = main_path + sep + participant
    onset_file_name = find_files(part_path, 'onset_stimuli')

    #Raise exception and continue with the next participant if the file is not in the folder
    if onset_file_name == '':
        text = ["the participant " + participant + "does not have the onset_video file required"]
        raise ValueError(text)
        continue
        number_of_trials.append(-1)

    #import pdb; pdb.set_trace()
    onset_data = np.loadtxt(part_path + sep + onset_file_name, dtype=int,  delimiter="\t", skiprows=1)


    number_of_trials.append(len(onset_data))
    print participant, onset_file_name, len(onset_data)

    #write it to a file
    f.write(participant + "\t" + str(number_of_trials[-1]) + "\n")
        
f.close()







