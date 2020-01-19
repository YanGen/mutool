from mutool.reader import *
from mutool.constants import *

keyword = "ICECO"
# keyword = "Acme Furniture"

req = requests.session()
req.headers = defaultStaticHeader

def parser():
    global req
    req.headers['Cookie'] = ""
    url = "https://www.trademarkia.com/china/trademarks-search.aspx?tn={}".format(keyword).replace(" ","+")
    html,req = getSource(url,session=req)
    print(html)

def parser2():
    global req
    req.headers['Cookie'] = "TMSearchsession=705753098.20480.0000; ROUTEID=.4"
    req.headers['Referer'] = "http://tmsearch.uspto.gov/bin/gate.exe?f=searchss&state=4805:44rm2m.1.1"
    url = "http://tmsearch.uspto.gov/bin/showfield?f=toc&state=4805%3A44rm2m.1.1&p_search=searchss&p_L=50&BackReference=&p_plural=yes&p_s_PARA1=&p_tagrepl%7E%3A=PARA1%24LD&expr=PARA1+AND+PARA2&p_s_PARA2=Acme+Furniture&p_tagrepl%7E%3A=PARA2%24COMB&p_op_ALL=AND&a_default=search&a_search=Submit+Query&a_search=%26%2325552%3B%26%2320132%3B%26%2326597%3B%26%2335810%3B"
    html, req = getSource(url, session=req)
    print(html)

if __name__ == '__main__':
    parser2()

