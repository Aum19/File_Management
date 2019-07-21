import numpy as np
import pandas as pd
from Levenshtein import levenshtein_lru, levenshtein_no_lru
import Recommend
import timeit
TEMP = 'C:/Users/N381554\Desktop\MFT_work'
df = pd.read_excel('directory_df.xlsx')
COHESION_ALPHA = 0.5
FEATURES_CSV = 'test.xlsx'
def create_features(path=None):
    df = pd.read_excel('directory_df.xlsx')
    #print(df['Folder_path'].unique())
    df_folders = pd.DataFrame(columns=['Folder_path'])
    df_folders['Folder_path'] = df['Folder_path'].unique()
    
    for i in df['Format'].unique():
        df_folders[str(i)+'_population'] = ''
        df_folders[str(i)+'_volume'] = ''
    
    df_folders = df_folders.set_index(['Folder_path'])
    d = df['Folder_path'].value_counts().to_dict()
    a = list()
    
    for path in df['Folder_path'].unique():
        for f_type in df['Format'].unique():
            temp = df[df['Folder_path']==path]
            temp1 = temp[temp['Format']==f_type]['Size_MB'].median()
            temp = temp[temp['Format']==f_type]['Format'].value_counts()
            if len(temp)>0:
                temp = int(temp) 
            else:
                temp = 0
                temp1 = 0
            x = temp/d.get(path)
            df_folders.at[path,str(f_type+'_population')] = x
            df_folders.at[path,str(f_type+'_volume')] = temp1
        
        df_folders.at[path,'Median_size'] = df[df['Folder_path']==path]['Size_MB'].median()
    #Adding the Only_file_name and Folder_distance columns to df
    df = add_column_folder_dist(df)
    unsafe_df = df[df['Folder_distance']>0]
    safe_df = df[df['Folder_distance']==0]
    df_dict = neighbour_cohesion(safe_df, unsafe_df, df)
    safe_df = df_dict.get('safe_df')
    unsafe_df = df_dict.get('unsafe_df')

    unsafe_df.to_excel('unsafe.xlsx')
    safe_df.to_excel('safe.xlsx')
    df.to_excel('modified_directory_df.xlsx')
    df_folders.to_excel('test.xlsx')
    print_stats(safe_df,unsafe_df,df)

def add_column_folder_dist(df):
    df['Only_file_name'] = df.File_name.str.split('.')
    df.Only_file_name = df.Only_file_name.str[:1]
    df.Only_file_name = df.Only_file_name.agg(lambda x: ','.join(map(str,x)))
    df['Folder_distance'] = ''
    #TIMEIT
    start_time = timeit.default_timer()
    for index, row in df.iterrows():
        #Checks if folder name is in File name
        if row['Parent'] in str(row['Only_file_name']):
            distance = 0
            df.loc[index, 'Folder_distance'] = distance
        else:
            substr = ''
            score = 0
            #Checks for parts of folder name in file name
            #More strict approach possible in future
            for chars in str(row['Parent']):
                substr += chars
                if substr in row['File_name']:
                    score += 1
                else:
                    break
            if score > 0.25*len(str(row['Parent'])):
                distance = 0
            else:
                distance = levenshtein_no_lru(str(row['Parent']),str(row['Only_file_name']))
    
            df.loc[index, 'Folder_distance'] = distance
    #TIMER        
    elapsed = timeit.default_timer() - start_time
    print('add_column_folder'+str(elapsed))
    return df

def neighbour_cohesion(safe_df, unsafe_df, df):
    #TIMER
    start_time = timeit.default_timer()

    unsafe_df = unsafe_df.assign(Cohesion_flag=True)
    safe_df = safe_df.assign(Cohesion_flag=False) 
    for row in unsafe_df.itertuples():
        neighbours = list(df[df['Folder_path']==row.Folder_path]['File_name'])
        neighbours.remove(row.File_name)
        current_file = row.File_name
        dist = 0
        for n in neighbours:
            try:
                dist += levenshtein_lru(current_file,n)
            except:
                dist += levenshtein_no_lru(current_file,n)

        neighbours_count = len(neighbours) if len(neighbours)>0 else 1
        cohesion_threshold = (dist/neighbours_count) > COHESION_ALPHA*len(current_file)
        unsafe_df.at[row.Index, 'Cohesion_flag'] = cohesion_threshold
        now_safe = unsafe_df[unsafe_df['Cohesion_flag']==False]
        safe_df = safe_df.append(now_safe, ignore_index=True)
        unsafe_df = unsafe_df[unsafe_df['Cohesion_flag']==True]
    
    #TIMER        
    elapsed = timeit.default_timer() - start_time
    print('neighbour_cohesion'+str(elapsed))
    return {'df': df, 'safe_df': safe_df, 'unsafe_df': unsafe_df}

#Create a graph here
def print_stats(safe_df, unsafe_df,df,out_file='results.txt'):
    fit_memory = safe_df['Size_MB'].sum()
    unfit_memory = unsafe_df['Size_MB'].sum()
    total_memory = df['Size_MB'].sum()
    share_fit_memory = (fit_memory/total_memory)*100
    share_unfit_memory = (unfit_memory/total_memory)*100
    fit_count = len(safe_df)
    unfit_count = len(unsafe_df)
    total_count = len(df)
    share_fit_count =  (fit_count/total_count)*100
    share_unfit_count = (unfit_count/total_count)*100
    results = '\nDirectory Health\n'
    results += '-'*100
    results += '\n'
    results += 'Fit Memory(MB):   {0}   Fit Memory %:   {1}% \n '.format(str(fit_memory), str(share_fit_memory))
    results += 'Unfit Memory(MB): {0}   Unfit Memory %: {1}% \n '.format(str(unfit_memory), str(share_unfit_memory))
    results += '-'*100
    results += '\n'
    results += 'Fit Files:   {0}   Fit Count %:   {1}% \n '.format(str(fit_count), str(share_fit_count))
    results += 'Unfit Count: {0}   Unfit Count %: {1}% \n '.format(str(unfit_count), str(share_unfit_count))
    results += '-'*100
    with open(out_file, "a") as results_file:
        results_file.write(results)

    #Recommend.match(unsafe, df, FEATURES_CSV)
    

create_features()
