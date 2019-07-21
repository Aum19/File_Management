'''
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
'''

'''
filter_button = tk.Button(button_frame, text='Start', fg='white', bg='green4', command=lambda: start_config())
move_button = tk.Button(button_frame, text='Pause', fg='white', bg='yellow2', command=lambda: set_auto_move(False))

# Radio Buttons
rb_pattern = IntVar()
rb_pattern.set('Filter_type_selection')
Radiobutton(selection_frame, text="Starting with", indicatoron=0, variable=rb_pattern, value=1, command=lambda: filter_files('radio_change')).pack(side=LEFT)
Radiobutton(selection_frame, text="Ending with", indicatoron=0, variable=rb_pattern, value=2, command=lambda: filter_files('radio_change')).pack(side=LEFT)
Radiobutton(selection_frame, text="Contains", indicatoron=0, variable=rb_pattern, value=3, command=lambda: filter_files('radio_change')).pack(side=LEFT)

# Scroll View to display result list
scrollbar = Scrollbar(results_frame)
scrollbar.pack(fill=Y, side=RIGHT)

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
'''
from functools import lru_cache
@lru_cache(maxsize=4095)
def ld(s, t):
	if not s: return len(t)
	if not t: return len(s)
	if s[0] == t[0]: return ld(s[1:], t[1:])
	l1 = ld(s, t[1:])
	l2 = ld(s[1:], t)
	l3 = ld(s[1:], t[1:])
	return 1 + min(l1, l2, l3)


s1 = 'Supported Operationsfeature of the code transformation pass'
s2 = 'Another feature of the code transformation pass'
print(ld(s1,s2))