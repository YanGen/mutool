import requests
import http.client
import hashlib
import urllib
import random
import json
import csv
import time
from bs4 import BeautifulSoup

def csvReader(path,encoding="gbk"):
    csvFile = open(path, encoding=encoding)
    csvReader = csv.reader(csvFile)
    dataList = list(csvReader)
    csvFile.close()
    return dataList

def func(q):

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    appid = '20200114000375416'  # 填写你的appid
    secretKey = 'lbIWxXZ9JhNbkkg9HBSK'  # 填写你的密钥salt = random.randint(32768, 65536)   # 生成一个随机数
    salt = random.randint(32768, 65536)
    sign = appid + q + str(salt) + secretKey  # 将appid和要翻译的字符、随机数、密钥组合成一个原始签名
    m = hashlib.new("md5")
    m.update(sign.encode(encoding="utf-8"))  # 注意使用utf-8编码
    sign = m.hexdigest()  # 得到原始签名的MD5值

    data = {
        "q": q,
        "from": "auto",
        "to": "en",
        "appid": appid,
        "salt": salt,
        "sign": sign
    }
    url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'

    response = requests.get(url, params=data)
    data = json.loads(response.text)
    content = ""
    for item in data['trans_result']:
        content += (item['dst']+"\n")
    time.sleep(1)
    return content

# 对list 进行统一编码 包括深层次的遍历
def codingList(dataList,coding="gbk") -> list:
    newData = []
    for item in dataList:
        if isinstance(item,str):
            newData.append(item.encode(coding,"ignore").decode(coding,"ignore"))
        elif isinstance(item,list):
            newData.append(codingList(item,coding))
        else:
            newData.append(item)
    return newData
# 获取文件流
def validateFileStream(path,mode="a",retryNumber=10,sleepTime=0.5,encoding="gbk",newline=""):

    def spin(path,mode):
        try:
            f = open(path,mode=mode,encoding=encoding,newline=newline)
        except Exception as e:
            print("尝试获取 {} 写入权失败~重新尝试".format(path),e)
            raise Exception
        else:
            return f
    return spin(path,mode)

def writerToCsv(path:str,data:list,append=True,encoding="gbk")->bool:
    assert path.endswith(".csv"),"该路径非 .csv 结尾"
    mode = "a" if append else "w"
    csvFile = validateFileStream(path,mode=mode,encoding=encoding,retryNumber=10,sleepTime=0.1)
    csvWriter = csv.writer(csvFile)
    for item in data:
        if isinstance(item,list):
            csvWriter.writerow(codingList(item))
    csvFile.close()

def parser(title,content):
    print([content])
    content = BeautifulSoup(content,"html.parser").get_text()
    lenth = len(content)
    end = 0
    ran = 1000
    result = ""
    for index in range(1,1000):
        if end + 1000 > lenth:
            part = content[end:lenth]
            end = len(content)
            print(part)
            part = func(part)
            result += part
            break
        else:
            current = end + 1000
            for cursor in range(0,current):
                start = current - cursor
                if content[start] == "。":
                    part = content[end:start]
                    break
        end = start + 1
        print(part)
        part = func(part)
        result += part
    title = func(title)
    writerToCsv("result.csv",[[title,result]])



if __name__ == '__main__':
    dataList = csvReader("source.csv",encoding="utf-8")
    for title ,content in dataList:
        if content:
            parser(title,content)

