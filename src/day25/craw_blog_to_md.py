import codecs
import os.path
import random
import re
import sys
import time

import requests
from bs4 import BeautifulSoup
from itertools import chain
import html2text as ht

# 越多越好
blog_headers = [
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
# 给请求指定一个请求头来模拟chrome浏览器
global headers
headers = {'User-Agent': random.choice(blog_headers)}

# Markdown中图片语法 ![](url) 或者 <img src='' />
img_patten = r'!\[.*?\]\((.*?)\)|<img.*?src=[\'\"](.*?)[\'\"].*?>'


def get_html(blog):
    res = requests.get(blog, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    title = soup.find(class_='postTitle').text
    title = title.strip()
    article = soup.find('div', class_='blogpost-body')
    article = article.decode_contents(formatter='html')
    info = {'title': title, 'article': article}
    return info


def create_file(md, title):
    print('系统默认编码: {}'.format(sys.getdefaultencoding()))
    save_file = 'E:\\py\\day25\\' + str(title) + '.md'
    # r+ 打开一个文件用于读写。文件指针将会放在文件的开头。
    # w+ 打开一个文件用于读写。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。
    # a+ 打开一个文件用于读写。如果该文件已存在，文件指针将会放在文件的结尾。文件打开时会是追加模式。如果该文件不存在，创建新文件用于读写。
    f = codecs.open(save_file, 'w+', 'utf-8')
    f.write(md)
    f.close()
    return save_file


# 将指定MD文件中引用的图片下载到本地，并替换URL
def replace_md_url(md_file):
    if os.path.splitext(md_file)[1] != '.md':
        return

    cnt_replace = 0
    dir_ts = 'E:\\py\\day25\\' + time.strftime('%Y%m', time.localtime())
    is_exists = os.path.exists(dir_ts)
    if not is_exists:
        os.mkdir(dir_ts)
    with open(md_file, 'r', encoding='utf-8') as f:
        post = f.read()
        matches = re.compile(img_patten).findall(post)
        if matches and len(matches) > 0:
            for match in list(chain(*matches)):
                if match and len(match) > 0:
                    array = match.split('/')
                    file_name = array[len(array) - 1]
                    file_name = dir_ts + '/' + file_name
                    img = requests.get(match, headers=headers)
                    f = open(file_name, 'ab')
                    f.write(img.content)
                    post = post.replace(match, file_name)
                    cnt_replace += 1
        if post and cnt_replace > 0:
            open(md_file, 'w', encoding='utf-8').write(post)
            print('有内容被替换')
        else:
            print('无内容被替换')


def main(blog):
    info = get_html(blog)
    text_maker = ht.HTML2Text()
    md = text_maker.handle(info['article'])
    save_file = create_file(md, info['title'])
    replace_md_url(save_file)


if __name__ == '__main__':
    main('https://www.cnblogs.com/crossoverJie/p/11318984.html')
