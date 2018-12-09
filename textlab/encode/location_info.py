#! python3
from fileutil import FileUtil
from pretreatment.pretreatment import prepo


class Encode(object):

    def __init__(self):
        pass

    def _dec2bin(self, num, bits=0):
        s = bin(num).lstrip('0b')
        if len(s) < bits:
            s = '0' * (bits - len(s)) + s
        return s

    
    # def __sitebin(self,r, rb, c, cb):    # 行坐标，行坐标比特位数，列坐标，列坐标比特位数
    #     row = self._dec2bin(num=r, bits=rb)
    #     col = self._dec2bin(num=c, bits=cb)
    #     return row + col


    def location(self,text_list, keywords, col_bits):  # 每个关键词在文本中的坐标
        n = pow(2, col_bits)  # 一行关键词数量
        row = []
        col = []
        for key in keywords:
            i = text_list.index(key)  # 秘密关键词在文档中的位置
            # yield i / n, i % n
            row.append(i // n)
            col.append(i % n)
        return row, col

    # @staticmethod
    # def len_row(row_list, row_num):  # 计算实际行坐标范围
    #     r_min = max(row_list)
    #     r_max = min(row_list)
    #     b = r_max - r_min + 1
    #
    #     row_bits = len(self._dec2bin(b))  # 行比特数
    #
    #     bits = self._dec2bin(row_num)
    #
    #     flag = self._dec2bin(r_min, len(bits)) + \
    #         self._dec2bin(r_max, len(bits))
    #
    #     return row_bits, flag

    def key2loc(self, col_bits=5, information='', filename='.'):

        N = pow(2, col_bits)

        url = FileUtil.readurl(filename)

        # text_kws = FileUtil.readkws(filename)

        text_kws = FileUtil.readupkws(filename)

        info_kws = prepo.seg(information)

        infolen = self._dec2bin(len(info_kws), col_bits)  # 秘密关键词长度的二进制表示 ???

        row, col = self.location(
            text_list=text_kws, keywords=info_kws, col_bits=col_bits)   # 得到每个关键词的坐标(x,y)

        total_bits = len(self._dec2bin(len(text_kws) // N))   # 总行数的二进制表示所需的比特数

        flag = self._dec2bin(min(row), total_bits) + \
            self._dec2bin(max(row), total_bits)  # 最小行和最大行的二进制表示

        row_bits = len(self._dec2bin(max(row) - min(row) + 1))   # 行比特数

        # print("表示行所需的比特数：", "表示关键词所在文本的最小行和最大行:")
        # print(row_bits, flag)
        s = ''
        for r, c in zip(row, col):

            # loc = self.__sitebin(r=r, rb=row_bits, c=c, cb=col_bits)
            loc = self._dec2bin(num=r, bits=row_bits) + \
                self._dec2bin(num=c, bits=col_bits)
            s = s + loc
        res = ''

        num_add_col_bits = self._dec2bin(col_bits, 5)
        l = len(s)
        num_add = ''
        if l % 8 ==0:
            num_add = '000'
        else:
            num_add = self._dec2bin((8 - l % 8), 3)
        res = num_add +num_add_col_bits + s

        print(len(res))
        return url, res

    def testdec(self):
        s = self._dec2bin(5,6)
        print(s)



if __name__ == '__main__':
    e = Encode()
    # e.testdec()
    filename1 = r'F:\LabData\NetBigData\test\testh\0+06_56_601_高中信息技术知识点汇总(必修)_高中信息技术_新浪博客.txt'
    filename2 = r'F:\LabData\NetBigData\test\testh\1+56_19_757_网络规划设计师知识点汇总-小马的博客-51CTO博客.txt'
    information ='基于网络文本的无载体信息隐藏技术利用互联网上大量的网络文本来隐藏信息，提高了隐藏容量、成功率及传输效率'
    info1 = "基于 网络 文本 无载体 信息 隐藏 技术 利用 互联网 上 大量 网络"
    info2 = "文 本来 隐藏 信息 提高 隐藏 容量 率 传输 效率"
    url, res = e.key2loc(col_bits=5,information=info2,filename=filename2)
    print(url)
    print(res)

    pass
