import pandas as pd 
import numpy as np


import pandasql as psql
#machine learning and statistical methods

#selected preprocessing and evaluation methods

from statsmodels.tsa.seasonal import seasonal_decompose

from plotly.subplots import make_subplots
import plotly.graph_objects as go


class decompose:
    def __init__(self):
        self.formtemplatesclones0=pd.read_csv("/home/batuhansaylam/Desktop/Jotform_staj_2023/data/formTemplatesClones.csv",parse_dates=["date"])
        self.formtemplatescategories0=pd.read_csv("/home/batuhansaylam/Desktop/Jotform_staj_2023/data/formTemplatesCategories.csv")
        self.formtemplates0=pd.read_excel("/home/batuhansaylam/Desktop/Jotform_staj_2023/data/formTemplates_1_.xlsx")
    def sd(self,yaxis):
        self.formtemplatesclones=self.formtemplatesclones0.copy()
        self.formtemplatescategories=self.formtemplatescategories0.copy()
        self.formtemplates=self.formtemplates0.copy()
        self.yaxis=yaxis                    
        self.formtemplatescategoriesy=self.formtemplatescategories[self.formtemplatescategories["metaKeywords"]==self.yaxis].copy()   
        self.formtemplatesclones=self.formtemplatesclones.rename({"templateID":"_id"},axis=1)
        formandclone=pd.merge(self.formtemplates,self.formtemplatesclones,how="inner",on="_id")
        self.formtemplates1=self.formtemplates.copy()
        self.formtemplates1=self.formtemplates1.rename({"_id":"id"},axis=1)
        self.formtemplates1=self.formtemplates1.rename({"_featuredCategory":"_id"},axis=1)
        df1_melt = self.formtemplates1.assign(_categories=self.formtemplates1._categories.str.split(","))
        self.formtemplates1=df1_melt._categories.apply(pd.Series) \
            .merge(self.formtemplates1, right_index=True, left_index=True) \
            .drop(["_categories"], axis=1) \
            .melt(id_vars=['id',"_title","_slug","_description","_id","_language"], value_name="_categories") \
            .drop("variable", axis=1) 
        self.formtemplates2=pd.merge(self.formtemplatescategoriesy,self.formtemplates1,how="inner",on="_id")
        self.formtemplates2=self.formtemplates2.rename({"_id":"_featuredCategory"},axis=1)
        self.formtemplates1=self.formtemplates1.rename({"_id":"_featuredCategory"},axis=1)
        self.formtemplates1=self.formtemplates1.rename({"_categories":"_id"},axis=1)
        self.formtemplates3=pd.merge(self.formtemplatescategoriesy,self.formtemplates1,how="inner",on="_id")
        self.formtemplates3=self.formtemplates3.rename({"_id":"_categories"},axis=1)
        self.formtemplates1=self.formtemplates1.rename({"_id":"_categories"},axis=1)
        self.formtemplates1=self.formtemplates1.rename({"id":"_id"},axis=1)
        self.formtemplatesclones=self.formtemplatesclones.rename({"_id":"templateID"},axis=1)
        self.formtemplates2=self.formtemplates2.drop_duplicates()
        self.formtemplates3=self.formtemplates3.drop_duplicates()
        formcat=pd.concat([self.formtemplates2,self.formtemplates3]).drop_duplicates()
        formcat=formcat.rename({"id":"_id"},axis=1)
        formcat=formcat.loc[:,[
            'name',
            'description',
            'metaKeywords',
            '_categories',
            '_featuredCategory',
            '_id']]
        formandclone=formandclone.loc[:,[
        '_id',
            '_title',
            '_slug',
            '_description',
            '_language',
            'formID',
            'form_type',
            'source',
            'date']]

        formclonecategnonnany=pd.merge(formandclone,formcat,on="_id")
        formclonecategnonnany=formclonecategnonnany.drop_duplicates(keep='first')
        formclonecategnonnany.index=formclonecategnonnany.date
        formclonecategnonnany.index=formclonecategnonnany.index.to_period("D")
        formclonecategnonnany=formclonecategnonnany.rename({"date":"date2"},axis=1)
        formclonecategnonnany.index=formclonecategnonnany.index.to_timestamp()
        df=formclonecategnonnany.loc[:,["date2","_id"]]
        df=df.resample('7D',on="date2").count()
        df=df.iloc[:len(df)-1,]
        df=df.rename({"_id":"y"},axis=1)
        df["ds"]=df.index
        decomposeresult2=seasonal_decompose(df["y"],period=52,model="add",extrapolate_trend="freq",two_sided=True)
        self.season = pd.DataFrame({"obs":decomposeresult2.observed,"trend":decomposeresult2.trend,"seasonal":decomposeresult2.seasonal,"resid":decomposeresult2.resid})
        self.season.index=pd.to_datetime(self.season.index,format="%d-%m-%Y")
        self.season=self.season.fillna(0)
        self.season=self.season.sort_index()
        self.season.index=self.season.index.to_period("D")
        self.season.index=self.season.index.to_timestamp()
        self.season.index=self.season.index.strftime('%d-%m-%Y')
        self.season.index=pd.to_datetime(self.season.index,format='%d-%m-%Y')
        fig=make_subplots(rows=4, cols=1,
                        subplot_titles=(self.yaxis, "Trend", "self.seasonal_yearly","resid"))
        fig.add_trace(
            go.Scatter(x=self.season.index,y=self.season.obs),row=1,col=1
            
        )
        fig.add_trace(
            go.Scatter(x=self.season.index,y=self.season.trend),row=2,col=1
        )
        fig.add_trace(
            go.Scatter(x=self.season.index,y=self.season.seasonal),row=3,col=1
            
        )
        fig.add_trace(
            go.Scatter(x=self.season.index,y=self.season.resid),row=4,col=1
            
        )


        fig.update_layout(height=1000, width=950)
        return fig


