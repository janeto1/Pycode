# -*- coding: utf-8 -*-
import json

import requests
from guangqi.entry import encry
from utils.times import dt_strftime, running_time

ip = '166.188.21.15'  # '166.188.30.53'


class PostApi:

    def __init__(self):
        self.key = 'dvpsos1234567890'
        self.en = encry()

    @running_time
    def request_varexcute(self, url, data):
        headers = {'Content-Type': 'application/json'}
        reponse = requests.post(url=url, headers=headers, data=data)
        return json.dumps(json.loads(reponse.content), ensure_ascii=False, indent=2)

    def upload_pbcc_report_v2(self, data):
        url = 'http://' + ip + ':8099/var-execute/api/v1/var/upload/pbcc_report_v2'
        body = {}
        body['reportNo'] = data['reportNo']
        body['zxqzId'] = data['zxqzId'] + dt_strftime('%Y%m%d%H%M%S%f')
        html_report = self.en.read_report_base64(data['report_path'])
        body['pbcc_report_v2'] = html_report
        return json.dumps(body, ensure_ascii=False), self.request_varexcute(url, json.dumps(body))

    def upload_pboc_company_v2(self, data):
        url = 'http://' + ip + ':8099/var-execute/api/v1/var/upload/pboc_company_v2'
        body = {}
        body['reportNo'] = data['reportNo']
        body['zxqzId'] = data['zxqzId'] + dt_strftime('%Y%m%d%H%M%S%f')
        html_report = self.en.read_report_base64(data['report_path'])
        body['pboc_company_v2'] = html_report
        return json.dumps(body, ensure_ascii=False), self.request_varexcute(url, json.dumps(body))

    def query_pbcc_report_v2(self, data):
        url = 'http://' + ip + ':8099/var-execute/api/v1/var/sync/query/pbcc_report_v2'
        body = {}
        body['reportNo'] = data['reportNo']
        body['custName'] = data['custName']
        body['custCertype'] = data['custCertype']
        body['custCertno'] = data['custCertno']
        body['queryId'] = data['queryId'] + dt_strftime('%Y%m%d%H%M%S%f')
        return json.dumps(body, ensure_ascii=False), self.request_varexcute(url, json.dumps(body))

    def query_pboc_company_v2(self, data):
        url = 'http://' + ip + ':8099/var-execute/api/v1/var/sync/query/pboc_company_v2/single'
        sm4_key = 'dvpsos1234567890'
        body = {}
        body['reportNo'] = data['reportNo']
        body['custName'] = self.en.encryptSM4(sm4_key, data['custName'])
        body['custCertype'] = data['custCertype']
        body['custCertno'] = self.en.encryptSM4(sm4_key, data['custCertno'])
        body['queryId'] = data['queryId'] + dt_strftime('%Y%m%d%H%M%S%f')
        return json.dumps(body, ensure_ascii=False), self.request_varexcute(url, json.dumps(body))

    def calc_api_pro(self, data):
        product_code = data['product_code']
        url = 'http://' + ip + ':8099/var-execute/api/v1/var/execute/' + product_code
        body = {}
        body['type'] = int(data.get('type')) if data.get('type') else None
        body['valuea'] = data.get('valuea')
        body['valueb'] = data['valueb'] + dt_strftime('%Y%m%d%H%M%S%f')
        return json.dumps(body, ensure_ascii=False), self.request_varexcute(url, json.dumps(body))

    def calc_other_pro(self, data):
        product_code = data['product_code']
        url = 'http://' + ip + ':8099//var-execute/api/v1/var/execute/' + product_code
        body = {}
        report = self.en.read_report(data['json_report_path'])
        body[data['report']] = json.loads(report)
        return json.dumps(body, ensure_ascii=False), self.request_varexcute(url, json.dumps(body))

    def query_pbcc_report_v2_multi(self, data):
        sm4_key = 'dvpsos1234567890'
        url = 'http://' + ip + ':8099/var-execute/api/v1/var/sync/query/pbcc_report_v2'
        body = {}
        body['queryId'] = data['queryId'] + dt_strftime('%Y%m%d%H%M%S%f')
        appUser = {}
        jointAppUser = None
        guarantorUser = None
        appUser['reportNo'] = data.get('appUser_reportNo')
        appUser['custName'] = self.en.encryptSM4(sm4_key, data.get('appUser_custName'))
        appUser['custCertype'] = data.get('appUser_custCertype')
        appUser['custCertno'] = self.en.encryptSM4(sm4_key, data.get('appUser_custCertno'))

        if data.get('jointAppUser_reportNo'):
            jointAppUser = {}
            jointAppUser['reportNo'] = data.get('jointAppUser_reportNo')
            jointAppUser['custName'] = self.en.encryptSM4(sm4_key, data.get('jointAppUser_custName'))
            jointAppUser['custCertype'] = data.get('jointAppUser_custCertype')
            jointAppUser['custCertno'] = self.en.encryptSM4(sm4_key, data.get('jointAppUser_custCertno'))

        if data.get('guarantorUser_reportNo'):
            guarantorUser = {}
            guarantorUser['reportNo'] = data.get('guarantorUser_reportNo')
            guarantorUser['custName'] = self.en.encryptSM4(sm4_key, data.get('guarantorUser_custName'))
            guarantorUser['custCertype'] = data.get('guarantorUser_custCertype')
            guarantorUser['custCertno'] = self.en.encryptSM4(sm4_key, data.get('guarantorUser_custCertno'))
        body['appUser'] = appUser
        body['jointAppUser'] = jointAppUser
        body['guarantorUser'] = guarantorUser
        return json.dumps(body, ensure_ascii=False), self.request_varexcute(url, json.dumps(body))
