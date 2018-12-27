#! python3
# -*- coding:utf-8 -*-
'''
隐藏结果, 统计, 成功率, 容量
'''
import numpy as np
import matplotlib.pyplot as plt


class Result(object):

    def __init__(self):
        pass

    def res(self, filename):
        SR = []
        HC = []

        with open(filename, 'r+', encoding='utf-8') as fin:
            for line in fin.readlines():
                pre, post = line.split('||')
                pre = pre.strip().split('\t')
                post = post.strip().split('\t')
                sr = int(pre[2])/int(pre[1])
                SR.append(sr)

                for p in post:
                    hc = int(p)
                    if hc > 0 and hc < 100:
                        HC.append(hc)
                pass

        x1 = np.linspace(0, len(SR),len(SR))
        x2 = np.linspace(0, len(HC), len(HC))


        plt.subplot(2, 1, 1)
        plt.plot(x1, SR)

        plt.subplot(2, 1, 2)
        plt.plot(x2, HC)

        plt.show()



if __name__ == '__main__':
    r = Result()

    r.res(r'F:\LabData\NetBigData\test\res.txt')
