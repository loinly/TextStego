#! python3
# -*- coding:utf-8 -*-
import os
import numpy
from fileutil import FileUtil


class Count(object):

    def __init__(self, filepath):
        self.filepath = filepath

    def kw_num(self):
        nums = []
        for file in os.listdir(self.filepath):
            filename = os.path.join(self.filepath, file)
            kws = FileUtil.readupkws(filename)
            nums.append(len(kws))
        return nums


if __name__ == '__main__':
    pass
    # c = count(r'F:\LabData\NetBigData\count\text')
    c = Count(r'F:\LabData\NetBigData\prepaper\隐藏_信息_网络_互联网_成功率_技术_利用_容量_传输_提高')
    # c = Count(r'F:\LabData\NetBigData\test\testh\0')
    n = c.kw_num()
    print(n)
    print(max(n),min(n),numpy.mean(n))

