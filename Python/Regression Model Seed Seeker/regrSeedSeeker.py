# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 22:21:12 2020

@author: Mamij
"""

import pandas as pd
import numpy as np

from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split


#read input - later on it will be read from sql server directly
df = pd.read_csv(r'G:\sample.csv',nrows=500000)
print(df.head())

df=shuffle(df)
print(df.head())

#convert generated seed data into 70-col dummy data from 20-col category fields



#here perform regression


#here perform tests


#here takes histoical inputs (20 digit numbers) and convert
#     