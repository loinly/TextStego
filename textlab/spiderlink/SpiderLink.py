#! python3
# -*- coding:utf-8 -*-
import os
import time
import random
import config
import logging
from fileutil import FileUtil
from urllib.parse import quote
from spiderlink.DataOutput import DataOutput
from spiderlink.HtmlManager import HtmlDownloader, Htmlparse


class SpiderLink(object):

    def __init__(self, keyword, root):
        self.root = root
        self.keyword = ' '.join(keyword)
        self.manager = UrlManager(keyword)
        self.output = DataOutput(keyword)
        self.downloader = HtmlDownloader()
        self.parser = Htmlparse()
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger("spider page")

        '''
        抓取网页
        :param pn: 抓取页数
        :return:
        '''
    def crawl(self, pagenum):
        new_url = ''
        start = int(time.time())
        for pn in range(1, pagenum + 1):
            try:
                # 获取新的url
                new_url = self.root.format(quote(self.keyword), pn * 10)
                # HTML下载器下载网页
                html = self.downloader.download(new_url)
                # 解析器抽取网页数据
                datas = self.parser.parse(new_url, html)
                # 将已经抽取的数据添加到列表中
                self.output.add_data(datas)
                self.logger.info(
                    "Fetching the {0}th page:{1}".format(
                        str(pn), new_url))
            except Exception as e:
                print(e)
                self.logger.info(
                    'Fetching the {0}th page failed'.format(
                        str(pn)))
                time.sleep(random.randint(10, 20))  # 暂停10~20s
                # 保存失败链接
                self.manager.save_page_url(new_url)
        if os.path.exists(self.manager.filename):
            self._failed(self.manager.filename)
        self.output.output_html()
        self.output.output_end()
        end = int(time.time())
        take = str((end - start) // 60)
        self.logger.info(
            "Fetching page links and titles takes {0} minutes".format(take))

    def _failed(self, filename):
        urls = FileUtil.readfilelist(filename)
        for i, failed_url in enumerate(urls):
            html = self.downloader.download(failed_url)
            datas = self.parser.parse(failed_url, html)
            self.logger.info(
                "the spider system has crawl %s failed links" % str(
                    i + 1))
            self.output.add_data(datas)

    '''
    抓取失败链接管理
    保存link到txt文件下,待爬取结束后,再进行处理
    '''


class UrlManager(object):
    def __init__(self, keywords, path=config.failedurlpath):
        name = '_'.join(keywords) + '.txt'
        self.filename = os.path.join(path, name)
        self._init_failed_file()

    def _init_failed_file(self):
        if os.path.exists(self.filename):
            FileUtil.clear(self.filename)
        else:
            # with open(self.filename, 'w+', encoding=config.ENCODING):
            #     pass
            pass
    def save_page_url(self, new_url):
        if os.path.exists(self.filename):
            FileUtil.write_apd_file(new_url + '\n', self.filename)
        else:
            FileUtil.writefile(new_url + '\n', self.filename)


if __name__ == '__main__':
    # string = '隐藏 信息 网络 互联网 成功率 技术 利用 容量 传输 提高 大量 文本 效率'
    string = '隐藏 信息 网络 互联网 成功率 技术'
    string = string.split()
    pagenums = 100
    roots = "http://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd={0}&pn={1}"
    spiderman = SpiderLink(string, roots)
    # 起始链接,关键词,页数
    spiderman.crawl(pagenum=pagenums)
