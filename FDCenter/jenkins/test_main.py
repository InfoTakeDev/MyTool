import sys
sys.path.append('/home/bart/workspace/MyTool')

from FDCenter.jenkins.jenkins_processor import JenkinsInfo
from FDCenter.object.gi import GI

# from FDCenter.jenkins.testdata import jenkinsXML, jenkinsXML2

if __name__ == "__main__":
        
    print("--------------")
    jenkin = JenkinsInfo("berwick")
    # jenkin.update_cache()
    obj_list = jenkin.get_jenkins_obj_list()
    
    print("--------------")
    for item in obj_list:
        # print("%d success=%s" % (item.build_num, item.success))
        print(item)
        gi = GI(item)
        gi.update_componets()
        
        break
