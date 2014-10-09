'''
   Calculates the time spent on the video and ERP phase per participant.
   Saves the results into a txt file with three columns: participant, time video phase, time ERP phase
'''
from open_GC_files import open_file_summary, available_parts, open_video_onset_file, open_erp_onset_file
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
    folders = available_parts(main_path)
    time_results = np.zeros((len(folders), 3))
    f = open('C:\Users\edz\OneDrive @ Tobii Technology AB\PhD\Chapter 2 - Gaze Contingency\Analysis\Results' + sep + 'mean_time_spent.txt', 'w')
    for i, folder in enumerate(folders):
        part_path = main_path + sep + folder
        onset_video = open_video_onset_file(part_path)
        onset_erp = open_erp_onset_file(part_path)
        time_results[i][0] = folder[1:]
        time_results[i][1] = time_spent(onset_video['Time'])
        time_results[i][2] = time_spent(onset_erp['Time'])
    write_file(f, time_results)
    f.close()
    print time_results