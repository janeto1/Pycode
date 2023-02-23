# -*- coding: utf-8 -*-
import gzip
import base64
import json


class entry:
    def base64_encode(self, str):
        return base64.b64encode(str)

    def base64_decode(self, str):
        return base64.b64decode(str)

    def gzip_base64(self, buf):
        return gzip.compress(buf)

    def ungzip_base64(self, buf):
        return gzip.decompress(buf)

    def read_report_gzipbase64(self, path):
        with open(path, 'rb') as f:
            test = f.read()
            base64_report = self.base64_encode(self.gzip_base64(test))
            return str(base64_report, 'utf-8')

    def decode_str(self, path):
        with open(path, 'r') as f:
            test_str = f.read()
            decode_base64_str = self.base64_decode(test_str)
            report = self.ungzip_base64(decode_base64_str)
            return str(report, 'utf-8')


if __name__ == '__main__':
    test = entry()
    path = r'E:\项目\19.振兴\【7】变量\1.人行报告\17d5785a-f510-4d81-9db4-8cb1282e9973.html'
    encodepath = r'E:\项目\19.振兴\【7】变量\1.人行报告\encode_report.txt'
    report = test.read_report_gzipbase64(path)
    # report2 = test.decode_str(encodepath)
    print(report)
