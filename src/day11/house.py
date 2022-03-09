import re
import requests
from bs4 import BeautifulSoup
from utils.db_util import mysql


def write_db(param):
    try:
        sql = 'insert into house(url, housing_estate, position,square_metre,unit_price,total_price,follow,take_look,pub_date) '
        sql += 'values(%(url)s,%(housing_estate)s, %(position)s,%(square_metre)s,%(unit_price)s,%(total_price)s,%(follow)s,%(take_look)s,%(pub_date)s)'
        mysql.insert(sql, param)
    except Exception as e:
        print(e)


def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}

    page_max = 100
    for i in range(1, int(page_max) + 1):
        print('第几页:' + str(i))
        if i == 1:
            house_url = 'https://qd.lianjia.com/ershoufang/shibei/'
        else:
            house_url = 'https://qd.lianjia.com/ershoufang/shibei/pg' + str(i)
        res = requests.get(house_url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        li_list = soup.find('ul', class_='sellListContent').find_all('li')
        for li in li_list:
            try:
                house_param = {}
                content = li.find('div', class_='houseInfo').text
                content = content.split('|')
                house_param['housing_estate'] = content[0]
                house_param['square_metre'] = re.findall(r'-?\d+\.?\d*e?-?\d*?', content[1])[0]
                position = li.find('div', class_='positionInfo').find('a').text
                house_param['position'] = position
                total_price = li.find('div', class_='totalPrice').text
                house_param['total_price'] = re.sub('\D', '', total_price)
                unit_price = li.find('div', class_='unitPrice').text
                house_param['unit_price'] = re.sub('\D', '', unit_price)
                follow = li.find('div', class_='followInfo').text
                follow = follow.split('/')
                house_param['follow'] = re.sub('\D', '', follow[0])
                house_param['take_look'] = re.sub('\D', '', follow[1])
                title_src = li.find('div', class_='title').find('a').attrs['href']
                house_param['url'] = re.sub('\D', '', title_src)
                title_res = requests.get(title_src, headers=headers)
                title_soup = BeautifulSoup(title_res.text, 'html.parser')
                pub_date = title_soup.find('div', class_='transaction').find_all('li')[0].find_all('span')[1].text
                house_param['pub_date'] = pub_date
                write_db(house_param)
            except Exception as e:
                print(e)
        mysql.end('commit')
    mysql.dispose()


# 爬取购房网站信息 并保存到数据库中
if __name__ == '__main__':
    main()

    # content = '90.25平米'
    # findall = re.findall(r'-?\d+\.?\d*e?-?\d*?', content)[0]
    # print(findall)
