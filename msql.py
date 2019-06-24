# -*- coding: utf-8 -*-
# @Time    : 2019/6/19 16:33
# @Author  : xiangkun qin
# @Email   : qinxiangkun@126.com
# @File    : msql.py
# @Software: PyCharm
import pymysql

def createTable():
    db = pymysql.connect(host="localhost", user="root", password="123456", db="test")
    cursor = db.cursor()

    # 如果数据表已经存在使用 execute() 方法删除表。
    cursor.execute("DROP TABLE IF EXISTS DGWORKSHOP_A")

    # 创建数据表SQL语句
    sql_create = """CREATE TABLE DGWORKSHOP_A (
                    id INT(11) UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
                    theme_1  VARCHAR (255),
                    theme_2  VARCHAR (255),
                    theme_3  VARCHAR (255),
                    table_name_zh  VARCHAR (255),
                    table_name_en  VARCHAR (255),
                    system_name_zh VARCHAR (255),
                    field VARCHAR (255) 
                    )"""

    cursor.execute(sql_create)

def insert_sql(list):
    print()

if __name__ == '__main__':
    createTable()