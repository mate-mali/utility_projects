# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 20:23:38 2020

@author: Mamij
"""

import pandas as pd
import numpy as np
import random as rd
from sqlalchemy import create_engine
import urllib

listSwag = [0]
memeSwag = ["SEED"]
for i in range(1,71):
    listSwag.append(i)
    memeSwag.append(f"N{str(i)}")

pdplc = pd.DataFrame(np.array(range(1,71)))
pdplc ['SEED']=-1
pdplc['variable'] = 'N99'
pdplc['value'] = pdplc.iloc[:,0]
pdplc = pdplc[["SEED","variable","value"]]


table_x = f"SEEDS_int1"
quoted = urllib.parse.quote_plus("Driver={SQL Server};Server=DESKTOP-FU3V8EN;Database=DB_KENO;Trusted_Connection=yes;")

engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(quoted))

sql = f"SELECT top (3000) * FROM {table_x} order by seed desc"

for chunk in pd.read_sql_query(sql , engine, chunksize=1000):
    transposed_sht = pd.DataFrame(chunk)
    transposed_sht = transposed_sht.melt(
        id_vars="SEED",
        value_vars=["N1","N2","N3","N4","N5","N6","N7","N8","N9","N10","N11","N12","N13","N14","N15","N16","N17","N18","N19","N20"])
    transposed_sht = transposed_sht.sort_values(["SEED","variable"],ascending=False)
    transposed_sht = pd.concat([transposed_sht, pdplc], axis=0)
    transposed_sht = transposed_sht[["SEED","value"]].reset_index()
    
    meta_sht = pd.DataFrame(transposed_sht)
    meta_sht = pd.get_dummies(meta_sht.value, prefix="N")
    
    #merge with placeholder list that has all 70 columns to get properly initiated dummies list
    transposed_sht = pd.merge(transposed_sht[['SEED']],meta_sht,left_index=True,right_index=True)
    transposed_sht = transposed_sht[transposed_sht['SEED'] > 0]
    
    #sum the dummies to get one line per one seed
    transposed_sht = transposed_sht.groupby("SEED").sum()
    print(transposed_sht.sum())