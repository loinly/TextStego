#! python3
# -*- coding:utf-8 -*-
import os
import time
import random
import config
import chardet
import logging
import requests
from lxml import etree
from fileutil import FileUtil
from fake_useragent import UserAgent


class Downloader(object):

    def __init__(self, filename):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger("Downloader")
        self.urls = set()
        self.manager = UrlManager(filename)
        self.filename = os.path.join(config.spiderlink, filename)  # 要抓取的文件名
        self.savepath = os.path.join(
            config.spiderhtml, filename.rstrip('.html'))
        self.init_config()

    def init_config(self):
        FileUtil.init_path(self.savepath)

    def download(self):
        url_title_list = self.get_url_titles()
        for i, item in enumerate(url_title_list):
            url = item.get('url')
            title = item.get('title')
            try:
                self.logger.info(
                    'the are %s links,fetching %dth link' %
                    (len(url_title_list), i + 1))
                self._downloader(url, title)
            except Exception as e:
                print('download failed: %s' % (str(e)))
                self.logger.info("the failed link:{0}".format(url))
                self.manager.save_content(url, title)
                time.sleep(random.randint(10, 20))  # 暂停10~20s
        self._failed(self.manager.file_name)

    def _failed(self, filename):
        content = FileUtil.readfilelist(filename)
        for i, item in enumerate(content):
            url, title = item.split('\t')
            try:
                self._downloader(url, title)
                self.logger.info(
                    "the spider system has crawl %s failed links" % str(
                        i + 1))
            except Exception as e:
                self.logger.info(
                    'crawl the failed contents still failed: %s' %
                    str(e))

    def get_url_titles(self):
        parse_list = []
        html_str = FileUtil.readfile(self.filename)
        linktr = etree.HTML(text=html_str).xpath('//tr')
        for item in linktr:
            url = item.xpath('string(./td[1])')
            title = item.xpath('string(./td[2])')
            parse_list.append(dict([('url', url), ('title', title)]))
        return parse_list

    def _downloader(self, url, title):
        ua = UserAgent()
        user_agent = ua.random
        accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
        header = {'Accept': accept, 'User-Agent': user_agent}
        r = requests.get(url, headers=header, timeout=(3, 7))
        if r.status_code == 200:
            r.encoding = chardet.detect(r.content)['encoding']
            if r.url not in self.urls:
                self._write(r.url, title, r)
                self.urls.add(r.url)
        self.logger.info("Fetching html :{0}".format(r.url))
        return r.url

    def _write(self, url, title, r):
        ct = time.time()
        secs = (ct - int(ct)) * 1000
        time_head = time.strftime("%M_%S", time.localtime())
        time_slot = "%s_%03d" % (time_head, secs)
        files = self.savepath + "\\%s_%s.html" % (time_slot, title)
        with open(files, 'a+', encoding=config.encoding) as f:
            f.write(url)
            f.write("\n")
            f.write(r.text)
            f.close()


class UrlManager(object):
    def __init__(self, filename):
        name = filename.rstrip('.html') + '.txt'
        self.file_name = os.path.join(config.failedtextpath, name)
        self.init_file()

    def init_file(self):
        if os.path.exists(self.file_name):
            FileUtil.clear(self.file_name)
        else:
            with open(self.file_name, 'w+', encoding=config.encoding):
                pass
            pass

    def save_content(self, new_url, new_title):
        content = new_url + '\t' + new_title + '\n'
        FileUtil.write_apd_file(content, self.file_name)


if __name__ == '__main__':

    filenames = r'隐藏_信息_网络_互联网_成功率_技术_利用.html'
    # filename = os.path.join(config.SPIDERLINK, filename)
    down = Downloader(filenames)
    down.download()

    # url_title = download.get_url_titles()
    # for item in url_title:
    #     print(item.get('url'), item.get('title'))
    # print(page_url)
    # print(p_title)
    # print(content)
