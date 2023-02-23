# -*- coding: utf-8 -*-
import json
import os

from utils.ReadExcel import ReadExcel
from utils.readMysql import readMysql
from utils.times import dt_strftime

rexe = ReadExcel()
tmpl_title_head = "INSERT INTO template (template_id,template_name,description,sort,data_source,data_type,var_type,version,explanation,is_preset,department_id,creator_id,create_time,compile_status,status,remark,history_id,drools,flowchart,template_type) VALUES"
tmpl_param_title_head = "INSERT INTO tmpl_param (param_id,template_id,param_name,param_type,data_type,description,optional_value) VALUES"
tmpl_relation_title_head = "INSERT INTO template_to_var (relation_id,template_id,variate_id) VALUES"

variate_title_head = "INSERT INTO variate (variate_id,var_name,sort,department_id,var_schema,var_type,data_type,version,description,template_id,explanation,status,create_date,history_id,param_info,need_upgrade,tag_id,data_length,remark) VALUES"
variate_reference_head = "INSERT INTO variate_reference (record_id,parent_id,children_id,parent_type,children_type) VALUES"
path = r'D:\AutoCase\TEST\guangqi\temple_new.xlsx'
sql_path = r'D:\AutoCase\TEST\guangqi'


class temple_sql:
    def __init__(self, report_id):
        self.rdb = readMysql(user='vp_gghlapp', pwd='VpGghlapp123!', host='166.188.30.52', database='vplatform_linshi')
        self.id_max_limit, self.id_generate_limit = self.read_max_generate_id()
        self.temple_datas = {}
        self.report_id = report_id
        self.vp_id_generate = []

    def write_sql_file(self, str_data, name):
        with open(sql_path + '\\add_new_var' + dt_strftime("%Y%m%d") + '.sql', 'a+', encoding="utf-8") as f:
            f.write("-- %s --" % (name) + '\n')
            f.write(str_data + '\n\n\n')

    def clear_file(self, ):
        sql_file_path = sql_path + '\\add_new_var' + dt_strftime("%Y%m%d") + '.sql'
        if os.path.exists(sql_file_path):
            with open(sql_file_path, 'r+') as f:
                f.truncate(0)

    def data_type(self, str_value):
        if str_value == '浮点型':
            return 'Double'
        elif str_value == '字符型':
            return 'String'
        elif str_value == '整数型':
            return 'Integer'
        else:
            return 'Long'

    def calc_data_length(self, str_value, length):
        if str_value == "浮点型" or str_value == "长整型":
            return "20"
        elif str_value == "整数型":
            return "10"
        else:
            return str(length)

    def generate_sql_condition(self, next_val, name):
        return "update vp_id_generate set next_val=%s where segment_name='%s' " % (next_val, name)

    def read_max_generate_id(self, ):
        try:
            table_max_ids_sql = """
                select 'variate' as 'segment_name',max(variate_id) as 'next_val' from variate v union 
            select 'variate_reference' as 'segment_name',max(record_id) as 'next_val'  from variate_reference vr  union
            select 'template' as 'segment_name',max(template_id) as 'next_val'  from template t union
            select 'template_to_var' as 'segment_name',max(relation_id) as 'next_val' from template_to_var ttv union
            select 'tmpl_param' as 'segment_name',max(param_id) as 'next_val' from tmpl_param ;
                """
            table_generate_ids_sql = """select * from vp_id_generate vig where segment_name in ('template','template_to_var','tmpl_param','variate','variate_reference');"""
            max_ids_len, max_ids = self.rdb.select_page_list_data(table_max_ids_sql)
            generate_ids_len, generate_ids = self.rdb.select_page_list_data(table_generate_ids_sql)
            table_max_ids = {item['segment_name']: item['next_val'] + 1 for item in max_ids}
            table_generate_ids = {item['segment_name']: item['next_val'] for item in generate_ids}
            return table_max_ids, table_generate_ids
        except Exception as e:
            print(e)
        finally:
            self.rdb.close_db()

    def read_variate(self, ):
        self.read_temple()
        sheet_name = 'variate'
        data = rexe.read_case_value_dic(path, sheet_name)
        variate_list = []
        variate_id = self.id_max_limit['variate']  # 101591
        variate_record_id = self.id_max_limit['variate_reference']  # 100000
        variate_record_list = []
        for item in data:
            temp_variate_list = []
            temp_variate_record = []
            temp_variate_list.append(str(variate_id))  # variate_id
            temp_variate_list.append("\'" + item.get('en_name') + "\'")  # var_name
            temp_variate_list.append("\'" + item.get('sort') + "\'")  # sort
            temp_variate_list.append("\'" + item.get('department') + "\'")  # department_id
            temp_variate_list.append("null")  # var_schema
            temp_variate_list.append("\'derivative\'")  # var_type
            temp_variate_list.append("\'" + self.data_type(item.get('data_type')) + "\'")  # data_type
            temp_variate_list.append("1")  # version
            temp_variate_list.append("\'" + item.get('ch_name') + "\'")  # description

            template_id = self.temple_datas[item.get('temple_name')]
            temp_variate_list.append(str(template_id))  # template_id
            temp_variate_list.append("\'" + item.get('explain') + "\'")  # explanation
            temp_variate_list.append("1")  # status
            temp_variate_list.append("sysdate()")  # create_date
            temp_variate_list.append(str(variate_id))  # history_id
            param_info = {}
            if item.get('p1') and len(item.get('p1')) > 0:
                param_info['p1'] = item.get('p1')
            if item.get('p2') and len(item.get('p2')) > 0:
                param_info['p2'] = item.get('p2')
            if item.get('p3') and len(item.get('p3')) > 0:
                param_info['p3'] = item.get('p3')

            temp_variate_list.append("\'" + json.dumps(param_info, ensure_ascii=False) + "\'")  # param_info
            temp_variate_list.append("0")  # need_upgrade
            temp_variate_list.append("null")  # tag_id
            temp_variate_list.append(
                self.calc_data_length(item.get('data_type'), item.get('data_length')))  # data_length
            temp_variate_list.append("null")  # remark
            variate_list.append(variate_title_head + "(" + ",".join(temp_variate_list) + ")")

            # variate_reference
            temp_variate_record.append(str(variate_record_id))  # record_id
            temp_variate_record.append(str(self.report_id))  # parent_id
            temp_variate_record.append(str(variate_id))  # children_id
            temp_variate_record.append("\'" + 'original' + "\'")  # parent_type
            temp_variate_record.append("\'" + 'derivative' + "\'")  # children_type
            variate_record_list.append(variate_reference_head + "(" + ",".join(temp_variate_record) + ")")
            variate_record_id += 1
            variate_id += 1
        if variate_id >= self.id_generate_limit['variate']:
            self.vp_id_generate.append(self.generate_sql_condition(variate_id, 'variate'))
        if variate_record_id >= self.id_generate_limit['variate_reference']:
            self.vp_id_generate.append(self.generate_sql_condition(variate_record_id, 'variate_reference'))
        self.write_sql_file(";\r\n".join(variate_list) + ";", 'variate')
        self.write_sql_file(";\r\n".join(variate_record_list) + ";", 'variate_reference')
        self.write_sql_file(";\r\n".join(self.vp_id_generate) + ";", 'vp_id_generate')

    def read_temple(self, ):
        """
        生成计算模板sql
        :return:
        """
        template_id = self.id_max_limit['template']  # 100110  # template 表 max_template_id
        relation_id = self.id_max_limit['template_to_var']  # 100142  # template_to_var 表 max_relation_id
        tmpl_param_id = self.id_max_limit['tmpl_param']  # 100117  # tmpl_param 表 max_param_id
        temple_list = []
        param_list = []
        tmpl_relation_list = []
        sheet_name = 'temple'
        data = rexe.read_case_value_dic(path, sheet_name)
        for item in data:
            temp_cell_list = []
            temp_param = []
            tmpl_relation = []
            self.temple_datas[item.get('en_name')] = template_id
            temp_cell_list.append(str(template_id))
            temp_cell_list.append("\'" + item.get('en_name') + "\'")  # template_name
            temp_cell_list.append("\'" + item.get('ch_name') + "\'")  # description
            temp_cell_list.append("\'" + item.get('sort') + "\'")  # sort
            temp_cell_list.append("\'" + item.get('datasource') + "\'")  # data_source
            temp_cell_list.append("\'" + self.data_type(item.get('data_type')) + "\'")  # data_type
            temp_cell_list.append("\'derivative\'")  # var_type
            temp_cell_list.append("1")  # 默认版本 version
            temp_cell_list.append("\'" + item.get('explain') + "\'")  # explanation
            temp_cell_list.append("1")  # 1表示内置，0自定义模板 is_preset
            temp_cell_list.append("\'" + item.get('department') + "\'")  # department_id
            temp_cell_list.append("1")  # creator_id
            temp_cell_list.append("sysdate()")  # create_time
            temp_cell_list.append("1")  # compile_status
            temp_cell_list.append("1")  # status
            temp_cell_list.append("null")  # remark
            temp_cell_list.append(str(template_id))  # history_id
            temp_cell_list.append("null")  # drools
            temp_cell_list.append("null")  # flowchart
            temp_cell_list.append("\'" + 'D' + "\'")  # template_type
            if item.get('p1') and len(item.get('p1')) > 0:
                temp_param.append(['p1', item.get('p1'), item.get('p1_ch')])  # value name
            if item.get('p2') and len(item.get('p2')) > 0:
                temp_param.append(['p2', item.get('p2'), item.get('p2_ch')])
            if item.get('p3') and len(item.get('p3')) > 0:
                temp_param.append(['p3', item.get('p3'), item.get('p3_ch')])
            for item in temp_param:
                temp_param_list = []
                temp_param_list.append(str(tmpl_param_id))  # param_id
                temp_param_list.append(str(template_id))  # template_id
                temp_param_list.append("\'" + item[0] + "\'")  # param_name
                temp_param_list.append("\'" + 'select' + "\'")  # param_type
                temp_param_list.append("null")  # data_type
                temp_param_list.append("\'" + str(item[2]) + "\'")  # description
                temp_param_list.append("\'" + item[1] + "\'")  # optional_value
                tmpl_param_id += 1
                param_list.append(tmpl_param_title_head + "(" + ",".join(temp_param_list) + ")")
            tmpl_relation.append(str(relation_id))
            tmpl_relation.append(str(template_id))
            tmpl_relation.append(str(self.report_id))
            relation_id += 1
            template_id += 1
            temple_list.append(tmpl_title_head + "(" + ",".join(temp_cell_list) + ")")
            tmpl_relation_list.append(tmpl_relation_title_head + "(" + ",".join(tmpl_relation) + ")")
        if template_id >= self.id_generate_limit['template']:
            self.vp_id_generate.append(self.generate_sql_condition(template_id, 'template'))
        if relation_id >= self.id_generate_limit['template_to_var']:
            self.vp_id_generate.append(self.generate_sql_condition(relation_id, 'template_to_var'))
        if tmpl_param_id >= self.id_generate_limit['tmpl_param']:
            self.vp_id_generate.append(self.generate_sql_condition(tmpl_param_id, 'tmpl_param'))
        self.write_sql_file(";\r\n".join(temple_list) + ";", 'temple')
        self.write_sql_file(";\r\n".join(param_list) + ";", 'tmpl_param')
        self.write_sql_file(";\r\n".join(tmpl_relation_list) + ";", 'template_to_var')


if __name__ == '__main__':
    report_id = 3  # 53环境在企业的id是3 select * from variate v where v.variate_id =3
    test = temple_sql(report_id)
    test.clear_file()
    test.read_variate()
