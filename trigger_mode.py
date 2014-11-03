from open_GC_files import open_erp_onset_file, open_file_summary, open_accepted_rejected_files
from os import sep

'''
    Calculates the gaze contingency results and creates a txt file containing the following information per participant:
        number of trials triggered by different modes
        number of accepted trials per mode
'''

participants_path = 'C:\GC data\Participant_data'
results_path = 'C:\Users\edz\OneDrive @ Tobii Technology AB\PhD\Chapter 2 - Gaze Contingency\Analysis\Results\partial results'
participant_results_path = results_path + '\participants'

#Open a file to save the results
f = open(results_path + sep + 'trigger_modes.txt', 'w')
f.write('Participant' + '\t' + '1st attempt' + '\t' + '1st accepted' + '\t' + '2nd attempt' + '\t' + '2nd accepted' + '\t' + '3rd attempt' + '\t' + '3rd accepted' + '\t'
        + 'Uncertain' + '\t' 'Uncertain_accepted' + '\t' + 'Total trials' + '\n')

#Open info files
summary_file = open_file_summary()
accepted_rejected = open_accepted_rejected_files()

for i, participant in enumerate(summary_file['Participants']):
    #If the participant was in gaze contingent mode...
    if summary_file['Included_GC'][i] and summary_file['GC'][i] == 1:
        #Open a txt file per GC participant to save the results
        p_file = open(participant_results_path + sep + str(participant) + '_trigger_mode.txt', 'w')
        p_file.write('Trial' + '\t' + 'A/R' + '\t' + 'Trigger_mode' + '\n')

        #Initialize the trigger mode count
        first_attempt = 0
        first_accepted = 0
        second_attempt = 0
        second_accepted = 0
        third_attempt = 0
        third_accepted = 0
        uncertain = 0
        uncertain_accepted = 0
        #Open erp onset file
        folder = 'P' + str(participant)
        path = participants_path + sep + folder
        onset_file = open_erp_onset_file(path)
        #Select right row in accepted-rejected file:
        ac_rej_row = [row for row in accepted_rejected if row[0] == participant][0]
        p_file.write('1' + '\t' + str(ac_rej_row[1]) + '\t' + '4' + '\n')

        for j in range(1, len(onset_file), 1):
            trial = j + 1
            p_file.write(str(trial) + '\t' + str(ac_rej_row[trial]) + '\t')
            time = onset_file['Time'][j] - onset_file['Time'][j-1]
            if time < 2.4:
                first_attempt += 1
                if ac_rej_row[trial] == 1:
                    first_accepted += 1
                p_file.write('1' + '\n')
            elif time < 6.1:
                second_attempt += 1
                if ac_rej_row[trial] == 1:
                    second_accepted += 1
                p_file.write('2' + '\n')
            elif time < 7.5:
                third_attempt += 1
                if ac_rej_row[trial] == 1:
                    third_accepted += 1
                p_file.write('3' + '\n')
            else:
                uncertain += 1
                if ac_rej_row[trial] == 1:
                    uncertain_accepted += 1
                p_file.write('4' + '\n')

        f.write(str(participant) + '\t' + str(first_attempt) + '\t' + str(first_accepted) + '\t' + str(second_attempt) + '\t' + str(second_accepted) + '\t' +
                str(third_attempt) + '\t' + str(third_accepted) + '\t' + str(uncertain) + '\t' + str(uncertain_accepted) + '\t' + str(len(onset_file)) + '\n')
        p_file.close()
f.close()