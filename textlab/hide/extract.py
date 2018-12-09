#! python3
# -*- coding:utf-8 -*-
import re
import os
import time
import math
import jieba
import config
import chardet
import requests
from fake_useragent import UserAgent


from fileutil import FileUtil


class Extract(object):

    def __init__(self):
        pass

    @staticmethod
    def download(url):
        if url is None:
            return None
        ua = UserAgent()
        user_agent = ua.random
        accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
        header = {'Accept': accept, 'User-Agent': user_agent}
        r = requests.get(url, headers=header, timeout=(3, 7))
        if r.status_code == 200:
            r.encoding = chardet.detect(r.content)['encoding']
            return r.text
        return None

    @staticmethod
    def _util(html):
        res = [('<script.*?>[\s\S]*?</script>', ''),
               ('<style.*?>[\s\S]*?</style>', ''),
               ('<[\s\S]*?>', ''), ('\s+', ' '),
               ('&nbsp;', ' ')
               ]
        for rei in res:
            html = re.sub(rei[0], rei[1], html)
        return html

    @staticmethod
    def _dec2bin(num, bits=0):
        s = bin(num).lstrip('0b')
        if len(s) < bits:
            s = '0' * (bits - len(s)) + s
        return s

    def extract(self, url_seq, col_bits):

        url, position = url_seq.split('/pos')

        html = self.download(url.rstrip('\n'))

        text = self._util(html)

        matrix = Predeal.getmatrix(text, col_bits)

        num = int(position[:3], 2)  # 补0数字

        _5_col_bits = int(position[3:8], 2)  # 获取5位比特数

        row_num = len(matrix)

        row_bits = len(self._dec2bin(row_num))   # 行比特数

        pos = position[8:]

        if num != 0:
            pos = position[8:].rstrip('0' * num)

        p_list = re.findall('.{%s}' % row_bits, pos)

        res = []
        for p in p_list:
            x = p[:row_num + 1]
            y = p[row_num + 1:]
            res.append(matrix[x][y])

        return res


class Predeal(object):

    stopwords = FileUtil.readfile(config.stopwordpath).splitlines()

    def __init__(self):
        pass

    @classmethod
    def seg(cls, sentences):
        sentences = cls._renostr(sentences)
        kws = []
        stopwords = cls.stopwords
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

    @staticmethod
    def getupkws(text):
        upkws = []
        kws = Predeal.seg(text)
        t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        FileUtil.writefile('\t'.join(kws), os.path.join('.', t))
        for k in kws:
            if k not in upkws:
                upkws.append(k)
        return upkws

    @staticmethod
    def getmatrix(text, col_bits):
        col_num = pow(2, col_bits)
        kws = Predeal.getupkws(text)
        row_num = math.ceil(len(kws) / col_num)
        r = 0
        matrix = [[] for i in range(row_num)]
        for i, keys in enumerate(kws):
            matrix[r].append(keys)
            if (i + 1) % col_num == 0:
                r = r + 1
        return matrix


if __name__ == '__main__':

    pass
