import requests
from mutool.htmlparser import *
from mutool.annotation import *
from mutool.validate import *
from mutool.output import *
from mutool.writer import *


from bs4 import BeautifulSoup


# 模拟请求头
headers = {
    'Host':'www.stats.gov.cn',
    'Referer':'http://www.stats.gov.cn/tjsj/pcsj/rkpc/6rp/left.htm',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}



req = requests.session()
req.headers = headers


@retry(10)
def loadPage(url,char = None):
    global req
    # 请求模块执行POST请求,response为返回对象
    response = req.get(url,timeout=10)
    # 从请求对象中拿到相应内容解码成utf-8 格式
    if char:
        html = response.content.decode(char)
    else:
        html = response.content.decode("utf-8")

    return html
@log("execute")
def func():


    url = "http://www.stats.gov.cn/tjsj/pcsj/rkpc/6rp/html/A0108c.htm"
    html = loadPage(url,"gb2312")
    soup = BeautifulSoup(html,"html.parser")
    Tbody = soup.find("table")

    searchParams = []
    searchParams.append(gengeralParamForParserTable(tag="tr",splitStart=5,splitEnd=37))
    searchParams.append(gengeralParamForParserTable(tag='td'))
    tableData = parserTable(Tbody,searchParams)
    for item in tableData:
        print(item)

def func2():
    f = validateFileStream("data.csv")
    f.write("aaa")
    f.close()



if __name__ == "__main__":

    data = [
        ["张三", "男", "19", "杭州", "研发工程师"],
         ["李四", "男", "22", "北京", "医生"],
         ["王五", "女", "33", "珠海", "出租车司机"]

    ]

    writerToXls("data.xls",data,sheetByNameOrIndex="default3",append=False)
    exit()


    for i in range(0, 100000, 1024):  # 模拟文件的传输
        progress(100000, i)
    func2()