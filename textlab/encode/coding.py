#! python3
# -*- coding:utf-8 -*-
import os


class Base64(object):
    """
    用base64加密，将3个8位拆成4个6位，并转换成ascii码
    long_string%24可能余0个字符、1个字符、2个字符，共三种可能
    """

    table = [
        'A',
        'B',
        'C',
        'D',
        'E',
        'F',
        'G',
        'H',
        'I',
        'J',
        'K',
        'L',
        'M',
        'N',
        'O',
        'P',
        'Q',
        'R',
        'S',
        'T',
        'U',
        'V',
        'W',
        'X',
        'Y',
        'Z',
        'a',
        'b',
        'c',
        'd',
        'e',
        'f',
        'g',
        'h',
        'i',
        'j',
        'k',
        'l',
        'm',
        'n',
        'o',
        'p',
        'q',
        'r',
        's',
        't',
        'u',
        'v',
        'w',
        'x',
        'y',
        'z',
        '0',
        '1',
        '2',
        '3',
        '4',
        '5',
        '6',
        '7',
        '8',
        '9',
        '-',
        '_']

    @staticmethod
    def encode(youth_string):
        count_six = []
        res = ''
        ll = len(youth_string)
        if ll % 24 == 0:
            i = 0
            while i < ll - 1:
                count = int(youth_string[i]) * 32 + int(youth_string[i + 1]) * 16 + int(youth_string[i + 2]) * 8 \
                    + int(youth_string[i + 3]) * 4 + int(youth_string[i + 4]) * 2 + int(youth_string[i + 5])
                # print(count)
                count_six.append(Base64.table[count])
                i += 6
            res = ''.join(count_six)
        elif ll % 24 == 8:
            youth_string = youth_string + "0000"  # +"0011110100111101"#‘==’
            i = 0
            while i < ll - 1:
                count = int(youth_string[i]) * 32 + int(youth_string[i + 1]) * 16 + int(youth_string[i + 2]) * 8 \
                    + int(youth_string[i + 3]) * 4 + int(youth_string[i + 4]) * 2 + int(youth_string[i + 5])
                # print(count)
                count_six.append(Base64.table[count])
                i += 6
            res = ''.join(count_six) + '=='
        elif ll % 24 == 16:
            youth_string = youth_string + "00"  # + "00111101" #"="
            i = 0
            while i < ll - 1:
                count = int(youth_string[i]) * 32 + int(youth_string[i + 1]) * 16 + int(youth_string[i + 2]) * 8 \
                    + int(youth_string[i + 3]) * 4 + int(youth_string[i + 4]) * 2 + int(youth_string[i + 5])
                # print(count)
                count_six.append(Base64.table[count])
                i += 6
            res = ''.join(count_six) + '='
        return res

    # 转化为2进制并补成6位
    @staticmethod
    def _dec2bin_6(string_num):
        base = [str(x) for x in range(10)] + [chr(x)
                                              for x in range(ord('A'), ord('A') + 6)]
        num = int(string_num)
        mid = []
        while True:
            if num == 0:
                break
            num, rem = divmod(num, 2)
            mid.append(base[rem])
        string_bin = ''.join([str(x) for x in mid[::-1]])
        string_last = str(string_bin).zfill(6)
        return string_last

    def decode(self, string):
        a = []
        string_last = ''
        num = 0
        for i in string:
            a.append(i)
        if a[-1] != '=':
            num = 0
        elif a[-1] == '=' and a[-2] != '=':
            num = 1
        elif a[-1] == '=' and a[-2] == '=':
            num = 2
        # print(num)

        if num == 0:
            for i in a:
                string_last += self._dec2bin_6(Base64.table.index(i))
        if num == 1:
            for i in a:
                if i != '=':
                    string_last += self._dec2bin_6(Base64.table.index(i))
            string_last = string_last[:-2]
        if num == 2:
            for i in a:
                if i != '=':
                    string_last += self._dec2bin_6(Base64.table.index(i))
            string_last = string_last[:-4]
        return string_last


if __name__ == '__main__':
    b = Base64()
    b.encode('')
    os.path.join('', '')
    pass
