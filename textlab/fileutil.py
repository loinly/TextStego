#! python3
# -*- coding:utf-8 -*-

import re
import os
import math
import shutil
import config
import fileinput
'''
文件处理类读取,写入,复制   
'''


class FileUtil(object):

    @staticmethod
    def readfile(filename):
        text = ''
        for line in fileinput.input(
            filename, openhook=fileinput.hook_encoded(
                config.encoding)):
            text += line
        fileinput.close()
        return text

    @staticmethod
    def writefile(string, filename):
        try:
            with open(filename, 'w+', encoding=config.encoding) as f:
                f.write(string)
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
        for line in fileinput.input(filename,
                                    openhook=fileinput.hook_encoded(config.encoding)):
            if fileinput.filelineno() == 1:
                continue
            kws = line.strip('\n').split('\t')
            res.extend(kws)
        fileinput.close()
        return res

    @staticmethod
    def readupkws(filename):
        res = []
        for line in fileinput.input(filename, openhook=fileinput.hook_encoded(config.encoding)):
            if fileinput.filelineno() == 1:
                continue
            kws = line.strip('\n').split('\t')
            for kw in kws:
                if kw not in res:
                    res.append(kw)
        fileinput.close()
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
        for line in fileinput.input(filename,
                                    openhook=fileinput.hook_encoded(config.encoding)):
            if fileinput.filelineno() == 1:
                fileinput.close()
                return line

    @staticmethod
    def readchinese(filename):
        chinese_text = ''
        pattern = re.compile('[\u4e00-\u9fa5]+')
        for line in fileinput.input(filename,
                                    openhook=fileinput.hook_encoded(config.encoding)):
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
        for line in fileinput.input(
            filename, openhook=fileinput.hook_encoded(
                config.encoding)):
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
        if os.listdir(filepath):
            print('init pretreatment directory.....')
            for file in os.listdir(filepath):
                filename = os.path.join(filepath, file)
                if os.path.isfile(filename):
                    os.remove(filename)
        else:
            print('the directory is empty...')
            pass

    @staticmethod
    def init_path(filepath):
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        else:
            FileUtil.removefiles(filepath)




if __name__ == '__main__':
    # url, text = FileUtil.geturlAndtext('./1.txt')
    # print(url)
    # print(text)

    pass
