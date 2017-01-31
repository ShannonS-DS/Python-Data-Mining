
# coding: utf-8

# In[ ]:

import sys
from pandas import *
import pandas as pd
import re
import numpy as np

import plotly
from plotly import __version__
from plotly.offline import *
import plotly.graph_objs as go
from plotly.graph_objs import *
import plotly.tools as tls
import plotly.plotly as py




import os 


from read3 import *
import read3 as rd

family=sys.argv[1]
device = sys.argv[2]
devicefile=sys.argv[3]

subfile1= "Data"
subfile2= "Plot"

#=================Create Folder in the Directory=====================================
import os
outpath= 'xx'
outfolder1=outpath+devicefile+'xx'
outfolder2=outpath+devicefile+'xxx'
outfolder3=outpath+devicefile+'xx'
outfolder4=outpath+devicefile+'xx'

os.makedirs(outfolder1, exist_ok=True)
os.makedirs(outfolder2, exist_ok=True)
os.makedirs(outfolder3, exist_ok=True)
os.makedirs(outfolder4, exist_ok=True)

#===================Read Files====================================================

filelist=rd.readfile(family, device)
lot_bin_file = getfilename("xx",filelist)
lot_bin_file_path = createpath(family,device,lot_bin_file)

if checkfilesize(lot_bin_file_path) =="False":
    sys.exit("No Data "+lot_bin_file_path)

LotBin = pd.read_csv(lot_bin_file_path)


#=================Create Output File Names===================================================



outputstring="xxx/type1/subfile/device_type1_type2_temp.xlsx"
def outputname_bin (type1,type2,temp):
    outputstring_new= outputstring.replace("devicefile",devicefile)
    outputstring_new= outputstring_new.replace("device",device)
    outputstring_new= outputstring_new.replace("subfile",subfile1)
    outputstring_new= outputstring_new.replace("type1",type1)
    outputstring_new= outputstring_new.replace("type2",type2)
    outputstring_new= outputstring_new.replace("temp",temp)
    return outputstring_new

def outputname_bin_plot (type1,type2,temp):
    outputstring_new= outputstring.replace("devicefile",devicefile)
    outputstring_new= outputstring_new.replace("device",device)
    outputstring_new= outputstring_new.replace("subfile",subfile2)
    outputstring_new= outputstring_new.replace("type1",type1)
    outputstring_new= outputstring_new.replace("type2",type2)
    outputstring_new= outputstring_new.replace("temp",temp)
    return outputstring_new


lot_bin_0 = outputname_bin("Lot","Bincount","0")
lot_bin_100 = outputname_bin("Lot","Bincount","100")
lot_bin_merge = outputname_bin("Lot","Bincount","merge")

lot_progressive_0 = outputname_bin("Lot","Progressive","0")
lot_progressive_100 = outputname_bin("Lot","Progressive","100")


lot_bin_0_plot = outputname_bin_plot("Lot","Bincount","0_Plot")
lot_bin_100_plot = outputname_bin_plot("Lot","Bincount","100_Plot")
lot_bin_merge_plot = outputname_bin_plot("Lot","Bincount","merge_Plot")


lot_progressive_0_plot = outputname_bin_plot("Lot","Progressive","0_Plot")
lot_progressive_100_plot = outputname_bin_plot("Lot","Progressive","100_Plot")

lot_test_0_plot = outputname_bin_plot("Lot","TestProgram","0_Plot")
lot_test_100_plot = outputname_bin_plot("Lot","TestProgram","100_Plot")

#=============Function For Extract Test Program===================================================
def find_testprogram(s,first,temp1,temp2):
    try:
        if temp1 in s:
            try:
                start= s. index(first)+len(first)
                end = s.index(temp1,start)
                return s[start:end]
            except ValueError:
                return s
        if temp2 in s:
            try:
                start= s. index(first)+len(first)
                end = s.index(temp2,start)
                return s[start:end]
            except ValueError:
                return s
        else:
            return s
    except ValueError:
        return s


#===============================================Clean and Extraction=========================================================
LotBin['Temp']=LotBin['Temp'].astype('str')
LotBin['Date'] = pd.to_datetime(LotBin['Date'])
LotBin["Test Program Extract"]=LotBin["Test Program"].apply(lambda row:find_testprogram(row,"_","_0c","_100c"))


