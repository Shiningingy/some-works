#!/usr/bin/env python
# coding: utf-8
import matplotlib.pyplot as plt
import time as t
import random
from tqdm import tqdm
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Dense, Dropout, LSTM
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras import backend as K
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import minmax_scale
import numpy as np
import pandas as pd
import datetime as dt
import os
import warnings
# local library for data pull and pre-processing
from stockData import stockData



warnings.filterwarnings("ignore")



class LSTM_agent():
    def __init__(self,lr=3e-4, window_size=3, batch_size=8,load_model=None): #start_date=dt.date(2016, 1, 1), end_date=dt.date(2019, 7, 31),
        self.data = stockData(period = window_size)

        self.lr = lr

        
        self.num_features = 14 #imput features
        self.record_daily = 1 #from the data there is 1 record/day
        self.window_size = window_size #how many datys data should be uesd for next time prediction

        self.batch_size = batch_size #the batchsize is 8 as default
        self.model = self.init_model()

        #split the data into training and testing data
        self.X_train,self.X_test,self.Y_train,self.Y_test = train_test_split(self.data.features,self.data.labels,test_size=0.4,shuffle=False)
        
        #make sure the data splited could fill up each day's record
        while len(self.X_train) % self.record_daily != 0 :
            x ,self.X_test= self.X_test[0,:].reshape(1,self.num_features),self.X_test[1:,:]
            self.X_train = np.append(self.X_train,x,axis=0)
            y ,self.Y_test = self.Y_test[0,:].reshape(1,3),self.Y_test[1:,:]
            self.Y_train = np.append(self.Y_train,y,axis=0)
            
        #normalize the data
##        self.X_train = minmax_scale(self.X_train,feature_range=(-1, 1))
##        self.X_test = minmax_scale(self.X_test,feature_range=(-1, 1))
##        self.Y_train = minmax_scale(self.Y_train,feature_range=(-1, 1))
##        self.Y_test = minmax_scale(self.Y_test,feature_range=(-1, 1))


        if load_model:
            self.model.load_weights(load_model)

    def init_model(self):
        input_shape = (self.window_size*self.record_daily,self.num_features) #we use 6 features per data as the input for the model
        num_classes = 3 #as 3 tpyes of the prediected result is: goes up, stay and goes down
        
        model = Sequential([
            Input(shape=input_shape),
            LSTM(128,return_sequences=True),
            Dropout(0.2),
            LSTM(64,return_sequences=False),
            Dropout(0.2),
##            Dense(64,activation="relu"),
            Dense(32,activation="relu"),
            Dense(1, activation='linear')
        ])
        
        model.compile(loss='mse',
                      optimizer=RMSprop(lr=self.lr),
                      metrics=['accuracy'])
        return model

    def train(self,episodes=10000,save_model=False,check_point=500):
        
        self.loss_all = []
        self.accuracy_all = []
        window_X = np.empty((0,self.window_size,self.num_features))
        window_Y = np.empty((0,1))
        for i in range(int(((len(self.X_train)/self.record_daily))-(self.window_size+1))): #have no label for last day so mius one from the iteration,and the initial window take 10 days' data,so minus 11 days in total
            window_X = np.append(window_X,self.X_train[self.record_daily*i:(self.window_size*self.record_daily + i*self.record_daily)].reshape(1,self.window_size,self.num_features),axis=0) #data for the window
            window_Y = np.append(window_Y,self.Y_train[self.window_size*self.record_daily+int(self.record_daily*i)].reshape(1,1),axis=0)
        self.window_X = window_X
        self.window_Y = window_Y
        with tqdm(range(episodes)) as t:

            for episode in t:
##                accuracy = []
##                loss = []
##                for i in range(0,len(self.window_X),self.batch_size):
##                    train_x = []
##                    train_y = []
##                    #fill up the mini batch
##                    for j in range(self.batch_size):
##                        try:
##                            train_x.append(self.window_X[i+j])
##                            train_y.append(self.window_Y[i+j])
##                        except:
##                            break
####                    print(train_x)
##                    train_x = np.asarray(train_x)
##                    train_y = np.asarray(train_y)
                    
                #make a prediction
                pred_y = self.model.predict(self.window_X)
                    
                #compute the accuracy and loss during training process
                accuracy = K.mean(K.equal(self.window_Y, K.round(pred_y)))
                loss = self.model.train_on_batch(self.window_X,self.window_Y)

                accuracy = np.asarray(accuracy)
                loss = np.asarray(loss)
                
                t.set_description('loss= %f ,accuracy = %f' %(np.average(np.asarray(loss)),np.average(np.asarray(accuracy))))

                self.loss_all.append(np.average(np.asarray(loss)))
                self.accuracy_all.append(np.average(np.asarray(accuracy)))

                
                if (episode+1)%500 == 0:
                    self.save_model("Window_Model_"+str(episode+1))
                    np.savetxt("Model_loss_" +str(episode+1),np.asarray(self.loss_all),delimiter=',')
                    np.savetxt("Model_accuracy_" +str(episode+1),np.asarray(self.accuracy_all),delimiter=',')

                    
        



    def test(self):
        window_X = np.empty((0,self.window_size,self.num_features))
        window_Y = []
        pred_y = []
        for i in range(int(((len(self.X_test)/self.record_daily))-(self.window_size+1))): #have no label for last day so mius one from the iteration,and the initial window take 10 days' data,so minus 11 days in total
            window_X = np.append(window_X,self.X_test[self.record_daily*i:(self.window_size*self.record_daily + i*self.record_daily)].reshape(1,self.window_size,self.num_features),axis=0) #data for the window
            window_Y.append(np.argmax(self.Y_test[self.window_size*self.record_daily+int(self.record_daily*i)]))

        preds = self.model.predict(window_X)
        for pred in preds:
            pred_y.append(np.argmax(pred))
            
        target_names = ['goes up', 'stay netural', 'goes down']
        print(classification_report(window_Y, pred_y, target_names=target_names))

        


    def save_model(self,name):
        self.model.save(f"{name}.h5")





if __name__ ==  "__main__":
    
##    use this code for training
    LSTM_agent=LSTM_agent()
    LSTM_agent.train()

##    use this code for testing
##    for i in range(1,21):
##        new_LSTM_agent=LSTM_agent(load_model="Window_Model_"+str(i*500)+".h5")
##        new_LSTM_agent.test()
