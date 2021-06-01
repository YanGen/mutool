from mutool.reader import *
import json,time

headers = {
    'authorization':'wxmp.d8af4505-bd17-4e47-b598-5a99b09feb8c',
    'device-fingerprint': 'WHJMrwNw1k/HC1NdButFFLRycQSGM2FFlhkOjmhnlEvYA7DBSVLkOYESFbCMLuJW8Cqtwti8XMr6VJLwL6vY0MCqWVMPGNdvndCW1tldyDzmauSxIJm5Txg==1487582755342',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
    'x-sign': 'X413b24309f343716112e5f930d127a82',
    'content-type': 'application/json',
    'referer': 'https://servicewechat.com/wxb296433268a1c654/38/page-frame.html',
    'accept-encoding': 'gzip, deflate, br'
}
req = requests.session()
req.headers = headers
for page in range(2,10):
    url = 'https://www.xiaohongshu.com/fe_api/burdock/weixin/v2/search/notes?keyword=%E6%96%B0%E5%86%A0&sortBy=general&page={}&pageSize=20&prependNoteIds=&needGifCover=true'.format(page)
    print(url)
    html,req,status = getSource(url,session=req)
    jsondata = json.loads(html)
    for item in jsondata['data']['notes']:
        print(item)
    time.sleep(2)