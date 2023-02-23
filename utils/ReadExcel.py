# -*- coding: utf-8 -*-
import xlrd


class ReadExcel():

    def __init__(self):
        pass

    def read_case_value(self, filepath, sheet):
        """返回list测试数据"""
        result = []
        workbook = xlrd.open_workbook(filepath)
        casesheet = workbook.sheet_by_name(sheet)
        rows = casesheet.nrows
        for i in range(1, rows):
            result.append(casesheet.row_values(i))
        return result

    def read_case_value_dic(self, filepath, sheet):
        """返回字典测试数据"""
        result = []
        workbook = xlrd.open_workbook(filepath)
        casesheet = workbook.sheet_by_name(sheet)
        rows = casesheet.nrows
        cols = casesheet.ncols
        titles = [casesheet.row_values(0)[i] for i in range(cols)]
        for i in range(1, rows):
            tmp_data = {}
            for name, value in zip(titles, casesheet.row_values(i)):
                tmp_data[name] = value
            result.append(tmp_data)
        return result

    def read_case_value_dic_by_flag(self, filepath, sheet):
        """仅加载可执行案例，返回字典测试数据"""
        result = []
        workbook = xlrd.open_workbook(filepath)
        casesheet = workbook.sheet_by_name(sheet)
        rows = casesheet.nrows
        cols = casesheet.ncols
        titles = [casesheet.row_values(0)[i] for i in range(cols)]
        for i in range(1, rows):
            tmp_data = {}
            if casesheet.row_values(i)[1] == 'Y':  # 仅加载可执行案例
                for name, value in zip(titles, casesheet.row_values(i)):
                    tmp_data[name] = value
                result.append(tmp_data)
        return result


if __name__ == '__main__':
    test = ReadExcel()
    data = test.read_case_value(r"D:\code\kgsapp\casefile\listmanager.xlsx")
    print(data)