LotBin_Filtered = LotBin[~LotBin['Fab Lot'].str.contains("_")]
LotBin_Filtered_0 = LotBin_Filtered[LotBin_Filtered['Temp']=='0']
LotBin_Filtered_100 = LotBin_Filtered[LotBin_Filtered['Temp']=='100']
LotBin_Filtered_merge = LotBin_Filtered[LotBin_Filtered['Temp']=='merge']



LotBin_Filtered_0.to_excel(lot_bin_0, index=False)
LotBin_Filtered_100.to_excel(lot_bin_100, index=False)
LotBin_Filtered_merge.to_excel(lot_bin_merge, index=False)

#==============================Layout =================================================================================
layout = go.Layout(
    autosize =False,
    width=1000,
    height=500,
    title=device+' Lot Level WS Plot',
    #width=500,
    legend=Legend(
        x=1.1,
        y=0.5,
        bgcolor='transparent',
        bordercolor='transparent',
        borderwidth=0,
        font=Font(
            color='',
            family='',
            size=10
        ),
        traceorder='normal',
        xanchor='left',
        yanchor='auto'
    ),
    margin=dict(
        b=50,
        l=30,
        r=5,
        t=50,
        autoexpand=True
    ),

#    legend=dict(x=200,y=1)
    yaxis=dict(
        title='Failing Bins%'
    ),
    yaxis2=dict(
        title='DD n/cm2',
        titlefont=dict(
            color='rgb(148, 103, 189)'
        ),
        tickfont=dict(
            color='rgb(148, 103, 189)'
        ),
        #autorange='reversed',
        overlaying='y',
        side='right'

    )
)


#============================== Test Program Data Plot==================================================================

Lot_Test_0 =LotBin_Filtered_0[['Date','Fab Lot', 'DD','Test Program Extract']]
Lot_Test_0['Freq'] =Lot_Test_0.groupby(['Fab Lot','Test Program Extract'])['Test Program Extract'].transform('count')
testlist0 = list(Lot_Test_0['Test Program Extract'].unique())

testtable_0 = pd.pivot_table(Lot_Test_0,index=["Fab Lot"],values=["Freq"],
               columns=["Test Program Extract"],aggfunc=[np.sum])

testtable_0=DataFrame(testtable_0)
testtable_0 = testtable_0['sum']['Freq']
testtable_0 = testtable_0.reset_index()

Lot_Test_100 =LotBin_Filtered_100[['Date','Fab Lot', 'DD','Test Program Extract']]
Lot_Test_100['Freq'] =Lot_Test_100.groupby(['Fab Lot','Test Program Extract'])['Test Program Extract'].transform('count')
testlist100 = list(Lot_Test_100['Test Program Extract'].unique())

testtable_100 = pd.pivot_table(Lot_Test_100,index=["Fab Lot"],values=["Freq"],
               columns=["Test Program Extract"],aggfunc=[np.sum])

testtable_100=DataFrame(testtable_100)
testtable_100 = testtable_100['sum']['Freq']
testtable_100 = testtable_100.reset_index()

def test_bardata(lst,table):
    data=[]
    for i in lst:
        data1 = go.Bar(
            x=table['Fab Lot'],
            y=table[i],
            name = str(i))
        data.append(data1)
    return data

def test_scatterdata(frame):
    data = [go.Scatter(
            x =frame['Fab Lot'],
            y =frame['DD'],
            name ="DD",
    yaxis='y2'
    )]
    return data

scatter0=test_scatterdata(LotBin_Filtered_0)
scatter100=test_scatterdata(LotBin_Filtered_100)

bar0 =test_bardata(testlist0,testtable_0)
bar100 =test_bardata(testlist100,testtable_100)

combtest0 = scatter0+bar0
combtest100 =scatter100+bar100


figtest0 = go.Figure(data=combtest0,layout=layout)
figtest0['layout'].update(barmode='stack')
figtest0['layout'].update(yaxis=dict(title='Count'))
figtest0['layout'].update(title=device+' Lot Level Test Program Plot: 0C')

figtest100 = go.Figure(data=combtest100,layout=layout)
figtest100['layout'].update(barmode='stack')
figtest100['layout'].update(yaxis=dict(title='Count'))
figtest100['layout'].update(title=device+' Lot Level Test Program Plot: 100C')


