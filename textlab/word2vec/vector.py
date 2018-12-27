#！python3
# -*- coding:utf-8 -*-

import os
import time
import config
import logging
from gensim.models import Word2Vec
from gensim.models.word2vec import PathLineSentences
from pretreatment.pretreatment import Prepaper


class Seg(object):

    @staticmethod
    def segtext(dirname, savepath):
        for path in os.listdir(dirname):
            outfile = os.path.join(savepath, path + '.txt')
            filepath = os.path.join(dirname, path)
            if os.path.isdir(filepath):
                fout = open(outfile, 'w+', encoding='utf-8')
                for name in os.listdir(filepath):
                    filename = os.path.join(filepath, name)
                    for line in open(filename, 'r', encoding='utf-8'):
                        _line = Prepaper.seg(line)
                        sentence = ' '.join(_line)
                        fout.write(sentence)
                        fout.write('\n')
                fout.close()


class Word2Vector(object):

    def __init__(self):
        self.logger = logging.basicConfig(
            format='%(asctime)s : %(levelname)s : %(message)s',
            level=logging.INFO)
        pass

    # 训练 corpus 下所有文件
    def train(self, corpus, modelpath):
        sentences = PathLineSentences(corpus)
        model = Word2Vec(iter=3)
        model.build_vocab(sentences)
        model.train(sentences, total_examples=model.corpus_count, epochs=model.iter)
        model.save(modelpath)

    # 增量训练
    def moretrain(self, models, corpus):
        sentences = PathLineSentences(corpus)
        model = Word2Vec.load(models)
        model.train(sentences, total_examples=model.corpus_count, epochs=model.iter)


    @staticmethod
    def similarwords(keyword, modelpath=config.modelpath, tops=5):
        # 默认获取前10个相似关键词
        start = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print(
"start execute Word2vec, get similar keywords! Time:" +
            start +
            ">>>>>>>>>>>>>>>>>>>>>")
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
        print(
            "get similar keywords end!................... Time:" +
            end +
            ">>>>>>>>>>>>>>>>>>>>>")
        return res


if __name__ == '__main__':
    dir = r''
    save = r''
    # 1.分割
    Seg.segtext(dirname=dir, savepath=save)
    # 2.训练
    wv = Word2Vector()
    wv.train(corpus=save, modelpath='./bin')
    # wv.train(r'F:\LabData\NetBigData\test\word2vec\x1.txt', './m.bin')
    # wv.moretrain('./m.bin', r'F:\LabData\NetBigData\test\word2vec\x2.txt')

