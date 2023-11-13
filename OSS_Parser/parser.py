

import pandas as pd
import os

class resultObj() :
    
    def __init__(self) -> None:
        pass
    
    
    
def __parse_repo(filename: str):
    xls = pd.ExcelFile(filename)

    # Now you can list all sheets in the file
    #xls.sheet_names
    # ['house', 'house_extra', ...]

    # to read just one sheet to dataframe:
    df = pd.read_excel(filename, sheet_name="Base Info")
    print(df)
    print('--------------------------')
    repo = df.to_dict()['Unnamed: 1'][6]
    fields = repo.split("--")
    branch = fields[0]
    fields2 = fields[1].split("/")
    repo_name = fields2[4]
    print(branch, repo_name)
    return branch, repo_name

def load_to_object(filename: str):
    

    # to read just one sheet to dataframe:
    df = pd.read_excel(filename, sheet_name="Code Scan")
    print(df)
    print('--------------------------')
    dict_data = df.to_dict()
    name =     version = dict_data['Name']
    version = dict_data['Version']
    base_version = dict_data['Version']

    print(name, version, base_version)

    # get repos: GIT REPOS


path = os.getcwd()+"/oss_result"
import os
for filename in os.listdir(path):
    if not filename.endswith("xlsx"):
        continue
    filename  =  os.path.join(path, filename)
    with open(filename, 'r') as f: # open in readonly mode
        load_to_object(filename)