# -*- coding: utf-8 -*-

import csv, requests, json, time,threadpool,threading
from urllib.request import quote

lock = threading.Lock()

account = {
    "15019542994": "zhangzi1314",

}
log = {
    "cur":None
}
req = requests.session()
req.headers['X-Requested-With'] = 'XMLHttpRequest'


# 获取文件流
def validateFileStream(path, mode="a", retryNumber=10, sleepTime=0.5, encoding="gbk", newline=""):
    def spin(path, mode):
        try:
            f = open(path, mode=mode, encoding=encoding, newline=newline)
        except Exception as e:
            print("尝试获取 {} 写入权失败~重新尝试".format(path), e)
            raise Exception
        else:
            return f

    return spin(path, mode)


# 对list 进行统一编码 包括深层次的遍历
def codingList(dataList, coding="gbk") -> list:
    newData = []
    for item in dataList:
        if isinstance(item, str):
            newData.append(item.encode(coding, "ignore").decode(coding, "ignore"))
        elif isinstance(item, list):
            newData.append(codingList(item, coding))
        else:
            newData.append(item)
    return newData


def postApi(url, data=None, json=None, enconding="utf-8", session: requests.session() = None):
    req = session if session else requests.session()
    response = req.post(url, data=data, json=None, timeout=20)
    html = response.content.decode(enconding, "ignore")
    return html, req, response.status_code
def getSource(url, rb=False,enconding="utf-8",params=None,session:requests.session()=None,timeout=10,sleepTime = 0):
    def inner(url, rb=False,enconding="utf-8",params=None,session:requests.session()=None,timeout=10):
        req = session if session else requests.session()
        response = req.get(url,params=params, timeout=timeout)
        # 从请求对象中拿到相应内容解码成utf-8 格式
        if rb:
            return response.content

        html = response.content.decode(enconding, "ignore")
        return html,req,response.status_code
    return inner(url=url, rb=rb,enconding=enconding,params=params,session=session,timeout=timeout)

def writerToCsv(path: str, data: list, append=True, encoding="gbk") -> bool:
    assert path.endswith(".csv"), "该路径非 .csv 结尾"
    mode = "a" if append else "w"
    csvFile = validateFileStream(path, mode=mode, encoding=encoding, retryNumber=10, sleepTime=0.1)
    csvWriter = csv.writer(csvFile)
    for item in data:
        if isinstance(item, list):
            csvWriter.writerow(codingList(item))
    csvFile.close()


def update():
    global req,log
    req.headers['Content-Type'] = 'application/json'
    for u in account:
        p = account[u]
        if u in log and log[u] <= 0:
            continue
        login = "https://api.chadianshang2.com/pc/user/newLogin"
        postData = '{"userName":"'+u+'","password":"'+p+'","account_type":"USER_PASSWORD"}'
        html, req, status = postApi(login, data=postData, session=req)
        if "登录成功" in html:
            jsonData = json.loads(html)
            token = jsonData['data']['token']
            req.headers['token'] = token
            check(u)
            if log[u] > 0:
                log['cur'] = u
                return
    exit()


def check(u):
    global req, log
    url = "https://api.chadianshang2.com/pc/user/getCurrentUser"
    postData = None
    html, req, status = postApi(url, data=postData, session=req)
    jsonData = json.loads(html.strip())
    print(html)
    userDayHasQueryNum = jsonData['data']['checkCount']
    dbNum = jsonData['data']['taokeCount']
    log[u] =  userDayHasQueryNum
    print("账号", u, "已查询", userDayHasQueryNum,"/",dbNum)

def executeFunction(funcation,params:list,threadNumber:int = 10):
    import threadpool

    validateParams = []
    for item in params:
        if isinstance(item,list):
            item = (item,None)
            validateParams.append(item)
        else:
            validateParams.append(item)

    taskPool = threadpool.ThreadPool(threadNumber)
    spiders = threadpool.makeRequests(funcation, validateParams)
    for spider in spiders:
        taskPool.putRequest(spider)
    taskPool.wait()

def func(uid):
    global log
    url = "https://api.chadianshang2.com/pc/check/checkCommonNum"
    postData = 'nick={}'.format(uid).encode("utf-8")
    req.headers['Content-type'] = "application/x-www-form-urlencoded;charset=UTF-8"
    html, req1, status = postApi(url, data=postData, session=req, enconding="utf-8")
    if '请您前往个人中心登录' in html:
        update()
        func(uid)
        return
    if '该旺旺ID不存在.请更改' in html:
        return
    jsonData = json.loads(html)
    info = [uid]
    title = [uid, 'fox', 'jiangNum', 'yunBlack', 'renZheng', 'sentRate', 'buyerTotalNum', 'sellerTotalNum',
         'wangwang', 'weekCount', 'countBefore', 'wwcreatedStr', 'vipInfo', 'searchTime', 'ifSearch',
         'weekCreditAverage', 'badTotal', 'receivedRate', 'vip', 'taoling', 'buyerGoodNum', 'gender']
    info = [uid, 'fox', 'jiangNum', 'yunBlack', 'renZheng', 'sentRate', 'buyerTotalNum', 'sellerTotalNum',
         'wangwang', 'weekCount', 'countBefore', 'wwcreatedStr', 'vipInfo', 'searchTime', 'ifSearch',
         'weekCreditAverage', 'badTotal', 'receivedRate', 'vip', 'taoling', 'buyerGoodNum', 'gender']
    for k in jsonData['data']:
        if k == 'isOk':continue
        if k == 'purchaseRecords':continue
        if k not in info:continue
        ind = info.index(k)
        if ind == -1:
            info[info.index(k)] = ""
            continue
        info[info.index(k)] = jsonData['data'][k]
    for ind in range(1,len(info)):
        t = title[ind]
        info[ind] = str(info[ind]).replace(t,"")
    print(info)
    writerToCsv("data.csv", data=[info])


    lock.acquire()
    log[log['cur']] = log[log['cur']] -1
    if log[log['cur']] == 1:
        log[log['cur']] = log[log['cur']] - 1
        update()
    lock.release()
    return

def Main():
    infoTitle = ['旺旺', '狐狸', '降权', '云黑名单', '认证', '给出好评率', '购买数', '商家信誉', '旺旺', '近一周查询商家数', '上一周查询商家数', '注册日期', 'vip信息', '查询时间', 'ifSearch', '买家总周平均', '差评总数', '好评率', 'vip', '淘龄', '好评', '性别']
    writerToCsv("data.csv", data=[infoTitle], append=False)
    text = open("source.txt", encoding="utf-8").read().split("\n")
    params = []
    for item in text:
        if item:
            params.append(item)
    func(params[0])
    executeFunction(func,params[1:])

if __name__ == '__main__':
    Main()