from plotly.offline.offline import _plot_html
plot_test_0, plotdivid, width, height = _plot_html(figtest0, False, "", True, '100%', 525,global_requirejs=False) #,global_requirejs=False

plot_test_100, plotdivid, width, height = _plot_html(figtest100, False, "", True, '100%', 525,global_requirejs=False)#,global_requirejs=False


file_test0="<html><head><script src='https://cdn.plot.ly/plotly-latest.min.js'></script></head><body>" + plot_test_0+ "</body></html>"
file_test100="<html><head><script src='https://cdn.plot.ly/plotly-latest.min.js'></script></head><body>" + plot_test_100+ "</body></html>"


html_test0= open(outfolder2 + "/"+"Lot_WS_Rev_0.html","w")
html_test0.write(file_test0)
html_test0.close()


html_test100= open(outfolder2 + "/"+"Lot_WS_Rev_100.html","w")
html_test100.write(file_test100)
html_test100.close()



#===============================Dynamic Plot Bin Count========================================================================

remlist1=[ 'DD', 'Date', 'Ship Volume',
       'Device', 'Fab Lot', 'Family', 'Gross Die', 'Grouping', 'Lot',
       'Mask', 'Mtl Finger Cap', 'Net Die', 'Probe Card',
       'RS_M6_OM/Q/.045', 'Temp', 'Test Location', 'Test Program',
       'Tester', 'Volume', 'Wafer', 'Yield']

def binname():
    binname=[]
    for i in range(100):
        name = "Bin "+ str(i)
        binname.append(name)
    return binname

remlist2=binname()



LotBin_0_Plot=LotBin_Filtered_0[list(set(LotBin_Filtered_0.columns.values)-set(remlist1)-set(remlist2))].mean()
LotBin_100_Plot= LotBin_Filtered_100[list(set(LotBin_Filtered_100.columns.values)-set(remlist1)-set(remlist2))].mean()
LotBin_merge_Plot= LotBin_Filtered_merge[list(set(LotBin_Filtered_merge.columns.values)-set(remlist1)-set(remlist2))].mean()

LotBin_0_Plot=pd.DataFrame(LotBin_0_Plot)
LotBin_100_Plot=pd.DataFrame(LotBin_100_Plot)
LotBin_merge_Plot=pd.DataFrame(LotBin_merge_Plot)

LotBin_0_Plot=LotBin_0_Plot.sort([0],ascending=False)
LotBin_100_Plot=LotBin_100_Plot.sort([0],ascending=False)
LotBin_merge_Plot=LotBin_merge_Plot.sort([0],ascending=False)

LotBin_0_Plot_Top20 = list(LotBin_0_Plot.index[0:15])
LotBin_100_Plot_Top20 = list(LotBin_100_Plot.index[0:15])
LotBin_merge_Plot_Top20 = list(LotBin_merge_Plot.index[0:15])
#plist =plist.rename(columns = {0:'mean'})








# In[24]:


def bardata(lst1,lst2):
    data=[]
    for i in lst1:
        data1 = go.Bar(
            x=lst2['Fab Lot'],
            y=lst2[i],
            name = str(i))
        data.append(data1)
    return data


def scatterdata(lst):
    data = [go.Scatter(
            x =lst['Fab Lot'],
            y =lst['DD'],
            name ="DD",
    yaxis='y2'
    )]
    return data


LotBin_Filtered_0=LotBin_Filtered_0.sort_values(by=['Date','Fab Lot'], ascending=True)
LotBin_Filtered_100=LotBin_Filtered_100.sort_values(by=['Date','Fab Lot'], ascending=True)
LotBin_Filtered_merge=LotBin_Filtered_merge.sort_values(by=['Date','Fab Lot'], ascending=True)

lot0bar= bardata(LotBin_0_Plot_Top20,LotBin_Filtered_0)
lot0scatter = scatterdata(LotBin_Filtered_0)

lot100bar= bardata(LotBin_100_Plot_Top20,LotBin_Filtered_100)
lot100scatter = scatterdata(LotBin_Filtered_100)

lotmergebar= bardata(LotBin_merge_Plot_Top20,LotBin_Filtered_merge)
lotmergescatter = scatterdata(LotBin_Filtered_merge)


