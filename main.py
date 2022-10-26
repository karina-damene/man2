# -*- coding: utf-8 -*-
"""
    generate eDHR 
    @author : Karina DAMENE 
    Reviewer : Loic Morel & Patrick MONTEUX
"""

import yaml
from pathlib import Path
from modules.utils import ergonomy, data_agregation, load_yaml 
from modules.bak_data import manage_bak_data
from modules.sage_data import manage_sage_data
from flask import Flask, request, render_template, session, redirect
import numpy as np
import pandas as pd
import socket
chanel_server = socket.gethostname()



def main_bak():
    bak_file_paths = sorted(Path().rglob("*.bak"))
    bak_file_path = ergonomy.request_file_path(bak_file_paths)
    # parse .bak data 
    df_bak_file_path = data_agregation.collect_df_from_sql(bak_file_path)
    df_asp_net_users = df_bak_file_path[0]
    df_plc1 = df_bak_file_path[1]
    df_base_article = df_bak_file_path[2]
    data_parameted, tables = load_yaml.load_yaml_func(r'config/config_data_bak.yaml')
    # then load yaml config to extract needed data
    noms_qualite = manage_bak_data.manage_asp_net_users_from_config(data_parameted, df_asp_net_users)
    num_serie = manage_bak_data.manage_plc1_from_config(data_parameted,df_plc1)
    noms_qualite = noms_qualite
    num_serie = num_serie
    a = pd.concat([noms_qualite, num_serie], axis=1)
    print(a)
    append_df_tohtml('out.html', a)
            # list_df = [noms_qualite, num_serie]
            # output = ""
            # for index, df in enumerate(list_df):   
            #     output += df.to_html() + '<br><h1>This is a heading</h1>'

            # with open('output.html', 'w') as f:
            #     f.writelines(output)   
            #append_df_tohtml('simple.html', noms_qualite )
            #append_df_tohtml('simple.html', num_serie )
            
            #append_df_tohtml ('simple.html', all_df_html)
            # nom_qualite_ht = noms_qualite.to_html()
            #noms_qualite.to_html(open('simple.html', 'w'))
            #noms_qualite.to_html(open('simple.html', 'w'))
    
def append_df_tohtml(html_filename, df):
        df.to_html(open(html_filename, 'w'))

    
# load template dhr (.html)
# the needed data wil be written into dhr template to have edhr.html (complete)
# convert edhr.html to edhr.pdf


def main_sage():
    pass


def main():
    
    #main_bak()
    #main_sage()

    bak_file_paths = sorted(Path().rglob("*.bak"))
    bak_file_path = ergonomy.request_file_path(bak_file_paths)
    # parse .bak data 
    df_bak_file_path = data_agregation.collect_df_from_sql(bak_file_path)
    df= df_bak_file_path[1]
    d = dict([*df.groupby(df['NumSerie'].ne(df['NumSerie'].shift()).cumsum())])
    print(d[1])
  

if __name__ == "__main__":
    main()

    