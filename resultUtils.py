import json

with open("result.json", "r") as f:
    content = json.loads(f.read())
    res = dict()
    for data in content['data']['list']:
        id = data['id']
        name = data['name']
        runCount = data['runCount']
        downloadCount = data['downloadCount']
        one = set()
        one.add({
            'id': id,
            'name': name,
            'runCount': runCount,
            'downloadCount': downloadCount,
        })
        res[id] = one
    with open("statistics_result.json", "w", encoding='utf-8') as f:
        json.dump(res, f, ensure_ascii=False)
    print(res)