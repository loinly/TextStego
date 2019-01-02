#! python3
# -*- coding:utf-8 -*-

import re
import os
import math
import shutil
import config
import fileinput


class FileUtil(object):
    """
    文件处理类: 读取,写入,添加,清空
    """

    @staticmethod
    def readfile(filename):
        text = ''
        with open(filename, 'r', encoding='utf-8') as fin:
            for line in fin.readlines():
                text += line
        return text

    @staticmethod
    def writefile(string, filename):
        try:
            with open(filename, 'w+', encoding=config.encoding) as fin:
                fin.write(string)
        except IOError as e:
            print(e)

    @staticmethod
    def write_apd_file(string, filename):
        try:
            with open(filename, 'a+', encoding=config.encoding) as f:
                f.write(string)
        except IOError as e:
            print(e)

    @staticmethod
    def readkws(filename):
        res = []
        with open(filename, 'r', encoding='utf-8') as fin:
            fin.readline()
            for line in fin.readlines():
                kws = line.strip('\n').split('\t')
                res.extend(kws)
        return res

    @staticmethod
    def readupkws(filename):
        res = []
        with open(filename, 'r', encoding='utf-8') as fin:
            fin.readline()
            for line in fin.readlines():
                kws = line.strip('\n').split('\t')
                for kw in kws:
                    if kw not in res:
                        res.append(kw)
        return res

    @staticmethod
    def readmatrix(filename, col_bits):
        col_num = pow(2, col_bits)
        kws = FileUtil.readupkws(filename)
        row_num = math.ceil(len(kws)/col_num)
        r = 0
        matrix = [[] for i in range(row_num)]
        for i, keys in enumerate(kws):
            matrix[r].append(keys)
            if (i+1) % col_num == 0:
                r = r+1
        return matrix

    @staticmethod
    def readurl(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            url = f.readline()
        return url

    @staticmethod
    def readchinese(filename):
        chinese_text = ''
        pattern = re.compile('[\u4e00-\u9fa5]+')
        for line in fileinput.input(filename, openhook=fileinput.hook_encoded(config.encoding)):
            if line:
                _line = re.findall(pattern, line)
                chinese_text += (''.join(_line))
        fileinput.close()
        return chinese_text

    @classmethod
    def get_url_text(cls, filename):
        url = cls.readurl(filename)
        chinese_text = cls.readchinese(filename)
        return url, chinese_text

    @staticmethod
    def readfilelist(filename):
        text = []
        for line in fileinput.input(filename, openhook=fileinput.hook_encoded(config.encoding)):
            text.append(line.rstrip('\n'))
        fileinput.close()
        return text

    @staticmethod
    def clear(filename):
        with open(filename, 'r+', encoding=config.encoding) as f:
            f.truncate()

    @staticmethod
    def copyfile(src, dst):
        shutil.copyfile(src, dst)

    @staticmethod
    def removefiles(filepath):
        if not os.listdir(filepath):
            return
        for file in os.listdir(filepath):
            filename = os.path.join(filepath, file)
            if os.path.isfile(filename):
                os.remove(filename)
            elif os.path.isdir(filename):
                shutil.rmtree(filename)

    @staticmethod
    def init_path(filepath):
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        elif os.path.isdir(filepath):
            FileUtil.removefiles(filepath)
        elif os.path.isfile(filepath):
            FileUtil.clear(filename=filepath)


if __name__ == '__main__':
    # url, text = FileUtil.geturlAndtext('./1.txt')
    # print(url)
    # print(text)
    pass
