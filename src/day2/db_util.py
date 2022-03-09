#!/usr/bin/python3
# -*- coding:utf-8 -*-

import os
import pymysql
import configparser
from pymysql.cursors import DictCursor
from dbutils.PooledDB import PooledDB


# 数据库连接工具类
class Config(object):
    def __init__(self, config_filename="dbMysqlConfig.cnf"):
        file_path = os.path.join(os.path.dirname(__file__), config_filename)
        self.cf = configparser.ConfigParser()
        self.cf.read(file_path)

    def get_sections(self):
        return self.cf.sections()

    def get_options(self, section):
        return self.cf.options(section)

    def get_content(self, section):
        result = {}
        for option in self.get_options(section):
            value = self.cf.get(section, option)
            result[option] = int(value) if value.isdigit() else value
        return result


class BasePymysqlPool(object):
    def __init__(self, host, port, user, password, db_name):
        self.db_host = host
        self.db_port = int(port)
        self.user = user
        self.password = str(password)
        self.db = db_name
        self.conn = None
        self.cursor = None


class MyPymysqlPool(BasePymysqlPool):
    __pool = None

    def __init__(self, conf_name=None):
        self.conf = Config().get_content(conf_name)
        super(MyPymysqlPool, self).__init__(**self.conf)
        self.__conn = self.__getConn()
        self.__cursor = self.__conn.cursor()

    def __getConn(self):
        if MyPymysqlPool.__pool is None:
            __pool = PooledDB(creator=pymysql, mincached=1, maxcached=20, host=self.db_host, port=self.db_port,
                              user=self.user, password=self.password, db=self.db, use_unicode=True, charset="utf8",
                              cursorclass=DictCursor)
            print('数据库初始化')

        return __pool.connection()

    def getAll(self, sql, param=None):
        if param is None:
            count = self.__cursor.execute(sql)
        else:
            count = self.__cursor.execute(sql, param)
        if count > 0:
            result = self.__cursor.fetchall()
        else:
            result = False
        return result

    def getOne(self, sql, param=None):
        if param is None:
            count = self.__cursor.execute(sql)
        else:
            count = self.__cursor.execute(sql, param)
        if count > 0:
            result = self.__cursor.fetchone()
        else:
            result = False
        return result

    def getMany(self, sql, num, param=None):
        if param is None:
            count = self.__cursor.execute(sql)
        else:
            count = self.__cursor.execute(sql, param)
        if count > 0:
            result = self.__cursor.fetchmany(num)
        else:
            result = False
        return result

    def insertMany(self, sql, values):
        count = self.__cursor.executemany(sql, values)
        return count

    def __query(self, sql, param=None):
        if param is None:
            count = self.__cursor.execute(sql)
        else:
            count = self.__cursor.execute(sql, param)
        return count

    def update(self, sql, param=None):
        return self.__query(sql, param)

    def insert(self, sql, param=None):
        return self.__query(sql, param)

    def __delete__(self, sql, param=None):
        return self.__query(sql, param)

    def begin(self):
        self.__conn.autocommit(0)

    def end(self, option='commit'):
        if option == 'commit':
            self.__conn.commit()
        else:
            self.__conn.rollback()

    def dispose(self, isEnd=1):
        if isEnd == 1:
            self.end('commit')
        else:
            self.end('rollback')
        self.__cursor.close()
        self.__conn.close()


if __name__ == '__main__':
    mysql = MyPymysqlPool('dbMysql')
    # sqlAll = 'select * from tb_account'
    # result = mysql.getAll(sqlAll)
    # print(result)

    sql = "INSERT INTO novel (title, content) VALUES('aa', 'bb');"
    # param = {"title": chapter, "content": content}
    mysql.insert(sql)
    mysql.dispose()
