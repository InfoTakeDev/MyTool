

import pandas as pd
import os

class resultObj() :
    
    def __init__(self, name="", version="", base_version="", result="") -> None:
        self.name = name
        self.version = version
        self.base_version = base_version        
        self.result = result
        
    def can_skip(self) -> (str, bool):
        
        msg = ""
        
        if self.result == "PASS":
            return msg, True
        
        base_version_list = self.base_version.split(',')
        
        if not self.version or not self.base_version:
            return True
        
        for bv in base_version_list:
            if ((self.version[1:] == bv) or 
                (self.version == bv[1:])):
                return "", True
        
        msg = f'{self.name} \tversion not match:{self.version}\t{self.base_version}'
        
        return msg, False
    
    def __str__(self) -> str:
        return f'''{self.name}
{self.version}
{self.base_version}        
{self.result}
'''
    
    
def parse_repo(filename: str):
    xls = pd.ExcelFile(filename)

    # to read just one sheet to dataframe:
    df = pd.read_excel(filename, sheet_name="Base Info")
    repo = df.to_dict()['Unnamed: 1'][6]
    fields = repo.split("--")
    branch = fields[0]
    fields2 = fields[1].split("/")
    repo_name = fields2[4]
    print(branch, repo_name)
    return branch, repo_name


# def continue_or_not(version, base_version, pass):
    


def load_to_object(filename: str) -> list[resultObj]:
    # to read just one sheet to dataframe:
    df = pd.read_excel(filename, sheet_name="Code Scan")
    dict_data = df.to_dict()

    name_list = dict_data['Name']
    version_list = dict_data['Version']
    base_version_list = dict_data['Version']
    pass_list = dict_data['Result']
    obj_list = []
    i = 0
    
    for _ in name_list:
        obj = resultObj(name_list[i], version_list[0], base_version_list[i],
                        pass_list[i])
        obj_list.append(obj)
        i += 1
    return obj_list


path = os.getcwd()+"/oss_result"
import os
for filename in os.listdir(path):
    if not filename.endswith("xlsx"):
        continue
    filename  =  os.path.join(path, filename)
    with open(filename, 'r') as f: # open in readonly mode
        branch, repo = parse_repo(filename)
        obj_list = load_to_object(filename)
        print(branch, repo)
        for obj in obj_list:
            if not obj.can_skip():
                print(obj)