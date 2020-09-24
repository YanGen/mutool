from mutool.reader import *
from mutool.constants import *
from mutool.writer import *
from mutool.date import *
from mutool.validate import *
import re,random
import json
from bs4 import BeautifulSoup
from concurrent.futures import ProcessPoolExecutor
from mutool.executer import *

mp = 10

validatePath("data")

req = requests.session()
req.headers = defaultStaticHeader

def main():
    global req
    kw = "箱子"
    validatePath("data/"+kw)
    for page in range(1,mp+1):
        print("页",page)
        if page == 1:
            url = "http://taoke.jsgrain.com/coupons.php?type=form&ish=&kw=" + kw
        else:
            url = 'http://taoke.jsgrain.com/coupons/0-k-j8nCjcCo-{}.html'.format(page)
        html,req,status = getSource(url,session=req)
        html = html.replace('<script src="/','<script src="http://taoke.jsgrain.com/')
        html = html.replace('type="text/css" href="/','type="text/css" href="http://taoke.jsgrain.com/')
        reg = re.compile('/coupons/0-k-j8nCjcCo-(\d+)\.html').findall(html)
        for item in reg:
            html = html.replace('<a href="/coupons/0-k-j8nCjcCo-{}.html">{}</a>'.format(item,item),'<a href="./{}.html">{}</a>'.format(item,item))
            html = html.replace('<a href="/coupons/0-k-j8nCjcCo-{}.html">下一页</a>'.format(item),'<a href="./{}.html">下一页</a>'.format(item))
        writerToText("html/"+kw+"/{}.html".format(page),html,encoding="utf-8",append=False)

if __name__ == '__main__':
    main()

