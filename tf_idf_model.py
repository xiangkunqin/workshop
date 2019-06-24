# -*- coding: utf-8 -*-
# @Time    : 2019/6/18 14:03
# @Author  : xiangkun qin
# @Email   : qinxiangkun@126.com
# @File    : tf_idf_model.py
# @Software: PyCharm
from gensim import corpora,models


def getListQA(file_path):
    data = []
    for line in open(file_path, "r",encoding="utf8"):  # 设置文件对象并读取每一行文件
        # list_temp=[]
        # list_line = str(line)
        # if(len(list_line)==2):
        #     list_temp.append(list_line)# 将每一行文件加入到list中

        data.append(str(line).replace('\n',''))
    return data


def saveModel():
    corpus = getListQA("./data/bank/data_qq_yes.txt")

    word_list = []
    for i in range(len(corpus)):
        word_list.append(corpus[i].split(' '))
    # print(word_list)
    # 赋给语料库中每个词(不重复的词)一个整数id
    dictionary = corpora.Dictionary(word_list)
    new_corpus = [dictionary.doc2bow(text) for text in word_list]
    # print(new_corpus)
    # 元组中第一个元素是词语在词典中对应的id，第二个元素是词语在文档中出现的次数
    # 通过下面的方法可以看到语料库中每个词对应的id
    # print(dictionary.token2id)

    tfidf = models.TfidfModel(new_corpus)
    tfidf.save("tfidf_yes_model.tfidf")

def testModel():
    corpus = getListQA("./data/bank/data_qq_yes.txt")

    word_list = []
    for i in range(len(corpus)):
        word_list.append(corpus[i].split(' '))
    dictionary = corpora.Dictionary(word_list)
    # 我们随便拿几个单词来测试
    # 载入模型
    tfidf = models.TfidfModel.load("tfidf_yes_model.tfidf")
    string = ['还款','方式']
    string_bow = dictionary.doc2bow(string)
    string_tfidf = tfidf[string_bow]
    print(string_tfidf)
if __name__ == '__main__':
   # saveModel()
   testModel()





