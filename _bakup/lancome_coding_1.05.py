"""
1. 环境搭建（软件、IED -> annaconda:spyder）
2. 文件准备（格式化数据文件、NewDict、Stopword文件准备）
3. 初始设置（导入/导出文件路径、其他一次性的基本设置）
4. 新建项目设置（数据文件名称、设问号修改）
5. 导出文件确认（目前设置在当前路径）
    数据->result_data.xlsx
    码表->result_code_list.xlsx
    wordCloud -> wordCloud.jpg
    spss syntax -> 
"""


# -*- coding: utf-8 -*-
import numpy as np
# from snownlp import SnowNLP
import pandas as pd
import re
import jieba
from wordcloud import WordCloud
# [初始 Setting] 自定义词典路径
jieba.load_userdict(r"C:\Users\tianyunchuan\iCloudDrive\Desktop\_win_Trans_mac_\NLP\dict_ti\newdict.txt")                     #加载自定义词典  

#### ----- coding 生成 excel data, code list -----
class FACODING:
    
    def __init__(self, file_path, question_no, output_word_num):
        self.file_path = file_path
        self.question_no = question_no
        self.output_word_num = output_word_num
        
    
    def get_rawData(self):
        # [初始 Setting]  原始数据绝对路径
        # [Setting]  数据格式columns 必须包含 SAMPLEID, 设问编号 两列
#        global df_raw
        df_raw = pd.read_excel(r'C:\Users\tianyunchuan\iCloudDrive\Desktop\_pyCodeSpyder_\survey\FaCoding\lancome\4.2 OE_Message Playback.xlsx',keep_default_na=False)
        df = df_raw[['user id', self.question_no]]
        df.rename(columns={list(df.columns)[1]: 'content', list(df.columns)[0]: 'SAMPLEID'}, inplace=True)
        return df_raw, df
    
    
    def proc_corpos(self, df):
        ##  1. corpos
        corpos=df.loc[:,['content','SAMPLEID']]
        
        ## 删除空白
        corpos = corpos.loc[:,:].replace(r'',np.NaN) 
        corpos.fillna(value='空白待删除', inplace=True)
        corpos = corpos[~(corpos['content']=='空白待删除')]
        corpos.drop_duplicates(subset=list(corpos.columns), keep='first', inplace=True)        
        return corpos
    
    
    def proc_segmentDataFrame(self, corpos):
        segments = []
        SAMPLEIDs = []
        for index, row in corpos.iterrows():
            SAMPLEID = row['SAMPLEID']
            content = row['content']
            segs = jieba.cut(content)
            for seg in segs:
                segments.append(seg)
                SAMPLEIDs.append(SAMPLEID)        
        segmentDataFrame = pd.DataFrame({'segment': segments,'SAMPLEID': SAMPLEIDs});
        return segmentDataFrame 
    
    
    def proc_segStat(self, segmentDataFrame):   
        ##  3. segStat
        ## Alart: Pandas1.0版之前
        # segStat = segmentDataFrame.groupby(by="segment")["segment"].agg({"计数":np.size}).reset_index().sort_values(by=["计数"],ascending=False);  
        segStat = segmentDataFrame.groupby(by="segment")["segment"].agg([("计数", "count")]).reset_index().sort_values(by=["计数"],ascending=False);  
        return segStat


    def input_stopwordFile(self):
        ##  4. stopword
        # [初始 Setting]  设置路径
        stopwords = pd.read_csv(r"C:\Users\tianyunchuan\iCloudDrive\Desktop\_win_Trans_mac_\NLP\dict_ti\StopwordsCN.txt", encoding='utf8', index_col=False)
        stopwordsTemp = pd.read_csv(r"C:\Users\tianyunchuan\iCloudDrive\Desktop\_win_Trans_mac_\NLP\dict_ti\StopwordsCN_temp.txt", encoding='utf8', index_col=False)
        return stopwords, stopwordsTemp
    
    def proc_fSegStat(self, segStat, stopwords, stopwordsTemp):        
        ##  5. fSegStat
        fSegStat = segStat[~segStat.segment.isin(stopwords.stopword)]
        fSegStat = fSegStat[~segStat.segment.isin(stopwordsTemp.stopword)]        
        fSegStat = fSegStat[fSegStat['segment'].str.len() >1]
        fSegStat = fSegStat[fSegStat['计数'] >2]
#        if len(fSegStat)>=199:     
#            fSegStat = fSegStat.iloc[:199,:]
        if len(fSegStat)>=self.output_word_num:     
            fSegStat = fSegStat.iloc[:self.output_word_num,:]
        return fSegStat
    
    def proc_wordsToDict(self, fSegStat):
        ##  6. get_wordsToDict
        wordsToDict = fSegStat.set_index('segment').to_dict()
        return wordsToDict
    
    
    def proc_wordCloud(self, wordsToDict):
        ##  7. wordCloud 配置
        # [初始 Setting]设置wordCloud图片的尺寸、精度
        wordCloud = WordCloud(
            font_path='.\simhei.ttf', 
            #background_color="black"
            background_color='white',
            max_words=2000,max_font_size=60,random_state=42,scale=8,
            width=400,height=200,prefer_horizontal=0.9)
        
        ##  8. get_pic
        wordCloud.fit_words(wordsToDict['计数'])
        # [Setting]  wordCloud保存路径 当前路径下
        wordCloud.to_file(r'.\wordCloud'+'.jpg')
        return
    
    def coding(self, df, fSegStat, df_raw):
        ## 9. QC_coding
        coding_list = []
        for index1, s in enumerate(df['content']):
            if type(s)!=float:
                
                print(str(index1)+s+'-'*30)
                coding_codeNum = ''
                for index2, key_word in enumerate(fSegStat['segment']):      
                    if key_word in s:
                        print(index2, key_word)
                        coding_codeNum = coding_codeNum + ',' + str(index2+1)    
                coding_codeNum = coding_codeNum + ','
                coding_list.append(coding_codeNum)
            else:
                coding_list.append('*')
