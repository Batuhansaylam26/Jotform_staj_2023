import pandas as pd 
import numpy as np


import pandasql as psql
#machine learning and statistical methods

#selected preprocessing and evaluation methods

from plotly.subplots import make_subplots
from statsmodels.tsa.seasonal import DecomposeResult
import plotly.graph_objects as go
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.metrics import mean_absolute_percentage_error
from prophet import Prophet
import torch 
from sklearn.model_selection import TimeSeriesSplit
from dash import Dash,dcc, html, Input, Output, callback



app = Dash(__name__)
formtemplatescategories=pd.read_csv("/home/batuhansaylam/Desktop/Jotform_staj_2023/data/formTemplatesCategories.csv")
app.layout=html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                formtemplatescategories.metaKeywords.unique().tolist(),
                'Pharmacy Forms',
                id="y",
                multi=True,
                searchable=True
        )
        ],style={"width":"33%",'display':'inline-block'}),
        html.Div([
            dcc.Dropdown(
                ["Covid","Noncovid"],
                'Noncovid',
                id="cov"
        )
        ],style={"width":"33%","float":"right",'display':'inline-block'})
    ]),
    html.Div(
        [
        html.Div(
            
            [dcc.Graph(id="plotindic1")],style={"width":"50%",'display':'inline-block'}
            
        ),
        html.Div(
            [dcc.Graph(id="plotindic2")],style={"width":"50%","float":"right",'display':'inline-block'}

        )
        ]),
    html.Div(
        [
        html.Div(
            
            [dcc.Graph(id="plotindic3")],style={"width":"50%",'display':'inline-block'}
            
        ),
        html.Div(
            [dcc.Graph(id="plotindic4")],style={"width":"50%","float":"right",'display':'inline-block'}

        )
        ]),
    html.Div(
        [
        html.Div(
            
            [dcc.Graph(id="plotindic5")],style={"width":"50%",'display':'inline-block'}
            
        ),
        html.Div(
            [dcc.Graph(id="plotindic6")],style={"width":"50%","float":"right",'display':'inline-block'}

        )
        ]),
    html.Div(
        [
        html.Div(
            
            [dcc.Graph(id="plotindic7")],style={"width":"50%",'display':'inline-block'}
            
        ),
        html.Div(
            [dcc.Graph(id="plotindic8")],style={"width":"50%","float":"right",'display':'inline-block'}

        )
        ]),
    html.Div(
        [
        html.Div(
            
            [dcc.Graph(id="plotindic9")],style={"width":"50%",'display':'inline-block'}
            
        ),
        html.Div(
            [dcc.Graph(id="plotindic10")],style={"width":"50%","float":"right",'display':'inline-block'}

        )
        ]),
        ]
    )
