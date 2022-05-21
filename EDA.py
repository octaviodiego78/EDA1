# -*- coding: utf-8 -*-
"""
Created on Thu May 19 19:40:32 2022

@author: octav
"""


import pandas as pd
import os

#Creating dataframe
file_name = "data"
df = pd.read_csv("{}\{}.csv".format(os.getcwd(),file_name))


#Droping rows with missing values in Handle Time column
df = df[df["Handle Time"].notnull()]


#Convert the handle time duration into minutes
df["Handle Time"] =  pd.to_timedelta(df["Handle Time"])
df["Handle Time"] = round(df["Handle Time"].dt.total_seconds()/60.0,2)



#Agrupating values by state
df = df.pivot_table(index =['State'],
                       values =['Calls','Cost','Handle Time',"Total revenue"],
                       aggfunc ='sum'
                       )

#Calculating calls_volume, cost_per_hour, cost_per_call, cost volume and AHT

df["Calls Volume"] = round((df['Calls']/ sum(df["Calls"]))*100,2)

df["cost_per_hour"] = round(df.Cost / (df["Handle Time"]/60),2)

df["Cost Volume"] = round((df['Cost']/ sum(df["Cost"]))*100,2)

df["AHT"] = round(df["Handle Time"] / df["Calls"],2) #Average Handle Time

df["Cost per call"] = round(df["Cost"] / df["Calls"],2)


#sorting by revenue
df = df.sort_values(
    by="Total revenue",
    ascending=False)


#Converting the results into a csv 
new_file_name = 'Results'
df.to_csv("{}\{}.csv".format(os.getcwd(),new_file_name))



#----------------------Plotting functions------------------------------




#Function to add text labels to the plot
def add_value_label(x_list,y_list):
    for i in range(0,len(x_list)):
        plt.text(i*1.02,
                 y_list[i]*1.02,
                 y_list[i],
                 weight='bold',
                 size = 14
                 )
        

def plotting(x,y,x_column_name,y_column_name): #(x & y are dataframes series)
    
    f = plt.figure()
    f.set_figwidth(15)
    f.set_figheight(10)
    
    x_name = x_column_name
    y_name = y_column_name
    title = "{} by {}".format(y_name,x_name)
    

    plt.xlabel(x_name)
    plt.ylabel(y_name)
    plt.title(title)
    
    plt.plot(x, y,
         marker='o',
         color ='orange',
         markerfacecolor='orange',
         markeredgecolor='orange',
         linewidth=3,
         markersize=12)
    
    add_value_label(x, y)
    plt.show()
    
#-----------------------------Plotting-----------------------------------
    
import matplotlib.pyplot as plt

df.reset_index(inplace=True)

#------------------Plotting config----------------------------------------------------------
columns_to_plot = ["Total revenue","Calls Volume","cost_per_hour","Cost Volume","AHT","Cost per call",]

#This will be the x axis for all plots
x_axis = df["State"]
x_name = 'State'

#-------------------------------------------------------------------------------------------

#Plotting loop
for column in columns_to_plot:
    
    plotting(x_axis,df[column],x_name,column)
    
    

"""
#Configuring plot
f = plt.figure()
f.set_figwidth(15)
f.set_figheight(10)

#Axis
x = df["State"]
y = df["Total revenue"]

#Labels and tittles
plt.xlabel("State")
plt.ylabel("Total revenue")
plt.title('Total Revenue by state')

#Plotting
plt.plot(x, y,
         marker='o',
         color ='orange',
         markerfacecolor='orange',
         markeredgecolor='orange',
         linewidth=3,
         markersize=12)

#Value labels
add_value_label(x, y)
plt.show()
"""





