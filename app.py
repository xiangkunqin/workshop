# coding=utf-8
import xlrd
import xlwt
import traceback
from xlutils.copy import copy


from imp import reload
import sys
import re
import codecs
import pymysql
import re
# reload(sys)
# # 需要加上，否则会报UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-1: ordinal not in range(128)
# sys.setdefaultencoding('utf-8')


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


def getString():

    f = codecs.open('./data/power/data_1.txt', 'r', 'utf-8')
    s = f.readlines()

    f.flush()
    f.close()
    for fileLine in s:

        if u'检查' in fileLine:
            line_pattern = r'\s*\d+\s?(.*)'

            def func(text):
                c = re.compile(line_pattern)
                lists = []
                lines = text.split('\n')
                for line in lines:
                    r = c.findall(line)
                    if r:
                        lists.append(r[0])

                return '\n'.join(lists)

            result = func(fileLine)
            with open("./data/power/data_2.txt", "w") as f:
                f.writelines(result)
def readExcel():
    ea = ExcelAction()
    # #################################################电力数据#################################################################
    # filename_1 = r'./data/power/术语库V2.3.xlsx'
    # sheetname_1_0 = '术语安全定级'
    # list_1_0 = ea.read_excel(filename_1, sheetname_1_0)
    #
    # sheetname_1_1 = '术语英文名称'
    # list_1_1 = ea.read_excel(filename_1, sheetname_1_1)
    #
    # sheetname_1_2 = '关联同义词'
    # list_1_2 = ea.read_excel(filename_1, sheetname_1_2)
    #
    # sheetname_1_3 = '脱敏规则映射'
    # list_1_3 = ea.read_excel(filename_1, sheetname_1_3)
    #
    # filename_2 = r'./data/power/术语库_安全等级分析V1.7.xlsx'
    # sheetname_2_0 = '术语安全定级'
    # list_2_0 = ea.read_excel(filename_2, sheetname_2_0)
    #
    # sheetname_2_1 = '一级分类对应关系'
    # list_2_1 = ea.read_excel(filename_2, sheetname_2_1)
    #
    # sheetname_2_2 = '二级分类对应关系'
    # list_2_2 = ea.read_excel(filename_2, sheetname_2_2)
    #
    # sheetname_2_3 = '关联同义词'
    # list_2_3 = ea.read_excel(filename_2, sheetname_2_3)
    #
    # sheetname_2_4 = '脱敏规则映射'
    # list_2_4 = ea.read_excel(filename_2, sheetname_2_4)
    #
    # list = []
    # for i in list_1_0:
    #     for j in i:
    #         regex_str = ".*?([\u4E00-\u9FA5])"
    #         match_obj = re.match(regex_str, str(j))
    #         if match_obj != None:
    #             list.append(match_obj.string)
    # for i in list_1_1:
    #     for j in i:
    #         regex_str = ".*?([\u4E00-\u9FA5])"
    #         match_obj = re.match(regex_str, str(j))
    #         if match_obj != None:
    #             list.append(match_obj.string)
    # for i in list_1_2:
    #     for j in i:
    #         regex_str = ".*?([\u4E00-\u9FA5])"
    #         match_obj = re.match(regex_str, str(j))
    #         if match_obj != None:
    #             list.append(match_obj.string)
    # for i in list_1_3:
    #     for j in i:
    #         regex_str = ".*?([\u4E00-\u9FA5])"
    #         match_obj = re.match(regex_str, str(j))
    #         if match_obj != None:
    #             list.append(match_obj.string)
    # for i in list_2_0:
    #     for j in i:
    #         regex_str = ".*?([\u4E00-\u9FA5])"
    #         match_obj = re.match(regex_str, str(j))
    #         if match_obj != None:
    #             list.append(match_obj.string)
    # for i in list_2_1:
    #     for j in i:
    #         regex_str = ".*?([\u4E00-\u9FA5])"
    #         match_obj = re.match(regex_str, str(j))
    #         if match_obj != None:
    #             list.append(match_obj.string)
    # for i in list_2_2:
    #     for j in i:
    #         regex_str = ".*?([\u4E00-\u9FA5])"
    #         match_obj = re.match(regex_str, str(j))
    #         if match_obj != None:
    #             list.append(match_obj.string)
    # for i in list_2_3:
    #     for j in i:
    #         regex_str = ".*?([\u4E00-\u9FA5])"
    #         match_obj = re.match(regex_str, str(j))
    #         if match_obj != None:
    #             list.append(match_obj.string)
    # for i in list_2_4:
    #     for j in i:
    #         regex_str = ".*?([\u4E00-\u9FA5])"
    #         match_obj = re.match(regex_str, str(j))
    #         if match_obj != None:
    #             list.append(match_obj.string)

    ############################################################银行数据#########################################################
    filename_1 = r'./data/bank/数据标准-交易主题.xlsx'

    sheetname_1_0 = '修改记录'
    list_1_0 = ea.read_excel(filename_1, sheetname_1_0)

    sheetname_1_1 = '术语与定义'
    list_1_1 = ea.read_excel(filename_1, sheetname_1_0)

    sheetname_1_2 = '交易基础分类'
    list_1_2 = ea.read_excel(filename_1, sheetname_1_0)

    sheetname_1_3 = '信息项框架'
    list_1_3 = ea.read_excel(filename_1, sheetname_1_0)

    sheetname_1_4 = '数据标准信息项'
    list_1_4 = ea.read_excel(filename_1, sheetname_1_0)

    sheetname_1_5 = '标准代码'
    list_1_5 = ea.read_excel(filename_1, sheetname_1_0)

    filename_2 = r'./data/bank/数据标准-产品主题.xlsx'
    sheetname_2_0 = '术语与定义'
    list_2_0 = ea.read_excel(filename_2, sheetname_2_0)
    sheetname_2_1 = '产品基础分类'
    list_2_1 = ea.read_excel(filename_2, sheetname_2_0)
    sheetname_2_2 = '信息项框架'
    list_2_2 = ea.read_excel(filename_2, sheetname_2_0)
    sheetname_2_3 = '数据标准信息项'
    list_2_3 = ea.read_excel(filename_2, sheetname_2_0)
    sheetname_2_4 = '标准代码'
    list_2_4 = ea.read_excel(filename_2, sheetname_2_0)

    filename_3 = r'./data/bank/数据标准-交易主题.xlsx'
    sheetname_3_0 = '术语与定义'
    list_3_0 = ea.read_excel(filename_2, sheetname_2_0)
    sheetname_3_1 = '交易基础分类'
    list_3_1 = ea.read_excel(filename_2, sheetname_2_0)
    sheetname_3_2 = '信息项框架'
    list_3_2 = ea.read_excel(filename_2, sheetname_2_0)
    sheetname_3_3 = '数据标准信息项'
    list_3_3 = ea.read_excel(filename_2, sheetname_2_0)
    sheetname_3_4 = '标准代码'
    list_3_4 = ea.read_excel(filename_2, sheetname_2_0)

    filename_4 = r'./data/bank/数据标准-协议主题.xlsx'
    sheetname_4_0 = '术语与定义'
    list_4_0 = ea.read_excel(filename_2, sheetname_2_0)
    sheetname_4_1 = '协议基础分类'
    list_4_1 = ea.read_excel(filename_2, sheetname_2_0)
    sheetname_4_2 = '信息项框架'
    list_4_2 = ea.read_excel(filename_2, sheetname_2_0)
    sheetname_4_3 = '数据标准信息项'
    list_4_3 = ea.read_excel(filename_2, sheetname_2_0)
    sheetname_4_4 = '标准代码'
    list_4_4 = ea.read_excel(filename_2, sheetname_2_0)

    filename_5 = r'./data/bank/数据标准-客户主题.xlsx'
    sheetname_5_0 = '术语与定义'
    list_5_0 = ea.read_excel(filename_2, sheetname_2_0)
    sheetname_5_1 = '信息项框架'
    list_5_1 = ea.read_excel(filename_2, sheetname_2_0)
    sheetname_5_2 = '数据标准信息项'
    list_5_2 = ea.read_excel(filename_2, sheetname_2_0)
    sheetname_5_3 = '标准代码'
    list_5_3 = ea.read_excel(filename_2, sheetname_2_0)

    filename_6 = r'./data/bank/数据标准-渠道主题.xlsx'
    sheetname_6_0 = '术语与定义'
    list_6_0 = ea.read_excel(filename_2, sheetname_2_0)
    sheetname_6_1 = '渠道分类'
    list_6_1 = ea.read_excel(filename_2, sheetname_2_0)
    sheetname_6_2 = '信息项框架'
    list_6_2 = ea.read_excel(filename_2, sheetname_2_0)
    sheetname_6_3 = '数据标准信息项'
    list_6_3 = ea.read_excel(filename_2, sheetname_2_0)
    sheetname_6_4 = '标准代码'
    list_6_4 = ea.read_excel(filename_2, sheetname_2_0)

    filename_7 = r'./data/bank/数据标准-组织机构主题.xlsx'
    sheetname_7_0 = '术语与定义'
    list_7_0 = ea.read_excel(filename_2, sheetname_2_0)

    sheetname_7_1 = '信息项框架'
    list_7_1 = ea.read_excel(filename_2, sheetname_2_0)
    sheetname_7_2 = '数据标准信息项'
    list_7_2= ea.read_excel(filename_2, sheetname_2_0)
    sheetname_7_3 = '标准代码'
    list_7_3 = ea.read_excel(filename_2, sheetname_2_0)

    filename_8 = r'./data/bank/数据标准-财务主题.xlsx'
    sheetname_8_0 = '术语与定义'
    list_8_0 = ea.read_excel(filename_2, sheetname_2_0)

    sheetname_8_1 = '信息项框架'
    list_8_1 = ea.read_excel(filename_2, sheetname_2_0)
    sheetname_8_2 = '数据标准信息项'
    list_8_2 = ea.read_excel(filename_2, sheetname_2_0)
    sheetname_8_3 = '标准代码'
    list_8_3 = ea.read_excel(filename_2, sheetname_2_0)

    filename_9 = r'./data/bank/数据标准-账户主题.xlsx'
    sheetname_9_0 = '术语与定义'
    list_9_0 = ea.read_excel(filename_2, sheetname_2_0)

    sheetname_9_1 = '信息项框架'
    list_9_1 = ea.read_excel(filename_2, sheetname_2_0)
    sheetname_9_2 = '数据标准信息项'
    list_9_2 = ea.read_excel(filename_2, sheetname_2_0)
    sheetname_9_3 = '标准代码'
    list_9_3 = ea.read_excel(filename_2, sheetname_2_0)

    filename_10 = r'./data/bank/数据标准映射-账户主题.xlsx'
    sheetname_10_0 = '标准映射'
    list_10_0 = ea.read_excel(filename_2, sheetname_2_0)

    sheetname_10_1 = '代码映射'
    list_10_1 = ea.read_excel(filename_2, sheetname_2_0)


    list = []
    # for i in list_1_0:
    #     for j in i:
    #         regex_str = ".*?([\u4E00-\u9FA5])"
    #         match_obj = re.match(regex_str, str(j))
    #         if match_obj != None:
    #             list.append(match_obj.string)
    # for i in list_1_1:
    #     for j in i:
    #         regex_str = ".*?([\u4E00-\u9FA5])"
    #         match_obj = re.match(regex_str, str(j))
    #         if match_obj != None:
    #             list.append(match_obj.string)
    #
    # for i in list_1_2:
    #     for j in i:
    #         regex_str = ".*?([\u4E00-\u9FA5])"
    #         match_obj = re.match(regex_str, str(j))
    #         if match_obj != None:
    #             list.append(match_obj.string)
    #
    # for i in list_1_3:
    #     for j in i:
    #         regex_str = ".*?([\u4E00-\u9FA5])"
    #         match_obj = re.match(regex_str, str(j))
    #         if match_obj != None:
    #             list.append(match_obj.string)

    for i in list_1_4:
        for j in i:
            regex_str = ".*?([\u4E00-\u9FA5])"
            match_obj = re.match(regex_str, str(j))
            if match_obj != None:
                list.append(match_obj.string)

    # for i in list_1_5:
    #     for j in i:
    #         regex_str = ".*?([\u4E00-\u9FA5])"
    #         match_obj = re.match(regex_str, str(j))
    #         if match_obj != None:
    #             list.append(match_obj.string)

    # for i in list_2_0:
    #     for j in i:
    #         regex_str = ".*?([\u4E00-\u9FA5])"
    #         match_obj = re.match(regex_str, str(j))
    #         if match_obj != None:
    #             list.append(match_obj.string)
    # for i in list_2_1:
    #     for j in i:
    #         regex_str = ".*?([\u4E00-\u9FA5])"
    #         match_obj = re.match(regex_str, str(j))
    #         if match_obj != None:
    #             list.append(match_obj.string)
    #
    # for i in list_2_2:
    #     for j in i:
    #         regex_str = ".*?([\u4E00-\u9FA5])"
    #         match_obj = re.match(regex_str, str(j))
    #         if match_obj != None:
    #             list.append(match_obj.string)

    for i in list_2_3:
        for j in i:
            regex_str = ".*?([\u4E00-\u9FA5])"
            match_obj = re.match(regex_str, str(j))
            if match_obj != None:
                list.append(match_obj.string)

    # for i in list_2_4:
    #     for j in i:
    #         regex_str = ".*?([\u4E00-\u9FA5])"
    #         match_obj = re.match(regex_str, str(j))
    #         if match_obj != None:
    #             list.append(match_obj.string)

    # for i in list_3_0:
    #     for j in i:
    #         regex_str = ".*?([\u4E00-\u9FA5])"
    #         match_obj = re.match(regex_str, str(j))
    #         if match_obj != None:
    #             list.append(match_obj.string)
    # for i in list_3_1:
    #     for j in i:
    #         regex_str = ".*?([\u4E00-\u9FA5])"
    #         match_obj = re.match(regex_str, str(j))
    #         if match_obj != None:
    #             list.append(match_obj.string)
    #
    # for i in list_3_2:
    #     for j in i:
    #         regex_str = ".*?([\u4E00-\u9FA5])"
    #         match_obj = re.match(regex_str, str(j))
    #         if match_obj != None:
    #             list.append(match_obj.string)

    for i in list_3_3:
        for j in i:
            regex_str = ".*?([\u4E00-\u9FA5])"
            match_obj = re.match(regex_str, str(j))
            if match_obj != None:
                list.append(match_obj.string)

    # for i in list_3_4:
    #     for j in i:
    #         regex_str = ".*?([\u4E00-\u9FA5])"
    #         match_obj = re.match(regex_str, str(j))
    #         if match_obj != None:
    #             list.append(match_obj.string)

    # for i in list_4_0:
    #     for j in i:
    #         regex_str = ".*?([\u4E00-\u9FA5])"
    #         match_obj = re.match(regex_str, str(j))
    #         if match_obj != None:
    #             list.append(match_obj.string)
    # for i in list_4_1:
    #     for j in i:
    #         regex_str = ".*?([\u4E00-\u9FA5])"
    #         match_obj = re.match(regex_str, str(j))
    #         if match_obj != None:
    #             list.append(match_obj.string)
    #
    # for i in list_4_2:
    #     for j in i:
    #         regex_str = ".*?([\u4E00-\u9FA5])"
    #         match_obj = re.match(regex_str, str(j))
    #         if match_obj != None:
    #             list.append(match_obj.string)

    for i in list_4_3:
        for j in i:
            regex_str = ".*?([\u4E00-\u9FA5])"
            match_obj = re.match(regex_str, str(j))
            if match_obj != None:
                list.append(match_obj.string)

    # for i in list_4_4:
    #     for j in i:
    #         regex_str = ".*?([\u4E00-\u9FA5])"
    #         match_obj = re.match(regex_str, str(j))
    #         if match_obj != None:
    #             list.append(match_obj.string)
    #
    # for i in list_5_0:
    #     for j in i:
    #         regex_str = ".*?([\u4E00-\u9FA5])"
    #         match_obj = re.match(regex_str, str(j))
    #         if match_obj != None:
    #             list.append(match_obj.string)
    # for i in list_5_1:
    #     for j in i:
    #         regex_str = ".*?([\u4E00-\u9FA5])"
    #         match_obj = re.match(regex_str, str(j))
    #         if match_obj != None:
    #             list.append(match_obj.string)

    for i in list_5_2:
        for j in i:
            regex_str = ".*?([\u4E00-\u9FA5])"
            match_obj = re.match(regex_str, str(j))
            if match_obj != None:
                list.append(match_obj.string)

    # for i in list_5_3:
    #     for j in i:
    #         regex_str = ".*?([\u4E00-\u9FA5])"
    #         match_obj = re.match(regex_str, str(j))
    #         if match_obj != None:
    #             list.append(match_obj.string)

    # for i in list_6_0:
    #     for j in i:
    #         regex_str = ".*?([\u4E00-\u9FA5])"
    #         match_obj = re.match(regex_str, str(j))
    #         if match_obj != None:
    #             list.append(match_obj.string)
    # for i in list_6_1:
    #     for j in i:
    #         regex_str = ".*?([\u4E00-\u9FA5])"
    #         match_obj = re.match(regex_str, str(j))
    #         if match_obj != None:
    #             list.append(match_obj.string)

    # for i in list_6_2:
    #     for j in i:
    #         regex_str = ".*?([\u4E00-\u9FA5])"
    #         match_obj = re.match(regex_str, str(j))
    #         if match_obj != None:
    #             list.append(match_obj.string)

    for i in list_6_3:
        for j in i:
            regex_str = ".*?([\u4E00-\u9FA5])"
            match_obj = re.match(regex_str, str(j))
            if match_obj != None:
                list.append(match_obj.string)

    # for i in list_6_4:
    #     for j in i:
    #         regex_str = ".*?([\u4E00-\u9FA5])"
    #         match_obj = re.match(regex_str, str(j))
    #         if match_obj != None:
    #             list.append(match_obj.string)

    # for i in list_7_0:
    #     for j in i:
    #         regex_str = ".*?([\u4E00-\u9FA5])"
    #         match_obj = re.match(regex_str, str(j))
    #         if match_obj != None:
    #             list.append(match_obj.string)
    # for i in list_7_1:
    #     for j in i:
    #         regex_str = ".*?([\u4E00-\u9FA5])"
    #         match_obj = re.match(regex_str, str(j))
    #         if match_obj != None:
    #             list.append(match_obj.string)

    for i in list_7_2:
        for j in i:
            regex_str = ".*?([\u4E00-\u9FA5])"
            match_obj = re.match(regex_str, str(j))
            if match_obj != None:
                list.append(match_obj.string)

    # for i in list_7_3:
    #     for j in i:
    #         regex_str = ".*?([\u4E00-\u9FA5])"
    #         match_obj = re.match(regex_str, str(j))
    #         if match_obj != None:
    #             list.append(match_obj.string)
    #
    # for i in list_8_0:
    #     for j in i:
    #         regex_str = ".*?([\u4E00-\u9FA5])"
    #         match_obj = re.match(regex_str, str(j))
    #         if match_obj != None:
    #             list.append(match_obj.string)
    # for i in list_8_1:
    #     for j in i:
    #         regex_str = ".*?([\u4E00-\u9FA5])"
    #         match_obj = re.match(regex_str, str(j))
    #         if match_obj != None:
    #             list.append(match_obj.string)

    for i in list_8_2:
        for j in i:
            regex_str = ".*?([\u4E00-\u9FA5])"
            match_obj = re.match(regex_str, str(j))
            if match_obj != None:
                list.append(match_obj.string)

    # for i in list_8_3:
    #     for j in i:
    #         regex_str = ".*?([\u4E00-\u9FA5])"
    #         match_obj = re.match(regex_str, str(j))
    #         if match_obj != None:
    #             list.append(match_obj.string)
    #
    # for i in list_9_0:
    #     for j in i:
    #         regex_str = ".*?([\u4E00-\u9FA5])"
    #         match_obj = re.match(regex_str, str(j))
    #         if match_obj != None:
    #             list.append(match_obj.string)
    # for i in list_9_1:
    #     for j in i:
    #         regex_str = ".*?([\u4E00-\u9FA5])"
    #         match_obj = re.match(regex_str, str(j))
    #         if match_obj != None:
    #             list.append(match_obj.string)

    for i in list_9_2:
        for j in i:
            regex_str = ".*?([\u4E00-\u9FA5])"
            match_obj = re.match(regex_str, str(j))
            if match_obj != None:
                list.append(match_obj.string)

    # for i in list_9_3:
    #     for j in i:
    #         regex_str = ".*?([\u4E00-\u9FA5])"
    #         match_obj = re.match(regex_str, str(j))
    #         if match_obj != None:
    #             list.append(match_obj.string)

    # for i in list_10_0:
    #     for j in i:
    #         regex_str = ".*?([\u4E00-\u9FA5])"
    #         match_obj = re.match(regex_str, str(j))
    #         if match_obj != None:
    #             list.append(match_obj.string)
    # for i in list_10_1:
    #     for j in i:
    #         regex_str = ".*?([\u4E00-\u9FA5])"
    #         match_obj = re.match(regex_str, str(j))
    #         if match_obj != None:
    #             list.append(match_obj.string)

    str_all =''
    for item in list:
        str_all=str_all+item
    with open("./data/bank/data_a.txt", "w") as f:
        f.writelines(str_all)
    # ea.write_excel(filename, sheetname, 0, 0, 'Optimus Prime')
    # ea.write_excel(filename, sheetname, 0, 1, 'Megatron', 1)
    # valueList = ['阿杜 - 烂好人', '阿杜 - 一诺千年', 'Coldplay - Hypnotised', 'Ruth B. - Superficial Love', '杨宗纬、张碧晨 - 凉凉']
    # ea.addSheet(filename, '第2页', 0, valueList)

