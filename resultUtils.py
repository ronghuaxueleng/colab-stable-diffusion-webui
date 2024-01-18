import json

from statistics import Models

with open("result.json", "r") as f:
    content = json.loads(f.read())
    res = dict()
    for data in content['data']['list']:
        model = {}
        model['id'] = data['id']
        model['name'] = data['name']
        model['runCount'] = data['runCount']
        model['downloadCount'] = data['downloadCount']
        Models.insert(model).execute()
