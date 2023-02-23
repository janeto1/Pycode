# -*- coding: utf-8 -*-
import json

import pytest


from utils.ReadExcel import ReadExcel
from guangqi.PostApi import PostApi

api_case_path = r'D:\AutoCase\TEST\guangqi\api_test.xlsx'


class TestPbocCompany:
    test_case = ReadExcel()
    case_api_pbccrm = test_case.read_case_value_dic_by_flag(api_case_path, 'pboc_company_v2')

    @pytest.fixture(scope='class', params=case_api_pbccrm)
    def data_api_pbccrm(self, request):
        return request.param

    @pytest.fixture(scope='class', autouse=True)
    def setup(self, ):
        global apitest
        apitest = PostApi()

    # @pytest.mark.skip(reasons='征信-企业-上报')
    def test_upload_pboc_company_v2(self, data_api_pbccrm):
        post_data, result = apitest.upload_pboc_company_v2(data_api_pbccrm)
        print('请求参数 : ', post_data)
        print('返回参数: ', result)

    # @pytest.mark.skip(reasons='SOS-企业-查询')
    def test_query_pboc_company_v2(self, data_api_pbccrm):
        post_data, result = apitest.query_pboc_company_v2(data_api_pbccrm)
        print('请求参数 : ', post_data)
        print('返回参数: ', result)


if __name__ == '__main__':
    pytest.main(["-s", "test_pboc_company.py"])
