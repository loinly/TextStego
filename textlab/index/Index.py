#! python3
#  -*- coding: utf-8 -*-
import os
import time
from whoosh.index import create_in
from whoosh.analysis import SpaceSeparatedTokenizer
from whoosh.fields import *
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from fileutil import FileUtil

'''
索引类 创建: 搜索:
'''


class Index(object):

    # def __init__(self,datapath,savepath):
    #     self.savepath = savepath

    @staticmethod
    def build(datapath, indexpath):
        if not indexpath:
            os.mkdir(indexpath)
        print(' the process of create build start!')
        schema = Schema(title=TEXT(stored=True), path=TEXT(stored=True),
                        content=TEXT(analyzer=SpaceSeparatedTokenizer()))
        if not os.path.exists(indexpath):  # 索引存储路径
            os.mkdir(indexpath)
        ix = create_in(indexpath, schema)  # 创建索引
        writer = ix.writer()
        for filename in os.listdir(datapath):
            filepath = os.path.join(datapath, filename)
            content = FileUtil.readfile(filepath)
            writer.add_document(path=filepath, title=filename, content=content)
        writer.commit()
        print(' the process of create build end!')

    @staticmethod
    def search(indexpath, querystring, limit=None):
        res = []
        ix = open_dir(indexpath)
        with ix.searcher() as searcher:
            # 1.解析器
            parser = QueryParser("content", ix.schema)
            # 2.联合搜索
            # query = And([Term('content',u'中国'),Term('content','哈哈哈!')]) #
            # 直接构造Query对象
            myquery = parser.parse(querystring)

            def start(): return int(time.time() * 1000)
            results = searcher.search(myquery, limit=limit)
            def end(): return int(time.time() * 1000)
            print("匹配 " + querystring + ",总共花费" + str((end() - start())
                                                      ) + "毫秒" + "查询到" + str(len(results)) + "个记录")
            for item in results:
                res.append(item.fields())
            # print(res)
        return res


if __name__ == '__main__':

    datapaths = r'F:\LabData\NetBigData\prepaper'
    indexpaths = r'F:\LabData\NetBigData\pindex'
    string = u'基于 网络 文本'
    r = Index.search(indexpaths, string)
    for result in r:
        print(result)
    pass
