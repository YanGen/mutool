import re,time
from mutool.reader import *
from mutool.constants import *
from mutool.writer import *
from bs4 import BeautifulSoup

req = requests.session()
req.headers = defaultStaticHeader

def func():
    global req

    for page in range(1,100):
        url = "https://www.c5game.com/dota.html?page={}".format(page)
        html ,req = getSource(url,session=req)

        soup = BeautifulSoup(html,"html.parser")
        liTags = soup.find_all("li",attrs={'class':'selling'})
        totalData = []
        for liTag in liTags:
            src = "https://www.c5game.com" + liTag.find('a')['href']
            num = liTag.find('span',attrs={'class':'num'}).get_text().strip(' on selling')
            name = liTag.find('p',attrs={'class':'name'}).get_text().strip('\n')
            detailHtml,req = getSource(src,session=req)
            reg = re.compile('href="(.*?)">View Steam Price</a>').findall(detailHtml)
            stream = reg[0] if len(reg)!=0 else None
            classId,market = None,None
            if stream:
                stream = stream.replace("&#039;",'\'')
                streamHtml,req = getSource(stream,session=req)
                classIdReg = re.compile('"classid":"(.*?)",').findall(streamHtml)
                classId = classIdReg[0] if len(classIdReg)!=0 else None

                classIdReg = re.compile('"market_hash_name":"(.*?)"').findall(streamHtml)
                market = classIdReg[0] if len(classIdReg)!=0 else None
                if not classId and not market:
                    print("空值")
                    time.sleep(5*60)

            dataList = [name,classId,market,num]
            print(dataList)
            totalData.append(dataList)
            time.sleep(2.5)
        writerToCsv("data.csv",totalData)


if __name__ == '__main__':
    func()