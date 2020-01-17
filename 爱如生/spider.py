from mutool.reader import *
from mutool.constants import *
from mutool.htmlparser import *
from mutool.executer import *
from mutool.writer import *

req = requests.session()
req.headers = defaultStaticHeader
req.headers['Cookie'] = "_webvpn_key=eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiMjAxNzI5MTUwOCIsImlhdCI6MTU3OTIyMzYwMCwiZXhwIjoxNTc5MzEwMDAwfQ.zKR2kk0GeoVBp07ETxEqay1L1jZrg5K30obrsW7cOxg; webvpn_username=2017291508%7C1579223600%7Cf9d788c58a4c5c6ebe16e2491e7132a50500845f; JSESSIONID=D62D69E87EEB5C7D2BEB75B4FECA9A19"

def parser(page,key):
    global req

    url = "https://dh-ersjk-com.vpn.sicnu.edu.cn/spring/front/qwsearch?pc=17&page={}&cv={};;;;;%E6%B8%85;1;23;0".format(
        page, key)
    html, req = getSource(url, session=req)
    soup = BeautifulSoup(html, "html.parser")
    tbodyTag = soup.find("tbody")
    if tbodyTag:
        searchParams = [gengeralParamForParserTable("tr"), gengeralParamForParserTable("td", {'class': 'cur'})]
        tableData = parserTable(tbodyTag, searchParams,searchData=[])
        totalData = []
        print(page,key,len(tableData))
        for row in tableData:
            row[0] = row[0].split(",")[0]
            # print(row)
            totalData.append(row)
        writerToCsv("{}.csv".format(key),totalData)

def func():
    paramsDict = {
        "反":5312,
        "乱":9387,
        "逆":5573,
        "叛":2355,
        "贼":32465,
    }
    params = []
    for key in paramsDict:
        for page in range(1,paramsDict[key]+1):
            params.append([page,key])
    executeFunction(parser,params,threadNumber=15)

if __name__ == '__main__':
    func()