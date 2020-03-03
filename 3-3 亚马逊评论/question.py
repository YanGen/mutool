import re
import lxml
import time
import json
from bs4 import BeautifulSoup
import requests
import csv
import os
import jieba
from collections import Counter
from Trans import Trans

Ts = Trans()

reqNum = 0

headers = {
    "user-agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
}

exceptText = ["答案","when","this","the","do","is","it","to","and","Q"]

req = requests.session()
req.headers = headers

req.get("https://www.amazon.cn")


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
    reqNum += 1
    print("程序第", reqNum, "次请求~")
    try:
        response = req.get(url, timeout=10)
    except:
        response = req.get(url, timeout=10)
    html = response.content.decode("utf-8")
    # print(html)
    if html == "":
        time.sleep(15)
        try:
            response = req.get(url, timeout=10)
        except:
            response = req.get(url, timeout=10)
        html = response.content.decode("utf-8")
        # raise (Exception("服务器不给数据,请重置起始页后重启！"))

    if "Access to this page has been denied because we believe you are using automation tools to browse the website." in html:
        print("err-被检查")
        print("url", url)
        time.sleep(60 * 15)
        raise Exception("错误重启。")
        req = requests.session()
        req.headers = headers
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
            if point > 100:
                break
            else:point += 1



    return data

def crawlIndex(uid,language="en"):
    timestamp = int(time.time() * 1000)
    page = 1
    while(1):
        csvFile = open("question.csv", mode="a", newline="",encoding="utf-8")
        csvWriter = csv.writer(csvFile)
        url = "https://www.amazon.com/ask/questions/asin/"+uid+"/"+str(page)+"/ref=ask_ql_psf_ql_hza?sort=HELPFUL&isAnswered=true&askLanguage=en_US"

        html = loadPage(url)
        soup = BeautifulSoup(html, "lxml")
        askTeaserQuestionsTag = soup.find("div", attrs={"class": "askTeaserQuestions"})

        if askTeaserQuestionsTag:
            print(len(list(askTeaserQuestionsTag.children)))
            for divTag in askTeaserQuestionsTag.children:
                if (str(divTag).replace("\n", "").strip() == ""): continue
                spanCountTag = divTag.find("span", attrs={'class': 'count'})
                count = 0
                if spanCountTag:
                    count = spanCountTag.get_text()
                quesTag = divTag.find("div", attrs={'class': 'a-fixed-left-grid-inner'})
                ques = ""
                tsContent = ""
                if quesTag:
                    ques = quesTag.get_text().replace("votevotesQuestion","").replace("{ display : none; }","").replace(".noScriptDisplayLongText","").replace(".noScriptNotDisplayExpander  { display : block; }","").replace(".noScriptNotDisplayExpander { display : none; }","").replace("  ","").replace("\n","").strip()


                    tsUrl = Ts.other_to_zn_translate(ques, language)
                    jsonText = loadPage(tsUrl)
                    jsonData = json.loads(jsonText)

                    for dataItem in jsonData[0]:
                        if (dataItem[0]):
                            tsContent += dataItem[0]

                    with open(uid+"问答.txt",mode="a",encoding="utf-8")as f:
                        for i in range(int(count)+1):
                            f.write(ques+"\n")

                    with open(uid + "翻译问答.txt", mode="a", encoding="utf-8")as f:
                        for i in range(int(count) + 1):
                            f.write(tsContent + "\n")


                dataList = [uid,count,ques,tsContent]
                print(dataList)

                csvWriter.writerow(dataList)
        else:
            break
        csvFile.close()
        page += 1


if __name__ == '__main__':
    uid = "B06Y5C863S"
    language = "en"
    # crawlIndex(uid,language)
    # print("结束！")
    # with open(uid+"问答.txt","r",encoding="utf-8")as f:
    #
    #     cip = frequency(f.read())
    #
    #     csvFile = open(uid+"问答词频.csv", mode="a", newline="", encoding="utf-8")
    #     csvWriter = csv.writer(csvFile)
    #     for c in cip:
    #
    #         csvWriter.writerow([str(c[0]),str(c[1])])
    #
    # with open(uid + "翻译问答.txt", "r", encoding="utf-8")as f:
    #
    #     cip = frequency(f.read())
    #
    #     csvFile = open(uid + "翻译问答词频.csv", mode="a", newline="", encoding="utf-8")
    #     csvWriter = csv.writer(csvFile)
    #     for c in cip:
    #         csvWriter.writerow([str(c[0]), str(c[1])])
    #     csvFile.close()
    oldfiles = os.listdir('.')
    for file in oldfiles:
        if '.txt' in file:
            os.remove(file)