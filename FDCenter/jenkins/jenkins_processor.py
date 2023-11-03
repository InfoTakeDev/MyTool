
import requests
import sys
from requests.packages import urllib3


RSS_ALL = "https://%s/view/entrypoints/job/%s-ondemand-pipeline-vxrail-build/rssAll"
URL = "osj-vxr-01-prd.cec.lab.emc.com"

def get_url(release_name: str) -> str:
    
    return RSS_ALL % (URL, release_name)


def prase_to_jenkins_object():
    pass

def parse_jenkins_content(content: str):
    pass
    # parse different build
    
        



def update_failed_build():
    RSS_FAIL = "https://%s/view/entrypoints/job/%s-ondemand-pipeline-vxrail-build/rssFailed"
               

def get_jenkins_content(release_name: str) -> (str, bool):
    urllib3.disable_warnings()
    ok = True
    endpoint = get_url("berwick")
    print("bart %s"%endpoint)
    token = '1173c0c5d01caa7f3023125a6c6cb741ea'
    
    #headers = {'Authorization': 'access_token %s' % token}
    auth    = ('bart_hsiao', '1173c0c5d01caa7f3023125a6c6cb741ea')
    
    response = requests.get(endpoint, auth=auth, verify=False)
    
    print(response.text)
    
    return response.text, response.ok

def get_jenkins_item_list():
    pass

# def pre_check() -> (str, bool):
#     result = ping.ping(URL) 
#     if result.ret_code != 0:
#         return "Can not find the host %s" % URL, False

