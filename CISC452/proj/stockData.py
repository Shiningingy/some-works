import numpy as np
import pandas as pd
import datetime as dt
import talib as tl

import jqdatasdk #this is the opensource database for chinese stock market

class stockData():
    def __init__(self,readFromLocal=True,contract='RB9999.XSGE', frequency='1d', start_date='2013-06-01', end_date='2019-07-31',period=10):
        print("collecting data from database")
        if not readFromLocal:
            jqdatasdk.auth('18630305086',"305086") #log in the database to pull data
            jqdatasdk.get_price(contract, start_date=start_date, end_date=end_date, frequency=frequency, fields=None, skip_paused=False,
                  fq='pre',
                  count=None).to_csv("data_"+ frequency +".csv")#pull the data from the database
            
        try: #load the data
            self.data = pd.read_csv("data_"+ frequency +".csv")
        except:
            print("do not find local data, start pulling")
            jqdatasdk.auth('18630305086',"305086") #log in the database to pull data
            jqdatasdk.get_price(contract, start_date=start_date, end_date=end_date, frequency=frequency, fields=None, skip_paused=False,
                  fq='pre',
                  count=None).to_csv("data_"+ frequency +".csv") #pull the data from the database
            
            self.data = pd.read_csv("data_"+ frequency +".csv")
            
        #process the pulled data
        print("processing")       
        self.data[self.data.columns[0]] = pd.to_datetime(self.data[self.data.columns[0]], format='%Y/%m/%d %H:%M:%S')
        self.data.set_index(self.data.columns[0], inplace=True)
        
        self.trade_days = np.unique(self.data.index.date)

        #extract the features and labels from the data for training use
        print("getting features")
        self.features = np.asarray(self.get_features(period=period),dtype="float32")
        while (True in np.isnan(self.features[0])):
            self.features = self.features[1:]
            
        print("getting labels")
        self.labels = np.asarray(self.get_labels(period=period),dtype="float32")
        if len(self.labels) > len(self.features):
            self.labels = self.labels[(len(self.labels)-len(self.features)):]
        elif len(self.labels) > len(self.features):
            self.features= self.features[(len(self.features)-len(self.labels)):]

    
    def get_features(self,period):
        F1 = tl.WILLR(self.data["high"], self.data["low"], self.data["close"])
        F2 = tl.EMA(self.data["close"],timeperiod=period)
        F3 = tl.RSI(self.data["close"],timeperiod=period)
        F4 = self.get_Rt(period)
        F5,F6,F7 = tl.MACD(self.data["close"])
        F8 = tl.ATR(self.data["high"], self.data["low"], self.data["close"])
        Features = pd.concat((self.data,F1, F2, F3, F4, F5, F6, F7, F8), axis=1)

    
        return Features
    def get_labels(self,period):
        data_label = []
        close = np.asarray(self.data["close"].copy())
        for i in range(period,len(close)):
            data_label.append(close[i])
        return data_label

##    def get_labels(self,period,factor = 0.005):
##        data_label = []
##
##        close = np.asarray(self.data["close"].copy())
##
##        for i in range(period,len(close)):
##            if close[i] > close[i-1]*(1 + factor):
##                data_label.append([1,0,0])
##            elif close[i] < close[i-1]*(1 - factor):
##                data_label.append([0,0,1])
##            else:
##                data_label.append([0,1,0])
##        return data_label


    def get_Rt(self,period):
        Rt = ((self.data.close - self.data.close.shift(period))*100) / self.data.close.shift(period)
        return Rt



