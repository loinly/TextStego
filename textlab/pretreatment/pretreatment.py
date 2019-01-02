#! python3
# -*- coding:utf-8 -*-
import re
import os
import jieba
import config
import logging
from fileutil import FileUtil


class PreDeal(object):
    """
提取中文字符,去停用词,分词,保存
    """

    stopwords = FileUtil.readfile(config.stopwordpath).splitlines()

    def __init__(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(message)s')
        self.logger = logging.getLogger("Text manipulation")

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
    def _renostr(strings):
        """
        提取所有汉字
        :param strings:
        :return:
        """
        pattern = re.compile('[\u4e00-\u9fa5]+')
        strs = re.findall(pattern, strings)
        return ''.join(strs)

    def savetexts(self, filepath, prepath):
        """
        保存预处理后的文本
        :param filepath: html文件路径
        :param prepath:  保存路径
        :return:
        """
        self.logger.info('init pretreatment directory:"{0}"'.format(prepath))
        FileUtil.init_path(prepath)
        try:
            file_lists = os.listdir(filepath)  # 返回当前路径下所有文件和路径,字符串类型
            for filename in file_lists:
                file = os.path.join(filepath, filename)
                if os.path.isfile(file):
                    # 1.获取url及文本
                    url, text = FileUtil.get_url_text(file)
                    # 2.关键词信息
                    kws = PreDeal.seg(text)
                    self.logger.info("Store pretreatment texts content:{0}".format(filename))
                    FileUtil.writefile(url + '\t'.join(kws), os.path.join(prepath, filename))
            self.logger.info('Text pretreatment End!')
        except Exception as e:
            print(e)


if __name__ == '__main__':
    pass
