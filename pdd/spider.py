from mutool.reader import *
from mutool.writer import *
from mutool.constants import *
from mutool.validate import *
from mutool.annotation import *
import re
from bs4 import BeautifulSoup


req = requests.session()
req.headers = defaultStaticHeader

headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Connection':'keep-alive',
    'Cookie':'api_uid=CiHfrV7oOS8shwBGPlo0Ag==; _nano_fp=XpEoX0Uqn0UqlpTjlT_~wO75vK_7g6Tene4OyKQr; ua=Mozilla%2F5.0%20(iPhone%3B%20CPU%20iPhone%20OS%2011_0%20like%20Mac%20OS%20X)%20AppleWebKit%2F604.1.38%20(KHTML%2C%20like%20Gecko)%20Version%2F11.0%20Mobile%2F15A372%20Safari%2F604.1; webp=1; pdd_vds=gaquZLhNBuBxDwZyvdvOuxutuwvGrddwdycIflDOvsYmutTOTIfdcuuxCyes',
    'Host':'mobile.pinduoduo.com',
    'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
}
req.headers = headers

validatePath("html")

def func(item):
    global req
    print(item)
    sid = item.strip('http://mobile.pinduoduo.com/goods.html?goods_id=')
    html,req,status = getSource(item,session=req)
    writerToText("html/{}.html".format(sid),html,append=False)

def main():
    source = open("source.txt").read()
    for item in source.split("\n"):
        func(item)

if __name__ == '__main__':
    main()
