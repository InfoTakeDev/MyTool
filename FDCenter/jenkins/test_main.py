import sys
sys.path.append('/home/bart/workspace/MyTool')

from FDCenter.jenkins.jenkins_processor import parse_jenkins_content

from FDCenter.jenkins.testdata import jenkinsXML

if __name__ == "__main__":
        
    # get_jenkins_content("berwick")
    print("--------------")
    parse_jenkins_content(jenkinsXML)
    print("--------------")
