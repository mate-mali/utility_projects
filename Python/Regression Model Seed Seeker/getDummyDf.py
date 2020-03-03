# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 20:20:23 2020

@author: Mamij
"""
def get_dummied_df(source_dataframe,
                            supplementary_dataframe,
                            target_hor_cols,
                            target_ver_cols):
    import pandas as pd
    transposed_tbl = pd.DataFrame(source_dataframe)
    transposed_tbl = transposed_tbl.melt(
        id_vars=[target_hor_cols],
        value_vars=["N1","N2","N3","N4","N5","N6","N7","N8","N9","N10","N11","N12","N13","N14","N15","N16","N17","N18","N19","N20"])
    
    transposed_tbl = transposed_tbl.sort_values(
        [supplementary_dataframe,"variable"],
        ascending=False)
    
    transposed_tbl = pd.concat(
        [transposed_tbl, 
         supplementary_dataframe], axis=0)
    
    transposed_tbl = transposed_tbl[[supplementary_dataframe,"value"]].reset_index()
    
    meta_tbl = pd.DataFrame(transposed_tbl)
    meta_tbl = pd.get_dummies(meta_tbl.value, prefix="N")
    
    #merge with placeholder list that has all 70 columns to get properly initiated dummies list
    transposed_tbl = pd.merge(
                            transposed_tbl[[supplementary_dataframe]],
                            meta_tbl,
                            left_index=True,
                            right_index=True)
    
    transposed_tbl = transposed_tbl[transposed_tbl[supplementary_dataframe] > 0]
    
    #sum the dummies to get one line per one seed
    transposed_tbl = transposed_tbl.groupby(supplementary_dataframe).sum()
    print(transposed_tbl.sum())
    return(transposed_tbl)