import csv
import xlrd
import requests

def csvReader(path,encoding="gbk"):
    csvFile = open(path, encoding=encoding)
    csvReader = csv.reader(csvFile)
    dataList = list(csvReader)
    csvFile.close()
    return dataList
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

def getSource(url, rb=False,enconding="utf-8",session:requests.session()=None):
    req = session if session else requests.session()
    response = req.get(url, timeout=10)
    # 从请求对象中拿到相应内容解码成utf-8 格式
    if rb:
        return response.content

    html = response.content.decode(enconding, "ignore")

    return html,req


def postApi(url,data, enconding="utf-8",session:requests.session()=None):
    req = session if session else requests.session()
    response = req.post(url, data=data, timeout=20)
    html = response.content.decode(enconding)
    return html