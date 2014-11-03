from scipy import misc
import matplotlib.pyplot as plt
from image_functions import open_image
from gaze_data_functions import open_gaze_data, find_timestamp, eye_average, per_valid_et_data, per_inside_aoi
from open_find_write import find_files
from os import sep, listdir
import numpy as np
import time
from open_find_write import as_string, write_line


def load_et_data(path, file_starts):
    gd_file = find_files(path, file_starts)
    return open_gaze_data(path + sep + gd_file[0])


def load_indexes(path, file_starts):
    in_file = find_files(path, file_starts)
    return np.loadtxt(path + sep + in_file[0], delimiter='\t', skiprows=1)


def find_index(indexes, position, list_times):
    time = indexes[position]*1000000
    return find_timestamp(list_times, time)


def calculate_image(part_path, image):
    print part_path[-3:]
    start = time.time()
    et_data = load_et_data(part_path, 'GazeData')
    print 'Load ET data:', time.time() - start

    start = time.time()
    #Start and ending index
    onset_indexes = load_indexes(part_path, 'calib_info')
    et_start_index = find_index(onset_indexes,  2, et_data['Local_timestamp'])
    et_end_index = find_index(onset_indexes, 3, et_data['Local_timestamp'])

    results = []
    errors = 0
    invalid = 0
    start = time.time()
    et_av_x = []
    et_av_y = []
    #Calculate average et data and change image
    for et_sample in range(et_start_index, et_end_index, 1):

        et_av_x.append(int(eye_average(et_data[et_sample]['Left']['x'], et_data[et_sample]['Right']['x'], et_data[et_sample]['Left']['Validity'],
                                et_data[et_sample]['Right']['Validity'])*res_x))

        et_av_y.append(int(eye_average(et_data[et_sample]['Left']['y'], et_data[et_sample]['Right']['y'], et_data[et_sample]['Left']['Validity'],
                                et_data[et_sample]['Right']['Validity'])*res_y))

        if et_data[et_sample]['Left']['Validity'] == 4 and et_data[et_sample]['Right']['Validity'] == 4:
            print 'invalid'
            invalid += 1
        try:
            image[et_av_y[-1]][et_av_x[-1]][:] = [255, 0, 0]
        except:
            errors += 1

    #Calculate percentage inside each AOI
    aoi_center = [(45, 40), (405, 245), (765, 165), (210, 518)] #AOI location x, y coordinates
    distance_from_center_pixels = 80
    percentage_aoi = []
    for aoi in aoi_center:
        percentage_aoi.append(per_inside_aoi(et_av_x, et_av_y, aoi, distance_from_center_pixels))
    '''
    #Print results
    print 'Percentage valid ET data:', per_valid_et_data(et_data['Right']['Validity'][et_start_index:et_end_index],
                                                         et_data['Left']['Validity'][et_start_index:et_end_index])
    print 'Percentage samples of out of screen:', round((errors/float(et_end_index - et_start_index))*100, 2)
    print 'Time including ET info on picture:', time.time() - start
    for i, percentage in enumerate(percentage_aoi):
        print "percentage", i+1, ":", percentage

    '''
    #Save results
    results.append(part_path[-2:])
    results.append(per_valid_et_data(et_data[et_start_index:et_end_index]['Right']['Validity'],
                                     et_data[et_start_index:et_end_index]['Left']['Validity']))
    results.append(round((errors/float(et_end_index - et_start_index))*100, 2))
    results.append(round((invalid/float(et_end_index - et_start_index))*100, 2))
    for i, percentage in enumerate(percentage_aoi):
            results.append(round(percentage, 2))

    plt.imshow(image)
    #plt.show(block=False)
    plt.savefig('verification_results_' + part_path[-2:] + '.png', bbox_inches='tight')
    plt.savefig(part_path + sep + 'verification_results.png', bbox_inches='tight')

    print 'Rest of stuff:', time.time() - start
    print ''
    print et_start_index
    print et_end_index

    return results

res_x = 800
res_y = 600

#Load the verification image

main_path = 'C:\GC data\Participant_data'

participants = listdir(main_path)

f = open('verification_results.txt', 'w')
f.write('participant' + "\t" + 'per_valid_data' + "\t" + 'per_outside' + "\t" + 'per_no_gaze' + "\t" + 'per_aoi_1' + "\t" + 'per_aoi_2' + "\t" + 'per_aoi_3' + "\t"
        + 'per_aoi_4' + "\n")

for participant in ['P19']:
    ver_im = open_image('C:\\Users\\edz\\Documents\\Python Scripts\\replay_et_data\\replay_et_data\\verification_image.jpg')
    try:
        part_path = main_path + sep + participant
        results = calculate_image(part_path, ver_im)
    except:
        restuls = [participant, -1]
    write_line(f, as_string(results))

f.close()


