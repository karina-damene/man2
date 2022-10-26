# -*- coding: utf-8 -*-
"""
    export dataframe filtred to  
    @author : Karina DAMENE 
    Reviewer : Loic Morel & Patrick MONTEUX
"""


def append_df_tohtml(html_filename, complete_table_dataframe ):
    complete_table_dataframe.to_html(open(html_filename, 'w'))

