import os
import yaml
from datetime import date

vrel_cmd = '/root/workspace/poxio/cmd/vrel/vrel'
github_user = 'bart_hsiao'
github_token = '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'
release = 'berwick'

# list of image to tag
images = [
    # LCM
    'microservice/vlcm',
    'microservice/hsm',
    # S12Y
    'microservice/event-history-service',
    'microservice/event-service',
    'microservice/rcs-service',
    # STORAGE
    'microservice/storage-service',
    'microservice/storage-ops-service',
    # Day2
    'microservice/ms-day2',
    'microservice/cms-service',
    "microservice/compute-service",
    'microservice/node-service',
    # UI
    'microservice/plugin-gateway-service',
    # PS
    'microservice/nim-service'
]

if not os.path.exists("./specs"):
    os.makedirs("./specs")

today = date.today().strftime('%Y-%m-%d')
spec_file_name = f"./specs/{release}-{today}.yaml"

# join list with , 
command_create_spec = f'{vrel_cmd} microservice create spec-info --bump-microservice-list {",".join(images)} --github-token {github_token} --github-user {github_user} --release {release} --spec {spec_file_name} -m major --skip-no-new-commit'
command_tag_repo = f'{vrel_cmd} microservice publish image-tags --spec {spec_file_name}'
command_create_pr = f'{vrel_cmd} microservice publish microservice-release --watch --spec {spec_file_name}'

# create spec-info
os.system(command_create_spec)

# parse yaml
with open(spec_file_name) as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

if data['repository_tags_to_create'] == {}:
    print('No new commit, skip bump version process')
    exit()

os.system(command_tag_repo)

# create PR
os.system(command_create_pr)