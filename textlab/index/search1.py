#! python3
# -*- coding:utf-8 -*-
import os
import config
from fileutil import FileUtil
from index.index import Index
from word2vec.vector import WV


class Search1(object):
    """
    在网页文本库中检索,并保存检索到的文本
    """

    def __init__(self, filename, pindexp):
        self.pindexp = pindexp
        self.filename = filename
        self.savepath, self.kwpath = self.init_path()

    def init_path(self):
        print('init retrieve save directory.....')
        dirs, f = os.path.split(self.filename)
        savepath = os.path.join(config.hidepath, dirs[-2:], f.rstrip('.txt'))
        kwpath = os.path.join(config.hidekwpath,  dirs[-2:])
        FileUtil.init_path(savepath)
        if not os.path.exists(kwpath):
            os.makedirs(kwpath)
        kwpath = os.path.join(kwpath, f)
        return savepath, kwpath

    def query(self, keywords):
        path = []    # 已经找到的文章列表
        num = []     # 每篇含文章组合的个数
        unmatch = 0  # 失配个数
        maxh = 0     # 关键词个数
        q = ''       # 联合关键词
        flag = True  # 失配标志
        hidekey = []
        while keywords:
            kw = keywords[0]
            paper = Index.search(self.pindexp, q + ' ' + kw, limit=None)
            if paper:
                keywords.pop(0)
                hidekey.append(kw)
                q = q + ' ' + kw
                maxh += 1
            else:                       # 当联合搜索无法进行下去时,转为寻找相似关键词
                simikeys = WV.similarwords(kw)
                t_paper = []
                if not simikeys:
                    print(".................Failed to find similar words................")
                    flag = False
                else:
                    for skw, similarity in simikeys:
                        sq = q + ' ' + skw
                        t_paper = Index.search(self.pindexp, sq, limit=None)
                        if t_paper:
                            hidekey.append(skw)
                            keywords.pop(0)
                            q = sq
                            maxh += 1
                            break
                    if not t_paper:      # 有关键词但联合搜索仍失败
                        flag = False
                # 失配
                if not flag:
                    doc = Index.search(self.pindexp, q, limit=None)
                    if not doc:
                        print("The keyword  '%s' is unMatch !" % kw)
                        unmatch += 1
                        num.append(0)
                        hidekey.append('0')
                        keywords.pop(0)
                        path.append(None)
                    else:
                        path.append(doc)
                        num.append(maxh)
                        maxh = 0
                        q = ''
                    flag = True
            if not keywords:
                path.append(paper)
                num.append(maxh)

        return path, hidekey, num

    # 不使用word2vec的查询
    # def query(self, keywords, kwpath=''):
    #     path = []  # 已经找到的文章列表
    #     num = []  # 每篇含关键词的个数
    #     maxh = 0  # 隐藏关键词的个数
    #     q = ''  # 联合关键词
    #     hidekey = []
    #     while keywords:
    #         kw = keywords[0]
    #         paper = Index.search(self.pindexp, q + ' ' + kw, limit=None)
    #         if paper:
    #             keywords.pop(0)
    #             hidekey.append(kw)
    #             q = q + ' ' + kw
    #             maxh += 1
    #         else:  # 当联合搜索无法进行下去时, 失配
    #             doc = Index.search(self.pindexp, q, limit=None)
    #             if not doc:
    #                 print("The keyword  '%s' is unMatch !" % kw)
    #                 num.append(0)
    #                 hidekey.append('0')
    #                 keywords.pop(0)
    #                 path.append(None)
    #             else:
    #                 path.append(doc)
    #                 num.append(maxh)
    #                 maxh = 0
    #                 q = ''
    #         if not keywords:
    #             path.append(paper)
    #             num.append(maxh)
    #
    #     return path, hidekey, num

    def retrieve(self, keywords):
        savepath, kwpath = self.savepath, self.kwpath
        path, hidekey, num = self.query(keywords)
        for i, doc in enumerate(path):
            if not doc:
                oldname = os.path.join(config.unMatch_path, config.unMatch_name)
                newname = os.path.join(savepath, str(i) + '+' + config.unMatch_name)
                FileUtil.copyfile(oldname, newname)
            elif len(doc) > 1:
                filepath = os.path.join(savepath, str(i))
                if not os.path.exists(filepath):
                    os.mkdir(filepath)
                for d in doc:
                    name = d.get('title')
                    oldname = d.get('path')
                    newname = os.path.join(filepath, str(i) + '+' + name)
                    FileUtil.copyfile(oldname, newname)
            else:
                name = doc[0].get('title')
                oldname = doc[0].get('path')
                newname = os.path.join(savepath, str(i) + '+' + name)
                FileUtil.copyfile(oldname, newname)
            hide_string = ' '.join(hidekey)
            FileUtil.writefile(hide_string, kwpath)
        return num



if __name__ == '__main__':
    pass