def getTheme(filename):
    ea = ExcelAction()
    str_all=[]
    sheetname = '数据标准信息项'
    list = ea.read_excel(filename, sheetname)
    for i in range(len(list)):
        if(i>0):
            str_temp = ''
            if (list[i])[1] != None:
                str_temp = str_temp + str((list[i])[1]) + " "
            if (list[i])[2] != None:
                str_temp = str_temp + str((list[i])[2]) + " "
            if (list[i])[3] != None:
                str_temp = str_temp + str((list[i])[3]) + " "
            if (list[i])[4] != None:
                str_temp = str_temp + str((list[i])[4]) + " "
            if (list[i])[5] != None:
                str_temp = str_temp + str((list[i])[5]) + " "
            if (list[i])[8] != None:
                str_temp = str_temp + str((list[i])[8]) + " \n"

            str_all.append(str_temp)

    return str_all


def get2Theme(filename):
    # 建表，插入数
    db = pymysql.connect(host="localhost", user="root", password="123456", db="test")
    cursor = db.cursor()
    ea = ExcelAction()
    try:
        sheetname2 = '表清单汇总'
        list2 = ea.read_excel(filename, sheetname2)
        num =0
        for i in range(len(list2)):
            num =num+1
            if(num>13527):
                print('插入数据：%s' % (str(num)))
                a = list2[i][0]
                b = list2[i][1]
                c = list2[i][2]
                d = list2[i][3]
                e = list2[i][4]  # 表名，唯一标示
                f = list2[i][5]
                sql_insert = "UPDATE  DGWORKSHOP_A SET theme_1='%s',theme_2='%s',theme_3='%s',table_name_zh='%s',system_name_zh='%s' WHERE table_name_en ='%s'" % (
                a, b, c, d, f, e)
                # 执行sql语句
                cursor.execute(sql_insert)
                # 提交到数据库执行
                db.commit()
    except Exception as e:
        print(e)
        # 发生错误时回滚
        db.rollback()

        # 关闭数据库连接
    db.close()


    # sheetname1 = '表清单汇总'
    # list1 = ea.read_excel(filename, sheetname1)
    # for i in range(len(list1)):
    #     list_temp =[]
    #     list_temp.append(str((list1[i])[0]))
    #     list_temp.append(str((list1[i])[1]))
    #     list_temp.append(str((list1[i])[2]))
    #     list_temp.append(str((list1[i])[3]))
    #     list_temp.append(str((list1[i])[4]))
    #     list_sheet1.append(list_temp)




