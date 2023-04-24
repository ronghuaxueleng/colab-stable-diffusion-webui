import json
import os

import requests
from diprompt.prompts import Prompt
from multiprocessing import Pool, cpu_count
import urllib.request, urllib.error, urllib.parse

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


def request_image(url, image_name):
    print(("正在下载 %s" % image_name))
    try:
        os.makedirs("images", exist_ok=True)
        req = urllib.request.Request(url)
        req.add_header('User-Agent', headers['User-Agent'])
        req.add_header('Cache-Control', 'no-cache')
        req.add_header('Accept', '*/*')
        req.add_header('Accept-Encoding', 'gzip, deflate')
        req.add_header('Connection', 'Keep-Alive')

        # if USE_PROXIES == 'true':
        #     opener = urllib.request.build_opener(urllib.request.ProxyHandler(PROXIES))
        #     urllib.request.install_opener(opener)

        resp = urllib.request.urlopen(req)

        respHtml = resp.read()
        path = 'images/%s' % image_name

        binfile = open(path, "wb")
        binfile.write(respHtml)

        binfile.close()
        Prompt.update(grabState=1).where(Prompt.url == url).execute()
        print(("%s 下载成功" % image_name))
        return True
    except Exception as e:
        print(e)
        print(("%s 下载失败" % image_name))
        return False


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
    response = requests.request("GET", url, headers=headers, timeout=10)
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


def download_image():
    images = Prompt.select().where(Prompt.grabState != 1).execute()
    if len(images) > 0:
        cpu_counts = cpu_count()
        print("cup数量：{}".format(cpu_counts))
        pool = Pool(processes=cpu_counts)
        for img in images:
            request_image(img.url, img.imageId + ".png")
        pool.close()
        pool.join()  # 运行完所有子进程才能顺序运行后续程序


if __name__ == '__main__':
    # get_data_to_db()
    download_image()
