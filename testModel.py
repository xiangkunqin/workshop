from gensim.models import Word2Vec
from gensim import corpora, models, similarities
# en_wiki_word2vec_model = Word2Vec.load('wiki.zh.text.model')
from numpy import vectorize
import numpy as np
from scipy import spatial
import jieba
import jieba.analyse
import jieba.posseg as pseg
from workshop.tf_idf import getTFIDF

def avg_feature_vector(sentence, model, num_features, index2word_set,dict_tfidf):
    words = sentence.split()
    feature_vec = np.zeros((num_features, ), dtype='float32')
    n_words = 0
    ## 取平均值
    # for word in words:
    #     if word in index2word_set:
    #         n_words += 1
    #         feature_vec = np.add(feature_vec, model[word])
    # if (n_words > 0):
    #     feature_vec = np.divide(feature_vec, n_words)

    ## 使用TF-IDF做权重
    sum_tf_idf =0.0
    for word in words:
        if (dict_tfidf.__contains__(word)):
            sum_tf_idf =sum_tf_idf+ dict_tfidf[word]
        else:
            sum_tf_idf =sum_tf_idf+ 0.00001

    print("TF-IDF总和："+str(sum_tf_idf))
    for word in words:
        if word in index2word_set:
                n_words += 1
                if(dict_tfidf.__contains__(word)):
                    word_tf_idf = dict_tfidf[word]
                else:
                    word_tf_idf=0.00001
                feature_vec = np.add(feature_vec, (word_tf_idf/sum_tf_idf)*model[word])

    # if (n_words > 0):
    #     feature_vec = np.divide(feature_vec, n_words)
    return feature_vec


def getSimilar(str1,list_qa):
    list =[]
    for item in list_qa:
        if(len(item)==2):
            dict ={}
            q_str = item[0]
            q_str = q_str.replace("/"," ")
            a_str = item[1]

            index2word_set = set(word2vec_model.wv.index2word)

            s1_afv = avg_feature_vector(str1, model=word2vec_model, num_features=100,
                                        index2word_set=index2word_set)
            s2_afv = avg_feature_vector(q_str, model=word2vec_model, num_features=100,
                                        index2word_set=index2word_set)
            sim = 1 - spatial.distance.cosine(s1_afv, s2_afv)

            dict["sim"]=sim
            dict["a_str"] = a_str
            dict["q_str"]=q_str

            if(sim>0):
                list.append(dict)
    return list

def getSimilar2(str1,list_qa,word2vec_model,dict_tfidf):
    '''

    :param str1:
    :param list_qa: 分词后数组
    :param word2vec_model: 模型
    :param dict_tfidf: TF-IDF
    :return:
    '''

    # sim1 = word2vec_model['性别']

    #对输入进行分词
    str1_cut = " ".join(jieba.cut(str1))
    index2word_set = set(word2vec_model.wv.index2word)
    list_str1_cut=str1_cut.split(' ')
    for item in list_str1_cut:
        if(item !=''):
            tf_idf_item = dict_tfidf[item]
            print(item+'---tf_idf-->'+str(tf_idf_item))
    s1_afv = avg_feature_vector(str1_cut,
                                model=word2vec_model,
                                num_features=100,
                                index2word_set=index2word_set,dict_tfidf=dict_tfidf)

    str_min = s1_afv.min()
    str_max = s1_afv.max()
    if(str_min==str_max==0.0):
        print(s1_afv)
        return None
    else:
        list =[]
        for item in list_qa:
            dict = {}
            index2word_set = set(word2vec_model.wv.index2word)
            # 对输入进行分词
            # q_str_cut = " ".join(jieba.cut(str_item[len(str_item)-3]+str_item[len(str_item)-2]+str_item[len(str_item)-1]))
            q_str_cut = " ".join(jieba.cut(str(item)))
            s2_afv = avg_feature_vector(q_str_cut, model=word2vec_model, num_features=100,
                                        index2word_set=index2word_set, dict_tfidf=dict_tfidf)
            sim = 1 - spatial.distance.cosine(s1_afv, s2_afv)

            dict["sim"] = sim
            # dict["a_str"] = a_str
            dict["q_str"] = item

            if (sim > 0):
                list.append(dict)


        return list

def getListQA(file_path):
    data = []
    for line in open(file_path, "r",encoding="utf8"):  # 设置文件对象并读取每一行文件
        # list_temp=[]
        # list_line = str(line)
        # if(len(list_line)==2):
        #     list_temp.append(list_line)# 将每一行文件加入到list中

        data.append(str(line).replace('\n',''))
    return data

if __name__ == '__main__':


    word2vec_model = Word2Vec.load('data_zhanyou_1_jieba_word2vec.model')
    # word2vec_model = Word2Vec.load('./model/bank_qq_jieba_no_word2vec.model')
    # word2vec_model = Word2Vec.load('./model/bank_qq_jieba_yes_word2vec.model')
    # testwords = ['性别','身份证','登记','期限','数据']
    #
    # # 取出词语对应的词向量。
    # vec = word2vec_model[['身份证']]
    # print('三个词的词向量矩阵的维度是：', vec.shape,'。')
    # print('-------------------------------我是分隔符------------------------')

    ## 计算两个词的相似程度。
    # print('性别 身份证的余弦相似度是：', word2vec_model.similarity('性别','身份证'),'。')
    # print('-------------------------------我是分隔符------------------------')

    # 得到和某个词比较相关的词的列表
    # sim1 = word2vec_model['E']
    # print(sim1)

    # # 计算TF-IDF
    str1 = 'SJZFP'
    list_tfidf = getListQA("./data/bank/data_qq_jieba_no.txt")
    a=" ".join(jieba.cut(str1))
    list_tfidf.append(a)
    dict_tfidf = getTFIDF(list_tfidf)

    # print(dict_tfidf)
    list_qa = getListQA("./data/bank/data_qq_no.txt")
    str1_cut = " ".join(jieba.cut(str1))

    res=getSimilar2(str1,list_qa,word2vec_model,dict_tfidf)

    # print('管理:'+str(dict_tfidf['管理']))

    if(res!=None):
        res.sort(key=lambda k: (k.get('sim', 1)))
        num=20
        for i in range(len(res)):
            if(num==0):
                break
            else:
                print(res[len(res)-num])
                num=num-1