def getQAList():

    # filename = r'./data/power/术语库_安全等级分析V1.7.xlsx'

    list_0  = getTheme(r'./data/bank/数据标准-交易主题.xlsx')
    list_1 = getTheme(r'./data/bank/数据标准-产品主题.xlsx')
    list_2 = getTheme(r'./data/bank/数据标准-协议主题.xlsx')
    list_3 = getTheme(r'./data/bank/数据标准-客户主题.xlsx')
    list_4 = getTheme(r'./data/bank/数据标准-渠道主题.xlsx')
    list_5 = getTheme(r'./data/bank/数据标准-组织机构主题.xlsx')
    list_6 = getTheme(r'./data/bank/数据标准-财务主题.xlsx')
    list_7 = getTheme(r'./data/bank/数据标准-账户主题.xlsx')


    with open("./data/bank/data_qq_yes.txt", "w") as f:
        for item in list_0:
            f.writelines(item)
        for item in list_1:
            f.writelines(item)
        for item in list_2:
            f.writelines(item)
        for item in list_3:
            f.writelines(item)
        for item in list_4:
            f.writelines(item)
        for item in list_5:
            f.writelines(item)
        for item in list_6:
            f.writelines(item)
        for item in list_7:
            f.writelines(item)


def read2Excel():
    '''
    读取语料库参考.xlsx
    :return:
    '''
    get2Theme(r'./data/语料库参考.xlsx')

    # insert_sql(listsheet2)

    # list_a = listsheet1
    # list_b =listsheet2
    # list_all = []
    # a =0
    #
    # with open("./data/data_big2.txt", "w") as f:
    #     for item1 in list_a:
    #         a =a+1
    #         if(a>167044):
    #             table_name_1 = item1[4]
    #             print('表1字段：' + str(a))
    #             for item2 in list_b:
    #                 table_name_2 = item2[0]
    #                 artif_name_2 = item2[1]
    #                 if (table_name_1 == table_name_2):
    #                     str_item = item1[0] + ' ' + item1[1] + ' ' + item1[2] + ' ' + item1[3] + ' ' + artif_name_2 +'\n'
    #                     print('str_item:' + str_item)
    #                     f.writelines(str_item)
    #                     list_all.append(str_item)
    #                     list_b.remove(item2)






