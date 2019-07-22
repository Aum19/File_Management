import tkinter as tk
from tkinter import *

import Controller
from Model import set_auto_move

WINDOW_TITLE = "Directory Analysis"

#TRANFER FILES
# Set DEFAULT source and destination paths
DEFAULT_SOURCE_PATH = "C:/Users/Aum/Desktop/From/"
DEFAULT_DESTINATION_PATH = "C:/Users/Aum/Desktop/To/"

# Set DEFAULT_FILTER_TIME to number of days you want to filter for
DEFAULT_FILTER_TIME = 3
SECONDS_IN_DAY = 86400
EPOCH_DELTA = DEFAULT_FILTER_TIME * SECONDS_IN_DAY
DEFAULT_FILTER_PATTERN = 'Aum'

#Function Definitions
def get_analysis():
     analysis_dict = Controller.analyze(str(source_input.get('1.0','end-1c')))
     generate_file_list(analysis_dict.get('Possible_Duplicates'), {'Title':'Possible Duplicates', 'Count': str(analysis_dict.get('Files_Analyzed'))})

def get_detailed_analysis():
     df = Controller.deep_analysis()
     duplicates_list = []
     for index, rows in df.iterrows():
          duplicates_list.append(str(rows['File_1'])+ ' | '+ str(rows['File_2']))

     generate_file_list(duplicates_list, {'Title': 'Confirmed Duplicates', 'Count': str(len(duplicates_list))})


def generate_file_list(file_list, title):
    file_view.delete(0, END)
    file_view.insert(END, '-'*100)
    file_view.insert(END, ' '*15+title.get('Title')+'\n'+' '*15+'Total files Analyzed = '+title.get('Count'))
    file_view.insert(END, '-'*100)
    for items in file_list:
        file_view.insert(END, '->' + str(items))

    file_view.pack()
    scrollbar.config(command=file_view.yview)


# UI root and frames
root = tk.Tk()
root.title(WINDOW_TITLE)
selection_frame = Frame(root)
selection_frame.pack(padx=15)
button_frame = Frame(root)
button_frame.pack()
input_frame = Frame(root)
input_frame.pack(pady=10)
results_frame = Frame(root)
results_frame.pack()
rb_pattern = IntVar()
rb_pattern.set('Filter_type_selection')

# Radio Buttons 
Radiobutton(selection_frame, text="Start Operations", indicatoron=0, variable=rb_pattern, value=1, fg='black',\
      bg='green2', padx=10, command=lambda: Controller.start_config()).pack(padx=5, side=LEFT)
Radiobutton(selection_frame, text="Pause Threads", indicatoron=0, variable=rb_pattern, value=2, fg='white', bg='IndianRed2', command=lambda: set_auto_move(False)).pack(padx=5, side=LEFT)
quit_button = tk.Button(button_frame, text='Run in background', fg='brown1', bg='snow', command=lambda: root.withdraw())
quit_button.pack(side=LEFT, padx=5, pady=10)

# Buttons
Analyze_button = tk.Button(input_frame, text='Analyze', fg='white', bg='RoyalBlue2',\
     command= lambda: get_analysis())

Detailed_analysis_button = tk.Button(input_frame, text='Compare suspects line-by-line', fg='white', bg='brown3',\
     command= lambda: get_detailed_analysis())

Analyze_button.pack(pady=10)
Detailed_analysis_button.pack(pady=10)

#FILE ANALYSIS
#Text Labels
txt_s = StringVar()
txt_s.set("Please Enter Root path ex: C:/Users/Aum/Desktop/From/ \n Will look through all sub-directories")
source_label = Label(input_frame, textvariable=txt_s, fg='snow', bg='dim gray', pady=5, relief=RAISED).pack()
source_input = Text(input_frame, bg='snow', height=1, width=50)
source_input.pack(pady=5)

#Text Scroll View
scrollbar = Scrollbar(results_frame)
scrollbar.pack(fill=Y,side=RIGHT)

file_view = Listbox(results_frame, yscrollcommand=scrollbar.set)
file_view.config(width=0, height=0)


root.mainloop()
'''Developed by Aum'''


