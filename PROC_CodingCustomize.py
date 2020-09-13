# -*- coding: utf-8 -*-
# import numpy as np
import pandas as pd
import re
import os
import collections


# [初始 Setting] 定义PATH_HEAD
PATH_HEAD = r'C:\Users\tianyunchuan\iCloudDrive\Desktop\_pyCodeSpyder_'

# [初始 Setting] 定义数据路径（读取、保存）
PATH_DATA = r'{}\_data\data_survey_coding\\'.format(PATH_HEAD)




class FACODING_CUSTOMIZE:
    
    def __init__(self, raw_file_name, id_col_name, question_col_name, dict_seg_var, dict_kw):
        self.raw_file_name = raw_file_name
        self.id_col_name = id_col_name
        self.question_col_name = question_col_name
        self.dict_seg_var = dict_seg_var
        self.dict_kw = dict_kw
        
    
    def get_rawData(self):
        df_raw = pd.read_excel(r'{}\\{}.xlsx'.format(PATH_DATA, self.raw_file_name),keep_default_na=False)
        if 'valid_sample' in list(df_raw.columns):
            df_raw = df_raw[df_raw['valid_sample']==1]

        df = df_raw[[self.id_col_name, self.question_col_name]]
        
        df.rename(columns={list(df.columns)[1]: self.question_col_name, list(df.columns)[0]: 'SAMPLEID'}, inplace=True)
        
        return df_raw, df
    
    def rawData_seg_append(self, df_raw, df):
        df['valid_sample'] = df_raw['valid_sample']
        for _s in self.dict_seg_var.keys():
            df[_s]=list(df_raw[_s])

        for _k, _v in self.dict_kw.items():
            _pat=re.compile('|'.join(_v))
            df['new']=[1 if _pat.search(s) else 0 for s in df[self.question_col_name]]
            df=df.rename(columns={'new':_k})
        return df
    
    
    def get_result(self, df):
        for seg_name in self.dict_seg_var.keys():
            print(seg_name)
            self.calc(df, seg_name)
        return seg_name
    

    def calc(self, df, seg_name):
        grouped = df.groupby(seg_name)
        list_results = []
        for k, w in self.dict_kw.items():
            d_tmp = {
                'key_word': k,
                'count': dict(grouped[k].sum()),
                'percent': dict(grouped[k].mean()),
                'details': w
                }
            list_results.append(d_tmp)
        
        _result_tmp = pd.DataFrame.from_dict(list_results)
        pd.DataFrame(list(_result_tmp['percent']))
         
        result_calc = pd.DataFrame(_result_tmp['key_word'])
            
        result_calc = result_calc.merge(pd.DataFrame(list(_result_tmp['percent'])),left_index=True, right_index=True)
        
        _z01 = pd.DataFrame(df.describe().transpose()['mean'])
        _z01['key_word'] = _z01.index
        _z01.reset_index()
        
        result_calc = result_calc.merge(_z01,left_on='key_word', right_on='key_word')
    
        for idx, s in enumerate(self.dict_seg_var[seg_name]):
            list(result_calc.columns)
            result_calc.rename(columns={list(result_calc.columns)[idx+1]:s}, inplace = True)    
        result_calc.rename(columns={'mean':'Total'}, inplace = True)


        
        d = dict(collections.Counter(df[seg_name]))
        d['Total'] = sum(d.values())
        d['key_word'] = 'Base'
        for idx, s in enumerate(self.dict_seg_var[seg_name]):
            d[s] = d.pop(idx+1)
        df_temp = pd.DataFrame.from_dict(d,orient='index').T
        df_temp.index = ["TTL"]
        result_calc = pd.concat([result_calc,df_temp],axis=0,ignore_index=False, sort=False)
        
        


        # with pd.ExcelWriter(r'{}\\result_byCustomize.xlsx'.format(PATH_DATA)) as _writer:
        #     # list_sheet_name = ['result_code_list.xlsx','result_data.xlsx']
        #     result_calc.to_excel(_writer, sheet_name= seg_name)
        # _writer.save()
        # _writer.close()
        result_calc.to_excel(r'{}\\result_Customize_by_{}.xlsx'.format(PATH_DATA,seg_name),sheet_name=seg_name) 
        return result_calc



            
    def go(self):
        df_raw, df = self.get_rawData()
        df = self.rawData_seg_append(df_raw, df)
        seg_name = self.get_result(df)
        result_calc = self.calc(df, seg_name)
        return df, result_calc
