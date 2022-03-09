# coding=utf-8
# !/usr/bin/python
import random
import time

import requests
import os
import bs4
from bs4 import BeautifulSoup
import sys
import importlib

importlib.reload(sys)

mock_headers = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0",
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
]

global headers
headers = {'User-Agent': random.choice(mock_headers)}
global save_path
save_path = 'E:\\py\\day1'
targetUrl = 'https://mmzztt.com/beauty'


def createFile(file_path):
    if os.path.exists(file_path) is False:
        os.makedirs(file_path)
    os.chdir(file_path)


def download(page_no, file_path):
    global headers
    res_sub = requests.get(page_no, headers=headers)
    soup_sub = BeautifulSoup(res_sub.text, 'html.parser')
    all_a = soup_sub.find('div', class_='g-list-beauty').find_all('a', target='_blank')
    count = 0
    for a in all_a:
        count = count + 1
        if (count % 2) == 0:
            headers = {'User-Agent': random.choice(mock_headers)}
            print('内存第几页:' + str(count))
            href = a.attrs['href']
            print('套图地址:' + href)
            res_sub1 = requests.get(href, headers=headers)
            soup_sub1 = BeautifulSoup(res_sub1.text, 'html.parser')

            try:
                #     pic_max = soup_sub1.find('div', class_='pagenavi').find_all('span')[6].text
                #     print('套图数量: ' + pic_max)
                #     for j in range(1, int(pic_max) + 1):
                #         time.sleep(random.randint(1, 3))
                #         headers = {'User-Agent': random.choice(mock_headers)}
                #         href_sub = href + '/' + str(j)
                #         print('图片地址:' + href_sub)
                #         res_sub2 = requests.get(href_sub, headers=headers)
                #         soup_sub2 = BeautifulSoup(res_sub2.text, 'html.parser')
                # img = soup_sub2.find('div', class_='main-image').find('img')
                img = soup_sub1.find('figure', class_='uk-inline').find('img')
                time.sleep(random.randint(1, 3))
                if isinstance(img, bs4.element.Tag):
                    url = img.attrs['src']
                    array = url.split('/')
                    file_name = array[len(array) - 1]
                    # 防盗链
                    headers = {'User-Agent': random.choice(mock_headers), 'Referer': url}
                    img = requests.get(url, headers=headers)
                    print('开始保存图片:' + img)
                    f = open(file_name, 'ab')
                    f.write(img.content)
                    print(file_name + '图片保存成功')
                    f.close()
            except Exception as e:
                print(e)


def main():
    res = requests.get(targetUrl, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    createFile(save_path)
    img_max = soup.find('nav', class_='m-pagination').find_all('a')[2].text
    print('总页数:' + img_max)
    for i in range(1, int(img_max) + 1):
        if i == 1:
            page = targetUrl
        else:
            page = targetUrl + 'page/' + str(i)
        filename = 'E:\\py\\day1\\1'
        createFile(filename)
        download(page, filename)


# 爬取网络图片并下载
if __name__ == '__main__':
    main()
