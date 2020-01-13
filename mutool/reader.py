import csv
import requests

def csvReader(path,encoding="gbk"):
    csvFile = open(path, encoding=encoding)
    csvReader = csv.reader(csvFile)
    dataList = list(csvReader)
    csvFile.close()
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