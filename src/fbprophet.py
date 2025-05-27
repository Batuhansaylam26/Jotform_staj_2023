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

class fbprophet:
    def __init__(self,train,test):
        self.data_train=train
        self.data_test=test
        params_grid_prophet = {
            'changepoint_prior_scale': [0.001, 0.01, 0.1],
            'seasonality_mode':['additive', 'multiplicative'],
            'weekly_seasonality':(True,False)
            }
        grid_prophet= [dict(zip(params_grid_prophet.keys(), v)) for v in itertools.product(*params_grid_prophet.values())]
        for p in grid_prophet:
            model = Prophet(daily_seasonality=False,**p)
            model=model.fit(self.data_train)
            forecast = model.predict(self.data_test)
            mape1=mean_absolute_percentage_error(self.data_test["y"], forecast["yhat"])
        return mape1,p