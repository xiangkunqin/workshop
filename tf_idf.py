# -*- coding: utf-8 -*-
# @Time    : 2019/6/18 13:39
# @Author  : xiangkun qin
# @Email   : qinxiangkun@126.com
# @File    : tf_idf.py
# @Software: PyCharm
import math
from collections import Counter


# word可以通过count得到，count可以通过countlist得到
# count[word]可以得到每个单词的词频， sum(count.values())得到整个句子的单词总数
def tf(word, count):
    print("===========计算TF=============")
    a =count[word]
    b = count.values()
    c = sum(count.values())
    d =a/c
    print(count)
    print('count[%s]/sum(count.values())=%s/%s=%s'%(word,a,c,d))
    return d


# 统计的是含有该单词的句子数
def n_containing(word, count_list):
    return sum(1 for count in count_list if word in count)

# len(count_list)是指句子的总数，n_containing(word, count_list)是指含有该单词的句子的总数，加1是为了防止分母为0
def idf(word, count_list):
    return math.log(len(count_list) / (1 + n_containing(word, count_list)))

# 将tf和idf相乘
def tfidf(word, count, count_list):

    return tf(word, count) * idf(word, count_list)

def getTFIDF(corpus):

    #对语料进行分词
    print("===========对语料进行分词=============")
    allword_list = []
    for i in range(len(corpus)):
        item_list = corpus[i].split(' ')
        _item_list = []
        for item in item_list:
            if item !='':
                _item_list.append(item)
        allword_list.append(_item_list)
    print(allword_list)

    #统计词频
    print("==========统计语料的词频=============")
    countlist = []
    for i in range(len(allword_list)):
        count = Counter(allword_list[i])
        countlist.append(count)
    print(countlist)

    dict ={}
    for i, count in enumerate(countlist):
        # print("Top words in document {}".format(i + 1))
        scores = {word: tfidf(word, count, countlist) for word in count}
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        for word, score in sorted_words[:]:
            dict[word]=round(score, 5)
            print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))

    return dict