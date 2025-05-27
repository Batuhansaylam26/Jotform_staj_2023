import pandas as pd 
import numpy as np
from sklearn.metrics import mean_absolute_percentage_error
from prophet import Prophet
import itertools 
from sklearn.model_selection import TimeSeriesSplit
import torch
import pickle
class model_trainer:
    def __init__(self,data,formsname):
        self.formname=formsname
        self.i=0
        self.data=data
        self.method=["prophet"]
        self.model_parameters = pd.DataFrame(columns = ['MAPE','Parameters',"Number"])
        params_grid_prophet = {
            'changepoint_prior_scale': [0.001, 0.01, 0.1],
            'seasonality_mode':['additive', 'multiplicative'],
            'weekly_seasonality':(True,False)
            }
        self.grid_prophet= [dict(zip(params_grid_prophet.keys(), v)) for v in itertools.product(*params_grid_prophet.values())]
        df2=self.data.copy()
        df2=df2.dropna()
        df2["ds"]=df2.index.tolist()
        tss = TimeSeriesSplit(n_splits = 5)
        days = np.sort(df2.index.unique())
        for train_index, test_index in tss.split(df2):
            train_days, test_days = days[train_index], days[test_index]
            X_train, X_test = df2.loc[train_days,], df2.loc[test_days,]
            for p in self.grid_prophet:
                model = Prophet(daily_seasonality=False,**p)
                model=model.fit(X_train)
                self.i+=1
                name="/home/batuhan-saylam/Desktop/JotformProject/projects/Formmodels/"+self.formname+str(self.i)+".pt"
                torch.save(model, name)
                forecast = model.predict(X_test)
                mape1=mean_absolute_percentage_error(X_test["y"], forecast["yhat"])
                self.model_parameters = self.model_parameters.append({'MAPE':mape1,'Parameters':p,"Number":self.i},ignore_index=True)
        minmape=pd.DataFrame(self.model_parameters.loc[self.model_parameters["MAPE"].argmin()])
        self.minmape=minmape.T
    def picking(self,filename):
        with open(filename, 'wb') as file:  
            pickle.dump(self.model_parameters, file)
    