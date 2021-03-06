#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Author:Limei

import xlrd
import json
import numpy as np
import os
import re


def getExcelSheet():
    # 读取Excel表格，项目的相对路径
    path = './Beta1.19.1+Beta1.20.1测试报告汇总.xlsx'
    if os.path.exists(path):
        excel = xlrd.open_workbook(path)
		# 输出Excel的工作簿
		# for sheet in excel.sheets():
		#     print(sheet.name)
		# 读取表格中特定工作簿
        sheet = excel.sheet_by_index(0)
        return sheet
    else:
        print("文件不存在")


# 获取某行所有值
def getRowValues(sheet):
    # 总行数、总列数
    rowNum = sheet.nrows
    colNum = sheet.ncols
    listValues = []
    for i in range(rowNum):
        sheetValues = sheet.row_values(i)
        if sheetValues[0] == '人员':
            # 获取当前索引
            listNum = []
            # 从人员下一行开始读取
            j = i + 1
            # 这是第39行数据(实际第40行)，作为字典的key值
            dictKey = sheet.row_values(i)  # <class 'list'>
            for m in range(sheet.nrows - (i + 1)):  # sheet.nrows - (i+1) = 43
                dict = {}
                try:
                    dictValues = sheet.row_values(j)  # <class 'list'>,len(dictValues) = 11
                except:
                    print('第{0}条数据处理失败'.format(m))
                listValues.append(sheet.row_values(j))
                j += 1
    # 逐行显示
    for i in listValues:
        # json.dumps 序列化时默认使用的ascii编码，想输出真正的中文需要指定ensure_ascii=False
        jsonTxt = json.dumps(i, ensure_ascii=False)  # <class 'str'>
        data = jsonTxt.replace('"', '')
        # data2=data.replace('\\n', '')
        # print(data2)
        json2Split = data.split(',')
        with open(txtPath, 'a', encoding='utf-8') as sheetTxt:
            sheetTxt.write(json2Split[2] + '\n')
            sheetTxt.write(json2Split[3] + '\n')
            sheetTxt.write(json2Split[4] + '\n')
        sheetTxt.close()


def getTxtData(txtPath):
    dict = {}
    with open(txtPath, 'r', encoding='utf-8') as file:
        txtData = file.read()  # <class 'str'>
        file.close()
    # 替换空格
    datas = txtData.replace('\\n', ' ')  # 只剩下空格,<class 'str'>
    datas2 = datas.split(' ')
    # print(datas2)
    for line in datas2:
        strs = line.replace('\n', '').split('/')
        # print(strs)
        if len(strs) >= 2 and strs[1] != '':
            if strs[1] not in dict:
                dict[strs[1]] = int(strs[0])
            else:
                dict[strs[1]] = int(dict[strs[1]]) + int(strs[0])
    # print(dict)
    return dict


if __name__ == '__main__':
    # 读取工作簿并返回
    sheet = getExcelSheet()  # <class 'xlrd.sheet.Sheet'>
    if sheet != None:
		# 写入TXT，创建TXT文件
        txtName = 'sheetTxt.txt'
		# 文件的相对路径地址
        txtPath = os.getcwd() + '\\' + txtName
		# 后面会重复写入文件，避免多次运行写入多次，写入文件前判断是否有这个文件，有就删除
        if (os.path.exists(txtPath)):
            os.remove(txtPath)
		# 抽取特定行列转化成list并返回
        rowValues = getRowValues(sheet)  # <class 'list'>
		# 读取TXT内容并统计
        datas = getTxtData(txtPath)
		# 对结果进行排序
        numSort = sorted(datas.items(), key=lambda kv: kv[1], reverse=True)
		# 统计总数
        numSum = sum(datas.values())
		# 写入原先的TXT文件
        with open(txtPath, 'w', encoding='utf-8') as file:
            file.write("统计结果：\n" + str(numSort) + '\n')
            file.write("总数一共：" + str(numSum))
            file.close()
        print("统计完成")
    else:
        print("无法统计")