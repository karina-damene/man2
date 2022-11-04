
from sqlalchemy.engine import URL
from sqlalchemy import create_engine
import socket
import pandas as pd 
import pyodbc



connection_string = f"DRIVER={'ODBC Driver 17 for SQL Server'};SERVER='{socket.gethostname() }' ;DATABASE= 'PLCData_Lake_20221012'"
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
engine = create_engine(connection_url)

def readAnyTable():
    conn = pyodbc.connect(engine)

    query_result = pd.read_sql_query(
            ''' 
                 SELECT * from PLCData_Lake_20221012.dbo.AspNetUsers, conn
                 ''')
            
    conn.close()
    
    return query_result
a=readAnyTable()