lot0=lot0bar+lot0scatter 
lot100=lot100bar+lot100scatter 
lotmerge=lotmergebar+lotmergescatter 


figlot0 = go.Figure(data=lot0,layout=layout)
figlot100 = go.Figure(data=lot100,layout=layout)
figlotmerge = go.Figure(data=lotmerge,layout=layout)




figlot0['layout'].update(barmode='stack')
figlot0['layout'].update(title=device+' Lot Level WS Plot: 0C')
figlot100['layout'].update(barmode='stack')
figlot100['layout'].update(title=device+' Lot Level WS Plot: 100C')
figlotmerge['layout'].update(barmode='stack')
figlotmerge['layout'].update(title=device+' Lot Level WS Plot: Merge')


#py.iplot(figlot0,filename="lot0")
#py.iplot(figlot100,filename="lot100")
#py.iplot(figlotmerge,filename="lotmerge")


from plotly.offline.offline import _plot_html
plot_html_lot0, plotdivid, width, height = _plot_html(figlot0, False, "", True, '100%', 525,global_requirejs=False)
plot_html_lot100, plotdivid, width, height = _plot_html(figlot100, False, "", True, '100%', 525,global_requirejs=False)
plot_html_lotmerge, plotdivid, width, height = _plot_html(figlotmerge, False, "", True, '100%', 525,global_requirejs=False)

file_lot0="<html><head><script src='https://cdn.plot.ly/plotly-latest.min.js'></script></head><body>" + plot_html_lot0+ "</body></html>"
file_lot100="<html><head><script src='https://cdn.plot.ly/plotly-latest.min.js'></script></head><body>" + plot_html_lot100+ "</body></html>"
file_lotmerge="<html><head><script src='https://cdn.plot.ly/plotly-latest.min.js'></script></head><body>" + plot_html_lotmerge+ "</body></html>"


html_lot0= open(outfolder2 + "/"+"Lot_Bin_0.html","w")
html_lot0.write(file_lot0)
html_lot0.close()



html_lot100= open(outfolder2 + "/"+"Lot_Bin_100.html","w")
html_lot100.write(file_lot100)
html_lot100.close()



html_lotmerge= open(outfolder2 + "/"+"Lot_Bin_merge.html","w")
html_lotmerge.write(file_lotmerge)
html_lotmerge.close()



addlist=['Date','DD', 'Fab Lot'] 

# In[ ]:
LotBin_Filtered_0_Plot=LotBin_Filtered_0[addlist+LotBin_0_Plot_Top20]
LotBin_Filtered_100_Plot= LotBin_Filtered_100[addlist+LotBin_100_Plot_Top20]
LotBin_Filtered_merge_Plot= LotBin_Filtered_merge[addlist+LotBin_merge_Plot_Top20]

LotBin_Filtered_0_Plot=LotBin_Filtered_0_Plot.sort_values(by=['Date'], ascending=True)
LotBin_Filtered_100_Plot=LotBin_Filtered_100_Plot.sort_values(by=['Date'], ascending=True)
LotBin_Filtered_merge_Plot=LotBin_Filtered_merge_Plot.sort_values(by=['Date'], ascending=True)

LotBin_Filtered_0_Plot.to_excel(lot_bin_0_plot, index=False)
LotBin_Filtered_100_Plot.to_excel(lot_bin_100_plot, index=False)
LotBin_Filtered_merge_Plot.to_excel(lot_bin_merge_plot, index=False)

# In[ ]:
#======================Lot Progressive ===================================================================

lot_progress_file = getfilename("Lot_Sort_WsProgressive",filelist)
lot_progress_file_path = createpath(family,device,lot_progress_file)

if checkfilesize(lot_progress_file_path) =="False":
    print("No Data "+lot_progress_file_path)
    sys.exit("No Data "+lot_progress_file_path)

LotProgressive=pd.read_csv(lot_progress_file_path)


LotProgressive['Temp']=LotProgressive['Temp'].astype('str')
LotProgressive['Date'] = pd.to_datetime(LotProgressive['Date'])
LotProgressive["Test Program Extract"]=LotProgressive["Test Program"].apply(lambda row:find_testprogram(row,"_","_0c","_100c"))



LotProgressive_Filtered=LotProgressive[~LotProgressive['Fab Lot'].str.contains("_")]