@callback(
    Output("plotindic1","figure"),
    Input("y","value"),
    Input("cov","value")
)
def update_graph(yaxis,cov):
    formtemplatesclones=pd.read_csv("/home/batuhan-saylam/Desktop/JotformProject/formTemplatesClones.csv",parse_dates=["date"])
    formtemplatescategories=pd.read_csv("/home/batuhan-saylam/Desktop/JotformProject/formTemplatesCategories.csv")
    formtemplates=pd.read_excel("/home/batuhan-saylam/Desktop/JotformProject/formTemplates_1_.xlsx")
    formtemplatescategoriesy=formtemplatescategories[formtemplatescategories["metaKeywords"]==yaxis[0]].copy()
    formtemplatesclones=formtemplatesclones.rename({"templateID":"_id"},axis=1)
    formandclone=pd.merge(formtemplates,formtemplatesclones,how="inner",on="_id")
    formtemplates=formtemplates.rename({"_id":"id"},axis=1)
    formtemplates=formtemplates.rename({"_featuredCategory":"_id"},axis=1)
    formtemplates2=pd.merge(formtemplatescategoriesy,formtemplates,how="inner",on="_id")
    formtemplates2=formtemplates2.rename({"_id":"_featuredCategory"},axis=1)
    formtemplates=formtemplates.rename({"_id":"_featuredCategory"},axis=1)
    df_melt = formtemplates.assign(_categories=formtemplates._categories.str.split(","))
    formtemplates=df_melt._categories.apply(pd.Series) \
        .merge(formtemplates, right_index=True, left_index=True) \
        .drop(["_categories"], axis=1) \
        .melt(id_vars=['id',"_title","_slug","_description","_featuredCategory","_language"], value_name="_categories") \
        .drop("variable", axis=1) 
    formtemplates=formtemplates.rename({"_categories":"_id"},axis=1)
    formtemplates3=pd.merge(formtemplatescategoriesy,formtemplates,how="inner",on="_id")
    formtemplates3=formtemplates3.rename({"_id":"_categories"},axis=1)
    formtemplates=formtemplates.rename({"_id":"_categories"},axis=1)
    formtemplates=formtemplates.rename({"id":"_id"},axis=1)
    formtemplatesclones=formtemplatesclones.rename({"_id":"templateID"},axis=1)
    formcat=pd.concat([formtemplates2,formtemplates3])
    formcat=formcat.rename({"id":"_id"},axis=1)
    formcat=formcat.loc[:,[
     'name',
     'description',
     'metaKeywords',
     '_categories',
     '_id']]
    formandclone=formandclone.loc[:,[
    '_id',
     '_title',
     '_slug',
     '_description',
     '_language',
     '_featuredCategory',
     'formID',
     'form_type',
     'source',
     'date']]
    formclonecategnonnany=pd.merge(formandclone,formcat,on="_id")
    formclonecategnonnany=formclonecategnonnany.drop_duplicates(keep='first')
    formclonecategnonnany.index=formclonecategnonnany.date
    formclonecategnonnany.index=formclonecategnonnany.index.to_period("D")
    formclonecategnonnany=formclonecategnonnany.rename({"date":"date2"},axis=1)
    formclonecategnonnany["day"]=formclonecategnonnany.index.dayofweek
    formclonecategnonnany["week"]=formclonecategnonnany.index.week
    formclonecategnonnany["dayofyear"]=formclonecategnonnany.index.dayofyear
    formclonecategnonnany["year"]=formclonecategnonnany.index.year
    formclonecategnonnany["quarter"]=formclonecategnonnany.index.quarter
    formclonecategnonnany["month"]=formclonecategnonnany.index.month
    formclonecategnonnany.index=formclonecategnonnany.index.to_timestamp()
    df=psql.sqldf("select count(_id),date,year,dayofyear,week,day,quarter,month from formclonecategnonnany  group by date")
    df.index=df.date.tolist()
    df.index=pd.to_datetime(df.index)
    df.index=df.index.to_period("D")
    df.index=df.index.to_timestamp()
    df.index=df.index.strftime('%d-%m-%Y')
    df["date"]=pd.to_datetime(df["date"])
    df=df.rename({"count(_id)":"y"},axis=1)
    df=df.rename({"date":"ds"},axis=1)
    df=df.loc[:,["y","ds"]]
    if cov=="Noncovid":
          df2=df.copy()
    elif cov=="Covid":
          df2=df.loc["01-07-2021":,]
    df3=df2.copy()
    df2=df2.resample('7D',on="ds").sum()
    decomposeresult2=seasonal_decompose(df2["y"],period=52,model="add",extrapolate_trend="freq",two_sided=True)
    season = pd.DataFrame({"obs":decomposeresult2.observed,"trend":decomposeresult2.trend,"seasonal":decomposeresult2.seasonal,"resid":decomposeresult2.resid})
    season.index=pd.to_datetime(season.index,format="%d-%m-%Y")
    season=season.fillna(0)
    season=season.sort_index()
    season.index=season.index.to_period("D")
    season.index=season.index.to_timestamp()
    season.index=season.index.strftime('%d-%m-%Y')
    season.index=pd.to_datetime(season.index,format='%d-%m-%Y')
    fig=make_subplots(rows=4, cols=1,
                      subplot_titles=(yaxis, "Trend", "Seasonal_yearly","resid"))
    fig.add_trace(
        go.Scatter(x=season.index,y=season.obs),row=1,col=1
        
    )
    fig.add_trace(
        go.Scatter(x=season.index,y=season.trend),row=2,col=1
    )
    fig.add_trace(
        go.Scatter(x=season.index,y=season.seasonal),row=3,col=1
        
    )
    fig.add_trace(
        go.Scatter(x=season.index,y=season.resid),row=4,col=1
        
    )


    fig.update_layout(height=1000, width=950)
    return fig

