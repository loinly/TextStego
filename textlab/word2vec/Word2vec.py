# #! python3
# # -*- coding:utf-8 -*-
# from gensim.models import Word2Vec
# import os
# import logging
# import time
# import config
# import warnings
# warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
#
#
# class WordVector(object):
#
#     def __init__(self):
#         pass
#
#         # 训练 词向量 corpus 预料库:是一个分好词的txt文档, models:模型保存路径
#     @staticmethod
#     def train(corpus=config.corpuspath):
#         logging.basicConfig(
#             format='%(asctime)s : %(levelname)s : %(message)s',
#             level=logging.INFO)
#         sentences = PathLineSentences(corpus)
#         model = Word2Vec(min_count=1)
#         model.build_vocab(sentences)
#         model.train(
#             sentences,
#             total_examples=model.corpus_count,
#             epochs=model.iter)
#         model.save(r'.\model.bin')
#
#     @staticmethod
#     def similarwords(keyword, modelpath=config.modelpath, tops=10):
#         # 默认获取前10个相似关键词
#         start = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
#         print(
#             "start execute Word2vec, get similar keywords! Time:" +
#             start +
#             ">>>>>>>>>>>>>>>>>>>>>")
#         try:
#             model = Word2Vec.load(modelpath)
#             words = model.wv.most_similar(keyword, topn=tops)
#         except KeyError:
#             print("word '%s' not in vocabulary" % keyword)
#             return None
#         end = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
#         if not words:
#             return None
#             # res = [[item[0], item[1]] for item in words]   # 相似关键词及其相似度
#         res = []
#         for word in words:
#             res.append([word[0], word[1]])
#             print(word[0], "\t", word[1])
#         print(
#             "get similar keywords end!................... Time:" +
#             end +
#             ">>>>>>>>>>>>>>>>>>>>>")
#         return res
#
#
# if __name__ == '__main__':
#     w = WordVector()
#     # w.train()
#     pass
#     keys = "推动"
#     simikeys = WordVector.similarwords(keys)
#     for item in simikeys:
#         print(item[0], "\t", item[1])
