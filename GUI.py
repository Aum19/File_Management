import tkinter as tk
import shutil
import datetime
from datetime import datetime
import os
from tkinter import *
from os import listdir
from os.path import isfile, join
from tkinter.messagebox import showinfo
# Set DEFAULT source and destination paths
DEFAULT_SOURCE_PATH = "C:/Users/n381554/Desktop/From/"
DEFAULT_DESTINATION_PATH = "C:/Users/n381554/Desktop/To/"

# Set DEFAULT_FILTER_TIME to number of days you want to filter for
DEFAULT_FILTER_TIME = 3
SECONDS_IN_DAY = 86400
EPOCH_DELTA = DEFAULT_FILTER_TIME * SECONDS_IN_DAY
DEFAULT_FILTER_PATTERN = 'Aum'


def retrieve_input():
    input_value = source_input.get('1.0', 'end-1c')
    out_value = destination_input.get('1.0', 'end-1c')
    threshold_time_value = time_input.get('1.0', 'end-1c')
    return list([input_value, out_value, threshold_time_value])


def filter_files(action):
    paths = retrieve_input()
    source_path = paths[0]
    destination_path = paths[1]
    filter_time = int(paths[2])*SECONDS_IN_DAY
    file_names = [f for f in listdir(source_path) if isfile(join(source_path, f))]
    file_paths = []
    file_times, file_times_raw = {}, {}
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
    filtered_file_names = pattern_filter(filtered_file_names)

# Updating the list of file paths
    [filtered_files.remove(path) for path, name in zip(filtered_files, filtered_file_names) if name not in path]

    if action == 'move':
        move_files(source_path, destination_path, filtered_file_names)
        generate_file_list(filtered_file_names, 'MOVED')
    elif action == 'radio_change':
        generate_file_list(filtered_file_names, 'SELECTION')
    else:
        generate_file_list(filtered_files, 'SELECTION')


def generate_file_list(file_list, state):
    file_view.delete(0, END)
    file_view.insert(END, '-'*27)
    file_view.insert(END, ' '*15+state)
    file_view.insert(END, '-'*27)
    for file_path in file_list:
        file_view.insert(END, ' >' + str(file_path))

    file_view.pack()
    scrollbar.config(command=file_view.yview)


def move_files(source_path, destination_path, file_list):
    errors = ''
    flag = False
    for f in file_list:
        try:
            shutil.move(source_path + '/' + str(f), destination_path)
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


def pattern_filter(file_list=[]):
    files_filtered = []
    available_filters = {1: 'starts_with', 2: 'ends_with', 3: 'contains'}
    pattern_type = available_filters.get(rb_pattern.get())
    pattern = pattern_input.get('1.0', 'end-1c')
    if pattern_type == 'starts_with':
        [files_filtered.append(f) for f in file_list if f.startswith(pattern)]
    elif pattern_type == 'ends_with':
        [files_filtered.append(f) for f in file_list if f.endswith(pattern)]
    else:
        [files_filtered.append(f) for f in file_list if pattern in f]
    return files_filtered

# UI root and frames


root = tk.Tk()
root.title("Aum's File Transfer")
button_frame = Frame(root)
button_frame.pack()
input_frame = Frame(root)
input_frame.pack(pady=5)
selection_frame = Frame(root)
selection_frame.pack()
results_frame = Frame(root)
results_frame.pack()
# Source and destination path input TEXT FIELDS
source_input = Text(input_frame, bg='SkyBlue1', height=1, width=50)
source_input.insert(END, DEFAULT_SOURCE_PATH)
destination_input = Text(input_frame, bg='coral1', height=1, width=50)
destination_input.insert(END, DEFAULT_DESTINATION_PATH)
time_input = Text(input_frame, fg='white', bg='midnight blue', height=1, width=5)
time_input.insert(END, DEFAULT_FILTER_TIME)
pattern_input = Text(selection_frame, fg='white', bg='midnight blue', height=1, width=20)
pattern_input.insert(END, DEFAULT_FILTER_PATTERN)
pattern_input.pack(side=RIGHT)

# Source Label text variables
txt_s = StringVar()
txt_d = StringVar()
txt_t = StringVar()
txt_f = StringVar()
txt_s.set("Please Enter Source path ex: C:/Users/Aum/Desktop/From/")
txt_d.set("Please Enter Destination path ex: C:/Users/Aum/Desktop/To/")
txt_t.set("Filter by Time in Days")
txt_f.set('Enter Filter pattern (No starting or tailing spaces)')
# Text labels(Samples)
source_label = Label(input_frame, textvariable=txt_s, relief=RAISED)
destination_label = Label(input_frame, textvariable=txt_d, relief=RAISED)
time_label = Label(input_frame, textvariable=txt_t, relief=RAISED)
filter_label = Label(input_frame, textvariable=txt_f, relief=None)

# Button declarations
filter_button = tk.Button(button_frame, text='Filter files',fg='white', bg='RoyalBlue1', command=lambda: filter_files('filter'))
move_button = tk.Button(button_frame, text='Move files', fg='white', bg='green4', command=lambda: filter_files('move'))
quit_button = tk.Button(button_frame, text='Exit', fg='red', bg='black', command=quit)

# Radio Buttons
rb_pattern = IntVar()
rb_pattern.set('Filter_type_selection')
Radiobutton(selection_frame, text="Starting with", indicatoron=0, variable=rb_pattern, value=1, command=lambda: filter_files('radio_change')).pack(side=LEFT)
Radiobutton(selection_frame, text="Ending with", indicatoron=0, variable=rb_pattern, value=2, command=lambda: filter_files('radio_change')).pack(side=LEFT)
Radiobutton(selection_frame, text="Contains", indicatoron=0, variable=rb_pattern, value=3, command=lambda: filter_files('radio_change')).pack(side=LEFT)

# Scroll View to display result list
scrollbar = Scrollbar(results_frame)
scrollbar.pack(fill=Y,side=RIGHT)

file_view = Listbox(results_frame, yscrollcommand=scrollbar.set)
file_view.config(width=0, height=0)

# Packing the UI objects (if something doesn't show up check here)
source_label.pack()
source_input.pack()
destination_label.pack()
destination_input.pack()
time_label.pack(side=LEFT, padx=5, pady=10)
time_input.pack(side=LEFT)

filter_button.pack(side=LEFT, padx=5, pady=10)
move_button.pack(side=LEFT, padx=5, pady=10)
quit_button.pack(side=LEFT, padx=5, pady=10)

root.mainloop()

'''Developed by Aum'''
