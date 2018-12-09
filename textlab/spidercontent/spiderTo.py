#! python3
# -*- coding:utf-8 -*-
import os
import logging
import config
from fileutil import FileUtil
from spidercontent.Parser import Htmlparse
from spidercontent.Downloader import Downloader

'''
抓取网页内容,
存入本地txt文档
'''


class SpiderTo(object):

    def __init__(self, filename):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger("spider")
        self.download = Downloader(filename)
        self.parse = Htmlparse()
        self.filepath = filename.rstrip('.html')

    def crawl(self):
        self.download.download()
        readpath = os.path.join(config.spiderhtml, self.filepath)
        savepath = os.path.join(config.spidertext, self.filepath)
        FileUtil.init_path(savepath)
        for filename in os.listdir(readpath):
            file = os.path.join(readpath, filename)
            url, content = self.parse.parse(file)
            filename = filename.rstrip('.html') + '.txt'
            self.logger.info("Save spider url and content:{0}".format(url))
            FileUtil.writefile(url+content, os.path.join(savepath, filename))
        print('crawl web contents end!')


if __name__ == '__main__':
    pass
    # st = SpiderTo(r'隐藏_信息_网络_互联网_成功率_技术_利用_容量_传输_提高.html')
    # st.crawl()









