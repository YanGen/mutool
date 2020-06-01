from mutool.reader import *
from mutool.writer import *
from mutool.constants import *
from bs4 import BeautifulSoup
import re,random
import configparser #引入模块

# 更换ip采集条数 = 1000000 #500条 换
更换ip间隔秒数 = 5*60

if not os.path.exists("log.ini"):
    writerToText("log.ini",text="[DEFAULT]")
req = requests.session()
req.headers = defaultStaticHeader

line = 0
pret = time.time()

data = []

def initStatus():
    global req
    req = requests.session()
    req.headers = defaultStaticHeader
    # req.headers['Cookie'] = open("status.txt").read()
    # html, req, status = getSource("https://www.qcc.com/")
    # html, req, status = getSource("https://www.qcc.com/material/theme/chacha/cms/v2/images/phoneCode2.json")
    req.headers[
        'Accept'] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    req.headers[
        'User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"


def resetIp():
    global req
    req = requests.session()
    url = "http://api.wandoudl.com/api/ip?app_key=e6c05c9a4209e893f38c63b22e979316&pack=207335&num=1&xy=3&type=1&lb=\n&mr=1&"
    txt = requests.get(url).content.decode("utf-8")

    # req.headers['Proxy-Connection'] = 'keep-alive'
    req.proxies = {
        'http': 'socks5://{}'.format(txt.replace("\n", "").strip()),
        'https': 'socks5://{}'.format(txt.replace("\n", "").strip())
    }
    print(req.proxies)

def func(keyword,page):
    global pret,data
    global line
    line += 1
    if len(data)>1000:
        writerToCsv("total.csv",data)
        data = []
    url = "https://xin.baidu.com/s?q={}&t=0".format(keyword)
    try:
        html,req1,status = getSource(url,session=req)
    except:
        print("链接错误，切换ip")
        resetIp()
        # time.sleep(10)
        return func(keyword,page)

    if "异常请求，请点击“诊断页面”"in html or "访问频率过高" in html:
        print("出现验证码 切换ip")
        resetIp()
        return func(keyword,page)

    if "请尝试输入更准确的关键词并重新搜索。" in html:
        return '小查没有找到相关数据'
    soup = BeautifulSoup(html,"lxml")
    resultTag = soup.find('div',attrs={'class':'zx-list-content'})
    if resultTag:
        trTags = resultTag.find_all('div',attrs={'class':'zx-list-item'})
        for trTag in trTags:
            name = trTag.find('a',attrs={'class':'zx-list-item-url'}).get_text()
            dzReg = re.compile('<span class="zx-ent-item zx-ent-text long"><span class="zx-ent-pre-title">地址：</span>(.*?)</span>').findall(str(trTag))
            dz = dzReg[0].strip() if dzReg else None
            print(name,dz)
            data.append([keyword,name,dz])
            break
        # writerToCsv("total.csv".format(keyword),data)
        return len(data)
    return func(keyword,page)

def main():
    if not os.path.exists("source.txt"):open("source.txt",mode="w").close()
    if not os.path.exists("status.txt"):open("status.txt",mode="w").close()
    if not os.path.exists("未找到.txt"):open("未找到.txt",mode="w").close()
    initStatus()

    sourceText = open("source.txt",encoding="utf-8").read()
    logText = open("log.ini",encoding="gbk").read()
    notFoundText = open("未找到.txt",encoding="gbk").read()
    index = 0
    for keyword in sourceText.split("\n"):
        index += 1
        statPage = 1
        if keyword+" = " in logText or "--"+keyword+'--' in notFoundText:
            continue
            # statPage = int(DEFAULT[keyword])

        print("-----\n",index,keyword)
        if keyword:
            for page in range(statPage,2):
                # time.sleep(random.randint(4,6))
                result = func(keyword,page)
                if result == '小查没有找到相关数据':
                    print('没有找到相关数据')
                    writerToText("未找到.txt",text="--"+keyword+'--\n')
                if result == 0:
                    break

                writerToText('log.ini',text=keyword + " = 1\n")
if __name__ == '__main__':
    main()
