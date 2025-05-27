from sklearn.model_selection import ParameterGrid
import pandas as pd 
from sqlite3 import connect
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from warnings import simplefilter
from scipy.signal import detrend
import matplotlib as mpl
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf
sns.set()
import pandasql as psql
import statsmodels.api as sm
import math
import datetime
from datetime import datetime
from sklearn.preprocessing import StandardScaler
from statsmodels.tsa.stattools import kpss
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from plotly.subplots import make_subplots
from statsmodels.tsa.seasonal import DecomposeResult
import plotly.graph_objects as go
from statsmodels.tsa.holtwinters import SimpleExpSmoothing, ExponentialSmoothing
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.metrics import mean_absolute_percentage_error
from prophet import Prophet
from neuralprophet import NeuralProphet
import itertools 



class model_trainer:
    
    def __init__(self,data):
        self.data=data
    def train(self):
        smoothing=["rolling","rolling-gaussian","resample","exponential3"]
        method=["classical","prophet","NeuralProphet"]
        self.model_parameters = pd.DataFrame(columns = ['Smoothing','Method','MAPE','Parameters'])
        df=self.data.copy()
        params_grid_prophet = {
            'changepoint_prior_scale': [0.001, 0.01, 0.1],
            'seasonality_mode':['additive', 'multiplicative'],
            'weekly_seasonality':(True,False)
            }
        grid_prophet= [dict(zip(params_grid_prophet.keys(), v)) for v in itertools.product(*params_grid_prophet.values())]
        params_grid_neuralprophet = {
            "epochs":[100,500,1000],
            "learning_rate":[0.01,0.1,1],
            'seasonality_mode':('multiplicative','additive'),
            'batch_size':[8,16,32],
            'weekly_seasonality':(True,False)}
        grid_neuralprophet= [dict(zip(params_grid_neuralprophet.keys(), v)) for v in itertools.product(*params_grid_neuralprophet.values())]
        for i in smoothing:
            df2=df.copy()
            df2.index=df2["ds"]
            df2.index=pd.to_datetime(df2.index)
            for j in method:
                if i=="rolling":
                    df2["y"]=df2["y"].rolling(window=7).mean()
                    df2=df2.dropna()
                    if j=="classical":
                        decomposeresult2=seasonal_decompose(df2["y"],period=365,model="add")
                        season = pd.DataFrame({"obs":decomposeresult2.observed,"trend":decomposeresult2.trend,"seasonal":decomposeresult2.seasonal})
                        season.index=pd.to_datetime(season.index)
                        season=season.fillna(0)
                        season["diff"]=season["obs"].sub(season["trend"],axis=0)
                        mape1=mean_absolute_percentage_error(df2["y"], (season.seasonal+season.trend))
                        self.model_parameters = self.model_parameters.append({'Smoothing':i,'Method':j,'MAPE':mape1,'Parameters':"No parameter"},ignore_index=True)
                    if j=="prophet":
                        for p in grid_prophet:
                            print(i,j,p)
                            model = Prophet(daily_seasonality=False,**p)
                            model=model.fit(df2)
                            forecast = model.predict(df2)
                            mape1=mean_absolute_percentage_error(df2["y"], forecast["yhat"])
                            self.model_parameters = self.model_parameters.append({'Smoothing':i,'Method':j,'MAPE':mape1,'Parameters':p},ignore_index=True)
                    if j=="NeuralProphet":
                        for p in grid_neuralprophet:
                            print(i,j,p)
                            m = NeuralProphet(trainer_config={"accelerator":"gpu"},daily_seasonality=False,**p)
                            m.add_country_holidays(country_name='US')
                            m.fit(df2, freq="D")
                            forecast = m.predict(df2)
                            mape1=mean_absolute_percentage_error(forecast["y"], forecast["yhat1"])
                            self.model_parameters = self.model_parameters.append({'Smoothing':i,'Method':j,'MAPE':mape1,'Parameters':p},ignore_index=True)
                if i=="rolling-gaussian":
                    df2["y"]=df2["y"].rolling(window=7,win_type="gaussian").mean(std=10)
                    df2=df2.dropna()
                    if j=="classical":
                        decomposeresult2=seasonal_decompose(df2["y"],period=365,model="add")
                        season = pd.DataFrame({"obs":decomposeresult2.observed,"trend":decomposeresult2.trend,"seasonal":decomposeresult2.seasonal})
                        season.index=pd.to_datetime(season.index,format="%d-%m-%Y")
                        season=season.fillna(0)
                        season["diff"]=season["obs"].sub(season["trend"],axis=0)
                        mape1=mean_absolute_percentage_error(df2["y"], (season.seasonal+season.trend))
                        self.model_parameters = self.model_parameters.append({'Smoothing':i,'Method':j,'MAPE':mape1,'Parameters':"No parameter"},ignore_index=True)
                    if j=="prophet":
                        for p in grid_prophet:
                            print(i,j,p)
                            model = Prophet(daily_seasonality=False,**p)
                            model=model.fit(df2)
                            forecast = model.predict(df2)
                            mape1=mean_absolute_percentage_error(df2["y"], forecast["yhat"])
                            self.model_parameters = self.model_parameters.append({'Smoothing':i,'Method':j,'MAPE':mape1,'Parameters':p},ignore_index=True)
                    if j=="NeuralProphet":
                        for p in grid_neuralprophet:
                            print(i,j,p)
                            m = NeuralProphet(trainer_config={"accelerator":"gpu"},daily_seasonality=False,**p)
                            m.add_country_holidays(country_name='US')
                            m.fit(df2, freq="D")
                            forecast = m.predict(df2)
                            mape1=mean_absolute_percentage_error(forecast["y"], forecast["yhat1"])
                            self.model_parameters = self.model_parameters.append({'Smoothing':i,'Method':j,'MAPE':mape1,'Parameters':p},ignore_index=True)
                if i=="resample":
                    df2=df2.resample("W").mean()
                    df2=df2.dropna()
                    df2["ds"]=df2.index.tolist()
                    if j=="classical":
                        decomposeresult2=seasonal_decompose(df2["y"],period=52,model="add")
                        season = pd.DataFrame({"obs":decomposeresult2.observed,"trend":decomposeresult2.trend,"seasonal":decomposeresult2.seasonal})
                        season.index=pd.to_datetime(season.index,format="%d-%m-%Y")
                        season=season.fillna(0)
                        season["diff"]=season["obs"].sub(season["trend"],axis=0)
                        mape1=mean_absolute_percentage_error(df2["y"], (season.seasonal+season.trend))
                        self.model_parameters = self.model_parameters.append({'Smoothing':i,'Method':j,'MAPE':mape1,'Parameters':"No parameter"},ignore_index=True)
                    if j=="prophet":
                        for p in grid_prophet:
                            print(i,j,p)
                            model = Prophet(daily_seasonality=False,**p)
                            model=model.fit(df2)
                            forecast = model.predict(df2)
                            mape1=mean_absolute_percentage_error(df2["y"], forecast["yhat"])
                            self.model_parameters = self.model_parameters.append({'Smoothing':i,'Method':j,'MAPE':mape1,'Parameters':p},ignore_index=True)
                    if j=="NeuralProphet":
                        for p in grid_neuralprophet:
                            print(i,j,p)
                            m = NeuralProphet(trainer_config={"accelerator":"gpu"},daily_seasonality=False,**p)
                            m.add_country_holidays(country_name='US')
                            m.fit(df2, freq="D")
                            forecast = m.predict(df2)
                            mape1=mean_absolute_percentage_error(forecast["y"], forecast["yhat1"])
                            self.model_parameters = self.model_parameters.append({'Smoothing':i,'Method':j,'MAPE':mape1,'Parameters':p},ignore_index=True)  
                if i=="exponential3":
                    es_simple = ExponentialSmoothing(df2["y"], trend= 'add', damped= True, seasonal= 'add', seasonal_periods= 365).fit()
                    df2["y"]=es_simple.fittedvalues
                    if j=="classical":
                        decomposeresult2=seasonal_decompose(df2["y"],period=365,model="add")
                        season = pd.DataFrame({"obs":decomposeresult2.observed,"trend":decomposeresult2.trend,"seasonal":decomposeresult2.seasonal})
                        season.index=pd.to_datetime(season.index,format="%d-%m-%Y")
                        season=season.fillna(0)
                        season["diff"]=season["obs"].sub(season["trend"],axis=0)
                        mape1=mean_absolute_percentage_error(df2["y"], (season.seasonal+season.trend))
                        self.model_parameters = self.model_parameters.append({'Smoothing':i,'Method':j,'MAPE':mape1,'Parameters':"No parameter"},ignore_index=True)
                    if j=="prophet":
                        for p in grid_prophet:
                            print(i,j,p)
                            model = Prophet(daily_seasonality=False,**p)
                            model=model.fit(df2)
                            forecast = model.predict(df2)
                            mape1=mean_absolute_percentage_error(df2["y"], forecast["yhat"])
                            self.model_parameters = self.model_parameters.append({'Smoothing':i,'Method':j,'MAPE':mape1,'Parameters':p},ignore_index=True)
                    if j=="NeuralProphet":
                        for p in grid_neuralprophet:
                            print(i,j,p)
                            m = NeuralProphet(trainer_config={"accelerator":"gpu"},daily_seasonality=False,**p)
                            m.add_country_holidays(country_name='US')
                            m.fit(df2, freq="D")
                            forecast = m.predict(df2)
                            mape1=mean_absolute_percentage_error(forecast["y"], forecast["yhat1"])
                            self.model_parameters = self.model_parameters.append({'Smoothing':i,'Method':j,'MAPE':mape1,'Parameters':p},ignore_index=True)

        minmape=pd.DataFrame(self.model_parameters.loc[self.model_parameters["mape"].argmin()])
        self.minmape=minmape.T
    def picking(self,filename):
        with open(filename, 'wb') as file:  
            pickle.dump(self.model_parameters, file)
    