def insert_sql_2(list):
    # 建表，插入数
    db = pymysql.connect(host="localhost", user="root", password="123456", db="test")
    cursor = db.cursor()
    try:
        # SQL 插入语句
        for i in range(len(list)):
            theme_1 = list[i][0]
            theme_2 = list[i][1]
            theme_3 = list[i][2]
            table_name_zh = list[i][3]
            table_name_en = list[i][4]

            sql_insert = "INSERT  DGWORKSHOP_A(theme_1,theme_2, theme_3, table_name_zh, table_name_en,system_name_zh) \
                               VALUES ('%s', %s, %s, %s, %s,%s )" % \
                  (theme_1,theme_2,theme_3,table_name_zh,table_name_en)
            print(sql_insert)
            # 执行sql语句
            cursor.execute(sql_insert)
            # 提交到数据库执行
            db.commit()
    except:
        # 发生错误时回滚
        db.rollback()

    # 关闭数据库连接
    db.close()


def insert_sql(list):
    # 建表，插入数
    db = pymysql.connect(host="localhost", user="root", password="123456", db="test")
    cursor = db.cursor()
    try:
        # SQL 插入语句
        for i in range(len(list)):
            theme_1 = list[i][0]
            theme_2 = list[i][1]
            theme_3 = list[i][2]
            table_name_zh = list[i][3]
            table_name_en = list[i][4]

            sql_insert = "INSERT  DGWORKSHOP_A(table_name_zh, table_name_en,system_name_zh) \
                               VALUES ('%s', %s, %s, %s, %s,%s )" % \
                  (theme_1,theme_2,theme_3,table_name_zh,table_name_en)
            print(sql_insert)
            # 执行sql语句
            cursor.execute(sql_insert)
            # 提交到数据库执行
            db.commit()
    except:
        # 发生错误时回滚
        db.rollback()

    # 关闭数据库连接
    db.close()


