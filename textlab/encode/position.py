#! python3
# -*- coding:utf-8 -*-
import os
import numpy
import config
from encode.coding import Base64
from fileutil import FileUtil


class Location(object):
    """
    最佳网页,位置信息
    """

    def __init__(self, keywords, col_bits):
        self.keywords = keywords
        self.col_bits = col_bits
        pass

    @staticmethod
    def _dec2bin(num, bits=0):
        s = bin(num).lstrip('0b')
        if len(s) < bits:
            s = '0' * (bits - len(s)) + s
        return s

    def location(self, keywords, text_list):
        """
        每个关键词在文本中的坐标
        :param keywords:
        :param text_list:
        :return: row column p
        """
        n = pow(2, self.col_bits)    # 一行关键词数量
        row = []
        col = []
        p = -1

        for i, key in enumerate(keywords):
            if key in text_list:
                j = text_list.index(key)  # 秘密关键词在文档中的位置
                row.append(j // n)
                col.append(j % n)
            else:
                p = i
                break
        return row, col, p

    #  编码
    def key2loc(self, keywords, filename='.'):
        col_bits = self.col_bits
        n = pow(2, col_bits)
        _url = FileUtil.readurl(filename)
        text_kws = FileUtil.readupkws(filename)
        row, col, p = self.location(keywords=keywords, text_list=text_kws)  # 得到每个关键词的坐标(x,y)
        row_bits = len(self._dec2bin(len(text_kws) // n))  # 总行数的二进制表示所需的比特数
        s = ''
        print('location information: ')
        for r, c in zip(row, col):
            loc = self._dec2bin(num=r, bits=row_bits) + \
                self._dec2bin(num=c, bits=col_bits)
            print(loc)
            s = s + loc
        num_add_col_bits = self._dec2bin(col_bits, 5)  # col_bits作为密钥，5位补全二进制流
        _res = ''
        if len(s) % 8 == 0:
            _res = '000' + num_add_col_bits + s
        else:
            num = 8 - len(s) % 8     # 补0的个数
            num_add = self._dec2bin(num, 3)
            _res = num_add + num_add_col_bits + s + '0' * num

        return _url, _res, p

    #   位置信息描述
    def describe(self, name):
        info_kws = self.keywords[:]
        res_list = []
        hidepath = os.path.join(config.hidepath, name)
        for filename in os.listdir(hidepath):
            filename = os.path.join(hidepath, filename)
            if os.path.isdir(filename):         # dir: 需要选取最佳网页
                filename = os.path.join(filename, self.optimal(filename, info_kws))
            if 'unMatch' in filename:
                print('keywords "%s" is unMatch!' % info_kws[0])
                string = Base64.encode('0000000011111111')
                res_list.append([info_kws[0], 'http://www.baidu.com/pos/%s' % string, os.path.split(filename)[1]])  # 失配
                info_kws.pop(0)
            else:
                url, string, p = self.key2loc(keywords=info_kws, filename=filename)
                res_string = Base64.encode(string)  # 编码之后的结果
                _res = url + '/pos/' + res_string  # 连接
                res_list.append([info_kws[:p], _res, os.path.split(filename)[1]])
                if p != -1:
                    info_kws = info_kws[p:]
        print(res_list)
        return res_list

    #  最优网页的选取
    def optimal(self, path, info_kws):
        files = os.listdir(path)
        res = []
        for i, file in enumerate(files):
            text_kws = FileUtil.readkws(os.path.join(path, file))
            index = []
            for key in info_kws:
                if key in text_kws:
                    index.append(text_kws.index(key))
                else:
                    break
            delta = []
            for k in range(1, len(index)):
                delta.append(index[k] - index[k - 1])
            var = numpy.var(delta)
            res.append(var)
        pos = res.index(min(res))
        return files[pos]


if __name__ == '__main__':
    # info_kws = ['无载体', '信息', '隐藏', '能', '在', '不经', '任何', '修改', '情况', '下', '将', '秘密', '信息', '传递', '给', '载体', '成为', '热点', '针对', '文本', '大', '数据', '隐藏', '能力', '低', '检索', '效率', '低', '匹配', '不', '匹配', '问题', '提出', '一种', '利用', '互联网', '上海', '量', '文本', '进行', '无', '覆盖', '信息', '隐藏', '新', '方法']
    # col_bits = 5
    # loc = Location(keywords=info_kws, col_bits=col_bits)
    # keys = '_'.join(['信息', '文本', '隐藏', '匹配', '载体', '能力', '进行', '秘密', '提出', '互联网'])
    # loc.describe(keys)
    pass
