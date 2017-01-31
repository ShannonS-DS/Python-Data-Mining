
# coding: utf-8

# In[3]:

from pandas import *
import pandas as pd
import numpy as np
import re
import sys
import matplotlib.pyplot as plt
import datetime as dt
import read3
from read3 import *
today = dt.date.today().strftime("%Y%m%d")
import math
pd.set_option("display.max_columns", 30)
pd.set_option("display.max_rows", 5)
import statsmodels.api as sm

from scipy import stats


#from IPython.display import IFrame
#A few imports we will need later
#from xlwings import Workbook, Sheet, Range, Chart

#import plotly.plotly as py
#import plotly.tools as tls
#from plotly.graph_objs import *

import os 


from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go
from plotly.graph_objs import  *
init_notebook_mode(connected=True)
import plotly.tools as tls
#from IPython.display import HTML


# In[2]:

family=sys.argv[1]
device=sys.argv[2]
devicefile=sys.argv[3]

import os
outpath = 'xxx'
outfolder1= outpath+devicefile+'xxx'
os.makedirs(outfolder1, exist_ok=True)

readpath= outpath+devicefile+'xx'+device+'xxx'

if checkfilesize(readpath) =="False":

    sys.exit("No Data "+readpath)

die = pd.read_csv(readpath)




def speccheck(device):
    if device =='xx':
        spec = 
        return spec
    elif device == 'xx':
        spec =
        return spec
    elif device == 'xx':
        spec = 
        return spec
    elif device =='xx':
        spec = 
        return spec

    else:
        print(device+" no spec data" )

devicespec = speccheck(device)
    


die=die[die['xx']=='xx']
die=die[['Date','Family', 'Device']]




die_group=die.sort_values(by=['Lot_Wafer','Date','BKM'],ascending=False)
die_group['Date']= die_group['Date'].fillna("No Data")

die_group['ID'] = die_group['Lot_Wafer']+'_'+die_group['BKM']

die_vccint = die_group.dropna(subset=['xxx','xxx'])

die_vdbl = die_group.dropna(subset=['xxx','xxx'])


#create unique list of names
UniqueID_vcc = die_vccint.ID.unique()
UniqueID_vdbl= die_vdbl.ID.unique()


#create a data frame dictionary to store your data frames
dict_vcc = {elem : pd.DataFrame for elem in UniqueID_vcc}
dict_vdbl= {elem : pd.DataFrame for elem in UniqueID_vdbl}

def cal_intercept(dfDict, df, parameter):
    lst=[]
    for key in dfDict.keys():
        ID =str(key)
        dfDict[key] = df[:][df.ID == key]
        df1 =dfDict[key]

        date = list(df1['Date'])[0]
        if len(df1[parameter])>0:
            slope, intercept, r_value, p_value, std_err = stats.linregress(df1[parameter],df1['xxx'])
            lst.append([date,ID,intercept,slope, r_value,std_err])

    return pd.DataFrame(lst,columns=('Date','ID','Intercept','Slope','R_value','IError'))

    
def cal_intercept1(dfDict, df1, parameter):
    lst=[]

    for key in dfDict.keys():
        ID =str(key)
        dfDict[key] = df1[df1['ID'] == ID]
        #dfDict[key] = die_group[:][die_group.ID == str(key)]
        df = dfDict[key]
        x=df[parameter]
        y=df['xxx']
        x = sm.add_constant(x)
        date = list(df['Date'])[0]
        huber_t = sm.RLM(y, x, M=sm.robust.norms.HuberT())
        try:
            result= huber_t.fit()
            lst.append([date,ID,result.params[0],result.bse[0],result.params[1], result.bse[1]])
        except:
            pass
    return pd.DataFrame(lst,columns=('Date','ID','Intercept','IError','Slope','SError'))

df_vcc = cal_intercept1(dict_vcc,die_vccint,'xxx')
df_vdbl = cal_intercept1(dict_vdbl,die_vdbl,'xxx')

df_vcc['Real Intercept'] = np.exp(df_vcc['Intercept'])
df_vcc['Lot_Wafer']=df_vcc['ID'].astype('str').apply(lambda x:x.rsplit("_",1)[0])
df_vcc['BKM']=df_vcc['ID'].astype('str').apply(lambda x:x.split("_")[2])


df_vdbl['Real Intercept'] = np.exp(df_vdbl['Intercept'])
df_vdbl['Lot_Wafer']=df_vdbl['ID'].astype('str').apply(lambda x:x.rsplit("_",1)[0])
df_vdbl['BKM']=df_vdbl['ID'].astype('str').apply(lambda x:x.split("_")[2])


#df_vdbl.to_csv("C:/Users/jiaqil/Desktop/test1.csv",index=False)

df_vcc =df_vcc.sort_values(by=['Lot_Wafer','Date','BKM'], axis=0, ascending=True, inplace=False, kind='quicksort', na_position='last')
df_vcc.to_excel(outfolder1+device+'_ICC_Benchmark_PMV.xlsx',index=False)

df_vdbl =df_vdbl.sort_values(by=['Lot_Wafer','Date','BKM'], axis=0, ascending=True, inplace=False, kind='quicksort', na_position='last')
df_vdbl.to_excel(outfolder1+device+'_ICC_Benchmark_VDBL.xlsx',index=False)





layout1 = go.Layout(
                autosize=True,
                title=device+' ICC Ratio',
                plot_bgcolor='rgb(229, 229, 229)',
                xaxis=go.XAxis(zerolinecolor='rgb(255,255,255)', gridcolor='rgb(255,255,255)'),
                yaxis=go.YAxis(zerolinecolor='rgb(255,255,255)', gridcolor='rgb(255,255,255)')

)

BKM_vcc= df_vcc['BKM'].unique()
BKM_vdbl= df_vdbl['BKM'].unique()


def errordata(lst,df1):
    data=[]
    for i in lst:
        base = df1[df1['BKM']==i]
        part = go.Scatter(
        x=base['Lot_Wafer'],
        y=base['Real Intercept'],
        mode = 'markers',
        text =base['BKM']+" "+base['Date'],
        name = str(i),
        error_y=dict(
            type='data',
            array=df1['IError'],
            visible=True)
        )
        data.append(part)
    return data



error_vcc = errordata(BKM_vcc,df_vcc)
    
error_vdbl = errordata(BKM_vdbl,df_vdbl)


#fig = tls.make_subplots(rows=2, cols=1)

errorfig_vcc= go.Figure(data=error_vcc, layout = layout1)
errorfig_vdbl= go.Figure(data=error_vdbl, layout = layout1)
errorfig_vcc['layout'].update(title=device+' ICC Ratio_PMV')#height=600, width=600, 
errorfig_vdbl['layout'].update(title=device+' ICC Ratio_VDBL')

#fig = go.Figure(data=databoth, layout=layout1)
#fig.append_trace(error_vcc, 1, 1)

#fig.append_trace(error_vdbl, 2, 1)

#plot(errorfig)

from plotly.offline.offline import _plot_html
plot_html, plotdivid, width, height = _plot_html(errorfig_vcc, False, "", True, '100%', 525,global_requirejs=False)

plot_html_1, plotdivid, width, height = _plot_html(errorfig_vdbl, False, "", True, '100%', 525,global_requirejs=False)

file="<html><head><script src='https://cdn.plot.ly/plotly-latest.min.js'></script></head><body>" + plot_html+plot_html_1+ "</body></html>"


Html_file= open(outfolder1+device+'_Die_Intercept.html',"w")



Html_file.write(file)
Html_file.close()


print(device + " Die ICC Done")





