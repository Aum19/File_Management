import System_Analysis
import Model
import Scan_Duplicates

def start_config():
    Model.start_config()

def analyze(path):
    scan_duplicate_dict = System_Analysis.start_analysis(path)
    return scan_duplicate_dict

def deep_analysis():
    df  = Scan_Duplicates.detail_comparision()
    return df