
import os
import requests
from datetime import datetime
from requests.packages import urllib3
from pyquery import PyQuery as pq



REPO_PREFIX = "https://eos2git.cec.lab.emc.com/"

POXIO_COMPONENT_URL = "http://buildd.poxio.odc-vxrail-deep-prod-dur.k8s.cec.lab.emc.com/api/v1/marvin/%s"

CACHE_FOLDER = "./cache"


from datetime import datetime


class JenkinsObj:
    
    def __init__(self) -> None:
        self.build_num: int = ""
        self.gi_build_name: str = ""
        self.vxm_build_name: str = ""
        self.update_time: datetime = None
        self.link: str = ""
        self.success: bool = True
        self.vxm_version: str = ""
        self.vxrail_system_version: str = ""
        self.auto_trigger: bool = True
        self.trigger: str = "Timer"

    def __str__(self) -> str:
        ret = f'''{self.build_num}
{self.gi_build_name}
{self.vxm_build_name}
{self.update_time}
{self.link}
{self.vxm_version}
{self.vxrail_system_version}
{self.auto_trigger}
{self.trigger}
{self.success}'''
        return ret

class Component():
    
    def __init__(self, name: str) -> None:
        self.name : str = ""
        self.tag: str = ""
        self.latest_repo_tag: str = ""
        self.latest_microservice_release_tag = ""

class GI:
    
    def __init__(self, obj :type[JenkinsObj]) -> None:
        
        self.name = obj.gi_build_name
        self.auto_trigger = obj.auto_trigger
        self.jenkins_link = obj.link
        self.update_time = obj.update_time
        self.build_success = obj.success
        self.vxm_build_name = obj.vxm_build_name
        self.componet_list : list[Component] 
    
    # @property
    # def name(self) -> str:
    #     return self.name
    
    @property
    def ps_version(self) -> str:
        return ""
    
    @property
    def vib_version(self) -> str:
        return ""
    
    def __get_component_list(self, content: str) -> list[Component]:
        object_dict = dict()
        doc = pq(content)
        entries = doc('entry').items()
        # first entry is for header only. Skip it
        first = True
        for item in entries:
            if first:
                first = False
                continue
            obj = self.__prase_to_jenkins_object(item)
            object_dict[str(obj.build_num)] = obj
        return 
    
    def __cache_exist(self):
        return os.path.exists(f'{CACHE_FOLDER}/{self.vxm_build_name}')
    
    def __save_to_cache(self, content):
        if not os.path.exists(CACHE_FOLDER):
            os.makedirs(CACHE_FOLDER)
            
        try:
            tmp = bytes(content, 'utf-8')
            with open(f"{CACHE_FOLDER}/{self.vxm_build_name}", "wb") as fout:
                fout.write(tmp)
        except IOError as e:
            print("Write to all_jbo.txt failed.", e)
    
    def __load_from_cache(self):
        content = ""
        with open(f"{CACHE_FOLDER}/{self.vxm_build_name}", "rb",) as fin:
            content = fin.read()
        return str(content)
    
    def update_componets(self):
        
        if not self.__cache_exist():
            endpoint = POXIO_COMPONENT_URL % self.vxm_build_name
            urllib3.disable_warnings()
            user = 'bart_hsiao'
            token = '1173c0c5d01caa7f3023125a6c6cb741ea'
            auth    = (user, token)
            response = requests.get(endpoint, auth=auth, verify=False)
            if not response.ok:
                return False
            print(response.text)
            self.__save_to_cache(response.text, )
        
        content = self.__load_from_cache()
        print(content)
        
        
        
        
        comp = self.__get_component_list(content)
        self.componet_list.append(comp)
        
        
        return True