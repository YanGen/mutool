import re
import os
from .annotation import retry,sleep
# 格式化文件标题
def validateFileTitle(title:str) -> str:
    return re.sub(r"[\/\\\:\*\?\"\<\>\|]", '_', title.strip().replace("/r","").replace(":","：").replace("  "," ").replace('\t','').replace("\n",""))[:260]

# 命名重复处理 文件名递增
def increasingFileName(filename):
    if not os.path.exists(filename):
        return filename
    dFile = filename.split(".")
    fExt = dFile[-1]
    lExt = -1 - len(fExt)
    newFile = filename[:lExt]
    newFile = re.sub('\(\d\)$', '', newFile)  # remove file sequencial number
    i = 1
    while os.path.exists(newFile + "(%s).%s" % (i, fExt)):
        i += 1
    dFile = newFile + "(%s).%s" % (i, fExt)
    return dFile

# 验证文件路径 如果不存在会创建
def validatePath(path) -> bool:
    if os.path.exists(path):
        return True
    else:
        try:
            os.makedirs(path)
        except:
            raise Exception
        else:
            return True

# 获取文件流
def validateFileStream(path,mode="a",retryNumber=10,sleepTime=0.5,encoding="gbk",newline=""):

    @retry(retryNumber)
    @sleep(sleepTime)
    def spin(path,mode):
        try:
            f = open(path,mode=mode,encoding=encoding,newline=newline)
        except Exception as e:
            print("尝试获取 {} 写入权失败~重新尝试".format(path),e)
            raise Exception
        else:
            return f
    return spin(path,mode)


# 对list 进行统一编码 包括深层次的遍历
def codingList(dataList,coding="gbk") -> list:
    newData = []
    for item in dataList:
        if isinstance(item,str):
            newData.append(item.encode(coding,"ignore").decode(coding,"ignore"))
        elif isinstance(item,list):
            newData.append(codingList(item,coding))
        else:
            newData.append(item)
    return newData

# list去重
def removeDuplication(dataList:list) -> list:
    pass


