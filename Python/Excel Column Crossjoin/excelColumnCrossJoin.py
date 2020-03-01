# -*- coding: utf-8 -*-
"""
This excercise was created for my problem with preparing large retrieve tables for Essbase queries, that are usually nested 
in excel spreadsheets
with this solution that takes two inputs:
    + sheet with columns and their values
    + sheet with labels whether column and its values should be used for row/column header
it is extreamely easy to create (and refresh on monthly basis) refresh grids
It is created in python because python does this crossjoin and arrangement that techniques i used originally in vba

Output is then saved as xlsx file.    
"""

import openpyxl as opx
import pandas as pd
import xlrd as xl
import numpy as np

controlFilePath = input("Please provide absolute path with extension to the Control file (xlsx): ")
tabs = input("Please provide tab name with columns and values as well as tab name with column settings, separated by SEMICOLON: ")
tabs = tabs.split(";")

#test
# controlFilePath = r"C:\Users\Mamij\OneDrive\utility_projects\utility_projects\Python\Excel Column Crossjoin\testFile.xlsx"
# tabs = ["Data","Control"]


colValues = pd.read_excel(controlFilePath,sheet_name=tabs[0])
colSettings = pd.read_excel(controlFilePath,sheet_name=tabs[1])
# we will need list of columns that will be moved to 
#   horizontal axis later on
#   under condition that their Axis value is 'h'
horizontals = list(colSettings[colSettings['Axis']=='h']['Column'].to_numpy())
verticals = list(colSettings[colSettings['Axis']=='v']['Column'].to_numpy())

#empty list to contain our columns (cleansed series)
list_of_cols = []

#empty list to contain column names
list_of_names =[]

for cols in colValues:   
    #add to list series (one column from dataframe) without na values (NaN)
    list_of_cols.append(colValues[cols].dropna())
    list_of_names.append(cols)

#we will create index for cross-joined values 
index = pd.MultiIndex.from_product(list_of_cols, names = list_of_names)

#new crossjoined dataset
cross_joined_data_frame = pd.DataFrame(index = index).reset_index()
#dummy Field for aggregation
cross_joined_data_frame["dummy"] = 0


#for cols in colSettings.items():

pivoted_data_frame = pd.pivot_table(cross_joined_data_frame,
                                    index = verticals,
                                    columns=horizontals,
                                    values=['dummy'], 
                                    aggfunc=np.sum).reset_index()

pivoted_data_frame["dummy"]=None

#outputFilePath = r"C:\Users\Mamij\OneDrive\utility_projects\utility_projects\Python\Excel Column Crossjoin\outputFile.xlsx"

outputFilePath = input("Please provide absolute path with extension for output file (xlsx): ")
pivoted_data_frame.to_excel(outputFilePath,
                            merge_cells=True,
                            sheet_name='Table')