from mutool.reader import *
from mutool.constants import *
from mutool.writer import *
from mutool.date import *
from mutool.validate import *
import re,random
from bs4 import BeautifulSoup
import json
from concurrent.futures import ProcessPoolExecutor
from mutool.executer import *

mp = 1

# validatePath("data")

req = requests.session()
req.headers = defaultStaticHeader

def parser(kw):
    global req
    # kw = "箱子"
    dataCache = [kw]
    code = ""
    rank = 0
    for page in range(0, mp + 1):
        print("页", page)
        if page == 0:
            url = "http://taoke.jsgrain.com/coupons.php?type=form&ish=&kw=" + kw
        else:
            url = 'http://taoke.jsgrain.com/coupons/{}-{}.html'.format(code,page)
        html, req, status = getSource(url, session=req)
        if page == 0:
            reg = re.compile('<a href="/coupons/(.*?)-2\.html">2</a>').findall(html)
            if not reg:return
            code = reg[0]
            print(code)
            continue
        html = html.replace('href="/', 'href="http://taoke.jsgrain.com/')

        soup = BeautifulSoup(html, "html.parser")
        lts = soup.find_all('div', attrs={'class': 'item'})
        for lt in lts:
            rank += 1
            # 写到解析 完事后三个脚本存数据库就ok

            ait = lt.find('a')
            aith = ait['href'] if ait else ""
            it = lt.find('img')
            its = it['src'] if it else ""
            lt.find
            tit = it['alt'] if it else ""
            xlt = lt.find('span', attrs={'class': 'goods-num'})
            xl = xlt.get_text().replace("销量 ", "") if xlt else ""
            pst = lt.find('span', attrs={'class': 'price'})
            prc = pst.get_text() if pst else ""
            bt = lt.find('b', attrs={'class': 'coupon'})
            dpl = bt.a['href'] if bt and bt.find('a') else ""
            dpt = bt.a.get_text() if bt and bt.find('a') else ""
            print(aith, its, tit, xl, prc, dpl, dpt)

            productItem = '''<li class="">
<div class="rank">{商品位置}</div>
<div class="item">
<div class="img-block">
< a href=" " target="_blank" rel="nofollow">
< img class="img" src="{商品推广链接}" alt="" width="100%">
</ a>
</div>
<div class="cont">
<p class="tit">< a href="{商品推广链接}" target="_blank" rel="nofollow">{标题}</ a></p >
< a href="{商品推广链接}" target="_blank" rel="nofollow">
<span class="num">{领券购买}</span>
<div class="line-block" title="{优惠券领取数量}">
<div class="line"><em style="width: 2%;"></em></div>
</div>
<div class="wrap">
<div class="price fl">￥<span>{价格}</span><i>{优惠券金额}</i></div>
<div class="ico fr"><i class="tmall tag_tit" title="{掌柜名}"></i></div>
</div>
</ a>
</div>
</div>
</li> '''.replace("{商品推广链接}", aith).replace("{商品图片地址}", its).replace("{标题}", tit).replace("{价格}", prc).replace(
                "{销量}", xl).replace("{店铺链接}", "dpl").replace("{掌柜名}", dpt)
            dataCache.append(productItem)
    writerToCsv("data.csv", [dataCache])

def main():
    source = open("source.txt",encoding='utf-8').read()
    for item in source.split("\n"):
        if item:
            item = item.strip()
            parser(item)



if __name__ == '__main__':
    main()