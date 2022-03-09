#!/usr/bin/python3

import MySQLdb


# mysql连接
def connect_mysql():
    db = MySQLdb.connect(host='121.5.54.219', port=3306, user='root', passwd='yqqlmGSYCL222', db='seata_test',
                         charset='utf8')

    cursor = db.cursor()

    # 使用 execute()  方法执行 SQL 查询
    cursor.execute("SELECT * FROM tb_account")

    # 使用 fetchall() 方法获取s所有数据.
    data = cursor.fetchall()
    print(data)

    cursor.close()
    db.close()


if __name__ == '__main__':
    connect_mysql()
