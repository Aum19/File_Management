import PySimpleGUI as sg
import webbrowser
import pandas as pd
colors = {0:'gray80', 1:'gray90', 2:'gray70', 'bg':'gray30', 'fg':'white', 'btn_clr':('white','black'), 'parent_bg':'gray20'}
dark_col = 'gray20'
light_col = 'gray30'
global_df = pd.DataFrame() 
fol_namePathmap = dict()
fol_choice = []
misfits = []

def view_results(duplicates):
    global misfits
    global fol_choice
    create_fol_choice()
    misfits.sort(key=len)
    misfits = [i+j+k for i,j,k in zip(misfits[::2], misfits[1::2], misfits[::3])]
    results_layout_duplicates = [[sg.Column(duplicates, pad=(3,3), background_color=dark_col,size=(2000,1500), scrollable=True)]]

    results_layout_misfits = [[sg.Column(fol_choice, pad=(0,0), background_color=dark_col, scrollable=True),\
        sg.Column(misfits, pad=(0,0), background_color=dark_col,size=(2000,1500), scrollable=True)]]
    results_layout = [[sg.TabGroup([[sg.Tab('Misfits', results_layout_misfits),\
         sg.Tab('Duplicates', results_layout_duplicates)]])]]
    results_window = sg.Window('File System Management', size=(800,500), resizable=True, auto_size_text=True).Layout(results_layout)
    while True:
        event, values= results_window.Read()
        if event is None:
            break
        if 'dup' in event:
            key = extract_key(event)
            Openfolder(key)
        elif 'file' in event:
            key = extract_key(event)
            Openfolder(key)
        elif '__folder' in event:
            key = extract_key(event)
            if values[event]:
                results_window.FindElement(key).Update(visible=True)
            else:
                results_window.FindElement(key).Update(visible=False)
            results_window.Refresh()

        

def Openfolder(path):
    webbrowser.open_new(path)

def extract_key(event):
    path = event.split('__')
    path = path[:-1]
    path = '__'.join(path)
    return path



def generate_file_list(df, title):
    global misfits
    global_df = df
    duplicates = []
    confirmed_duplicates=True
    width = 800
    unique_id = ''
    count = 0
    webgui = ''
    for index, rows in df.iterrows():
        color = colors.get(int(count%3))
        count += 1
        unique_id = '__dup'+str(count)
        duplicates.append([sg.Button(str(rows['File_name_1']), key=rows['File_1']+unique_id,\
		    enable_events=True, button_color=('black',color)),])
        duplicates.append([sg.Button('Open Folder', key=rows['Folder_path_1']+unique_id, enable_events=True, \
        button_color=colors.get('btn_clr')), sg.Text(str(rows['Folder_path_1']), text_color=colors.get('fg'),\
            background_color=colors.get('parent_bg'))])
        count += 1
        unique_id = '__dup'+str(count)
        duplicates.append([sg.Button(str(rows['File_name_2']), key=rows['File_2']+unique_id, \
			enable_events=True, button_color=('black',color)),])
        duplicates.append([sg.Button('Open Folder', key=rows['Folder_path_2']+unique_id, enable_events=True,\
			button_color=colors.get('btn_clr')), sg.Text(str(rows['Folder_path_2']), text_color=colors.get('fg'),\
                background_color=colors.get('parent_bg'))])
        duplicates.append([sg.Text(' '*width,text_color=colors.get('fg'), background_color=colors.get('bg')),])
	
    misfits_df = pd.read_csv('unsafe.csv')
    grouped = misfits_df.groupby('Folder_path_raw')
    for name, group in grouped:
        parent =''
        frame_l = []
        for index, rows in group.iterrows():
            parent = rows['Parent']
            color = colors.get(int(count%2))
            count += 1
            unique_id = '__ file'+str(count)	
            frame_l.append(
                [sg.Button(str(rows['File_name']), key=rows['Path']+unique_id,\
                    enable_events=True, size=(35,2), button_color=('black',color))])
            frame_l.append(		
                [sg.Text(str(rows['Folder_path_raw']),size=(35,2),\
                        text_color=colors.get('fg'), background_color=colors.get('parent_bg')),])

        frame_l.insert(0,[sg.Button('Open Folder', key=rows['Folder_path_raw']+unique_id, enable_events=True, \
                    button_color=colors.get('btn_clr')),])
        misfits.append([sg.Frame(parent, frame_l,key=name,size=(200,150),background_color='black', font='Any 12',\
            relief=sg.RELIEF_GROOVE, title_color='olivedrab1')])
        global fol_namePathmap
        fol_namePathmap[name]=parent

    view_results(duplicates)

def create_fol_choice():
    global fol_choice
    fol_choice = []
    fol_choice.append([sg.Text('Folders', text_color='white', background_color=dark_col)])
    for keys, values in fol_namePathmap.items():
        fol_choice.append([sg.Checkbox(values,
            default=True,
            size=(None, None),
            auto_size_text=None,
            font=None,
            background_color=dark_col,
            text_color='greenyellow',
            change_submits=False,
            enable_events=True,
            disabled=False,
            key=keys+'__folder',
            pad=None,
            tooltip=None,
            visible=True)])
    