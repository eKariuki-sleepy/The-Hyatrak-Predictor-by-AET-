#-------------------------------------------------------------------------------
# Name:        Data Relationships
# Purpose:
#
# Author:      Caleb @calebjuma27@gmail.com
#
# Created:     27/09/2022
# Copyright:   (c) -----
# Licence:     <your licence>
#-------------------------------------------------------------------------------


# Data Manipulation
import numpy as np
import pandas as pd

# Visualization
import matplotlib
import matplotlib.pyplot as plt

from scipy.optimize import curve_fit

#changes text size
plt.rcParams.update({'font.size':23})


def time_vs_var(variable):

    """function to plot any feature per year"""

    year_var=dict({"year":[],"var":[]})
    for m in range(39):

        current_year=1984+m

        df_1=df[(df["Year"] == current_year)]

        df_2=df_1[(df_1[variable] != 0)]
        val=df_2[variable].tolist()
        try:
            val_mean=sum(val)/len(val)
            year_var["year"].append(current_year)
            year_var["var"].append(val_mean)
            print(current_year,)
        except:
            pass
    plt.plot(year_var["year"],year_var["var"])
    plt.title("Annual variation of {}".format(variable))
    plt.xlabel("year")
    plt.ylabel("{} in km²".format(variable))

    plt.show()

    return year_var




def funcline(x, a, b):
    """linear regression"""
    return a*x + b


def data_relationship(dataframe,feature):

    """ plots the relationship between a specified feature and other features in the dataframe"""
    column_names=list(dataframe.columns.values)
    del column_names[0] #delete the first usually empty column
    for i in column_names:
        try:


            df_feature_1=dataframe[(dataframe[i]!=0)]
            df_feature_2=df_feature_1[(df_feature_1[feature] !=0)]
            on_x=df_feature_2[i].tolist()
            on_y=df_feature_2[feature].tolist()



            ydata = np.asarray(on_y, dtype=np.float32)
            xdata = np.asarray(on_x, dtype=np.float32)


            poptline, pcovline = curve_fit(funcline, xdata, ydata)



            gradient="{:.2f}".format(poptline[0])
            print(gradient)

            plt.scatter(on_x,on_y, label="data points")


            plt.plot(xdata, funcline(xdata, *poptline), 'r-', label="Fitted Curve, gadient= {}".format(gradient))

            plt.title("{} vs {}".format(feature,i))
            plt.xlabel(i)
            plt.ylabel("{} in km² ".format(feature))

            plt.legend()

            plt.show()
        except:
            pass



input_file=r'D:\PROJECTS\Humburg_Lake_Victoria\data\Winam_Gulf_Satellite_Data.csv'

df_original = pd.read_csv(input_file)

#emove no data records
df=df_original[(df_original["mean_monthly_temp"] > 0)]

#main feature to plot
feature="hyacinth_area"#"hyacinth_mean_monthly_ndvi"

##call functions
year_var=time_vs_var(feature)
data_relationship(df,feature)









