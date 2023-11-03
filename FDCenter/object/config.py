import os
import yaml

class ReleaseConfig:
    
    def __init__(self, filename: str) -> None:
        with open(filename, "r") as stream:
            config = yaml.safe_load(stream)
        
        self.__release_name = config['RELEASE_NAME']
        self.__release_version = config['RELEASE_VERSION']
        self.__vrel_cmd = config['VREL_CMD']
        self.__github_user = config['GITHUB_USER']
        self.__github_token = config['GITHUB_TOKEN']
           
    @property
    def release_name()-> str:
        pass

    @property
    def release_version()->str:
        pass

    @property
    def release_version()->str:
        pass

    @property
    def github_user()->str:
        pass

    @property
    def github_token()->str:
        pass

    @property
    def vrel_cmd()->str:
        pass


    def __str__(self) -> str:
        output = f'''
RELEASE_NAME: {self.__release_name}
RELEASE_VERSION: {self.__release_version}
VREL_CMD: {self.__vrel_cmd}
GITHUB_USER: {self.__github_user}
GITHUB_TOKEN: {self.__github_token}'''
        return output

if __name__ == "__main__":
    
    cur_path = os.path.dirname(os.path.abspath(__file__))
    rel_config = ReleaseConfig(f"{cur_path}/../releaseInfo.yml")
    
    print(rel_config)