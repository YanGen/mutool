from mutool.writer import *

data = [
        ["张三", "男", "19", "杭州", "研发工程师"],
         ["李四", "男", "22", "北京", "医生"],
         ["王五", "女", "33", "珠海", "出租车司机"]

    ]

writerToXls("data.xls",data,sheetByNameOrIndex="default3",appendSheet=True,appendBook=False)
exit()