from bs4 import BeautifulSoup
from mutool.constants import defaultStaticHeader
from mutool.reader import *
from mutool.writer import *
from mutool.executer import *

#迭代层数
rec = 2

req = requests.session()
req.headers = defaultStaticHeader

log = []
checkIn = []
words = ['东柄','黄色']
newData = []

def check(url):
    for word in words:
        if word in url:
            return True
    return False


def readNext(url):
    global newData,checkIn
    print("检查：",url)
    if len(log) > 100:
        writerToText("log.txt", text="\n".join(log))
        newData = []
    html, req1, status = getSource(url, session=req, timeout=30)
    soup = BeautifulSoup(html,"html.parser")
    # 这里拿所有url 和 判断
    urls = soup.find_all("a", href=True)
    for urlTag in urls:
        url = urlTag['href'] if urlTag.__contains__("href") else None
        if url:
            if ".css" in url or ".js" in url:
                continue
            newData.append(url)
            result = check(url)
            if result:
                checkIn.append(url)
                if len(checkIn) > 10:
                    writerToText("checkIn.txt", text="\n".join(checkIn))
                    checkIn = []


def func(urlList,rec,num):
    global log,newData
    if rec == num:
        return

    newData = []

    executeFunction(readNext,urlList,threadNumber=20)

    writerToText("log.txt",text="\n".join(log))


    func(newData, rec, num+1)
    
if __name__ =='__main__':
    ks = open("source.txt",encoding="utf-8").read().split("\n")
    num = 0
    func(ks,rec,num)