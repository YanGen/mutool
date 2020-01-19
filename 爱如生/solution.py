import string
from mutool.reader import csvReader
from mutool.writer import *

paramsDict = {
        "反":5312,
        "乱":9387,
        "逆":5573,
        "叛":2355,
        "贼":32465,
    }
dataDict = {

}
for item in paramsDict:
    dataList = csvReader("{}.csv".format(item))
    for item1,item2,item3 in dataList:
        item1 = item1.strip("卷").strip(string.digits)
        if "志" in item1 and not item1.endswith("志"):
            item1 = item1.split("志")[0]+"志"
        if dataDict.__contains__(item1):
            dataDict[item1][item].append(item3)
        else:
            dataDict[item1] = {
                "反": [],
                "乱": [],
                "逆": [],
                "叛": [],
                "贼": [],
            }
            dataDict[item1][item].append(item3)
totalData = []
totalData.append(["县志名","乱","反","叛","逆","贼"])

for item in dataDict:
    print(item)
    row = [item]
    tag = False
    for item1 in paramsDict:
        if len(dataDict[item][item1]) > 400:
            tag = True
        row.append("共{}个， {}".format(len(dataDict[item][item1]),"，  ".join(dataDict[item][item1][0:400])))
    if len(row) == 6:
        totalData.append(row)

    if tag:
        tag = False
        row = [item]
        for item1 in paramsDict:
            if len(dataDict[item][item1]) > 800:
                tag = True
            row.append("共{}个， {}".format(len(dataDict[item][item1]),"，  ".join(dataDict[item][item1][400:800])))
        if len(row) == 6:
            totalData.append(row)

        if tag:
            tag = False
            row = [item]
            for item1 in paramsDict:
                if len(dataDict[item][item1]) > 1200:
                    tag = True
                row.append("共{}个， {}".format(len(dataDict[item][item1]),"，  ".join(dataDict[item][item1][800:1200])))
            if len(row) == 6:
                totalData.append(row)
            if tag:
                tag = False
                row = [item]
                for item1 in paramsDict:
                    if len(dataDict[item][item1]) > 1600:
                        tag = True
                    row.append(
                        "共{}个， {}".format(len(dataDict[item][item1]), "，  ".join(dataDict[item][item1][1200:1600])))
                if len(row) == 6:
                    totalData.append(row)
                if tag:
                    tag = False
                    row = [item]
                    for item1 in paramsDict:
                        if len(dataDict[item][item1]) > 2000:
                            tag = True
                        row.append(
                            "共{}个， {}".format(len(dataDict[item][item1]), "，  ".join(dataDict[item][item1][1600:2000])))
                    if len(row) == 6:
                        totalData.append(row)
                    if tag:
                        tag = False
                        row = [item]
                        for item1 in paramsDict:
                            if len(dataDict[item][item1]) > 2400:
                                tag = True
                            row.append(
                                "共{}个， {}".format(len(dataDict[item][item1]),
                                                  "，  ".join(dataDict[item][item1][2000:])))
                        if len(row) == 6:
                            totalData.append(row)
writerToCsv("结果.csv",totalData,append=False)

#
# for item in dataDict:
#     # print(item)
#     反 = "共{}个， {}".format(len(dataDict[item]['反']), "，  ".join(dataDict[item]['反']))
#     乱 = "共{}个， {}".format(len(dataDict[item]['乱']), "，  ".join(dataDict[item]['乱']))
#     逆 = "共{}个， {}".format(len(dataDict[item]['逆']), "，  ".join(dataDict[item]['逆']))
#     叛 = "共{}个， {}".format(len(dataDict[item]['叛']), "，  ".join(dataDict[item]['叛']))
#     贼 = "共{}个， {}".format(len(dataDict[item]['贼']), "，  ".join(dataDict[item]['贼']))
#     totalData.append([item, 乱, 反, 叛, 逆 ,贼])
# writerToCsv("结果.csv",totalData,append=False)