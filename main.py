# -*- coding: utf-8 -*-
"""
    generate eDHR 
    @author : Karina DAMENE 
    Reviewer : Loic Morel & Patrick MONTEUX
"""

import yaml
from pathlib import Path
from modules.utils import ergonomy, data_agregation
from modules import manage_bak_data, manage_sage_data


def main_bak():
    bak_file_paths = sorted(Path().rglob("*.bak"))
    bak_file_path = ergonomy.request_file_path(bak_file_paths)
    # parse .bak data 
    df_bak_file_path = data_agregation.collect_df_from_sql(bak_file_path)
    df_asp_net_users = df_bak_file_path[0]
    df_plc1 = df_bak_file_path[1]
    df_base_article = df_bak_file_path[2]
    # then load yaml config to extract needed data
    with Path("config/config_data_bak.yaml").open() as f:
        config = yaml.safe_load(f)
    for bak, tables in config.items():
        for table, data_parameted in tables.items():
            noms_qualite = manage_bak_data.manage_asp_net_users_from_config(data_parameted, df_asp_net_users)
            print(noms_qualite)
            noms_qualite = noms_qualite.reset_index()
            nom_qualite_ht = noms_qualite.to_html()
            print(nom_qualite_ht,nom_qualite_ht)
    
    # load template dhr (.html)
    # the needed data wil be written into dhr template to have edhr.html (complete)
    # convert edhr.html to edhr.pdf


def main_sage():
    pass


def main():
    #main_bak()
    #main_sage()
    pass

if __name__ == "__main__":
    main_bak()
