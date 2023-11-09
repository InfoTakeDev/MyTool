import os
import requests
from datetime import datetime
from requests.packages import urllib3
# from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
from FDCenter.object.gi import JenkinsObj


URL = "osj-vxr-01-prd.cec.lab.emc.com"

RSS_ALL = "https://%s/view/entrypoints/job/%s-ondemand-pipeline-vxrail-build/rssAll"
RSS_FAIL = "https://%s/view/entrypoints/job/%s-ondemand-pipeline-vxrail-build/rssFailed"


CACHE_FOLDER = "./cache"


class JenkinsInfo :


    def __init__(self, release_name) -> None:
        self.__all_url = RSS_ALL % (URL, release_name)
        self.__fail_url = RSS_FAIL % (URL, release_name)
        # self.__url = HOMEPAGE % (URL, release_name)


    def __update_all_cache(self):
        try:
            content, _ = self.__get_url_content(self.__all_url)
            tmp = bytes(content, 'utf-8')

            with open(f"{CACHE_FOLDER}/all_job.txt", "wb") as fout:
                fout.write(tmp)
        except IOError as e:
            print("Write to all_jbo.txt failed.", e)


    def __update_fail_cache(self):
        try:
            content, _ = self.__get_url_content(self.__fail_url)
            tmp = bytes(content, 'utf-8')
            with open(f"{CACHE_FOLDER}/failed_job.txt", "wb") as fout:
                fout.write(tmp)
        except IOError as e:
            print("Write to failed_job.txt failed.", e)


    def update_cache(self) -> None:
        # get from url and update cache file
        if not os.path.exists(CACHE_FOLDER):
            os.makedirs(CACHE_FOLDER)
        self.__update_all_cache()
        self.__update_fail_cache()


    def __load_all_job_cache(self) -> str:
        content = ""
        with open(f"{CACHE_FOLDER}/all_job.txt", "rb",) as fin:
            content = fin.read()
        return str(content)


    def __load_failed_job_cache(self) -> str:
        content = ""
        with open(f"{CACHE_FOLDER}/failed_job.txt", "rb") as fin:
            content = fin.read()
        return str(content)


    def __update_from_title(self, title: str, obj: JenkinsObj):

        # berwick-ondemand-pipeline-vxrail-build #94-7.0.510-official-vxm:28315534-vxrail-system:28315535-user:\
        # Timer Trigger (stable)
        title = title.split(' ', 1)[-1]
        title = title[:title.index('(')].strip()

        fields = title.split('-')
        # ['#94', '7.0.510', 'official', 'vxm:28315534', 'vxrail', 'system:28315535', 'user:Timer Trigger']
        print(fields)
        build_num = fields[0][1:]
        obj.build_num = int(build_num)

        if len(fields) < 7:
            return
        
        ver = fields[1]
        vxm_ver = fields[3].split(":")[-1]
        vxrail_sys_ver = fields[5].split(":")[-1]
        user = fields[6].split(":", 1)[-1]
        gi_name = f'{ver}-{vxrail_sys_ver}'
        vxm_name = f'{ver}-{vxm_ver}'


        obj.build_num = int(build_num)
        obj.gi_build_name = gi_name
        obj.vxm_build_name = vxm_name
        obj.trigger = user
        obj.auto_trigger = True if user == "Timer Trigger" else False
        obj.vxm_version = vxm_ver
        obj.vxrail_system_version = vxrail_sys_ver


    def __prase_to_jenkins_object(self, item) -> JenkinsObj:

        obj = JenkinsObj()

        link = item('link').attr('href')
        date_str = item('updated').text()
        # 2023-11-02T13:35:08Z
        update = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
        title = item('title').text()
        self.__update_from_title(title, obj)
        obj.update_time = update
        obj.link = link
        return obj


    def __get_failed_build_number(self) -> list[str]:
        
        content = self.__load_failed_job_cache()

        failed_build_number_list = []
        doc = pq(content)
        entries = doc('entry').items()
        for item in entries:
            title = item('title').text()
            print("failed title", title)
            build_num = title.split(' ', 2)[1][1:]
            build_num = build_num.split('-')[0]
            failed_build_number_list.append(build_num)
        return failed_build_number_list


    def __get_jenkins_object_dict(self) -> dict[str, JenkinsObj]:

        content = self.__load_all_job_cache()
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
        return object_dict


    def get_jenkins_obj_list(self) -> list:
        
        build_list = self.__get_failed_build_number()
        print("failed list", build_list)
        object_dict = self.__get_jenkins_object_dict()
        for build in build_list:
            if build in object_dict:
                object_dict[build].success = False
        
        return sorted(object_dict.values(), key=lambda obj: obj.build_num, reverse=True)
            

    def __get_url_content(self, endpoint: str) -> (str, bool):
        urllib3.disable_warnings()
        user = 'bart_hsiao'
        token = '1173c0c5d01caa7f3023125a6c6cb741ea'
        auth    = (user, token)
        response = requests.get(endpoint, auth=auth, verify=False)
        print(response.text)
        return response.text, response.ok


    # def pre_check() -> (str, bool):
    #     result = ping.ping(URL) 
    #     if result.ret_code != 0:
    #         return "Can not find the host %s" % URL, False

