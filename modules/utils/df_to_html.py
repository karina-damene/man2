# -*- coding: utf-8 -*-
"""
    export dataframe filtred to  
    @author : Karina DAMENE 
    Reviewer : Loic Morel & Patrick MONTEUX
"""

from data_agregation import collect_df_from_sql

bak_file = 'PLCData_Lake_20221012'
df_apt = collect_df_from_sql(bak_file)
print(df_apt)
