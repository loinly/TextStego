#! python3
# -*- coding: utf-8 -*-

import chardet
import requests
from lxml import etree
from fake_useragent import UserAgent


class HtmlDownloader(object):
    """
    html 页面下载器
    """

    @staticmethod
    def download(url):
        if url is None:
            return None
        ua = UserAgent()
        user_agent = ua.random
        accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
        header = {'Accept': accept, 'User-Agent': user_agent}
        r = requests.get(url, headers=header, timeout=(3, 7))
        if r.status_code == 200:
            r.encoding = chardet.detect(r.content)['encoding']
            return r.text
        return None


class Htmlparse(object):
    """
    html 页面解析器,提取url, title
    """

    def parse(self, page_url, html_content):
        if page_url is None or html_content is None:
            return
        xpath = etree.HTML(text=html_content).xpath(
            '//div[contains(@class,"result c-container")]/h3/a')
        new_datas = self._get_new_data(xpath)
        return new_datas

    @staticmethod
    def _get_new_data(_xpath):
        """
        获取数据
        :param _xpath: xpath
        :return: 字典列表,每个字典包含 url,title
        """

        data = []
        for link in _xpath:
            link_url = link.xpath('./@href')[0]
            p_title = link.xpath('string(.)')
            title = p_title.replace(':', '').replace("\\", '').replace("/", '').replace("*", '')\
                .replace("\"", '').replace("?", '').replace("<", '').replace(">", '').replace("|", '')
            data.append(dict([('url', link_url), ('title', title)]))
        return data
