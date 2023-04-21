import json

import requests

from diprompt.prompts import Prompt

baseUrl = "https://api.diprompt.com/images?keyword=&page={}&size=50"
headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '"Chromium";v="21", " Not;A Brand";v="99"',
    'Accept': 'application/json, text/plain, */*',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    'Origin': 'https://www.diprompt.com',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://www.diprompt.com/',
    'Accept-Language': 'zh-CN,zh;q=0.9'
}


def get_data_from_diprompt(images, page=1):
    if images is None:
        images = list()
    url = baseUrl.format(page)
    response = requests.request("GET", url, headers=headers)
    data = json.loads(response.text)
    if len(data) > 0:
        images.extend(data)
        page = page + 1
        get_data_from_diprompt(images, page)


def get_data_to_db(page=1):
    url = baseUrl.format(page)
    response = requests.request("GET", url, headers=headers)
    data = json.loads(response.text)
    try:
        Prompt.insert(data).execute()
    except Exception as e:
        exit(1)

    if len(data) > 0:
        page = page + 1
        get_data_to_db(page)


def save_to_json_file():
    images = list()
    get_data_from_diprompt(images, 1)
    with open('images.json', 'w', encoding='utf-8') as f:
        json.dump(images, f, ensure_ascii=False)


def read_images_to_db():
    with open('images.json', 'r', encoding='utf-8') as f:
        images = json.load(f)
        for image in images:
            try:
                Prompt.insert(image).execute()
            except Exception as e:
                print(e)


if __name__ == '__main__':
    get_data_to_db()
