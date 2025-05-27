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
from sklearn.model_selection import TimeSeriesSplit
from  neuralprophet import set_random_seed



class NP:
    def __init__(self,train,test):
        self.data_train=train
        self.data_test=test
        params_grid_neuralprophet = {
            "learning_rate":[0.01,0.1,1],
            'seasonality_mode':('multiplicative','additive'),
            'batch_size':[8,16,32],
            'weekly_seasonality':(True,False)}
        grid_neuralprophet= [dict(zip(params_grid_neuralprophet.keys(), v)) for v in itertools.product(*params_grid_neuralprophet.values())]
        for p in grid_neuralprophet:
            print(i,j,p)
            set_random_seed(0)
            m = NeuralProphet(trainer_config={"accelerator":"gpu"},daily_seasonality=False,epochs=1000,**p)
            m.add_country_holidays(country_name='US')
            df_model=m.fit(self.data_train, freq="D",early_stopping=True,checkpointing=True)
            p["epoch" ]=df_model.iloc[-1,4]
            forecast = m.predict(self.data_test)
            mape1=mean_absolute_percentage_error(forecast["y"], forecast["yhat1"])
            return mape1,p