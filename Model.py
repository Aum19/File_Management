import shutil
import time
import datetime
from datetime import datetime
import os
from threading import Thread
from os import listdir
from os.path import isfile, join
from tkinter.messagebox import showinfo

from write_log import write_to_file as w_to_f
from write_log import read_config as r_c

# Set AUTOMATION
AUTO_MOVE = True
DEFAULT_INTERVAL = 20
DEFAULT_THREADS = 1


# Set DEFAULT source and destination paths
DEFAULT_SOURCE_PATH = "C:/Users/Aum/Desktop/From/"
DEFAULT_DESTINATION_PATH = "C:/Users/Aum/Desktop/To/"

# Set DEFAULT_FILTER_TIME to number of days you want to filter for
DEFAULT_FILTER_TIME = 3
TIME_CONVERSION_TO_SECONDS = {'Seconds': 1, 'Minutes': 60, 'Hours': 3600, 'Days': 86400, 'Weeks': 604800, 'Months': 2628000, 'Years': 31540000}
DEFAULT_FILTER_PATTERN = 'Aum'
WORKER_THREAD_LIST = []


def start_config():
    global AUTO_MOVE
    AUTO_MOVE = True
    config_list = r_c()
    print(config_list)
    for item in config_list:
        create_threads(item)


'''Thread'''


def create_threads(config_list):
    global WORKER_THREAD_LIST
    WORKER_THREAD_LIST.append(Thread(name=config_list[0], target=filter_files, args=('bla bla', config_list)))
    WORKER_THREAD_LIST[-1].daemon = True
    WORKER_THREAD_LIST[-1].start()


'''Thread'''


def filter_files(vois, config_list):
    while AUTO_MOVE:
        automate(config_list)


def automate(config_list):
    # print('Working')
    source_path = config_list[1]
    destination_path = config_list[2]
    filter_time = int(config_list[3])*TIME_CONVERSION_TO_SECONDS.get(config_list[4])
    file_paths = []
    time.sleep(config_list[7]*TIME_CONVERSION_TO_SECONDS.get(config_list[8]))
    file_times, file_times_raw = {}, {}
    file_names = [f for f in listdir(source_path) if isfile(join(source_path, f))]
    [file_paths.append(source_path + f) for f in file_names]
    [file_times_raw.update({os.path.getmtime(f): f}) for f in file_paths]

# Call to time filter passing dictionary {time:path} and time in seconds for days given by user
    filtered_files = time_filter(file_times_raw, filter_time)

# Additional/Optional steps to get readable time format
    [file_times.update({datetime.fromtimestamp(key).strftime('%Y:%m:%d:%H:%M:%S'): value}) for key, value in
     file_times_raw.items()]

    filtered_file_names = []
# Extracting file name from path
    for f in filtered_files:
        temp = f.split('/')
        filtered_file_names.append(temp[-1])
# Filtering the file names by the pattern given by user
    filtered_file_names = pattern_filter([config_list[5], config_list[6]], filtered_file_names)

# Updating the list of file paths
    [filtered_files.remove(path) for path, name in zip(filtered_files, filtered_file_names) if name not in path]
    file_ops(source_path, destination_path, filtered_file_names, config_list[9])


def file_ops(source_path, destination_path, file_list, action):
    errors = ''
    flag = False
    for f in file_list:
        try:
            if action == 'Move':
                shutil.move(source_path + '/' + str(f), destination_path)
                w_to_f(str('Moved' + f+','+source_path+','+destination_path))
            elif action == 'Delete':
                os.remove(source_path + '/' + str(f))
                w_to_f(str('Deleted' + f+','+source_path+','+'None'))
            else:
                shutil.copy(source_path + '/' + str(f), destination_path)
                w_to_f(str('Copied' + f+','+source_path+','+destination_path))
        except shutil.Error as err:
            errors += str(err.args[0]) + '\n'
            flag = True
    if flag:
        showinfo("Errors:", errors)


def time_filter(file_dict, time_threshold):
    file_list = list()
    now_time = datetime.now().timestamp()
    threshold_time = now_time-time_threshold
    for key, value in file_dict.items():
        if threshold_time > key:
            file_list.append(value)
    return file_list


def pattern_filter(pattern_config_list, file_list=[]):
    files_filtered = []
    # available_filters = {1: 'Starts_with', 2: 'Ends_with', 3: 'Contains'}
    pattern_type = pattern_config_list[0]# available_filters.get(rb_pattern.get())
    pattern = pattern_config_list[1]
    if pattern_type == 'Starts_with':
        [files_filtered.append(f) for f in file_list if f.startswith(pattern)]
    elif pattern_type == 'Ends_with':
        [files_filtered.append(f) for f in file_list if f.endswith(pattern)]
    else:
        [files_filtered.append(f) for f in file_list if pattern in f]
    return files_filtered


def set_auto_move(new_state):
    global AUTO_MOVE
    AUTO_MOVE = new_state
    print(AUTO_MOVE)


'''Developed by Aum'''
