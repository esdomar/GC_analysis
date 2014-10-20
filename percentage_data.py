import numpy as np
from os import sep, listdir
from open_find_write import find_files
from gaze_data_functions import open_gaze_data, find_timestamp, per_outside_screen, per_inside_aoi, per_valid_et_data, per_valid_et_data_both_eyes_found
import time
'''
    Saves into a txt file the percentage of valid data, inside and outside the screen during the video and during the ERP phase
'''


main_path = 'C:\GC data\Participant_data'
results_path = 'C:\Users\edz\OneDrive @ Tobii Technology AB\PhD\Chapter 2 - Gaze Contingency\Analysis\Results\partial results'

#Open a file to write the results to a txt file
f = open(results_path + sep + 'percentage_data.txt', 'w')
f.write('Participant' + '\t' + 'Perc valid' + '\t' + 'Perc inside' + '\t' + 'Perc outside' + '\t' + 'Perc outliers' '\t' + 'Perc valid video' + '\t' 'Perc inside video'
        + '\t' + 'Perc outside video' + '\t' + 'Perc outliers video' + '\t' + 'Per valid erp' + '\t' + 'Perc inside erp' + '\t' + 'Perc outside erp' + '\t' + 'Perc outliers erp' + '\n')
folders = listdir(main_path)
part_name = []
percentage_data = np.zeros((len(part_name), 6), dtype=float)

for j, participant in enumerate(folders):
        print "participant", participant
        part_path = main_path + sep + participant
        onset_file_name = find_files(part_path, 'onset_stimuli')
        onset_video_name = find_files(part_path, 'onset_video', '.txt')
        gaze_data_name = find_files(part_path, 'GazeData')

        #Raise exception and continue with the next participant if the file is not in the folder
        if onset_file_name == '':
            print "the participant " + participant + "does not have the onset_video file required"
            percentage_data[j] = -1
            continue

        if gaze_data_name == '':
            print "the participant " + participant + "does not have the gaze_data file required"
            percentage_data[j] = -1
            continue

        if len(onset_file_name) > 1:
            print 'More than one onset file for participant ' + str(participant)

        if len(gaze_data_name) > 1:
            print 'More than one gaze data file for participant ' + str(participant)

        #Open files
        #Onset of every stimulus
        onset_erp = np.loadtxt(part_path + sep + onset_file_name[0], dtype=([('Trial', np.int), ('Cond', np.int), ('Time', np.float_)]), delimiter="\t", skiprows=1, ndmin=1)
        onset_video = np.loadtxt(part_path + sep + onset_video_name[0], dtype=([('Trial', np.int), ('Time', np.float_)]), delimiter="\t", skiprows=1, ndmin=1)
        start = time.time()
        gaze_data = open_gaze_data(part_path + sep + gaze_data_name[0])
        print 'Time opening gaze data = ', time.time() - start

        video_ts = find_timestamp(gaze_data['Local_timestamp'], onset_video['Time'][0]*1000000)
        video_te = find_timestamp(gaze_data['Local_timestamp'], onset_video['Time'][-1]*1000000)
        try:
            erp_ts = find_timestamp(gaze_data['Local_timestamp'], onset_erp['Time'][0]*1000000)
            erp_te = find_timestamp(gaze_data['Local_timestamp'], onset_erp['Time'][-1]*1000000)
        except:
            erp_ts = -1
            erp_te = -1



        per_valid_et_data_both_eyes_found(gaze_data['Left']['Validity'], gaze_data['Right']['Validity'])

        windows = [range(0, len(gaze_data['Left']['Validity']), 1)]
        if video_ts != -1:
            windows.append(range(video_ts, video_te, 1))
        if erp_ts != -1:
            windows.append(range(erp_ts, erp_te, 1))

        per_valid = []
        per_inside = []
        per_outside = []
        per_outliers = []

        for window in windows:
            samples = 0
            for validity in gaze_data['Left']['y'][window]:
                if validity != -1:
                    samples += 1

            try:
                per_valid.append(round(samples/float(len(gaze_data['Left']['x'][window]))*100, 2))
            except:
                per_valid.append('error')
            per_inside.append(per_inside_aoi(gaze_data['Left']['x'][window], gaze_data['Left']['y'][window]))
            per_outside.append(per_outside_screen(gaze_data['Left']['x'][window], gaze_data['Left']['y'][window]))
            per_outliers.append(per_outside_screen(gaze_data['Left']['x'][window], gaze_data['Left']['y'][window], 100000000000, 100000000000, 1.50001, 1.250001, -0.5, -0.25))

        print 'percentage of valid data', per_valid[0]
        print 'percentage inside the screen', per_inside[0]
        print 'percentage outside the screen', per_outside[0]
        print 'percentage of outlier', per_outliers[0]
        print 'sum:', per_inside[0] + per_outside[0] + per_outliers[0]

        f.write(participant + '\t' + str(per_valid[0]) + '\t' + str(per_inside[0]) + '\t' + str(per_outside[0]) + '\t' + str(per_outliers[0]) + '\t' +
                str(per_valid[1]) + '\t' + str(per_inside[1]) + '\t' + str(per_outside[1]) + '\t' + str(per_outliers[1]) + '\t')

        if len(per_valid) > 2:
                f.write(str(per_valid[2]) + '\t' + str(per_inside[2]) + '\t' + str(per_outside[2]) + '\t' + str(per_outliers[2]) + '\n')
        else:
            f.write('\n')

        del gaze_data

f.close()