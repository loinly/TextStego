#! python3
# -*- coding:utf-8 -*-
import re


class Htmlparse(object):
    """
    解析网页, 提取url, 中文内容
    """

    @staticmethod
    def parse(filename):
        text = ''
        if filename is None:
            return
        with open(filename, 'r+', encoding='utf-8') as fr:
            page_url = fr.readline()
            for line in fr.readlines():
                text += line
        content = Htmlparse._util(text)
        return page_url, content

    @staticmethod
    def _util(html):
        res = [('<script.*?>[\s\S]*?</script>', ''),
               ('<style.*?>[\s\S]*?</style>', ''),
               ('<[\s\S]*?>', ''), ('\s+', ' '),
               ('&nbsp;', ' ')
               ]
        for rei in res:
            html = re.sub(rei[0], rei[1], html)
        return html


if __name__ == '__main__':
    url, contents = Htmlparse.parse('test.html')
    print(url)
    print(contents)
    pass
