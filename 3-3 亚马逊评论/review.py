import jieba,configparser,json,hashlib,random
from bs4 import BeautifulSoup
from collections import Counter
from mutool.executer import *
from mutool.writer import *
from mutool.reader import *
from mutool.validate import *
from mutool.constants import *
from mutool.date import *
req = requests.session()
req.headers= defaultDynamicHeader
req.headers["content-type"]="application/x-www-form-urlencoded;charset=UTF-8"
req.headers["x-requested-with"]="XMLHttpRequest"
excludeText = ["答案","when","this","the","do","is","it","to","and","Q"]

validatePath("data")

config = configparser.ConfigParser()
config.read('config.ini')
default = config['DEFAULT']
threadNumber = int(default['thread'])
commentLimit = int(default['commentLimit'])
sortBy = default['sortBy']
print("同时执行数：",threadNumber)
print("单asin数量限制：",commentLimit)

# sortBy = "helpful"
# sortBy = "recent"


config = configparser.ConfigParser()
config.read('log.ini')
logging =config['LOGGING']

def batch(content):
    if not content:
        return ""
    lenth = len(content)
    end = 0
    ran = 500
    result = ""
    for index in range(1, 1000):
        if end + ran > lenth:
            part = content[end:lenth]
            part = trans(part)
            result += part
            break
        else:
            current = end + ran
            for cursor in range(0, current):
                start = current - cursor
                if content[start] == ".":
                    part = content[end:start]
                    break
        end = start + 1
        part = trans(part)
        result += part
    return result

def trans(q):
    if not q:
        return ""

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
        "to": "zh",
        "appid": appid,
        "salt": salt,
        "sign": sign
    }
    url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'

    jsonText,req1,status = getSource(url, params=data,session=req)
    data = json.loads(jsonText)
    content = ""
    for item in data['trans_result']:
        content += (item['dst'] + "\n")
    time.sleep(1)
    return content
def splitWord(text,name):
    words = []
    for item in jieba.cut(text):
        if len(item) >= 2:
            words.append(item)
    counter = Counter(words).most_common(100)

    for item in counter:
        if item[0] in excludeText:
            counter.remove(item)
    dataList = []

    for item in counter:
        if item[0] in excludeText:
            continue
        dataList.append([col for col in item])
    writerToCsv("{}词频.csv".format(name), data=dataList, append=False)

    # 设置柱状图的主标题与副标题
    # bar = Bar("词频", "")
    # x = [item[0] for item in dataList]
    # y = [item[1] for item in dataList]
    #
    # bar.add("次数", x, y, background_color='#fff', mark_line=["average"], mark_point=["max", "min"])
    # bar.render(name + "词频.html")
    #
    # wordcloud = WordCloud(
    #     # 背景颜色
    #     background_color='#fff',
    #     # 画布宽度和高度，如果设置了msak则不会生效
    #     # width=1000,
    #     # height=800,
    # )
    # wordcloud.add("次数", x, y, word_size_range=[20, 100])
    # wordcloud.render(name + "词云.html")
def parser(asin):
    global req
    validatePath("data/{}".format(asin))

    url = "https://www.amazon.com/hz/reviews-render/ajax/lazy-widgets/stream?asin=B07J2Z5DBM&lazyWidget=cr-summarization-attributes&lazyWidget=cr-solicitation&lazyWidget=cr-summarization-lighthut"
    postData = 'scope=reviewsAjax0'
    html, req, status = postApi(url,data=postData,session=req)
    reg = re.compile(r"lighthouseTerms\\\":\\\"(.*?)\\\"}}'></span>").findall(html)
    lighthouseTerms = reg[0] if len(reg) > 0 else None
    words = []
    if lighthouseTerms:
        for lighthouseTerm in lighthouseTerms.split('/'):
            words.append(lighthouseTerm.strip())
    words = ",".join(words)
    print("words:",words)
    writerToText("data/{}/mention.txt".format(asin),text=words,append=False)




    page,count = 1,0
    if logging.__contains__(asin):
        page = int(logging[asin])
    while 1:
        if count >= commentLimit:
            break

        print("当前页", page)

        api = "https://www.amazon.com/hz/reviews-render/ajax/reviews/get/ref=cm_cr_getr_mb_paging_btm_{}".format(
            page)
        postData = "sortBy="+sortBy+"&reviewerType=all_reviews&pageNumber=" + str(
            page) + "&shouldAppend=true&deviceType=mobile&reftag=cm_cr_getr_mb_paging_btm_" + str(
            page) + "&pageSize=20&asin=" + asin + "&scope=reviewsAjax1"

        html,req,status = postApi(api, data=postData,session=req)
        if (html.count('["append","') == 0):
            break

        itemList = html.split("&&&")
        for item in itemList:
            imageCheck = "有图" if 'https://images-na.ssl-images-amazon.com/images/I' in item else "无图"
            if not item or '"append"' not in item:
                continue
            try:
                itemList = json.loads(item.strip())
            except:
                continue
            reviewTag = itemList[2]
            startSearch = re.compile('a-star-small-(\d)').findall(reviewTag)
            start = 0
            if len(startSearch) != 0:
                start = startSearch[0]

            productSearch = re.compile(
                '<span data-hook="format-strip-linkless" class="a-size-small a-color-tertiary">(.*?)</span>').findall(
                reviewTag)
            productType = ""
            if len(productSearch) != 0:
                productType = productSearch[0]

            heplfulSearch = re.compile('>(\d+) people found this helpful</span>').findall(reviewTag)
            heplful = 0
            if len(heplfulSearch) != 0:
                heplful = heplfulSearch[0]

            soup = BeautifulSoup(reviewTag, "html.parser")
            reviewContentTag = soup.find('div', attrs={"class": 'review-text-content'})
            reviewContent = reviewContentTag.get_text().strip() if reviewContentTag else None
            tsContent = batch(reviewContent)


            saveList = [asin, productType, heplful, start,imageCheck,reviewContent,tsContent]

            print(asin, productType, heplful, start)
            writerToCsv('data/{}/问答.csv'.format(asin),data=[saveList],append=True)
            count += 1
        config.set('LOGGING',asin,str(page+1))
        config.write(open('log.ini', 'w'))
        page += 1


    if os.path.exists('data/{}/问答.csv'.format(asin)):
        data = csvReader('data/{}/问答.csv'.format(asin))
        zh = ""
        for row in data:
            zh += row[5]
        ot = ""
        for row in data:
            ot += row[4]

        splitWord(zh, "data/{}/问答中文".format(asin))
        splitWord(ot, "data/{}/问答英文".format(asin))


def run():
    params = []
    asins = open("asin.txt").read().split("\n")
    for asin in asins:
        if asin:
            params.append(asin)
    print(params)
    parser(asin)
    # executeFunction(parser,params=params,threadNumber=threadNumber)


if __name__ == '__main__':
    run()