# -*- coding: utf-8 -*-
import json

import pytest

from utils.ReadExcel import ReadExcel
from guangqi.PostApi import PostApi

api_case_path = r'D:\AutoCase\TEST\guangqi\api_test.xlsx'


class TestApi:
    test_case = ReadExcel()
    case_api_pbccrc = test_case.read_case_value_dic_by_flag(api_case_path, 'pbcc_report_v2')
    case_api_pbccrm = test_case.read_case_value_dic_by_flag(api_case_path, 'pboc_company_v2')
    case_calc_apipro = test_case.read_case_value_dic_by_flag(api_case_path, 'api_pro')
    case_calc_other_pro = test_case.read_case_value_dic_by_flag(api_case_path, 'other_pro')

    @pytest.fixture(scope='class', params=case_calc_other_pro)
    def data_calc_other_pro(self, request):
        return request.param

    @pytest.fixture(scope='class', params=case_calc_apipro)
    def data_calc_apipro(self, request):
        return request.param

    @pytest.fixture(scope='class', params=case_api_pbccrc)
    def data_api_pbccrc(self, request):
        return request.param

    @pytest.fixture(scope='class', params=case_api_pbccrm)
    def data_api_pbccrm(self, request):
        return request.param

    @pytest.fixture(scope='class', autouse=True)
    def setup(self, ):
        global apitest
        apitest = PostApi()

    @pytest.mark.skip(reasons='其他产品-计算')
    def test_calc_other_pro(self, data_calc_other_pro):
        post_data, result = apitest.calc_other_pro(data_calc_other_pro)
        print('请求参数 : ', post_data)
        print('返回参数: ', result)

    @pytest.mark.skip(reasons='接口-计算')
    def test_calc_api_pro(self, data_calc_apipro):
        post_data, result = apitest.calc_api_pro(data_calc_apipro)
        print('请求参数 : ', post_data)
        print('返回参数: ', result)

    @pytest.mark.skip(reasons='征信-个人-上报')
    def test_upload_pbcc_report_v2(self, data_api_pbccrc):
        post_data, result = apitest.upload_pbcc_report_v2(data_api_pbccrc)
        print('请求参数 : ', post_data)
        print('返回参数: ', result)

    @pytest.mark.skip(reasons='SOS-个人-查询')
    def test_query_pbcc_report_v2(self, data_api_pbccrc):
        post_data, result = apitest.query_pbcc_report_v2(data_api_pbccrc)
        print('请求参数 : ', post_data)
        print('返回参数: ', result)

    @pytest.mark.skip(reasons='征信-企业-上报')
    def test_upload_pboc_company_v2(self, data_api_pbccrm):
        post_data, result = apitest.upload_pboc_company_v2(data_api_pbccrm)
        print('请求参数 : ', post_data)
        print('返回参数: ', result)

    @pytest.mark.skip(reasons='SOS-企业-查询')
    def test_query_pboc_company_v2(self, data_api_pbccrm):
        post_data, result = apitest.query_pboc_company_v2(data_api_pbccrm)
        print('请求参数 : ', post_data)
        print('返回参数: ', result)


if __name__ == '__main__':
    pytest.main(["-s", "test_api.py"])
