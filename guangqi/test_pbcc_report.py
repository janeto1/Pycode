# -*- coding: utf-8 -*-
import json

import pytest

from utils.ReadExcel import ReadExcel
from guangqi.PostApi import PostApi

api_case_path = r'D:\AutoCase\TEST\guangqi\api_test.xlsx'


class TestPbccReport:
    test_case = ReadExcel()
    case_api_pbccrc = test_case.read_case_value_dic_by_flag(api_case_path, 'pbcc_report_v2')
    case_api_pbccrc_multi = test_case.read_case_value_dic_by_flag(api_case_path, 'pbcc_report_v2_sos_multi')

    @pytest.fixture(scope='class', params=case_api_pbccrc)
    def data_api_pbccrc(self, request):
        return request.param

    @pytest.fixture(scope='class', params=case_api_pbccrc_multi)
    def data_api_pbccrc_multi(self, request):
        return request.param

    @pytest.fixture(scope='class', autouse=True)
    def setup(self, ):
        global apitest
        apitest = PostApi()

    # @pytest.mark.skip(reasons='征信-个人-上报')
    def test_upload_pbcc_report_v2(self, data_api_pbccrc):
        post_data, result = apitest.upload_pbcc_report_v2(data_api_pbccrc)
        print('请求参数 : ', post_data)
        print('返回参数: ', result)

    @pytest.mark.skip(reasons='SOS-个人-查询-old')
    def test_query_pbcc_report_v2(self, data_api_pbccrc):
        post_data, result = apitest.query_pbcc_report_v2(data_api_pbccrc)
        print('请求参数 : ', post_data)
        print('返回参数: ', result)

    # @pytest.mark.skip(reasons='SOS-个人-查询-new')
    def test_query_pbcc_report_v2_multi(self, data_api_pbccrc_multi):
        post_data, result = apitest.query_pbcc_report_v2_multi(data_api_pbccrc_multi)
        print('请求参数 : ', post_data)
        print('返回参数: ', result)


if __name__ == '__main__':
    pytest.main(["-s", "test_pbcc_report.py"])
