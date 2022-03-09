from db_util import MyPymysqlPool
import requests
from bs4 import BeautifulSoup
import importlib
import sys

importlib.reload(sys)

global headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
server = 'http://www.xbiquge.la/'

book = 'http://www.xbiquge.la/5/5623/'
mysql = MyPymysqlPool('dbMysql')


def get_contents(chapter):
    req = requests.get(url=chapter)
    html = req.content
    html_doc = str(html, 'utf8')
    bf = BeautifulSoup(html_doc, 'html.parser')
    texts = bf.find_all('div', id='content')
    content = texts[0].text.replace('\xa0' * 4, '\n')
    return content


# 写入数据库
def write_db(chapter, content):
    sql = "INSERT INTO novel (title, content) VALUES(%(title)s, %(content)s);"
    param = {"title": chapter, "content": content}
    mysql.insert(sql, param)


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
            chapter = each.string
            write_db(chapter, content)
            break
        except Exception as e:
            print(e)
    mysql.dispose()


# 爬取小说网站并存到数据库
if __name__ == '__main__':
    main()
