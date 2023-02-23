import datetime

import pymysql
from utils.times import time_to_str


class readMysql():
    def __init__(self, user, pwd, host, database):
        self.conn = None
        self.cursor = None
        self.user = user  # 'shapp'
        self.pwd = pwd  # '123456'
        self.host = host  # '166.188.30.85'
        self.database = database  # 'complex_network2'

    def connect_db(self):
        """autocommit=True 自动提交事务，预防重复查询，丢失数据"""
        if self.conn is None:
            conn = pymysql.connect(host=self.host, user=self.user, password=self.pwd, database=self.database,
                                   charset="utf8", autocommit=True)

        return conn, conn.cursor()

    def excute_sql(self, sql):
        if self.cursor is None:
            self.conn, self.cursor = self.connect_db()
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        col = self.cursor.description
        return data, col

    def excute_delete(self, sql):
        if self.cursor is None:
            self.conn, self.cursor = self.connect_db()
        self.cursor.execute(sql)
        self.conn.commit()

    def close_db(self):
        if self.cursor:
            self.cursor.close
            self.cursor = None
        if self.conn:
            self.conn.close
            self.conn = None

    def select_count(self, sql):
        data, col = self.excute_sql(sql)
        return data[0][0]

    def select_page_list_data(self, sql):
        # 根据查询条件返回查询列表
        result = []
        data, col = self.excute_sql(sql)
        col_name = [item[0] for item in col]
        for item in data:
            temp_cell = {}
            for name, value in zip(col_name, item):
                if isinstance(value, (datetime.datetime)):
                    temp_cell[name.lower()] = time_to_str(value)
                else:
                    temp_cell[name.lower()] = value
            result.append(temp_cell)
        return len(result), result

    def select_key_data(self, key_name, sql):
        datalen, data = self.select_page_list_data(sql)
        result = None
        if len(data) > 0:
            for key, value in data[0].items():
                if key == key_name:
                    result = value
                    break
        return result


if __name__ == '__main__':
    sql = u"select p.prod_name ,f.* from field_define f join prod_config p on f.prod_num=p.prod_num where (org_num = 'JJYH0000001' or auth_org_num = 'JJYH0000001')    order by f.field_name asc limit 0,10"
    test = readMysql()
    data, col = test.excute_sql(sql)
    print(data)
