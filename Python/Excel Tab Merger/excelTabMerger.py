# -*- coding: utf-8 -*-
"""
This is excercise that i performede for my colleaugue who struggled with data 
preparation for his academic process, that was separated into multiple tabs that each of them 
was connected with another with one ID column, because of limitation of old Excel 97 file type (255 columns)

I usually would use Alteryx or Knime for this kind of operation, but since it was outside of
corporate scope, the best solution was to use Python instead 
This file accepts user input

+ absolute path to source Excel file (xlsx.xls) - fullPath
+ then, user is prompted in loop to provide input that contains both tab name and merge reference column
    that is stored then in dictionary called fileTabs
+ than, based on dictionary, pandas performs data merging from all indicated tabs and returns
    them as DataFrame named finalOutput
+ then user is prompted to indicate full path to output files in xlsx format - it is again stored in tab fullPath
"""
import pandas as pd

#variables declarations
fileTabs = dict()
fullPath = input("Provide full absolute path to file with extension (xls,xlsx): ")
promptu = ""

#we will collect now sheets in the file 
# and the information about column that will be used as a merger
while promptu != 'exit':
    promptu = input("Type sheet name and merge column, separated by semicolon, or type 'exit' to finish: ")
    if promptu!="" and ";" in promptu:
        sep_propmptu = promptu.split(";")
        fileTabs[sep_propmptu[0]] = sep_propmptu[1]
    else:
        "Wrong input! Try again or type 'exit' to finish: "

#opening all of the indicated sheets as temporary df
# to be collected in a list
finalOutput = pd.DataFrame()
if len(fileTabs.keys())==0:
    print("Wrong tab declaration! restart process to try again.")
elif len(fileTabs.keys()) !=0:
    tempDf = pd.DataFrame()
    listDf = []
    for sheet,column in fileTabs.items():
        tempDf=pd.read_excel(fullPath,sheet_name=sheet)
        listDf.append((tempDf,column))
        
#we will now perform merge as many times
# as we have read temp dataframes
finalOutput = listDf[0][0]
if len(listDf) >1:
    for tempDfr in listDf[1:]:
        finalOutput = pd.DataFrame.merge(
                            finalOutput,
                            tempDfr[0],
                            left_on = listDf[0][1],
                            right_on=tempDfr[1],
                            how='outer')

#then we will output tthe 
# file to indicated location
fullPath = input("Provide full absolute path to desired output file with extension (xlsx): ")
finalOutput.to_excel(fullPath,sheet_name = 'Merged',index=False)


        



    


        
            
    



    