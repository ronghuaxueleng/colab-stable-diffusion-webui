import os
import json
import requests

from chilloutai.prompts import Chilloutai
from multiprocessing import Pool, cpu_count
import urllib.request, urllib.error, urllib.parse

baseUrl = "https://chilloutai.xyz/api/trpc/task.allpic?batch=1&input={}"

payload = {}
headers = {
    'authority': 'chilloutai.xyz',
    'sec-ch-ua': '"Chromium";v="21", " Not;A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    'content-type': 'application/json',
    'accept': '*/*',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://chilloutai.xyz/nsfw',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': 'NEXT_LOCALE=en; __Secure-next-auth.session-token=248c1b10-600c-40c3-a4c1-3b1a961956ee; __Host-next-auth.csrf-token=615514725f520dd217dc322d83905790fd132a2c38ab5ccf4ab0f2f3e3466c67%7C32dc286d8c914c8142fdebc488aec0e2911810f09246f1ff8194ee9f61f96458; __Secure-next-auth.callback-url=https%3A%2F%2Fchilloutai.xyz; __Secure-next-auth.session-token=248c1b10-600c-40c3-a4c1-3b1a961956ee'
}


def get_data_to_db(nextCursor=None, page=1, stop_page=None):
    input = '{"0":{"json":{"style":"all","template_name":"chilloutmix","cursor":' + str(nextCursor) + '}}}'
    if nextCursor is None:
        input = '{"0":{"json":{"style":"all","template_name":"chilloutmix","cursor":null},"meta":{"values":{"cursor":["undefined"]}}}}'
    url = baseUrl.format(urllib.parse.quote(input))
    response = requests.request("GET", url, headers=headers, timeout=10)
    data = json.loads(response.text)
    if len(data) > 0:
        res = data[0]['result']['data']['json']
        datas = res['data']
        for data in datas:
            id = data['id']
            image_url = data['image_url']
            data_input = data['input']
            data_input['id'] = id
            data_input['image_url'] = image_url
            try:
                Chilloutai.insert(data_input).execute()
            except Exception as e:
                if 'UNIQUE constraint failed: chilloutai.id' not in e.args:
                    print(data_input)
                    print(e)
                pass
        nextCursor = res['nextCursor']
        if not page == stop_page and nextCursor is not None:
            page = page + 1
            get_data_to_db(nextCursor, page, stop_page)


def request_image(url, image_name, PROXIES=None):
    print(("正在下载 %s" % image_name))
    try:
        os.makedirs("images", exist_ok=True)
        req = urllib.request.Request(url)
        req.add_header('User-Agent', headers['user-agent'])
        req.add_header('Cache-Control', 'no-cache')
        req.add_header('Accept', '*/*')
        req.add_header('Accept-Encoding', 'gzip, deflate')
        req.add_header('Connection', 'Keep-Alive')

        if PROXIES is not None:
            opener = urllib.request.build_opener(urllib.request.ProxyHandler(PROXIES))
            urllib.request.install_opener(opener)

        resp = urllib.request.urlopen(req)

        respHtml = resp.read()
        path = 'images/%s' % image_name

        binfile = open(path, "wb")
        binfile.write(respHtml)

        binfile.close()
        Chilloutai.update(grabState=1).where(Chilloutai.image_url == url).execute()
        print(("%s 下载成功" % image_name))
        return True
    except Exception as e:
        print(e)
        print(("%s 下载失败" % image_name))
        return False


def download_image(proxy=None):
    images = Chilloutai.select().where(Chilloutai.grabState != 1).execute()
    if len(images) > 0:
        cpu_counts = cpu_count()
        print("cup数量：{}".format(cpu_counts))
        pool = Pool(processes=cpu_counts)
        for img in images:
            request_image(img.image_url, img.id + ".png", PROXIES=proxy)
        pool.close()
        pool.join()  # 运行完所有子进程才能顺序运行后续程序


if __name__ == '__main__':
    # get_data_to_db(stop_page=None)
    PROXIES = {
        'http': 'http://127.0.0.1:1080',
        'https': 'http://127.0.0.1:1080'
    }
    download_image(PROXIES)
