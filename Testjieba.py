import jieba
import jieba.analyse
import jieba.posseg as pseg
import codecs,sys
def cut_words(sentence):
    #print sentence
    return " ".join(jieba.cut(sentence)).encode('utf-8')
# f=codecs.open('wiki.zh.jian.text','r',encoding="utf8")
# target = codecs.open("zh.jian.wiki.seg-1.3g.txt", 'w',encoding="utf8")
f=codecs.open('./data/data_big.txt','r',encoding="utf8")
target = codecs.open("./data/data_big_jieba.txt", 'w',encoding="utf8")

#读取停止词文件并保存到列表stopkey
# stopkey=[line.strip() for line in open('./data/bank/stopkey.txt', encoding="utf8").readlines()]
stopkey=['主题','信息','的', '。',' / ','人']
print ('open files')
line_num=1
line = f.readline()
while line:
    print('---- processing ', line_num, ' article----------------')
    jiebas = jieba.cut_for_search(line)  # jieba.cut_for_search() 结巴分词搜索引擎模式
    fenci_key = " ".join(list(set(jiebas) - set(stopkey)))  # 使用join链接字符串输出
    target.writelines(fenci_key.strip())
    line_num = line_num + 1
    line = f.readline()
f.close()
target.close()
exit()
while line:
    curr = []
    for oneline in line:
        #print(oneline)
        curr.append(oneline)
    after_cut = map(cut_words, curr)
    target.writelines(after_cut)
    print ('saved',line_num,'articles')
    exit()
    line = f.readline1()
f.close()
target.close()

# python Testjieba.py