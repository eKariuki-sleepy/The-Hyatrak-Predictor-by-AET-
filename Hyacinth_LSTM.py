#-------------------------------------------------------------------------------
# Name:        LSTM for Hyacinth monitoring
# Purpose:      using LSTM to carry out Hyacinth prediction
#
# Author:      Caleb
# reources:    Gigital Sreeni (https://www.youtube.com/watch?v=tepxdcepTbY)
# Created:     06/12/2022
# Copyright:   (c) Acer 2022
# Licence:     <open source license>
#-------------------------------------------------------------------------------

import os

import keras
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense, Dropout
from keras.models import load_model
from sklearn.preprocessing import StandardScaler

import numpy as np
import pandas as pd
import random

from matplotlib import pyplot as plt
import seaborn as sns

plt.rcParams.update({'font.size':18})




def data_prep(input_file,no_past_records=30,no_future_records=1):

    df = pd.read_csv(input_file)#put in a diff folder to the py file

    ##scale train dataset
    df=df.astype(float)
    scaler=StandardScaler()
    scaler=scaler.fit(df)
    df_scaled=scaler.transform(df)


    # input and output sequences
    output_seq=no_future_records
    input_seq=no_past_records

    #train dataset
    data_x=[]
    data_y=[]

    for i in range(input_seq,len(df_scaled)-output_seq+1):
        data_x.append(df_scaled[i - input_seq:i,0:df.shape[1]])
        data_y.append(df_scaled[i + output_seq - 1:i+output_seq,12]) #column 12 is what we are predicting

    data_x,data_y=np.array(data_x), np.array(data_y)

    return data_x, data_y





def train_lstm(input_file, saved_model_folder,epoch=1000,batch_size=24,no_past_records=30,no_future_records=1):

    data_x,data_y=data_prep(input_file,no_past_records,no_future_records)

    saved_model=saved_model_folder+'\LSTM_epoch_{}_batch_size_{}_inseq_{}_out_seq_{}.hdf5'.format(epoch,batch_size,no_past_records,no_future_records)


    model=Sequential()
    model.add(LSTM(64, activation='relu', input_shape=(data_x.shape[1],data_x.shape[2]),return_sequences=True))
    model.add(LSTM(32, activation='relu', return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(data_y.shape[1]))

    model.compile(optimizer='adam',loss='mse')
    model.summary()

    history=model.fit(data_x, data_y,batch_size=batch_size,epochs=epoch,validation_split=0.1,verbose=1)

    model.save(saved_model)

    plt.plot(history.history['loss'],label='Training loss')
    plt.plot(history.history['val_loss'],label='Validation loss')
    plt.legend()
    plt.show()

    return saved_model



def predict_lstm(input_file,saved_model,data_x,data_y,future_prediction=60,from_duration=0, to_duration=10):

    df = pd.read_csv(input_file)

    output_seq=future_prediction

    model_loaded=load_model(saved_model)
    forecast=model_loaded.predict(data_x[-output_seq:])

    ##unscale
    df=df.astype(float)
    scaler=StandardScaler()
    scaler=scaler.fit(df)
    forecast_copies=np.repeat(forecast,df.shape[1],axis=1)
    y_pred_future=scaler.inverse_transform(forecast_copies)[:,12]# 12 column contains the hyacinth values

    months_to_use=df["digit_count"][-output_seq:]
    original_hyacinth=df["hyacinth_area"][-output_seq:]



    ##plotting
    original_df=pd.DataFrame({"month values":np.array(months_to_use),"Hyacinth area":np.array(original_hyacinth)})
    pred_df=pd.DataFrame({"month values":np.array(months_to_use),"Hyacinth area":y_pred_future})
    sns.lineplot(original_df['month values'],original_df['Hyacinth area'],color='blue', label="Actual")
    ax=sns.lineplot(pred_df['month values'],pred_df['Hyacinth area'],color='red',label="Predicted")
    ax.set_title("Monthly hyacinth area (km² ) Predictions vs. Actual")
    plt.legend(loc="upper right")
    plt.show()



    ##predict for a specified duration for error metrics

    y_test_whole=np.array(original_hyacinth)


    y_test_list=y_test_whole.tolist()[from_duration:to_duration]
    y_pred_list=y_pred_future.tolist()[from_duration:to_duration]


    y_test=np.array(y_test_list)
    y_pred=np.array(y_pred_list)


    ###Metrics

    #MAE
    mae=np.mean(abs(y_pred-y_test))

    #MAPE
    mape=100*np.mean(abs((y_pred-y_test)/y_test))

    #MSE and RMSE
    mse=np.mean((y_test - y_pred)**2)
    rmse=np.sqrt(mse)


    #calcluate R2 using residual sum of squares (rss) and total sum of squares(tSS)
    y_test_mean=np.mean(y_test)

    rss=np.sum((y_test - y_pred)**2)
    tss=np.sum((y_test - y_test_mean)**2)
    r2_statistic=1-(rss/tss) # the closer it is to one, the better our prediction


    print("\n***********************************************************************")
    print("METRICS\n")
    print('Mean Absolute Error: {:.4f}'.format(mae))
    print('Mean Absolute Percentage Error: {:.2f}%'.format(mape))
    print('Mean Squared Error: {:.4f}'.format(mse))

    print('Root Mean Squared Error: {:.4f}'.format(rmse))

    print("R squared is {:.4f}".format(r2_statistic))




##example
##input_file=r'D:\PROJECTS\Humburg_Lake_Victoria\data\Winam_Gulf_Satellite_Data.csv'
##saved_model_folder=r'D:\PROJECTS\Humburg_Lake_Victoria\Delivery_2\weights'
##
##
###to train the model
##saved_model=train_lstm(input_file, saved_model_folder,epoch=1000,batch_size=24,no_past_records=30,no_future_records=1)
##
##
####carry prediction
##data_x,data_y=data_prep(input_file,no_past_records=30,no_future_records=1)
##
##file_name=os.listdir(saved_model_folder)
##saved_model=saved_model_folder+"/"+file_name[0]
##
##predict_lstm(input_file,saved_model,data_x,data_y,future_prediction=60,from_duration=0, to_duration=10)
##
