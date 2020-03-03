import re
import csv
import jieba
from collections import Counter
import json
import time
import requests
import os
from bs4 import BeautifulSoup
from Trans import Trans

Ts = Trans()


headers = {
    "content-type":"application/x-www-form-urlencoded;charset=UTF-8",
    "origin":"https://www.amazon.com",
    "user-agent":"Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25",
    "x-requested-with":"XMLHttpRequest"
}

reqNum = 0

req = requests.session()
req.headers = headers

exceptText = ["when","this","the","do","is","it","to","and"]


def retry(count=1):
    def dec(f):
        def ff(*args, **kwargs):
            ex = None
            for i in range(count):
                try:
                    ans = f(*args, **kwargs)
                    return ans
                except Exception as e:
                    ex = e
            raise ex

        return ff

    return dec


def log(text):
    def decorator(func):
        def wrapper(*args, **kw):
            print('%s %s():' % (text, func.__name__))
            return func(*args, **kw)

        return wrapper

    return decorator

@retry(3)
def loadPage(url):
    global req
    global reqNum
    reqNum +=1
    print("程序第",reqNum,"次请求~")
    try:
        response = req.get(url,timeout=10)
    except:
        response = req.get(url, timeout=10)
    html = response.content.decode("utf-8")
    # print(html)
    if html=="":
        time.sleep(15)
        try:
            response = req.get(url, timeout=10)
        except:
            response = req.get(url, timeout=10)
        html = response.content.decode("utf-8")
        # raise (Exception("服务器不给数据,请重置起始页后重启！"))

    if "Access to this page has been denied because we believe you are using automation tools to browse the website." in html:
        print("err-被检查")
        print("url",url)
        time.sleep(60*15)
        raise Exception("错误重启。")
        req = requests.session()
        req.headers = headers
    return html

@retry(3)
def postApi(url,data):
    global req
    global reqNum
    reqNum +=1


    print("程序第",reqNum,"次请求~")

    response = req.post(url, data=data)

    html = response.content.decode("utf-8")
    # print(html)
    return html

def frequency(txt,):

    words = []
    for x in jieba.cut(txt):
        if len(x) >= 2:
            words.append(x)
    c=Counter(words).most_common(100)
    words1 = []

    data = []
    point = 1
    for item in c:
        if item[0] not in exceptText:
            data.append(item)
            if point > 99:
                break
            else:point += 1



    return data

def crawlIndex(uid,language="en"):
    page = 1
    while(1):
        print("当前页",page)

        csvFile = open("review.csv",mode="a",newline="")
        csvWriter = csv.writer(csvFile)


        reviewAPI = "https://www.amazon.com/hz/reviews-render/ajax/reviews/get/ref=cm_cr_getr_mb_paging_btm_{}".format(page)
        postData = "reviewerType=all_reviews&pageNumber="+str(page)+"&shouldAppend=true&deviceType=mobile&reftag=cm_cr_getr_mb_paging_btm_"+str(page)+"&pageSize=20&asin="+uid+"&scope=reviewsAjax1"

        html = postApi(reviewAPI,postData)
        if(html.count('["append","') == 0):
            break
        page += 1
        dataList = html.replace('\n',"").strip().split("&&&")
        for data in dataList:
            try:
                itemList = json.loads(data.strip())
                if itemList[0] == "append":
                    reviewTag = itemList[2]
                    startSearch = re.compile('a-star-small-(\d)').findall(reviewTag)
                    start = 0
                    if len(startSearch) !=0:
                        start = startSearch[0]

                    productSearch = re.compile('<span data-hook="format-strip-linkless" class="a-size-small a-color-tertiary">(.*?)</span>').findall(reviewTag)
                    productType = ""
                    if len(productSearch)!=0:
                        productType = productSearch[0]

                    heplfulSearch = re.compile('>(\d+) people found this helpful</span>').findall(reviewTag)
                    heplful = 0
                    if len(heplfulSearch) != 0:
                        heplful = heplfulSearch[0]

                    soup = BeautifulSoup(reviewTag,"html.parser")
                    reviewContent = soup.find('div',attrs={"class":'review-text-content'})

                    review = ""
                    tsContent = ""
                    if reviewContent:
                        review = reviewContent.get_text()
                        tsUrl = Ts.other_to_zn_translate(review,language)
                        jsonText = loadPage(tsUrl)
                        jsonData = json.loads(jsonText)

                        for dataItem in jsonData[0]:
                            if(dataItem[0]):
                                tsContent+= dataItem[0]


                        with open(uid + "评论.txt", mode="a", encoding="utf-8")as f:
                            for i in range(int(heplful) + 1):
                                f.write(review + "\n")
                        with open(uid + "翻译评论.txt", mode="a", encoding="utf-8")as f:
                            for i in range(int(heplful) + 1):
                                f.write(tsContent + "\n")

                    saveList = [uid,productType,heplful,start]
                    print(saveList)
                    csvWriter.writerow(saveList)


            except:
                continue
        csvFile.close()

if __name__ == '__main__':
    uid = "B0140JKN2G"
    language = "en"
    crawlIndex(uid,language)
    print("结束")
    with open(uid+"评论.txt","r",encoding="utf-8")as f:

        cip = frequency(f.read())

        csvFile = open(uid+"评论词频.csv", mode="a", newline="", encoding="utf-8")
        csvWriter = csv.writer(csvFile)
        for c in cip:

            csvWriter.writerow([str(c[0]),str(c[1])])
        csvFile.close()

    with open(uid+"翻译评论.txt","r",encoding="utf-8")as f:

        cip = frequency(f.read())

        csvFile = open(uid+"翻译评论词频.csv", mode="a", newline="", encoding="utf-8")
        csvWriter = csv.writer(csvFile)
        for c in cip:

            csvWriter.writerow([str(c[0]),str(c[1])])
        csvFile.close()

    oldfiles = os.listdir('')
    for file in oldfiles:
        if '.txt' in file:
            os.remove(file)