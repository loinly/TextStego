#! python3
# -*- coding:utf-8 -*-
from gensim.models import Word2Vec
from pretreatment.pretreatment import Prepaper


def wmd(sent1, sent2):
    sent1 = Prepaper.seg(sent1)
    sent2 = Prepaper.seg(sent2)
    model = Word2Vec.load(r'F:\LabData\NetBigData\model\word2vec.model')
    #  这边是归一化词向量，不加这行的话，计算的距离数据可能会非常大
    model.init_sims(replace=True)
    distance = model.wv.wmdistance(sent1,sent2)
    return distance

s1 = '无载体信息隐藏由于能在不经任何修改的情况下将秘密信息传递给载体而成为热点。摘要针对文本大数据隐藏能力低、检索效率低、匹配不匹配等问题，提出了一种利用互联网上海量web文本进行无覆盖信息隐藏的新方法。'
s2 = '无载体 信息 隐藏 能 在 0 任何 修改 情况 下 将 秘密 信息 传递 给 载体 成为 热点 摘要 针对 文本 大 数据 隐藏 能力 低 查询 效率 低 匹配 不 匹配 问题 提出 一种 利用 互联网 上海 量 文本 进行 无 覆盖 信息 隐藏 新 方法'
dis = wmd(s1, s2)
print(dis)