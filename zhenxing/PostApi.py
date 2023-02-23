# -*- coding: utf-8 -*-
import json

import requests
from zhenxing.entry import entry
from utils.times import dt_strftime


class PostApi:

    def request_varexcute(self, url, data):
        headers = {'Content-Type': 'application/json'}
        reponse = requests.post(url=url, headers=headers, data=data)
        return json.dumps(json.loads(reponse.content), ensure_ascii=False, indent=2)

    def execute_product(self, data):
        en = entry()
        url = 'http://166.188.20.80:8889/var-execute/api/v1/var/execute'
        post = {}
        sys_header = {
            "sysid": "sysid-001",
            "syskey": ""
        }
        local_header = {
            "ip": "192.168.0.0",
            "mac": "fakemacaddrsi891"
        }
        app_header = {}
        body = {}

        body['product_code'] = data['product_code']
        html_report = en.read_report_gzipbase64(data['html_file'])
        body['html_file'] = html_report

        app_header['trans_no'] = data['trans_no'] + dt_strftime('%Y%m%d%H%M%S%f')
        app_header['reqtime'] = dt_strftime('%Y%m%d%H%M%S%f')

        post['sys_header'] = sys_header
        post['local_header'] = local_header
        post['app_header'] = app_header
        post['body'] = body

        return json.dumps(post, ensure_ascii=False), self.request_varexcute(url, json.dumps(post))

    def query_product(self, data):
        en = entry()
        url = 'http://166.188.20.80:8889/var-execute/api/v1/var/db/query'
        post = {}
        sys_header = {
            "sysid": "sysid-001",
            "syskey": ""
        }
        local_header = {
            "ip": "192.168.0.0",
            "mac": "fakemacaddrsi891"
        }
        app_header = {}
        body = {}

        body['product_code'] = data['product_code']
        trans_no = data.get('trans_no')
        id_no = data.get('id_no')
        report_no = data.get('report_no')
        if trans_no and len(trans_no) > 0:
            body['trans_no'] = trans_no

        if id_no and len(id_no) > 0:
            body['id_no'] = id_no

        if report_no and len(report_no) > 0:
            body['report_no'] = report_no

        app_header['trans_no'] = data['trans_pre'] + dt_strftime('%Y%m%d%H%M%S%f')
        app_header['reqtime'] = dt_strftime('%Y%m%d%H%M%S%f')

        post['sys_header'] = sys_header
        post['local_header'] = local_header
        post['app_header'] = app_header
        post['body'] = body
        return json.dumps(post, ensure_ascii=False), self.request_varexcute(url, json.dumps(post))
