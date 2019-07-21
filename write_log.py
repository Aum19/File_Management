import datetime
import pandas as pd

Default_Log_File = 'C:/Users/N381554/Desktop/MFT_work/Files_moved_log.txt'
sample = 'file_name,source,destination'
DEFAULT_CONFIG_PATH = 'C:/Users/N381554/Desktop/MFT_work/configuration_set.xlsx'


def write_to_file(log):
    # current_time|empId|file_name|source|destination
    current_time = datetime.datetime.now().strftime("%Y-%m-%d|%H:%M:%S")
    emp_id = 'coming_soon'
    temp = log.replace(',', '|')
    log_data = current_time+'|'+emp_id+'|'+temp
    # Append-adds at last
    with open(Default_Log_File, "a") as log_file:
        log_file.write(log_data+'\n')


def read_config():
    df = pd.read_excel(DEFAULT_CONFIG_PATH)
    # dropping incomplete configurations
    df = df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)
    config_lst = df.values.tolist()
    return config_lst


def write_error_log():
    pass


x = read_config()
