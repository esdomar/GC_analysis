import numpy as np
from open_GC_files import open_accepted_rejected_files, open_file_summary
from os import sep

'''
    Calculates per participant the number of accepted and rejected trials
'''

main_path = 'C:\GC data\Participant_data'
results_path = 'C:\Users\edz\OneDrive @ Tobii Technology AB\PhD\Chapter 2 - Gaze Contingency\Analysis\Results\partial results'

#Open a file to save the results
f = open(results_path + sep + 'accepted_rejected_trials.txt', 'w')
f.write('Participant' + '\t' + 'GC' + '\t' + 'Accepted' + '\t' + 'Rejected' + '\t' + 'Uncertain' + '\n')

#Open accepted/rejected file
acc_rej_file = open_accepted_rejected_files()
summary_file = open_file_summary()

for participant in acc_rej_file:
    accepted = len(participant[participant == 1])
    rejected = len(participant[participant == 0])
    uncertain = len(participant[participant == 2])
    rest = len(participant[participant == 9])
    part_row = summary_file[summary_file['Participants'] == participant[0]]
    GC = part_row['GC'][0]
    if accepted + rejected + uncertain + rest != 144:
        print 'lengths do not match!'
    f.write(str(participant[0]) + '\t' + str(GC) + '\t' + str(accepted) + '\t' + str(rejected) + '\t' + str(uncertain) + '\n')
f.close()