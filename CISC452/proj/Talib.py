import numpy as np
import pandas as pd
import datetime as dt

import jqdatasdk #this is the opensource database for chinese stock market

class stockData():
    def __init__(self,readFromLocal=False,contract='RB9999.XSGE', frequency='1d', start_date='2013-06-01', end_date='2019-07-31'):
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
        self.features = np.asarray(self.get_features(),dtype="float32")
        print("getting labels")
        self.labels = np.asarray(self.get_labels(factor_up=0.006, factor_down=0.007, tolerance=0.40),dtype="float32")


    
    def get_features(self,period=3, windows=60, gap=2):
        F1 = self.get_WVAD(period)
        F2 = self.get_EMA(period).diff()
        F3 = self.get_RSI(period)
        F4 = self.get_Rt(period)
        F5 = self.get_MACD(short_=5, long_=13, m=9)
        F6 = self.get_ATR(period)

        Features = pd.concat((F1, F2, F3, F4, F5, F6), axis=1)


        Features = Features[(Features.index.hour > 9) & (Features.index.hour < 15)]

    
        return Features

    def get_labels(self, factor_up, factor_down, tolerance=0.55):
        data_label = pd.DataFrame(index=self.data.index)
        
        data_label['up'] = None
        data_label['neutral'] = None
        data_label['down'] = None

        for days in np.unique(self.data.index.date):
            subdata = self.data[self.data.index.date == days]
            open_new = subdata['open'][0]
            if open_new * (1 + factor_up) <= np.max(subdata.high[6:-3]):
                begin = np.min(np.where(subdata['high'] >= open_new * (1 + factor_up * 0.99))[0])
                bound = np.min(subdata['low'][begin:-3])
                if bound >= open_new * (1 + factor_up * tolerance):
                    data_label.up[data_label.index.date == days] = 1
                    data_label.neutral[data_label.index.date == days] = 0
                    data_label.down[data_label.index.date == days] = 0

                else:
                    data_label.up[data_label.index.date == days] = 0
                    data_label.neutral[data_label.index.date == days] = 1
                    data_label.down[data_label.index.date == days] = 0

            elif open_new * (1 - factor_down) >= np.min(subdata.low[6:-3]):
                begin = np.min(np.where(subdata['low'] <= open_new * (1 - factor_down * 0.99))[0])
                bound = np.max(subdata['high'][begin:-3])
                if bound <= open_new * (1 - factor_down * tolerance):
                    data_label.up[data_label.index.date == days] = 0
                    data_label.neutral[data_label.index.date == days] = 0
                    data_label.down[data_label.index.date == days] = 1

                else:
                    data_label.up[data_label.index.date == days] = 0
                    data_label.neutral[data_label.index.date == days] = 1
                    data_label.down[data_label.index.date == days] = 0
            else:
                data_label.up[data_label.index.date == days] = 0
                data_label.neutral[data_label.index.date == days] = 1
                data_label.down[data_label.index.date == days] = 0

        data_label = data_label[(data_label.index.hour > 9) & (data_label.index.hour < 15)]
        return data_label




    #following codes are used for extracting the feautures from the pulled data.
    def get_EMA(self,period):
        EMA = self.data['close'].copy()
        for i in range(len(self.data['close'])):
            if i == 0:
                EMA[i] = self.data['close'][i]
            if i > 0:
                EMA[i] = (((period - 1) * EMA[i - 1] + 2 * self.data['close'][i]) / (period + 1))
            return EMA


    def get_ATR(self,period):
        TR = self.data['close'].copy()
        
        for i in range(1, len(TR)):
            TR[i] = max(self.data["high"][i] - self.data["low"][i],
                        max(abs(self.data["high"][i] - self.data["close"][i - 1]), abs(self.data["low"][i] - self.data["close"][i - 1])))

                
        TR = TR.iloc[1:, ]

        ATR = TR.copy()
        for i in range(len(TR)):
            if i == 0:
                ATR[i] = TR[i]
            if i > 0:
                ATR[i] = (((period - 1) * ATR[i - 1] + 2 * TR[i]) / (period + 1))
        return ATR

    def get_RSI(self,period):
        series = self.data['close']
        delta = series.diff().dropna()
        u = delta * 0
        d = u.copy()
        u[delta > 0] = delta[delta > 0]
        d[delta < 0] = -delta[delta < 0]
        u[u.index[period - 1]] = np.mean(u[:period])  # first value is sum of avg gains
        u = u.drop(u.index[:(period - 1)])
        d[d.index[period - 1]] = np.mean(d[:period])  # first value is sum of avg losses
        d = d.drop(d.index[:(period - 1)])
        avgGain = u.ewm(com=period - 1, adjust=False).mean()
        avgLoss = d.ewm(com=period - 1, adjust=False).mean()
        rs = avgGain / avgLoss
        result = 100 - 100 / (1 + rs)
        return result

    def get_MACD(self,short_,long_, m):
        self.data['diff'] = self.data['close'].ewm(adjust=False, alpha=2 / (short_ + 1), ignore_na=True).mean() - self.data['close'].ewm(
            adjust=False, alpha=2 / (long_ + 1), ignore_na=True).mean()
        self.data['dea'] = self.data['diff'].ewm(adjust=False, alpha=2 / (m + 1), ignore_na=True).mean()
        MACD = 2 * (self.data['diff'] - self.data['dea'])

        return MACD

    def get_WVAD(self,period):
        VAD = self.data.close.copy()
        for i in range(len(VAD)):
            if (self.data["high"][i] - self.data["low"][i]) == 0:
                judge = ((self.data["close"][i] - self.data["low"][i]) - (self.data["high"][i] - self.data["close"][i])) * self.data["volume"][i]
                if judge >0:
                    VAD[i] = float("inf")
                elif judge == 0:
                    VAD[i] = 0
                else:
                    VAD[i] = float("-inf")
            else:
                VAD[i] = ((self.data["close"][i] - self.data["low"][i]) - (self.data["high"][i] - self.data["close"][i])) * self.data["volume"][i] / (self.data["high"][i] - self.data["low"][i])

        WVAD = VAD.ewm(period).mean()

        return WVAD

    def get_Rt(self,period):
        Rt = ((self.data.close - self.data.close.shift(period))*100) / self.data.close.shift(period)
        return Rt


