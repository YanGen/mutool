from mutool.reader import *
from mutool.constants import *

keyword = "Acme Furniture"

req = requests.session()
req.headers = defaultStaticHeader

def parser():
    req.headers['Cookie'] = ""
    url = "https://www.trademarkia.com/china/trademarks-search.aspx?tn={}".format(keyword).replace(" ","+")
