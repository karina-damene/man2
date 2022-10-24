# -*- coding: utf-8 -*-
"""
    manage bak data from config 
    @author : Karina DAMENE 
    Reviewer : Loic Morel & Patrick MONTEUX
"""

def manage_asp_net_users_from_config(parameters, df_bak):
    # get values from yaml dictionary 
    noms = parameters["AspNetUsers"]["Noms"]
    if noms:
        df_asp_net_users = df_bak 
        df_asp_net_users =  eval(noms)
    return df_asp_net_users


def manage_plc1_from_config(parameters, df_bak):
    pass


def manage_tbl_ref_basearticle_from_config(parameters, df_bak):
    pass