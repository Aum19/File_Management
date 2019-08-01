import System_Analysis
import Model
import Scan_Duplicates
import Directory_health

def start_config():
    Model.start_config()

def analyze(path):
    scan_duplicate_df = System_Analysis.start_analysis(path)
    return scan_duplicate_df

def deep_analysis():
    df  = Scan_Duplicates.detail_comparision()
    return df

def directory_health():
    Directory_health.create_features()