LotProgressive_Filtered_0=LotProgressive_Filtered[LotProgressive_Filtered['Temp']=='0']
LotProgressive_Filtered_100=LotProgressive_Filtered[LotProgressive_Filtered['Temp']=='100']
#LotProgressive_Filtered_merge=LotProgressive_Filtered[LotProgressive_Filtered['Temp']=='merge']

LotProgressive_Filtered_0.to_excel(lot_progressive_0, index=False)
LotProgressive_Filtered_100.to_excel(lot_progressive_100, index=False)


LotPro_0_Plot=LotProgressive_Filtered_0[list(set(LotProgressive_Filtered_0.columns.values)-set(remlist1)-set(remlist2))].mean()
LotPro_100_Plot= LotProgressive_Filtered_100[list(set(LotProgressive_Filtered_100.columns.values)-set(remlist1)-set(remlist2))].mean()


LotPro_0_Plot=pd.DataFrame(LotPro_0_Plot)
LotPro_100_Plot=pd.DataFrame(LotPro_100_Plot)

LotPro_0_Plot=LotPro_0_Plot.sort([0],ascending=False)
LotPro_100_Plot=LotPro_100_Plot.sort([0],ascending=False)

LotPro_0_Plot_Top20 = list(LotPro_0_Plot.index[0:15])
LotPro_100_Plot_Top20 = list(LotPro_100_Plot.index[0:15])

LotProgressive_Filtered_0=LotProgressive_Filtered_0.sort_values(by=['Date','Fab Lot'], ascending=True)
LotProgressive_Filtered_100=LotProgressive_Filtered_100.sort_values(by=['Date','Fab Lot'], ascending=True)


lotpro0bar=bardata(LotPro_0_Plot_Top20, LotProgressive_Filtered_0)
lotpro0scatter =scatterdata(LotProgressive_Filtered_0)


lotpro100bar=bardata(LotPro_100_Plot_Top20, LotProgressive_Filtered_100)
lotpro100scatter =scatterdata(LotProgressive_Filtered_100)



lotpro0=lotpro0bar+lotpro0scatter
lotpro100=lotpro100bar+lotpro100scatter

figlotpro0=go.Figure(data=lotpro0,layout=layout)
figlotpro100=go.Figure(data=lotpro100,layout=layout)


figlotpro0['layout'].update(barmode='stack')
figlotpro0['layout'].update(title=device+' Lot Level Progressive Plot: 0C')
figlotpro100['layout'].update(barmode='stack')
figlotpro100['layout'].update(title=device+' Lot Level Progressive Plot: 100C')



plot_html_lotpro0, plotdivid, width, height = _plot_html(figlotpro0, False, "", True, '100%', 525,global_requirejs=False)
plot_html_lotpro100, plotdivid, width, height = _plot_html(figlotpro100, False, "", True, '100%', 525,global_requirejs=False)

file_lotpro0="<html><head><script src='https://cdn.plot.ly/plotly-latest.min.js'></script></head><body>" + plot_html_lotpro0+ "</body></html>"
file_lotpro100="<html><head><script src='https://cdn.plot.ly/plotly-latest.min.js'></script></head><body>" + plot_html_lotpro100+ "</body></html>"

html_lotpro0= open(outfolder2 + "/"+"Lot_Progressive_0.html","w")
html_lotpro0.write(file_lotpro0)
html_lotpro0.close()


html_lotpro100= open(outfolder2 + "/"+"Lot_Progressive_100.html","w")
html_lotpro100.write(file_lotpro100)
html_lotpro100.close()

LotBin_Progressive_0_Plot=LotProgressive_Filtered_0[addlist+LotPro_0_Plot_Top20]
LotBin_Progressive_100_Plot= LotProgressive_Filtered_100[addlist+LotPro_0_Plot_Top20]

LotBin_Progressive_0_Plot=LotBin_Progressive_0_Plot.sort_values(by=['Date'], ascending=True)
LotBin_Progressive_100_Plot=LotBin_Progressive_100_Plot.sort_values(by=['Date'], ascending=True)

LotBin_Progressive_0_Plot.to_excel(lot_progressive_0_plot, index=False)
LotBin_Progressive_100_Plot.to_excel(lot_progressive_100_plot, index=False)






print(device+" Bin Lot Done")





