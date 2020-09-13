# -*- coding: utf-8 -*-
""" CodingByJieba """

import PROC_CodingByJieba

RAW_FILE_NAME = 'FaCoding_RawSample'
ID_COL_NAME = 'SAMPLEID'
QUESTION_COL_NAME = 'q30fa'
OUTPUT_KW_NUM = 1000

codingJieba = PROC_CodingByJieba.FACODING_BY_JIEBA(RAW_FILE_NAME, ID_COL_NAME, QUESTION_COL_NAME, OUTPUT_KW_NUM)
df_raw, corpos, segmentDataFrame, df_coding, fSegStat = codingJieba.go()