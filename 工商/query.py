from mutool.reader import *
from mutool.constants import *
import json
from bs4 import BeautifulSoup
import time

req = requests.session()
req.headers = defaultDynamicHeader
req.headers['Cookies'] = "BAIDUID=63559594F3C2CC8748F85776FBEA2586:FG=1; PSTM=1575971620; BIDUPSID=E7E3CB03A41C36242A1A19FEC49A1668; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_WISE_SIDS=140349_114745_139397_135846_125696_139148_120167_138470_138772_139193_133995_138878_137985_140173_131247_132552_137743_118883_118874_118856_118833_118791_138165_107318_138883_140259_136431_139214_140267_139297_138148_140122_138778_139175_140078_140113_136196_137105_140590_139693_133847_140793_137734_134046_131423_140718_136537_141103_110085_140325_127969_140285_140593_140864_139885_137253_139406_127417_138313_139908_138426_139733_140684_139926_140597_140230_140962; H_PS_PSSID=1426_21089_26350_30499; BDSFRCVID=viFsJeCCxG3e4WjuX5BoXfu-45WmsOHdnSYc3J; H_BDCLCKID_SF=tRk8oKPyJKvbfP0k-nOKMJOH-UnLqhop257Z0lOnMp05eDn5hnoBDxFFKn3A04Qpb6bX2-oVBtJPeIO_e6_5D55WjNts-bbfHjcL3RRsHJOoDDv1WMjcy4LdjG5NJ-cDMJ7thpkb5lczfn31yPnm3qLe3-Aq5xc9tnPeWbb7KROEH4jkQ-KbQfbQ0bnPqP-jW5ILhU7jMn7JOpkRbUnxy50vQRPH-Rv92DQMVU52QqcqEIQHQT3m5-5bbN3ut6IDJbKe_IK-fbjjfbTCMJOBq4k0-qJ-a4JQa5TbsJOOaCkKOpTRy4oTLnk1DU_JL-Ttyg0eQ-I5Jlc0Mf3zKUn1b-C9Wf-eBjIDJbKe_IK-fbjjfbTCMJOBq4k0-qJ-a4JQa5TbsJOOaCkBoCJRy4oTLnk1DU_JL-TtynTWbRnqb4cajx3zKUn1b-C9Wf-eBjIDJbKe_IK-fbjjfbTCMJOBq4k0-qJ-a4JQa5TbsJOOaCv-jqQRy4oTLnk1DU_JL-TtynTGWMnDb6CMMf3zKUn1b-C9Wf-eBjT2-DA_oD-KtIoP; delPer=0; PSINO=6; pgv_pvi=8005358592; pgv_si=s8622326784; Hm_lvt_55b574651fcae74b0a9f1cf9c8d7c93a=1577342219,1578282024,1578908128,1578908153; Hm_lpvt_55b574651fcae74b0a9f1cf9c8d7c93a=1578908153"

for comp in open("source.txt",encoding="utf-8").readlines():
    location = None
    fromTag = None
    comp = comp.strip("\n")
    url = "https://baike.baidu.com/wikiui/api/getcertifyinfo?lemma={}".format(comp)
    jsonText,req = getSource(url,session=req)
    jsonData = json.loads(jsonText)
    if len(jsonData['data'])!=0:
        location = jsonData['data']['location']
        fromTag = "baidu"
    else:
        url = "https://www.kanzhun.com/autocomplete/searchkey.json?query={}&type=3".format(comp)
        jsonText, req = getSource(url, session=req)
        jsonData = json.loads(jsonText)
        if len(jsonData['suggestions'])!=0:
            dataId = jsonData['suggestions'][0]['data']
            url = "https://www.kanzhun.com/gso{}.html?ka=com1-title".format(dataId)
            html,req = getSource(url,session=req)
            soup = BeautifulSoup(html,"html.parser")
            locationTag = soup.find("div",attrs={'class':'location'})
            if locationTag:
                location = locationTag.get_text().strip('\n')
                fromTag = "kanzhun"
        else:
            pass

    print(location,fromTag)