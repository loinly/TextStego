#! python3
# -*- coding:utf-8 -*-
import re
import os
import jieba
import config
import logging
from fileutil import FileUtil

'''          
提取中文字符,去停用词,分词,保存
'''


class Prepaper(object):

    stopwords = FileUtil.readfile(config.stopwordpath).splitlines()

    def __init__(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(message)s')
        self.logger = logging.getLogger("text manipulation")

    @classmethod
    def seg(cls, sentences):

        sentences = cls._renostr(sentences)
        kws = []
        stopwords = cls.stopwords
        # departs = jieba.cut_for_search(sentences, HMM=True)  # 搜索引擎模式分词
        departs = jieba.cut(sentences, HMM=True)  # 普通模式
        for word in departs:
            if word not in stopwords:   # 去停用词
                kws.append(word)
        return kws

    @staticmethod
    def _renostr(strings):           # ''' 提取所有汉字 '''
        pattern = re.compile('[\u4e00-\u9fa5]+')
        strs = re.findall(pattern, strings)
        return ''.join(strs)

    def savetexts(self, filepath, propath):
        print('init pretreatment directory.....')
        FileUtil.init_path(propath)
        try:
            file_lists = os.listdir(filepath)  # 返回当前路径下所有文件和路径,字符串类型
            for filename in file_lists:
                file = os.path.join(filepath, filename)
                if os.path.isfile(file):
                    # 1.获取url及文本
                    url, text = FileUtil.get_url_text(file)
                    # 2.关键词信息
                    kws = Prepaper.seg(text)
                    self.logger.info("Save prepo content:{0}".format(filename))
                    FileUtil.writefile(
                        url + '\t'.join(kws),
                        os.path.join(
                            propath,
                            filename))
            print('pretreatment texts end...................................')
        except Exception as e:
            print(e)


if __name__ == '__main__':
    pass
    # p = Prepaper()
    # string = '隐藏 信息 网络 互联网 成功率 技术 利用 容量 传输 提高 大量 文本 效率'
    # keywords = string.split()
    # filepaths = os.path.join(config.spidertext, '_'.join(keywords))
    # propath = os.path.join(config.prepapath, '_'.join(keywords))
    # p.saveIndex(filepaths, propath)
    # print(prepo.seg(txt))
    # print()
    # kws = p.seg("湖南大学简称湖大，坐落于历史文化名城湖南长沙市，隶属于中国教育部，建有中国书院博物馆,国家超级计算长沙中心,是一所历史悠久,蜚声中外的综合类研究型大学")
    # kws = p.seg('基于网络文本的无载体信息隐藏技术利用互联网上大量的网络文本来隐藏信息，提高了隐藏容量、成功率及传输效率')
    # 基于 网络 文本 无载体 信息 隐藏 技术 利用 互联网 上 大量 网络 文 本来 隐藏 信息 提高 隐藏 容量 成功率 传输 效率
    # kws = p.seg('基于 网络 文本 无载体 信息 隐藏 技术 利用 互联网 上 大量 网络')
    # for s in kws:
    #     print(s,end=' ')
