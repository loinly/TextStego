#! python3
# -*- coding:utf-8 -*-

import os
import time
import warnings
import config
import logging
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence, PathLineSentences
from pretreatment.pretreatment import PreDeal
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')


'''
一行一句,主要考虑文件过大的情况,节省内存
'''


class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):
                yield line.split()


''' 
分割路径下所有文件
'''


class Seg(object):

    def __init__(self):
        logging.basicConfig(
            format='%(asctime)s : %(levelname)s : %(message)s',
            level=logging.INFO)
        self.logger = logging.getLogger("Segment")

    def segtext(self, dirname, savepath):
        for path in os.listdir(dirname):
            outfile = os.path.join(savepath, path + '.txt')
            filepath = os.path.join(dirname, path)
            if os.path.isdir(filepath):
                self.logger.info('seg all files under "path"')
                fout = open(outfile, 'w+', encoding='utf-8')
                for name in os.listdir(filepath):
                    filename = os.path.join(filepath, name)
                    for line in open(filename, 'r', encoding='utf-8'):
                        _line = PreDeal.seg(line)
                        sentence = ' '.join(_line)
                        fout.write(sentence)
                        fout.write('\n')
                fout.close()
        self.logger.info(' all files are segmented!')


class WV(object):
    """
    word2vec类
    """

    def __init__(self):
        logging.basicConfig(
            format='%(asctime)s : %(levelname)s : %(message)s',
            level=logging.INFO)
        pass

    # 训练 corpus 下所有文件(每个文件事先分好词以空格隔开), 并保存到modelpath
    @staticmethod
    def train(corpus, modelpath):
        if not os.path.isdir(corpus):
            raise ValueError('input is should be a path')
        sentences = PathLineSentences(corpus)
        model = Word2Vec(iter=3)
        model.build_vocab(sentences)
        model.train(sentences, total_examples=model.corpus_count, epochs=model.iter)
        model.save(modelpath)

    # 增量训练,输入一个分好词的文本corpus
    @staticmethod
    def moretrain(models, corpus):
        sentences = LineSentence(corpus)
        model = Word2Vec.load(models)
        model.train(sentences, total_examples=model.corpus_count, epochs=model.iter)

    @staticmethod
    def similarwords(keyword, modelpath=config.modelpath, tops=5):
        # 默认获取前10个相似关键词
        start = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print("start execute Word2vec, get similar keywords! Time:" + start +">>>>>>>>>>>>>>>>>>>>>")
        try:
            model = Word2Vec.load(modelpath)
            words = model.wv.most_similar(keyword, topn=tops)
        except KeyError:
            print("word '%s' not in vocabulary" % keyword)
            return None
        end = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        if not words:
            return None
            # res = [[item[0], item[1]] for item in words]   # 相似关键词及其相似度
        res = []
        for word in words:
            res.append([word[0], word[1]])
            print(word[0], "\t", word[1])
        print("get similar keywords end!................... Time:" + end + ">>>>>>>>>>>>>>>>>>>>>")
        return res

    #  WMD 距离
    @staticmethod
    def wmd(model, sent1, sent2):
        sent1 = PreDeal.seg(sent1)
        sent2 = PreDeal.seg(sent2)
        # model = Word2Vec.load(model)
        #  这边是归一化词向量，不加这行的话，计算的距离数据可能会非常大
        model.init_sims(replace=True)
        distance = model.wv.wmdistance(sent1, sent2)
        return distance


if __name__ == '__main__':
    dirname1 = r'F:\LabData\NetBigData\test\word2vec'
    savename1 = r'F:\LabData\NetBigData\test\out'
    # 1.分割
    s = Seg()
    s.segtext(dirname=dirname1, savepath=savename1)
    # 2.训练
    wv = WV()
    wv.train(corpus=savename1, modelpath='./m.bin')
    # wv.train(r'F:\LabData\NetBigData\test\word2vec\x1.txt', './m.bin')
    # wv.moretrain('./m.bin', r'F:\LabData\NetBigData\test\word2vec\x2.txt')
    # keys = "推动"
    # simikeys = WV.similarwords(keys)
