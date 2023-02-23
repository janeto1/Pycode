# -*- coding: utf-8 -*-

import pytest
from utils.ReadExcel import ReadExcel
from zhenxing.PostApi import PostApi

api_case_path = r'D:\AutoCase\TEST\zhenxing\api_case.xlsx'


class TestPoc:
    test_case = ReadExcel()
    case_calc_api = test_case.read_case_value_dic_by_flag(api_case_path, 'calc_api')
    case_calc_query = test_case.read_case_value_dic_by_flag(api_case_path, 'query')

    @pytest.fixture(scope='class', params=case_calc_api)
    def data_calc_api(self, request):
        return request.param

    @pytest.fixture(scope='class', params=case_calc_query)
    def data_calc_query(self, request):
        return request.param

    @pytest.fixture(scope='class', autouse=True)
    def setup(self, ):
        global apitest
        apitest = PostApi()

    # @pytest.mark.skip(reasons='接口-计算')
    def test_calc_api(self, data_calc_api):
        post_data, result = apitest.execute_product(data_calc_api)
        print('请求参数 : ', post_data)
        print('返回参数: ', result)

    @pytest.mark.skip(reasons='接口-查询')
    def test_query_api(self, data_calc_query):
        post_data, result = apitest.query_product(data_calc_query)
        print('请求参数 : ', post_data)
        print('返回参数: ', result)


if __name__ == '__main__':
    pytest.main(["-s", "test_pboc.py"])