#        df['coding'] = [',{},'.format(len(fSegStat)+1) if s==',' else s for s in coding_list]
        coding_col_name = '{}_coding'.format(list(df_raw.columns)[-1])
        df[coding_col_name] = [',{},'.format(len(fSegStat)+1) if s==',' else s for s in coding_list]
        return df
    
    
    def go(self):
        df_raw, df = self.get_rawData()
        corpos = self.proc_corpos(df)
        segmentDataFrame = self.proc_segmentDataFrame(corpos)
        segStat = self.proc_segStat(segmentDataFrame)
        stopwords, stopwordsTemp = self.input_stopwordFile()
        fSegStat = self.proc_fSegStat(segStat, stopwords, stopwordsTemp)
        wordsToDict = self.proc_wordsToDict(fSegStat)
        self.proc_wordCloud(wordsToDict)
        df_coding = self.coding(df, fSegStat, df_raw)
        return df_raw, df, corpos, segmentDataFrame, segStat, fSegStat, df_coding
    

if __name__ == '__main__':
    # [Setting] 第一个参数可暂时忽略，第二个参数为题号，第三个参数为选择词频数前n个关键词
    facoding = FACODING('filePath', 'content',1000)
    df_raw, df, corpos, segmentDataFrame, segStat, fSegStat, df_coding = facoding.go()
    
    # [初始 Setting]  result文件, 整理、保存在当前路径下    
    fSegStat = fSegStat.append({'segment':'其他', '计数':999999}, ignore_index=True)      
    col_name = fSegStat.columns.tolist()
    col_name.insert(col_name.index('计数'),'code_number')# 在某列前面列前面插入
    fSegStat = fSegStat.reindex(columns=col_name)   
    fSegStat['code_number'] = [i for i in range(1, len(fSegStat)+1 )]      
    
    fSegStat.to_excel(r'result_code_list.xlsx',sheet_name='code_list') 
    df_coding.to_excel(r'result_data.xlsx',sheet_name='data') 



#### ----- word extrat (Customize) -----

## [Setting 待添加Segment字段信息录入！]、选项注意按照顺序
dict_var_seg = {
    'city age': ['Tier1_20-29','Tier1_30-39','Tier2_20-29','Tier2_30-39',],
    'gender': ['Male', 'Famale'],      
    }


## 导入BD字段
for _s in dict_var_seg.keys():
    df[_s]=list(df_raw[_s]) 


## [Setting 自定义词典，词典的key最终追加列至DF]
dict_kw={
      # '可爱':['可爱','可可','卡哇伊','萌'],
      '时尚':['时尚','时髦','潮流','新潮'],
      '个性':['独特','个性',],
      '兰蔻 LANCOME':["兰蔻","兰寇","蓝口","LANCOME","lancome",],
      '兰蔻':["兰蔻","兰寇","蓝口","蓝蔻",],
      'LANCOME':["LANCOME","lancome",],
      '喷泉':["喷",],
}


## 根据 dict_kw 追加包含value的 0,1 数据列
for _k, _v in dict_kw.items():
    _pat=re.compile('|'.join(_v))
    df['new']=[1 if _pat.search(s) else 0 for s in df_coding['content']]
    df=df.rename(columns={'new':_k})


## 查看数据概貌
df_desc = df.describe()





def calc(seg_name):
    
    # grouped = df.groupby('city age')
    grouped = df.groupby(seg_name)
    # grouped
    # grouped.groups
    
    list_results = []
    for k, w in dict_kw.items():
        # print(idx,k)
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
    
    
    # result_calc.merge(_result_tmp,left_on="lkey",right_on="rkey")
    result_calc = result_calc.merge(pd.DataFrame(list(_result_tmp['percent'])),left_index=True, right_index=True)
    
    _z01 = pd.DataFrame(df.describe().transpose()['mean'])
    _z01['key_word'] = _z01.index
    _z01.reset_index()
    
    result_calc = result_calc.merge(_z01,left_on='key_word', right_on='key_word')

    for idx, s in enumerate(dict_var_seg[seg_name]):
        list(result_calc.columns)
        result_calc.rename(columns={list(result_calc.columns)[idx+1]:s}, inplace = True)

    result_calc.rename(columns={'mean':'Total'}, inplace = True)
    
    return result_calc

result_calc = calc('gender')
result_calc = calc('city age')


# [('{:.0f}%'.format(s*100)) for s in result_calc['Male']]