@callback(
    Output("plotindic2","figure"),
    Input("y","value"),
    Input("cov","value")
)
def update_graph(yaxis,cov):
    formtemplatesclones=pd.read_csv("/home/batuhan-saylam/Desktop/JotformProject/formTemplatesClones.csv",parse_dates=["date"])
    formtemplatescategories=pd.read_csv("/home/batuhan-saylam/Desktop/JotformProject/formTemplatesCategories.csv")
    formtemplates=pd.read_excel("/home/batuhan-saylam/Desktop/JotformProject/formTemplates_1_.xlsx")
    formtemplatescategoriesy=formtemplatescategories[formtemplatescategories["metaKeywords"]==yaxis[1]].copy()
    formtemplatesclones=formtemplatesclones.rename({"templateID":"_id"},axis=1)
    formandclone=pd.merge(formtemplates,formtemplatesclones,how="inner",on="_id")
    formtemplates=formtemplates.rename({"_id":"id"},axis=1)
    formtemplates=formtemplates.rename({"_featuredCategory":"_id"},axis=1)
    formtemplates2=pd.merge(formtemplatescategoriesy,formtemplates,how="inner",on="_id")
    formtemplates2=formtemplates2.rename({"_id":"_featuredCategory"},axis=1)
    formtemplates=formtemplates.rename({"_id":"_featuredCategory"},axis=1)
    df_melt = formtemplates.assign(_categories=formtemplates._categories.str.split(","))
    formtemplates=df_melt._categories.apply(pd.Series) \
        .merge(formtemplates, right_index=True, left_index=True) \
        .drop(["_categories"], axis=1) \
        .melt(id_vars=['id',"_title","_slug","_description","_featuredCategory","_language"], value_name="_categories") \
        .drop("variable", axis=1) 
    formtemplates=formtemplates.rename({"_categories":"_id"},axis=1)
    formtemplates3=pd.merge(formtemplatescategoriesy,formtemplates,how="inner",on="_id")
    formtemplates3=formtemplates3.rename({"_id":"_categories"},axis=1)
    formtemplates=formtemplates.rename({"_id":"_categories"},axis=1)
    formtemplates=formtemplates.rename({"id":"_id"},axis=1)
    formtemplatesclones=formtemplatesclones.rename({"_id":"templateID"},axis=1)
    formcat=pd.concat([formtemplates2,formtemplates3])
    formcat=formcat.rename({"id":"_id"},axis=1)
    formcat=formcat.loc[:,[
     'name',
     'description',
     'metaKeywords',
     '_categories',
     '_id']]
    formandclone=formandclone.loc[:,[
    '_id',
     '_title',
     '_slug',
     '_description',
     '_language',
     '_featuredCategory',
     'formID',
     'form_type',
     'source',
     'date']]
    formclonecategnonnany=pd.merge(formandclone,formcat,on="_id")
    formclonecategnonnany=formclonecategnonnany.drop_duplicates(keep='first')
    formclonecategnonnany.index=formclonecategnonnany.date
    formclonecategnonnany.index=formclonecategnonnany.index.to_period("D")
    formclonecategnonnany=formclonecategnonnany.rename({"date":"date2"},axis=1)
    formclonecategnonnany["day"]=formclonecategnonnany.index.dayofweek
    formclonecategnonnany["week"]=formclonecategnonnany.index.week
    formclonecategnonnany["dayofyear"]=formclonecategnonnany.index.dayofyear
    formclonecategnonnany["year"]=formclonecategnonnany.index.year
    formclonecategnonnany["quarter"]=formclonecategnonnany.index.quarter
    formclonecategnonnany["month"]=formclonecategnonnany.index.month
    formclonecategnonnany.index=formclonecategnonnany.index.to_timestamp()
    df=psql.sqldf("select count(_id),date,year,dayofyear,week,day,quarter,month from formclonecategnonnany  group by date")
    df.index=df.date.tolist()
    df.index=pd.to_datetime(df.index)
    df.index=df.index.to_period("D")
    df.index=df.index.to_timestamp()
    df.index=df.index.strftime('%d-%m-%Y')
    df["date"]=pd.to_datetime(df["date"])
    df=df.rename({"count(_id)":"y"},axis=1)
    df=df.rename({"date":"ds"},axis=1)
    df=df.loc[:,["y","ds"]]
    if cov=="Noncovid":
          df2=df.copy()
    elif cov=="Covid":
          df2=df.loc["01-07-2021":,]
    df3=df2.copy()
    df2=df2.resample('7D',on="ds").sum()
    decomposeresult2=seasonal_decompose(df2["y"],period=52,model="add",extrapolate_trend="freq",two_sided=True)
    season = pd.DataFrame({"obs":decomposeresult2.observed,"trend":decomposeresult2.trend,"seasonal":decomposeresult2.seasonal,"resid":decomposeresult2.resid})
    season.index=pd.to_datetime(season.index,format="%d-%m-%Y")
    season=season.fillna(0)
    season=season.sort_index()
    season.index=season.index.to_period("D")
    season.index=season.index.to_timestamp()
    season.index=season.index.strftime('%d-%m-%Y')
    season.index=pd.to_datetime(season.index,format='%d-%m-%Y')
    fig=make_subplots(rows=4, cols=1,
                      subplot_titles=(yaxis, "Trend", "Seasonal_yearly","resid"))
    fig.add_trace(
        go.Scatter(x=season.index,y=season.obs),row=1,col=1
        
    )
    fig.add_trace(
        go.Scatter(x=season.index,y=season.trend),row=2,col=1
    )
    fig.add_trace(
        go.Scatter(x=season.index,y=season.seasonal),row=3,col=1
        
    )
    fig.add_trace(
        go.Scatter(x=season.index,y=season.resid),row=4,col=1
        
    )


    fig.update_layout(height=1000, width=950)
    return fig
if __name__ == '__main__':
	app.run(host='127.0.0.1', port='8050',debug=True)
    
