import requests
import codecs
import os
from bs4 import BeautifulSoup
import sys
import importlib

importlib.reload(sys)

global headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
server = 'http://www.xbiquge.la/'

book = 'http://www.xbiquge.la/5/5623/'

global save_path

save_path = 'E:\\py\\day3'
if os.path.exists(save_path) is False:
    os.makedirs(save_path)


def get_contents(chapter):
    req = requests.get(url=chapter)
    html = req.content
    html_doc = str(html, 'utf8')
    bf = BeautifulSoup(html_doc, 'html.parser')
    texts = bf.find_all('div', id='content')
    content = texts[0].text.replace('\xa0' * 4, '\n')
    return content


def write_txt(chapter, content, code):
    with codecs.open(chapter, 'a', encoding=code) as f:
        f.write(content)


def main():
    res = requests.get(book, headers=headers)
    html = res.content
    html_doc = str(html, 'utf8')
    soup = BeautifulSoup(html_doc, 'html.parser')
    a = soup.find('div', id='list').find_all('a')
    print('总章数：%d' % len(a))
    for each in a:
        try:
            chapter = server + each.get('href')
            content = get_contents(chapter)
            chapter = save_path + "/" + each.string.replace("?", "") + ".txt"
            write_txt(chapter, content, 'utf8')
        except Exception as e:
            print(e)


# 爬取小说网站并下载到本地
if __name__ == '__main__':
    main()
