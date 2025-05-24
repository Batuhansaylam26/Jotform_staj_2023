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



class seasonaldecompose:
    def __init__(self,data):
        self.data=data
        decomposeresult2=seasonal_decompose(self.data["y"],period=365,model="add")
        season = pd.DataFrame({"obs":decomposeresult2.observed,"trend":decomposeresult2.trend,"seasonal":decomposeresult2.seasonal})
        season.index=pd.to_datetime(season.index)
        season=season.fillna(0)
        season["diff"]=season["obs"].sub(season["trend"],axis=0)
        mape1=mean_absolute_percentage_error(self.data["y"], (season.seasonal+season.trend))
        return mape1