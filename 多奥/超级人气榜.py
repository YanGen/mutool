from mutool.reader import *
from mutool.constants import *
from mutool.writer import *
from mutool.date import *
from mutool.validate import *
import re,random
# from bs4 import BeautifulSoup
import json
from concurrent.futures import ProcessPoolExecutor
from mutool.executer import *

mp = 10

# validatePath("data")

req = requests.session()
req.headers = defaultStaticHeader

def parser(kw):
    global req
    # kw = "箱子"
    dataCache = [kw]
    code = ""
    for page in range(1, mp + 1):
        print("页", page)
        if page == 1:
            url = "http://taoke.jsgrain.com/search.php?type=form&ish=&kw=" + kw
        else:
            url = 'http://taoke.jsgrain.com/search/{}-{}.html'.format(code,page)
        html, req, status = getSource(url, session=req)
        print(html)
        if page == 1:
            reg = re.compile('<a href="/search/(.*?)-2\.html">2</a>').findall(html)
            if not reg:return
            code = reg[0]
        html = html.replace('href="/', 'href="http://taoke.jsgrain.com/')

        soup = BeautifulSoup(html, "html.parser")
        lts = soup.find_all('li', attrs={'class': 'g_over'})
        for lt in lts:
            ait = lt.find('a', attrs={'class': 'img'})
            aith = ait['href'] if ait else ""
            it = lt.find('img')
            its = it['src'] if it else ""
            tit = it['alt'] if it else ""
            xlt = lt.find('span', attrs={'class': 'goods-num'})
            xl = xlt.get_text().replace("销量 ", "") if xlt else ""
            pst = lt.find('span', attrs={'class': 'price'})
            prc = pst.get_text() if pst else ""
            bt = lt.find('b', attrs={'class': 'coupon'})
            dpl = bt.a['href'] if bt and bt.find('a') else ""
            dpt = bt.a.get_text() if bt and bt.find('a') else ""
            print(aith, its, tit, xl, prc, dpl, dpt)

            productItem = '''<br>
        <p align="center"><a href="{商品推广链接}" target="_blank"><img src="{商品图片地址}"  alt="{标题}" border="0" /></a></p>
        <p align="center"><b><a href="{商品推广链接}" target="_blank">{标题}</a></b> (<b>{价格}</b>元)</p >
        <p align="center">
        30天售出 <b>{销量}</b> 件 -  <a href="{店铺链接}" target="_blank">{掌柜名}</a></p>
        <p align="center">
        <a href="{商品推广链接}" target="_blank"><img src="http://jd.jsgrain.com/style/images/buy_item.gif" border="0" /></a>
        <a href="{店铺链接}" target="_blank"><img src=""http://jd.jsgrain.com/style/images/buy_shop.gif" border="0" /></a>
        </p>'''.replace("{商品推广链接}", aith).replace("{商品图片地址}", its).replace("{标题}", tit).replace("{价格}", prc).replace(
                "{销量}", xl).replace("{店铺链接}", "dpl").replace("{掌柜名}", dpt)
            dataCache.append(productItem)
            # if len(dataCache) >= 50:
            #     newData = []
            #     dataCache = dataCache[:50]
            #     if os.path.exists("data/{}.csv".format(kw)):
            #         data = csvReader("data/{}.csv".format(kw))[:50]
            #         for ind in range(50):
            #             row = data[ind]
            #             row.append(dataCache[ind])
            #             newData.append(row)
            #     else:
            #         for item in dataCache:
            #             newData.append([item])
            #     writerToCsv("data/{}.csv".format(kw),data=newData,append=False)
            #     dataCache = []
    writerToCsv("data.csv", [dataCache])

def main():
    source = open("source.txt",encoding='utf-8').read()
    for item in source.split("\n"):
        if item:
            item = item.strip()
            parser(item)



if __name__ == '__main__':
    main()