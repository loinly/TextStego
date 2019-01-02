#! python3
# -*- coding:utf-8 -*-
import os
import config
import codecs


class DataOutput(object):

    def __init__(self, keyword):
        self.datas = []
        self.keyword = keyword
        self.filename = self.init_path()

    def init_path(self):
        name = '_'.join(self.keyword) + ".html"
        if not os.path.exists(config.spiderlink):
            os.makedirs(config.spiderlink)
        filename = os.path.join(config.spiderlink, name)
        self.output_head(filename)
        return filename

    def add_data(self, data):
        for dat in data:
            self.datas.append(dat)

    # 输出文件头
    @staticmethod
    def output_head(path):
        fout = codecs.open(path, 'w+', encoding=config.encoding)
        fout.write("<html>")
        fout.write("<head><meta charset='utf-8'/></head>")
        fout.write("<body>")
        fout.write("<table>")
        fout.close()

    # 输出抽取的数据
    def output_html(self):
        fout = codecs.open(self.filename, 'a', encoding=config.encoding)
        for data in self.datas:
            fout.write("<tr>")
            fout.write("<td>%s</td>" % data['url'])
            fout.write("<td>%s</td>" % data['title'])
            fout.write("</tr>")
        self.datas.clear()
        fout.close()

    # 输出文件尾部
    def output_end(self):
        fout = codecs.open(self.filename, 'a', encoding=config.encoding)
        fout.write("</table>")
        fout.write("</body>")
        fout.write("<html>")
        fout.close()
