# -*- coding: utf-8 -*-
# @Time    : 2019/6/24 14:24
# @Author  : xiangkun qin
# @Email   : qinxiangkun@126.com
# @File    : zhanyou_1.py
# @Software: PyCharm
import xlrd
import xlwt
import jieba
import jieba.analyse
import jieba.posseg as pseg
import codecs,sys
from xlutils.copy import copy


class ExcelAction:
    '''
    只支持xls格式
    '''

    def transCode(self, filename, sheetname):
        filename = filename.decode('utf-8')
        sheetname = sheetname.decode('utf-8')
        return filename, sheetname

    def read_excel(self, filename, sheetname):
        '''
        读取excel
        '''
        # filename, sheetname = self.transCode(filename, sheetname)
        workbook = xlrd.open_workbook(filename)  # 获得工作薄
        sheet = workbook.sheet_by_name(sheetname)  # 获得sheet
        rows = sheet.nrows  # 文件总行数
        list = []
        print(u'-------文件内容-------')
        for i in range(0, rows):
            line = sheet.row_values(i)  # 获得一行的值，返回列表
            list.append(line)
            # 避免打印包含中文的列表时变成unicode
            # print('[' + ','.join("'" + str(element) + "'" for element in line) + ']')
        print(u'-----------------------')
        return list

    def write_excel(self, filename, sheetname, row, col, value, type=0):
        '''
        修改excel
        '''
        filename, sheetname = self.transCode(filename, sheetname)
        # 转成整形是因为要在ride中使用，ride把参数传过来默认是字符串，除非这样传${1}
        row = int(row)
        col = int(col)
        type = int(type)
        # formatting_info=True保存之前数据的格式
        rb = xlrd.open_workbook(filename, formatting_info=True)
        wb = copy(rb)
        sheet = wb.get_sheet(sheetname)
        # 设置样式，写入的文字为红色加粗
        style = xlwt.easyxf('font: bold 1, color red;')
        if type == 1:
            sheet.write(row, col, value, style)
        else:
            sheet.write(row, col, value)
        wb.save(filename)

    def addSheet(self, filename, sheetname, row, valueList):
        '''
        写入excel,一次写一行
        '''
        filename, sheetname = self.transCode(filename, sheetname)

        wb = xlwt.Workbook(filename)
        # 其实会覆盖第一个sheet页
        sheet = wb.add_sheet(sheetname)
        for i in range(len(valueList)):
            # 需要转码
            valueList[i] = str(valueList[i]).decode('utf-8')
            sheet.write(row, i, valueList[i])
        wb.save(filename)
def cut_words(sentence):
    #print sentence
    return " ".join(jieba.cut(sentence)).encode('utf-8')

def getDateFromExcel():
    ea = ExcelAction()
    filename = r'./data/power/PMS2.0系统数据目录清单0606_汇总(3).xlsx'
    try:
        sheetname = '1. 数据表清单及目录分类（全606）'
        list = ea.read_excel(filename, sheetname)
        num = 0
        with open("./data/power/data_zhanyou_1.txt", "w") as f:
            for i in range(len(list)):

                print('插入数据：%s' % (str(num)))
                table_name_en = list[i][3]
                table_name_zh = list[i][4]
                # if(table_name_zh != ''):
                num = num + 1
                if table_name_en != None:
                    table_name_en = str(table_name_en).replace('_', '')
                f.writelines(table_name_en + '\n')


    except Exception as e:
        print(e)

def feiciMethod():
    f = codecs.open('./data/power/data_zhanyou_1.txt', 'r', encoding="utf8")
    target = codecs.open("./data/power/data_zhanyou_1_jieba.txt", 'w', encoding="utf8")

    # 读取停止词文件并保存到列表stopkey
    # stopkey=[line.strip() for line in open('./data/bank/stopkey.txt', encoding="utf8").readlines()]
    stopkey = ['主题', '信息', '的', '。', ' / ', '人']
    print('open files')
    line_num = 1
    line = f.readline()
    while line:
        print('---- processing ', line_num, ' article----------------')
        # jiebas = jieba.cut_for_search(line)  # jieba.cut_for_search() 结巴分词搜索引擎模式
        fenci_key = " ".join(list(line))  # 使用join链接字符串输出
        target.writelines(fenci_key)
        line_num = line_num + 1
        line = f.readline()
    f.close()
    target.close()
    exit()
    while line:
        curr = []
        for oneline in line:
            # print(oneline)
            curr.append(oneline)
        after_cut = map(cut_words, curr)
        target.writelines(after_cut)
        print('saved', line_num, 'articles')
        exit()
        line = f.readline1()
    f.close()
    target.close()


def getMatchQA():
    ea = ExcelAction()
    filename = r'./data/power/PMS2.0系统数据目录清单0606_汇总(3).xlsx'
    try:
        sheetname = '1. 数据表清单及目录分类（全606）'
        list = ea.read_excel(filename, sheetname)
        num = 0
        with open("./data/power/data_zhanyou_qa_1.txt", "w") as f:
            for i in range(len(list)):

                print('插入数据：%s' % (str(num)))
                table_name_en = list[i][3]
                table_name_zh = list[i][4]
                # if(table_name_zh != ''):
                num = num + 1
                if table_name_en != '' and table_name_zh != '':
                    f.writelines(table_name_en +' '+table_name_zh+ '\n')
    except Exception as e:
        print(e)

if __name__ == '__main__':
    print()
    # getDateFromExcel()
    # feiciMethod()
    getMatchQA()

