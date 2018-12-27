#! python3
# -*- coding:utf-8 -*-
import os
import config
import jieba.analyse
from fileutil import FileUtil
from index.Index import Index
from index.Search1 import Search1
from spidercontent.spiderTo import SpiderTo
from spiderlink.SpiderLink import SpiderLink
from pretreatment.pretreatment import Prepaper


class Hide(object):
    def __init__(self, root):
        self.root = root
        pass

    def info(self, fi='', pagenum=100):
        info = FileUtil.readfile(fi)
        keywords = Prepaper.seg(info)
        # 1, 基于 TextRank 算法进行关键词提取
        keys = jieba.analyse.textrank(
            info, topK=10, withWeight=False, allowPOS=(
                'ns', 'n', 'vn', 'v'))
        # 2, 调用搜索引擎爬取相关网页
        # 2.1 抓取链接
        spider_link = SpiderLink(keys, self.root)
        spider_link.crawl(pagenum)
        # 2.2 抓取内容
        filename = '_'.join(keys) + '.html'
        spider_to = SpiderTo(filename)
        spider_to.crawl()
        # 3, 文本预处理,去重,去停用词,分词,保留url和关键词集合
        p = Prepaper()
        filepath = os.path.join(config.spidertext, '_'.join(keys))
        propath = os.path.join(config.prepapath, '_'.join(keys))
        p.savetexts(filepath=filepath, propath=propath)
        # 4,构建索引, 并检索,得到包含关键词信息的网页
        # 4.1 索引构建
        indexpath = os.path.join(config.indexpath, '_'.join(keys))
        Index.build(datapath=propath, indexpath=indexpath)
        search = Search1(filename=fi, pindexp=indexpath)
        # 4.2 搜索并保存
        info_k = keywords[:]
        num = search.retrieve(keywords=info_k)
        return keywords, num

    def expriment(self, path='', pagenum=100):
        savename = os.path.join(config.hidepath, 'res.txt')
        for dirname in os.listdir(path):   # dir: hidepath
            filepath = os.path.join(path, dirname)
            if os.path.isdir(filepath):
                for f in os.listdir(filepath):
                    fi = os.path.join(filepath, f)
                    res = []
                    keywords, num = self.info(fi=fi, pagenum=pagenum)
                    unmatch = 0
                    hidenum = 0
                    s = '\t||'
                    for i in num:
                        if i == 0:
                            unmatch += 1
                        else:
                            hidenum = hidenum + i
                        s = s + '\t' + str(i)
                    res.append(fi)
                    res.append(str(len(keywords)))
                    res.append(str(hidenum))
                    res.append(str(len(num)))
                    res.append(str(unmatch))
                    res_str = '\t'.join(res) + s + '\n'
                    FileUtil.write_apd_file(res_str, savename)
                FileUtil.write_apd_file(dirname + ' End !\n', savename)
                pass
        pass

if __name__ == '__main__':
    roots = "http://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd={0}&pn={1}"
    h = Hide(root=roots)
    path1 = r'F:\LabData\NetBigData\test\hideinfo'
    h.expriment(path=path1, pagenum=100)
    pass