def readSql():
    # 建表，插入数
    db = pymysql.connect(host="localhost", user="root", password="123456", db="test")
    cursor = db.cursor()
    try:
        # SQL 插入语句
        sql = """select * from DGWORKSHOP_A;"""
        cursor.execute(sql)
        results = cursor.fetchall()
        with open("./data/data_big.txt", "w") as f:
            a=0
            for row in results:
                a = a+1

                if(a>0):
                    print(str(a))
                    theme_1 = row[1]
                    theme_2 = row[2]
                    theme_3 = row[3]
                    table_name_zh = row[4]
                    field = row[7]

                    if(theme_1==None and theme_2==None and theme_3==None):
                        print()
                    else:
                        if (theme_1 == None):
                            theme_1 = ''
                        if (theme_2 == None):
                            theme_2 = ''
                        if (theme_3 == None):
                            theme_3 = ''
                        if (table_name_zh == None):
                            table_name_zh = ''
                        if (field == None):
                            field = ''
                        str_item = theme_1 + ' ' + theme_2 + ' ' + theme_3 + ' ' + table_name_zh + ' ' + field + '\n'
                        print('第'+str(a)+'条：'+str_item)
                        f.writelines(str_item)
    except Exception as e:
        print(e)
        # # 发生错误时回滚
        db.rollback()

    # 关闭数据库连接
    db.close()




if __name__ == '__main__':
    print()
    #getString()

    #读取Excel
    # readExcel()

    # 分级标准匹配库
    # getQAList()

    # read2Excel()

    # readSql()

