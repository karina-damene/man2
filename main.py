# -*- coding: utf-8 -*-
"""
    generate eDHR 
    @author : Karina DAMENE 
    Reviewer : Loic Morel & Patrick MONTEUX
"""

import yaml
from pathlib import Path
import numpy as np
import pandas as pd
import socket
from flask import Flask, render_template
from modules.utils import ergonomy, data_agregation, load_yaml 
from modules.bak_data import manage_bak_data
from modules.sage_data import manage_sage_data

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
    return num_serie
    

    
    #a = pd.concat([noms_qualite, num_serie], axis=1)
    #print(a)
    #append_df_tohtml('out.html', a)
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
  

def main_sage():
    pass


def main():
    
    num_serie = main_bak()
    num_serie= num_serie.to_html(index=False)
    dhr="CK062529"
    lot = 2237
    quantite_totale_fabriquee = 168
    quantite_rebutee = 0
    quantite_de_produits_conformes = quantite_totale_fabriquee - quantite_rebutee
    reference = 22177
    reference_dm = "yl079100"
    indice_manu = "ref2"
    indice_add = ""
    number = 2



    app = Flask(__name__)
    @app.route('/')
    @app.route('/table')
    def table():
        return render_template('table.html', page_title_text='eDHR',
                        title_text='eDHR _ Device History Record',
                        #text =':DHR - [Référence DM] - [Lot]',
                        #<p>DHR - {{dhr}} - {{lot}}<strong>{{text}}</strong>
                        dhr = dhr,
                        lot = lot,
                        quantite_totale_fabriquee = quantite_totale_fabriquee,
                        quantite_rebutee = quantite_rebutee,
                        quantite_de_produits_conformes = quantite_de_produits_conformes,
                        reference = reference,
                        reference_dm= reference_dm,
                        indice_manu= indice_manu,
                        indice_add=indice_add,
                        prices_text='Historical prices of S&P 500',
                        stats_text='Historical prices summary statistics',
                        num_serie=num_serie,
                        show_number='show number',
                        number = number)
    app.run(host="localhost", port=int("5000"))
    #main_sage()

    # bak_file_paths = sorted(Path().rglob("*.bak"))
    # bak_file_path = ergonomy.request_file_path(bak_file_paths)
    # df_apt = data_agregation.collect_df_from_sql(bak_file_path)
    # print(df_apt)

    # parse .bak data 
    #df_bak_file_path = data_agregation.collect_df_from_sql(bak_file_path)
    #df= df_bak_file_path[1]
    #print(df.iloc[:,0:7])
    #d = dict([*df.groupby(df['NumSerie'].ne(df['NumSerie'].shift()).cumsum())])
    #print(d[0])
  

if __name__ == "__main__":
    main()
    