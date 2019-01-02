#! python3
# -*- coding:utf-8 -*-
import os
import config
from fileutil import FileUtil
from index.index import Index
from word2vec.vector import WV


class Search(object):
    """
    在网页文本库中检索,并保存检索到的文本
    """

    def __init__(self, keys, pindexp):
        self.pindexp = pindexp
        self.keys = keys
        self.savepath, self.kwpath = self.init_path()

    def init_path(self):
        savepath = os.path.join(config.hidepath, '_'.join(self.keys))
        kwpath = os.path.join(config.hidekwpath, '_'.join(self.keys))
        if not os.path.exists(savepath):
            os.makedirs(savepath)
        else:
            FileUtil.init_path(savepath)
        return savepath, kwpath

    def query(self, keywords, kwpath=''):
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
                    print(
                        ".................Failed to find similar words................")
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
                        hidekey.append('0')
                        keywords.pop(0)
                        path.append(None)
                        # flag = True
                    else:
                        path.append(doc)
                        num.append(maxh)
                        maxh = 0
                        q = ''
                    flag = True
            if not keywords:
                path.append(paper)
        hide_string = ' '.join(hidekey)
        FileUtil.writefile(hide_string, kwpath)
        return path

    def retrieve(self, keywords):
        savepath, kwpath = self.savepath, self.kwpath
        path = self.query(keywords, kwpath)
        for i, doc in enumerate(path):
            if not doc:
                oldname = os.path.join(
                    config.unMatch_path, config.unMatch_name)
                newname = os.path.join(
                    savepath, str(i) + '+' + config.unMatch_name)
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
        return path

    # def retrieve1(self, keywords):
    #
    #     savepath, kwpath = self.savepath, self.kwpath
    #
    #     res = self.query(keywords, kwpath)
    #
    #     for i, doc in enumerate(res):
    #         if not doc:
    #             oldname = os.path.join(
    #                 config.unMatch_path, config.unMatch_name)
    #             newname = os.path.join(
    #                 savepath, str(i) + '+' + config.unMatch_name)
    #             FileUtil.copyfile(oldname, newname)
    #             continue
    #         name = doc[0].get('title')
    #         oldname = doc[0].get('path')
    #         newname = os.path.join(savepath, str(i) + '+' + name)
    #         FileUtil.copyfile(oldname, newname)
    #     return res


if __name__ == '__main__':
    pass
