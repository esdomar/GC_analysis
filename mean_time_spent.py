'''
   Calculates the time spent on the video and ERP phase per participant.
   Saves the results into a txt file with three columns: participant, time video phase, time ERP phase
'''
from open_GC_files import open_file_summary, available_files, open_video_onset_file, open_erp_onset_file
from os import sep
import numpy as np
from open_find_write import write_file

def time_spent(times):
    '''
    :param times: list of onset times
    :return: difference between last and first  timestamp
    '''
    if times.size > 1:
        return times[-1] - times[0]
    else:
        return 0


if __name__ == '__main__':
    file_summary = open_file_summary()

    main_path = 'C:\GC data\Participant_data'
    folders = available_files(main_path)
    time_results = np.zeros((len(folders), 5))
    f = open('C:\Users\edz\OneDrive @ Tobii Technology AB\PhD\Chapter 2 - Gaze Contingency\Analysis\Results\partial results' + sep + 'mean_time_spent.txt', 'w')
    f.write('Participant' + '\t' + 'Included GC' + '\t' + 'GC' + '\t' + 'Time video' + '\t' + 'Time ERP' + '\n')

    for i, folder in enumerate(folders):
        part_path = main_path + sep + folder
        onset_video = open_video_onset_file(part_path)
        onset_erp = open_erp_onset_file(part_path)
        time_results[i][0] = folder[1:]
        participant_row = [row for row in file_summary if row[1] == int(folder[1:])][0]
        time_results[i][1] = participant_row[3]
        time_results[i][2] = participant_row[4]

        time_results[i][3] = time_spent(onset_video['Time'])
        time_results[i][4] = time_spent(onset_erp['Time'])
    write_file(f, time_results)
    f.close()
