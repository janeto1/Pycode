# -*- coding: utf-8 -*-
import json

import pytest

from utils.ReadExcel import ReadExcel
from guangqi.PostApi import PostApi

api_case_path = r'D:\AutoCase\TEST\guangqi\api_test.xlsx'


class TestApi:
    test_case = ReadExcel()
    case_calc_other_pro = test_case.read_case_value_dic_by_flag(api_case_path, 'other_pro')

    @pytest.fixture(scope='class', params=case_calc_other_pro)
    def data_calc_other_pro(self, request):
        return request.param

    @pytest.fixture(scope='class', autouse=True)
    def setup(self, ):
        global apitest
        apitest = PostApi()

    # @pytest.mark.skip(reasons='其他产品-计算')
    def test_calc_other_pro(self, data_calc_other_pro):
        post_data, result = apitest.calc_other_pro(data_calc_other_pro)
        print('请求参数 : ', post_data)
        print('返回参数: ', result)


if __name__ == '__main__':
    pytest.main(["-s", "test_other_pro.py"])
