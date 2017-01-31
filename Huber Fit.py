#!/usr/bin/env python

import sys

import pandas as pd
#from StringIO import StringIO

import statsmodels.api as sm

def fit_data(df, Lot_Wafer):
    fname_raw_data = 'plot/data_'+Lot_Wafer

    df = df[df['Lot_Wafer']==Lot_Wafer]
    df.to_csv(fname_raw_data,
              columns=["xxx", "xxx"],
              sep=' ',
              header=False,
              index=False)

    results = {}
    
    print (Lot_Wafer)
    X = df["xxx"]
    Y = df["xxx"]
    X = sm.add_constant(X)
    model = sm.OLS(Y,X)
    results['OLS'] = model.fit()

    huber_t = sm.RLM(Y, X, M=sm.robust.norms.HuberT())
    results['Huber'] = huber_t.fit()
    
    return results

def main():
    df = pd.read_csv('xxx',
                     header=0,
              
                     usecols=["xxx", "xxx", "Corner", "Baseline", "Lot_Wafer"])
    df = df.dropna()
    df = df[df['Baseline']=='POR1.0']
    df = df[df['Corner']=='TT']

    
    Lot_Wafer_list = sorted(df['Lot_Wafer'].unique())
    print (Lot_Wafer_list)
    all_results = {}
    for Lot_Wafer in Lot_Wafer_list:
        all_results[Lot_Wafer] = fit_data(df, Lot_Wafer)

    df_res = pd.DataFrame(columns=('Lot_Wafer', 'OLS_a', 'OLS_a_err', 'OLS_b', 'OLS_b_err', 'OLS_R2', 'Huber_a', 'Huber_a_err', 'Huber_b', 'Huber_b_err'))
    for Lot_Wafer in Lot_Wafer_list:
        row = [Lot_Wafer]
        res = all_results[Lot_Wafer]['OLS']
        row.append(res.params[0])
        row.append(res.bse[0])
        row.append(res.params[1])
        row.append(res.bse[1])
        row.append(res.rsquared)

        res = all_results[Lot_Wafer]['Huber']
        row.append(res.params[0])
        row.append(res.bse[0])
        row.append(res.params[1])
        row.append(res.bse[1])

        df_res.loc[len(df_res)] = row

    df_res.to_csv('plot/fit_results',
                  sep=' ')
        
    print ('\n\n\n')
    print (df_res)


    



    return

main()
