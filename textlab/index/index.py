#! python3
#  -*- coding: utf-8 -*-
import os
import time
import logging
from whoosh.index import create_in
from whoosh.analysis import SpaceSeparatedTokenizer
from whoosh.fields import *
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from fileutil import FileUtil


class Index(object):
    """
    索引类 创建: 搜索:
    """
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger("Index")

    def build(self, datapath, indexpath):
        self.logger.info('the process of create full-text index!')
        schema = Schema(title=TEXT(stored=True), path=TEXT(stored=True),
                        content=TEXT(analyzer=SpaceSeparatedTokenizer()))
        if not os.path.exists(indexpath):  # 索引存储路径
            os.makedirs(indexpath)
        ix = create_in(indexpath, schema)  # 创建索引
        writer = ix.writer()
        for filename in os.listdir(datapath):
            filepath = os.path.join(datapath, filename)
            content = FileUtil.readfile(filepath)
            writer.add_document(path=filepath, title=filename, content=content)
        writer.commit()

    @staticmethod
    def search(indexpath, querystring, limit=None):
        res = []
        ix = open_dir(indexpath)
        with ix.searcher() as searcher:
            # 1.解析器
            parser = QueryParser("content", ix.schema)
            # 2.联合搜索
            # query = And([Term('content',u'中国'),Term('content','哈哈哈!')])
            # 直接构造Query对象
            query = parser.parse(querystring)
            def start(): return int(time.time() * 1000)
            results = searcher.search(query, limit=limit)
            def end(): return int(time.time() * 1000)
            print("match {0} | total token {1} ms, total query {2} records".format(
                querystring, str((end() - start())), str(len(results))))
            for item in results:
                res.append(item.fields())
        return res


if __name__ == '__main__':

    datapaths = r'F:\LabData\NetBigData\prepaper'
    indexpaths = r'F:\LabData\NetBigData\pindex\信息_载体_秘密_传递_情况_成为_热点_修改_隐藏'
    string = u'基于 网络 文本'
    r = Index.search(indexpaths, string)
    for result in r:
        print(result)
    pass
