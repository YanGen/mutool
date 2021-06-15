import os
import csv
import requests
import json
import random
from mutool.annotation import *

requests.packages.urllib3.disable_warnings()
prePath = os.getcwd()
# 切换目录到当前脚本下
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# 这里加载一些东西
ua = json.loads(open("source/ua.txt").read())
# 返回旧工作目录
os.chdir(prePath)

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
def xlsReader(path:str,sheetByNameOrIndex=0)->list:
    import xlrd
    readWorkbook = xlrd.open_workbook(path)
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


@retry(20)
def getSource(url, rb=False,enconding="utf-8",params=None,session:requests.session()=None,timeout=10,sleepTime = 0,switchUA = False):
    if switchUA:
        session.headers["User-Agent"] = random.choice(ua)
    @sleep(sleepTime)
    def inner(url, rb=False,enconding="utf-8",params=None,session:requests.session()=None,timeout=10):
        req = session if session else requests.session()
        response = req.get(url,params=params, timeout=timeout,verify=False)
        # 从请求对象中拿到相应内容解码成utf-8 格式
        if rb:
            return response.content

        html = response.content.decode(enconding, "ignore")
        return html,req,response.status_code
    return inner(url=url, rb=rb,enconding=enconding,params=params,session=session,timeout=timeout)


@retry(20)
def postApi(url,data=None,json=None,enconding="utf-8", session:requests.session()=None):

    req = session if session else requests.session()
    response = req.post(url, data=data,json=None, timeout=30)
    html = response.content.decode(enconding)
    return html,req,response.status_code