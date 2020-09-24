from mutool.reader import *
from mutool.constants import *
from mutool.writer import *
from mutool.date import *
from mutool.validate import *
import re,random
from urllib.parse import quote
import json
import string
from random import choice
from concurrent.futures import ProcessPoolExecutor
from mutool.executer import *
import random

mp = 3
ins = 10 # 插入链接数量
mode = "随机" #顺序

validatePath("html")

log = []

req = requests.session()
req.headers = defaultStaticHeader

def suiji(length=15,chars=string.ascii_letters+string.digits):
    return ''.join([choice(chars) for i in range(length)])

def parser(kw):
    global log
    global req
    # kw = "箱子"
    sj = random.randint(1000000,1000000000)
    code = ""
    if len(log) <= ins:
        insertLog = log
    else:
        if mode:
            # 随机
            insertLog = random.sample(log, ins)
        else:
            # 顺序
            insertLog = log[-ins:]

    for page in range(1,100000):

        if page != 1 and page != mp:
            continue

        print("页",page)
        if page == 1:
            url = "http://taoke.jsgrain.com/search.php?type=form&ish=&kw=" + kw
        else:
            url = 'http://taoke.jsgrain.com/search/{}-{}.html'.format(code,page)
        print(url)
        html,req,status = getSource(url,session=req)
        if page == 1:
            reg = re.compile('<a href="/search/(.*?)-2\.html">2</a>').findall(html)
            if not reg:return
            code = reg[0]

        if page == mp:

            title = '<title>xxx</title>'
            keywords = '<title>xxx</title>'
            description = '<title>xxx</title>'

            r = re.compile('<title>(.*?)</title>').findall(html)
            if r:
                html = html.replace('<title>'+r[0]+'</title>',title)
            r = re.compile('<meta name="description" content="(.*?)" />').findall(html)
            if r:
                html = html.replace('<meta name="description" content="'+r[0]+'" />',description)
            html = html.replace('<meta name="keywords" content="{},全部,商品,多奥淘宝客程序" />'.format(kw),keywords)
            html = html.replace('<script src="/','<script src="http://taoke.jsgrain.com/')
            html = html.replace('type="text/css" href="/','type="text/css" href="http://taoke.jsgrain.com/')
            reg = re.compile('/search/'+code+'-(\d+)\.html').findall(html)
            for item in reg:
                html = html.replace('<a href="/search/{}-{}.html">{}</a>'.format(code,item,item),'<a href="./{}{}.html">{}</a>'.format(sj,item,item))
                html = html.replace('<a href="/search/{}-{}.html">下一页</a>'.format(code,item),'<a href="./{}{}.html">下一页</a>'.format(sj,item))
            if insertLog:
                s = ""
                for kw1,sj1 in insertLog:
                    s += '<li><a href="./{}{}.html">{}</a></li>\n'.format(sj1,page,kw1)
                insertText = '''<div class="cat-wrap main-container">
                    <div class="cat-list clearfix">
                        <span class="cat-lit-title">热门</span>
                        <ul id="duoao_cn_cat" class="clearfix" style="height: 85px;">
                            {}
                            </ul>
                    </div>
                </div>'''.format(s)
                html = html.replace('<div id="footer"',insertText+'\n<div id="footer"')
            writerToText("html/{}{}.html".format(sj,page),html,encoding="utf-8",append=False)
            log.append([kw,sj])
            break

def main():
    source = open("source.txt",encoding='utf-8').read()
    for item in source.split("\n"):
        if item:
            item = item.strip()
            parser(item)

if __name__ == '__main__':
    mode = True if mode == '随机' else False
    main()