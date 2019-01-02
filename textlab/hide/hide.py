#! python3
# -*- coding:utf-8 -*-
import os
import config
import jieba.analyse
from index.index import Index
from index.search import Search
from encode.position import Location
from spidercontent.spiderTo import SpiderTo
from spiderlink.spiderlink import SpiderLink
from pretreatment.pretreatment import PreDeal


class Hide(object):
    def __init__(self, root):
        self.root = root
        pass

    def info(self, info='', col_bits=5, pagenum=100):
        keywords = PreDeal.seg(info)
        # 1. 关键词提取
        keys = jieba.analyse.textrank(
            info, topK=10, withWeight=False, allowPOS=(
                'ns', 'n', 'vn', 'v'))
        # 2. 调用搜索引擎爬取相关网页
        # 2.1 抓取链接
        spider_link = SpiderLink(keys, self.root)
        spider_link.crawl(pagenum)
        # 2.2 抓取内容
        filename = '_'.join(keys) + '.html'
        spider_to = SpiderTo(filename)
        spider_to.crawl()
        # 3. 文本预处理,去重,去停用词,分词,保留url和关键词集合
        p = PreDeal()
        filepath = os.path.join(config.spidertext, '_'.join(keys))
        propath = os.path.join(config.prepapath, '_'.join(keys))
        p.savetexts(filepath=filepath, prepath=propath)
        # 4. 构建索引, 并检索,得到包含关键词信息的网页
        # 4.1 索引构建
        indexpath = os.path.join(config.indexpath, '_'.join(keys))
        Index.build(datapath=propath, indexpath=indexpath)
        search = Search(keys=keys, pindexp=indexpath)
        # 4.2 搜索并保存
        search.retrieve(keywords=keywords)
        # 5. 选取最佳网页,位置信息描述,编码
        info_kws = keywords[:]
        loc = Location(keywords=info_kws, col_bits=col_bits)
        name = '_'.join(keys)
        res_list = loc.describe(name)
        return res_list


if __name__ == '__main__':
    roots = "http://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd={0}&pn={1}"
    h = Hide(root=roots)
    # text1 ='基于网络文本的无载体信息隐藏技术利用互联网上大量的网络文本来隐藏信息，提高了隐藏容量、成功率及传输效率'
    text1 = '无载体信息隐藏由于能在不经任何修改的情况下将秘密信息传递给载体而成为热点。'
    res1 = h.info(info=text1, col_bits=5, pagenum=100)
    for items in res1:
        print(items)
    pass
