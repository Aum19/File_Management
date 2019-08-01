
import os
import PySimpleGUI as sg
import random
#from Model import start_configSimple_UI
#from Model import set_auto_move
import results_view
from System_Analysis import start_analysis
import Controller
import pandas as pd

#Colors = ['SlateBlue1', 'RoyalBlue1', 'RoyalBlue2', 'SteelBlue1', 'DeepSkyBlue2', 'SkyBlue4', 'SlateGray4', \
# 'green4', 'chartreuse2', 'DarkOliveGreen4', 'IndianRed3', 'IndianRed4',  'sienna3', 'sienna4', 'chocolate3', 'firebrick3', 'firebrick4', 'brown1', 'brown4', 'thistle4']
colors = {0:'gray80', 1:'gray90', 2:'gray70', 'bg':'gray30', 'fg':'white', 'btn_clr':('white','black'), 'parent_bg':'gray20'}
def get_analysis():
	analysis_dict = Controller.analyze(values['start_path'])
	Controller.directory_health()
	results_view.generate_file_list(analysis_dict.get('Possible_Duplicates'), {'Title':'Possible Duplicates', 'Count': str(analysis_dict.get('Files_Analyzed'))})

main_layout = [[sg.Text('Configurations:', size=(30, 1), font=("Helvetica", 15), text_color='tomato')],
          [sg.Text('Enter a path:', size=(15, 1), auto_size_text=False, justification='right'),\
			   sg.InputText('Start Directory',key='start_path'),sg.FolderBrowse()],
          [sg.Radio('Default rules     ', key='use_default', group_id='customize_radio', change_submits=True, default=True), \
			  sg.Radio('Custom',key='customize', change_submits=True, group_id='customize_radio', default=False)],
		  [sg.Checkbox('Search Duplicates',key='check_search_duplicates'),],
		  [sg.Checkbox('Match folder name',key='check_use_foldername', disabled=True, visible=False)],
		  [sg.Checkbox('Match neighbours', key='check_match_neighbours', disabled=True, visible=False)],
		  [sg.Checkbox('Use size and format', key='check_use_size_format', disabled=True, visible=False)],
          [sg.Text('Omit these folders from Analysis ', size=(25, 1), key='omit_list_txt', auto_size_text=False, justification='right'), \
			  sg.Multiline(default_text='Ex. root/../folder1, root/../folder2', key='omit_list')],
          [sg.Text('Folder affinity %', key='fol_aff_txt', size=(15, 1), auto_size_text=False, justification='right', visible=False),\
           sg.Slider(key='folder_affinity', range=(0, 100), orientation='h', size=(35, 20), default_value=25, disabled=True, visible=False)],
          [sg.Text('Neighbour affinity %', key='n_aff_txt', size=(15, 1), auto_size_text=False, justification='right', visible=False), \
           sg.Slider(key='neighbour_affinity', range=(0, 100), orientation='h', size=(35, 20), default_value=25, disabled=True, visible=False)],
          [sg.Button('Start', key='start_analysis', enable_events=True), 
		  sg.Button('View Results', key='view_results', enable_events=True)]]




main_window = sg.Window('File System Management', background_color='gray30', auto_size_text=True).Layout(main_layout)

ml_elements = ['check_use_foldername','check_match_neighbours','check_use_size_format','fol_aff_txt','folder_affinity','n_aff_txt','neighbour_affinity']
def create_self():
	while True:
		event, values= main_window.Read()
		if event is None:
			break
		if event=='start_analysis':
			get_analysis()
		use_ml = int(values['customize'])
		if event=='view_results':
			pass
			event = None
		if use_ml==True:
			for element in ml_elements:
				main_window.FindElement(element).Update(visible=True)
				if element not in ['fol_aff_txt','n_aff_txt']:
					main_window.FindElement(element).Update(disabled=False)
		else:
			for element in ml_elements:
				if element not in ['fol_aff_txt','n_aff_txt']:
					main_window.FindElement(element).Update(disabled=True)
				main_window.FindElement(element).Update(visible=False)

create_self()