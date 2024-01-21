# -*- coding: utf-8 -*-
import os

import requests
import json

from jinja2 import Environment, PackageLoader

from statistics import Models

url = "https://liblib-api.vibrou.com/api/www/model/list?timestamp=1705544639924"

payload = json.dumps({
    "pageNo": 1,
    "pageSize": 10,
    "uuid": None,
    "status": -2,
    "type": 0
})
headers = {
    'authority': 'liblib-api.vibrou.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-type': 'application/json',
    'dnt': '1',
    'origin': 'https://www.liblib.art',
    'referer': 'https://www.liblib.art/userpage/02749e73219936808ff45d707b2d01cf/publish',
    'sec-ch-ua': '"Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'token': 'd1894681b7c5438b9051b840431e9b59',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.160 Safari/537.36',
    'webid': '1701832232487tengpuwz'
}

response = requests.request("POST", url, headers=headers, data=payload)

content = json.loads(response.text)
for data in content['data']['list']:
    model = {}
    model['id'] = data['id']
    model['name'] = data['name']
    model['runCount'] = data['runCount']
    model['downloadCount'] = data['downloadCount']
    Models.insert(model).execute()
models = Models.select(Models.id, Models.name).group_by(Models.id).execute()
env = Environment(loader=PackageLoader('resources', 'templates'))
template_name = 'index.html'
template = env.get_template(template_name)
html = template.render(models=models)
current_dir = os.getcwd()
output_dir = os.path.join(current_dir, "./templates/")
if not os.path.exists(output_dir):
    os.mkdir(output_dir)
os.chdir(output_dir)

fo = open(template_name, "w", encoding='utf-8')
fo.writelines(html)
fo.close()
os.chdir(current_dir)
print(f"create {template_name}: finish")