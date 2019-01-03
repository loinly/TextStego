#! python3
# -*- coding:utf-8 -*-
import os
import shutil
# root = r"F:\LabData\NetBigData"  # 给定一个文件夹路径,作为实验数据路径


encoding = 'utf-8'
corpuspath = r"F:\LabData\NetBigData\corpus"
modelpath = r"F:\LabData\NetBigData\model\word2vec.model"
prepapath = r"F:\LabData\NetBigData\prepaper"
indexpath = r"F:\LabData\NetBigData\pindex"
spiders = r"F:\LabData\NetBigData\spiders"   # 爬取路径
spiderlink = r"F:\LabData\NetBigData\spiders\spiderlink"
spiderhtml = r'F:\LabData\NetBigData\spiders\spiderhtml'
spidertext = r"F:\LabData\NetBigData\spiders\spidertext"
stopwordpath = r"F:\LabData\NetBigData\stopword.txt"
failedurlpath = r'F:\LabData\NetBigData\spiders\failed\failed_url'
failedtextpath = r'F:\LabData\NetBigData\spiders\failed\failed_content'
unMatch_path = r'F:\LabData\NetBigData\unmatch'
unMatch_name = "unMatch.txt"
hidepath = r'F:\LabData\NetBigData\test\testh'
hidekwpath = r'F:\LabData\NetBigData\test\testkw'

# root = r"F:\LabData\NetBigData"  # 给定一个文件夹路径,作为实验数据路径
# encoding = 'utf-8'
# corpuspath = os.path.join(root,"corpus")
# modelpath = r"model\word2vec.model"
# prepapath = r"prepaper"
# indexpath = "pindex"
# spiders = r"spiders"   # 爬取路径
# spiderlink = r"spiders\spiderlink"
# spiderhtml = r'spiders\spiderhtml'
# spidertext = r"spiders\spidertext"
# stopwordpath = r"stopword.txt"
# failedurlpath = r'spiders\failed\failed_url'
# failedtextpath = r'spiders\failed\failed_content'


if __name__ == '__main__':
    pass
    # print(ROOT)
    # print(STOPWORDPATH)
    # print(CORPUSPATH)
    # print(PREPAPATH)
    # print(MODELPATH)
    # print(SPIDERPATH)
    # print(os.path.join("1", "2", "3.txt"))
    # shutil.rmtree(r'F:\LabData\NetBigData\spidertext\spiderhtml\\')




