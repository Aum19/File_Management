import os
from os import walk
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bokeh_plots import get_panels
from Scan_Duplicates import duplicate_filter
import Scan_Duplicates
from functools import lru_cache
#import seaborn as sns
start_path = 'C:/Users/N381554/Desktop/MFT_work/To'
f_size, f_created, f_modified, f_last_access, f_format_type = [], [], [], [], []


class FileData:
    df_cols = ['Path', 'Folder_path', 'File_name', 'Created', 'Modified', 'Accessed', 'Size', 'Format', 'Creation_Age_Days', 'Size_MB']
    df = pd.DataFrame(columns=df_cols)
     #Set up patterns:
    
    def __init__(self, mypath):
        self.path = mypath
        f = []
        for (dirpath, dirnames, filenames) in walk(self.path):
            f.extend(filenames)
            for file_name in filenames:
                try:
                    now_path = str(dirpath)+'/'+str(file_name)
                    parent = str(dirpath)
                    temp_format = str(file_name).split('.')
                    current_time = datetime.now().timestamp()
                    creation_time = os.stat(now_path).st_ctime
                    size_kb = os.stat(now_path).st_size
                    size_mb = size_kb/1000000
                    age_days = (current_time - creation_time)/86400
                    self.df = self.df.append({'Path':now_path, 
                        'Folder_path': parent.lower(),
                        'File_name': file_name.lower(), 
                        'Created': os.stat(now_path).st_ctime, 
                        'Modified': os.stat(now_path).st_mtime, 
                        'Accessed': os.stat(now_path).st_atime, 
                        'Size': os.stat(now_path).st_size, 
                        'Format': str(temp_format[-1]).lower(), 
                        'Creation_Age_Days':age_days, 
                        'Size_MB':size_mb}, ignore_index=True)
                except:
                    pass
        self.df = add_parent_column(self.df)
    
    



class Analysis:
    def __init__(self, df):
        self.df = df


class Scatter(Analysis):
    
    def plot_age_size_format(self):
        df = self.df
        return df


class Size(Analysis):
    def size_by_format(self):
        df = self.df
        format_total_size = dict(df.groupby('Format').apply(lambda x: x['Size_MB'].sum()))
        return format_total_size


class Idle(Analysis):
    pass

class Format(Analysis):

    def format_pie_dist(self):
        df = self.df
        f_dict = df['Format'].value_counts().to_dict()
        temp = list(f_dict.values())
        plt.pie(temp, labels=f_dict.keys(),
                autopct= '%1.1f%%', shadow=True, startangle=140)
        plt.show()


class Plots:
    def manage_plots(self, df, format_size_dict, meta_dict):
        get_panels(df, format_size_dict, meta_dict)
        

def add_parent_column(df):
        df['Folder_path_raw'] = df.Folder_path
        df.Folder_path = df.Folder_path.str.replace('\\','/')
        df['Parent'] = df.Folder_path.str.split('/')
        df.Parent = df.Parent.str[-1:]
        df.Parent = df.Parent.agg(lambda x: ','.join(map(str,x)))
        return df
@lru_cache(maxsize=5000)
def start_analysis(crawl_path):
    # Create a DF using FileData object
    file_data = FileData(crawl_path)
    #Get the DF through corresponding class object
    scatter1 = Scatter(file_data.df)
    df_scatter = scatter1.plot_age_size_format()
    #Creates the pie chart Format vs. Count
    format1 = Format(file_data.df)
    format1.format_pie_dist()
    #To create any plots or dashboard using packages data flows through plot
    # Should be consistent with the recieving method
    dict_of_plots = dict()
    #dictionary for plots each entry should correspond to an object of plots
    dict_of_plots['bokeh'] = Plots()
    size_1 = Size(file_data.df)
    format_total_size = size_1.size_by_format()
    dict_of_plots.get('bokeh').manage_plots(df_scatter, format_total_size, {'file_title':'Scatter Plots','fig_title':'Access_time vs Size'})
    Scan_Duplicates.store_in_csv(file_data.df, 'directory_df.csv')
    return {'Files_Analyzed': str(len(format1.df)), 'Possible_Duplicates': duplicate_filter(format1.df)}
#start_analysis(start_path)