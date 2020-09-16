# -*- coding: utf-8 -*-
""" CodingByJieba """

import PROC_CodingCustomize

# RAW_FILE_NAME = '4.2 OE_Message Playback'
# ID_COL_NAME = 'user id'
# QUESTION_COL_NAME = 'content'

RAW_FILE_NAME = 'Playback'
ID_COL_NAME = 'SAMPLEID'
QUESTION_COL_NAME = 'q23fa'


# -*- coding: utf-8 -*-
""" CodingByCustomize """

# DICT_SEG_VAR = {
#     'city age': ['Tier1_20-29','Tier1_30-39','Tier2_20-29','Tier2_30-39',],
#     'gender': ['Male', 'Famale'],      
#     }

DICT_SEG_VAR = {
    'city': ['Tier1_20-29','Tier1_30-39','Tier2_20-29','Tier2_30-39',],
    'user': ['user', 'no_user'],      
    }

## [Setting 自定义词典，词典的key最终追加列至DF]
DICT_KW ={
      # '可爱':['可爱','可可','卡哇伊','萌'],
      '时尚':['时尚','时髦','潮流','新潮'],
      '个性':['独特','个性',],
      '兰蔻 LANCOME':["兰蔻","兰寇","蓝口","LANCOME","lancome",],
      '兰蔻':["兰蔻","兰寇","蓝口","蓝蔻",],
      'LANCOME':["LANCOME","lancome",],
      '喷泉':["喷",],
}



codingCustomize = PROC_CodingCustomize.FACODING_CUSTOMIZE(RAW_FILE_NAME, ID_COL_NAME, QUESTION_COL_NAME, DICT_SEG_VAR, DICT_KW)
# df, result_calc = codingCustomize.go
df, result_calc = codingCustomize.go()