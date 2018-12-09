#! python3
# -*- coding:utf-8 -*-
import re
import fileinput
import config

'''
解析页面,提取文字内容
:return:
'''


class Htmlparse(object):

    @staticmethod
    def parse(filename):
        page_url = ''
        text = ''
        if filename is None:
            return
        for line in fileinput.input(
            filename, openhook=fileinput.hook_encoded(
                config.encoding)):
            if fileinput.isfirstline():
                page_url = line
                continue
            text += line
        fileinput.close()
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
    pass
    h = Htmlparse()
    filenames = r'F:\LabData\NetBigData\spiders\spiderhtml\隐藏_信息_网络_互联网_成功率_技术_利用\51_48_135_墨尔本理工大学开发光线角动量复用技术大幅提高光纤传输容量.html'
    url, contents = h.parse(filenames)
    print(url)
    print(contents)
