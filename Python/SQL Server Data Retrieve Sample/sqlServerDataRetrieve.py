# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 22:21:12 2020

@author: Mamij
"""

import pandas as pd
from sqlalchemy import create_engine
import urllib


quoted = urllib.parse.quote_plus(
    "Driver={SQL Server};Server=DESKTOP-FU3V8EN;Database=DB_KENO;Trusted_Connection=yes;"
    )

engine = create_engine(
    'mssql+pyodbc:///?odbc_connect={}'.format(quoted)
    )

query = """
    select * from [SEEDS_int1] tablesample(0.5 percent)
    union
    select * from [SEEDS_int2] tablesample(0.5 percent)
    union
    select * from [SEEDS_int3] tablesample(0.5 percent)
    union
    select * from [SEEDS_int4] tablesample(0.5 percent)
    """
    
df = pd.read_sql(query,engine)
df.to_csv(
    r'G:\sample.csv',
    index=False,
    chunksize=10000
    )
