import pandas as pd
import filecmp
from functools import lru_cache

DUPLICATE_EXCEL = 'posibble_duplicates.xlsx'
FINAL_DUPLICATES = 'final_duplicates.xlsx'

# Filter files by size and format
def duplicate_filter(df):
    df['Compare_Group'] = None
    df = df.sort_values(by=['Format', 'Size'],ascending=[True,False])
    duplicate_file_list = ['*'*100+'\n DUPLICATE FILES \n'+'*'*100]
    current_list = list()
    current_group = 0
    last_size = last_name = ''
    for index, row in df.iterrows():
        if last_size==row['Size']:
            if len(current_list)==0:
                current_group += 1
                current_list.append(str(last_size)+' :'+str(last_name)+' | '+str(last_full_path))
                current_list.append(str(row['Size'])+' :'+str(row['File_name'])+' | '+str(row['Path']))
                df.loc[index, 'Compare_Group'] = current_group
                df.loc[last_index, 'Compare_Group'] = current_group
            else:
                current_list.append(str(row['Size'])+' :'+str(row['File_name'])+' | '+str(row['Path']))
                df.loc[index, 'Compare_Group'] = current_group

        else:
            if len(current_list) != 0:
                duplicate_file_list.extend(current_list)
                duplicate_file_list.append('-'*40+' Group :'+str(current_group)+'-'*40)
                current_list = []
            df.loc[index, 'Compare_Group'] = 0

        last_size = row['Size']
        last_name = row['File_name'] 
        last_full_path = row['Path']
        last_index = index

    store_in_excel(df, DUPLICATE_EXCEL)
    return duplicate_file_list

#Store results to excel
def store_in_excel(df, name):
    df.to_excel(name)

#Compare files line by line
@lru_cache(maxsize=5000)
def detail_comparision():
    try:
        df = pd.read_excel(DUPLICATE_EXCEL)
    except:
        return 

    df = df.sort_values(by=['Compare_Group', 'Path'],ascending=[True,False])
    grouped = df.groupby('Compare_Group')
    df.reset_index(inplace=True)
    df_duplicates = pd.DataFrame(columns=['Index', 'File_1', 'File_2'])

    for name, group in grouped:
         
        for index, rows in group.iterrows():
            for i, r in group.iterrows():
                if index != i and name != 0:
                    rx = filecmp.cmp(rows['Path'], r['Path'],shallow=False)
                    if rx and r['Path'] not in df_duplicates.File_1.unique():
                        df_duplicates = df_duplicates.append({'Index': index*i, 'File_1': rows['Path'], 'File_2': r['Path']}, ignore_index=True)
    
    df_duplicates.drop_duplicates('Index', inplace = True)
    store_in_excel(df_duplicates, FINAL_DUPLICATES)
    
    return df_duplicates
