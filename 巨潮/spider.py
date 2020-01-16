import json
from mutool.reader import *
from mutool.constants import *
from mutool.date import *
from mutool.writer import *
from mutool.validate import *

req = requests.session()

def func():
    global req

    for page in range(1,100):
        print("page",page)
        req.headers = defaultDynamicHeader
        postData = "pageNum={}&pageSize=30&column=szse&tabName=fulltext&plate=&stock=&searchkey=%E5%A7%94%E6%89%98%E8%B4%B7%E6%AC%BE&secid=&category=&trade=&seDate=2014-01-01~2019-12-31&sortName=&sortType=&isHLtitle=true".format(page)
        jsonText,req = postApi("http://www.cninfo.com.cn/new/hisAnnouncement/query",data=postData,session=req)
        try:
            jsonData = json.loads(jsonText)
        except:
            print(jsonText)
            exit()
        announcements = jsonData['announcements']
        totalData = []
        req.headers = defaultStaticHeader
        for item in announcements:
            secCode = item['secCode']
            secName = item['secName']
            announcementTitle = item['announcementTitle'].replace("<em>","").replace("</em>","")
            announcementTime = item['announcementTime']
            announcementTime = timestampToDate(announcementTime/1000,format="%Y-%m-%d")
            adjunctUrl = "http://static.cninfo.com.cn/"+item['adjunctUrl']
            print(secCode,secName,announcementTitle,announcementTime)
            dataItem = [secCode, secName, announcementTitle, announcementTime]
            totalData.append(dataItem)
            fileTitle = "{}-{} {}：{}".format(secCode, announcementTime, secName, announcementTitle)
            fileTitle = validateFileTitle(fileTitle)
            if os.path.exists("pdf/{}.pdf".format(fileTitle)):
                continue

            response = getSource(adjunctUrl, rb=True, session=req)
            validatePath("pdf")
            writerToMedia("pdf/{}.pdf".format(fileTitle), stream=response)
        writerToCsv("data.csv",data=totalData)



if __name__ == '__main__':
    func()