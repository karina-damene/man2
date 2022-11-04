# -*- coding: utf-8 -*-
"""
    parse (all) data and convert them into dataframe 
    @author : Karina DAMENE 
    Reviewer : Loic Morel & Patrick MONTEUX
"""
import pandas as pd
import pyodbc   
import socket
from datetime import date
import time
import sqlite3
from sqlite3 import OperationalError


def collect_df_from_sql(bak_file):
    chanel_server = socket.gethostname()
    conn = pyodbc.connect('Driver={SQL Server};'
                       f'Server={chanel_server};'
                       f'Database={bak_file};'
                       'Trusted_Connection=yes;')

    sql_query1 = pd.read_sql_query(f'''
                               select * from {bak_file}.dbo.AspNetUsers
                               '''
                               ,conn) 
    df1 = pd.DataFrame(sql_query1)


    sql_query2 = pd.read_sql_query(f'''
                               select * from {bak_file}.dbo.PLC1
                               '''
                               ,conn) 
    df2 = pd.DataFrame(sql_query2)

    sql_query3 = pd.read_sql_query(f'''
                               select * from {bak_file}.dbo."Tbl-Ref-BaseArticle";
                               '''
                               ,conn) 
    df3 = pd.DataFrame(sql_query3)
    
    sql_query4 = pd.read_sql_query(f'''
                               select * from {bak_file}.dbo."Tbl-Ref-Fab-Detail";
                               '''
                               ,conn) 
    df4 = pd.DataFrame(sql_query4)

    sql_query5 = pd.read_sql_query(f'''
                               select * from {bak_file}.dbo."Tbl-Ref-Fab-Liste";
                               '''
                               ,conn) 
    df5 = pd.DataFrame(sql_query5)

    sql_query6 = pd.read_sql_query(f'''
                               select * from {bak_file}.dbo."Tbl-Ref-Parametres";
                               '''
                               ,conn) 
    df6 = pd.DataFrame(sql_query6)

    return df1, df2, df3, df4, df5, df6


# collect each NmeSerie of date current from plc 
def collect_plc_from_bak(bak_file):
    df_plc1 = collect_df_from_sql(bak_file)[1]
    d = dict([*df_plc1.groupby(df_plc1['NumSerie'].ne(df_plc1['NumSerie'].shift()).cumsum())])
    print(d[1])
    today = date.today()
    print(today)
    print(time.strftime("%d%m%Y"))
  

def collect_df_from_sage():
    pass 

# def collect_df_from_sql(bak_file):
#     chanel_server = socket.gethostname()
#     conn = pyodbc.connect('Driver={SQL Server};'
#                        f'Server={chanel_server};'
#                        f'Database={bak_file};'
#                        'Trusted_Connection=yes;')

# conn = collect_df_from_sql('PLCData_Lake_20221012')
# fd=open('req_cr_fcgf.sql','r') 
# sqlFile = fd.read()

