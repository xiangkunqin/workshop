# -*- coding: utf-8 -*-
# @Time    : 2019/6/24 9:45
# @Author  : xiangkun qin
# @Email   : qinxiangkun@126.com
# @File    : sql_to_csv.py
# @Software: PyCharm
import pymysql
import pandas as pd
import jieba

if __name__ == '__main__':
    stopwords = pd.read_csv("./data/stopwords.txt", index_col=False, quoting=3, sep="\t", names=['stopword'],
                            encoding='utf-8')
    stopwords = stopwords['stopword'].values

    db = pymysql.connect(host="localhost", user="root", password="123456", db="test")
    cursor = db.cursor()
    sql = """SELECT * FROM DGWORKSHOP_A ;"""
    cursor.execute(sql)

    try:
        # 遍历结果
        results = cursor.fetchall()
        sentences =[]
        a =0
        for row in results:
            # 遍历数据库中每一条数据
            id = row[0]
            theme_1 = row[1]
            if theme_1 != None:

                theme_2 = row[1]
                if theme_2 ==None:
                    theme_2=''

                theme_3 = row[3]
                if theme_3 ==None:
                    theme_3=''

                table_name_zh = row[4]
                if table_name_zh ==None:
                    table_name_zh=''

                field = row[7]
                if field==None:
                    field=''

                line = theme_2 +' '+theme_3 +' '+table_name_zh+'' +field

                segs = jieba.lcut(line)
                segs = filter(lambda x: len(x) > 1, segs)
                segs = filter(lambda x: x not in stopwords, segs)

                sentences.append((" ".join(segs), theme_1))
                a = a + 1
                print(str(a))
                print(str(len(sentences)))

    except  Exception as e:
        print()
    finally:
        db.close()

    name_attribute = [ 'content', 'tag']
    writerCSV = pd.DataFrame(columns=name_attribute, data=sentences)
    writerCSV.to_csv('./theme_1.csv', encoding='utf-8')

    # with open("./data_theme_1.txt", "w") as f:
    #     for item in sentences:
    #         str_item = item[0]+'==='+item[1]+'\n'
    #         print(str_item)
    #         f.writelines(str_item)


