import os
import csv
import xlrd
import requests
from mutool.annotation import *

def csvReader(path,encoding="gbk"):
    csvFile = open(path, encoding=encoding)
    csvReader = csv.reader(csvFile)
    dataList = list(csvReader)
    csvFile.close()
    return dataList
def textReader(path,encoding="gbk")->str:
    txtFile = open(path, encoding=encoding)
    text = txtFile.read()
    txtFile.close()
    return text
def xlsReader(path:str,sheetByNameOrIndex=0,encoding="gbk")->list:
    readWorkbook = xlrd.open_workbook(path, formatting_info=True)
    assert sheetByNameOrIndex in readWorkbook.sheet_names(),"没有 {} sheet".format(sheetByNameOrIndex)

    if isinstance(sheetByNameOrIndex, int):
        sheet = readWorkbook.get_sheet(sheetByNameOrIndex)  # 获得要操作的页
    else:
        sheet = readWorkbook.sheet_by_name('{}'.format(sheetByNameOrIndex))
    dataList = []
    for indRow in range(len(sheet.nrows)):
        row = sheet.row_values()
        dataList.append(row)
    return dataList

# 搜索文件 包括深层次搜索
def searchFile(dirPath:str,include:str=None,exclude:str=None,startWith:str=None,endWith:str=None,deepSearch=True,result=None):
    if os.path.isfile(dirPath):
        return []

    if not result:
        result = []
    fls = os.listdir(dirPath)
    for f in fls:
        innerDirPath = dirPath + '/' + f
        if os.path.isfile(innerDirPath) and (exclude not in f) if exclude else True and ((include in f) if include else False or (f.startswith(startWith))if startWith else False or (f.endswith(endWith)) if endWith else False):
            result.append(innerDirPath)
        elif not os.path.isfile(innerDirPath) and deepSearch:
            result = searchFile(innerDirPath,include=include,exclude=exclude,startWith=startWith,endWith=endWith, result=result)
    return result


@retry(10)
def getSource(url, rb=False,enconding="utf-8",session:requests.session()=None,timeout=10,sleepTime = 0):
    @sleep(sleepTime)
    def inner(url, rb=False,enconding="utf-8",session:requests.session()=None,timeout=10):
        req = session if session else requests.session()
        response = req.get(url, timeout=timeout)
        # 从请求对象中拿到相应内容解码成utf-8 格式
        if rb:
            return response.content

        html = response.content.decode(enconding, "ignore")
        return html,req,response.status_code



    return inner(url=url, rb=rb,enconding=enconding,session=session,timeout=timeout)


@retry(10)
def postApi(url,data=None,json=None,enconding="utf-8", session:requests.session()=None):

    req = session if session else requests.session()
    response = req.post(url, data=data,json=None, timeout=20)
    html = response.content.decode(enconding)
    return html,req,response.status_code