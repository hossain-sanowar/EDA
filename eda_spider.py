#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 09:44:14 2022

@author: mdsanowarhossain
"""
# importing libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import os

# loading dataset
path = "train_bikes.csv"

dataset=pd.read_csv(path)
df=dataset.copy()

# basic statistic
print(df.head())

print(df.shape)

#get data information
print(df.info())
print(df.describe().T)

#get the missing values

df.isnull().sum()

feature_with_na=[feature for feature in df.columns if df[feature].isnull().sum()>0]

for feature in feature_with_na:
    print(feature, np.round(df.isnull().mean()*100,4),'% misisng')

#fill up the missing values by 1 or mean
for feature in feature_with_na:
    data=df.copy()
    data[feature]=np.where(df[feature].isnull(),1,0)
    data.groupby(feature)['count'].median().plot.bar()
    plt.title(feature)
    plt.show()
    
#Numerical feature
numerical_features=[feature for feature in df.columns if df[feature].dtype!='O']
df[numerical_features]
print('Number of numerical features: {}'.format(len(numerical_features)))

#get relationship between discreate features and target feature
discreate_features=[feature for feature in numerical_features if len(df[feature].unique())<25]
df[discreate_features]
for feature in discreate_features:
    data=df.copy()
    data.groupby(feature)['count'].median().plot.bar()
    plt.title(feature)
    plt.xlabel(feature)
    plt.ylabel('count')
    plt.show()
    
#get relationship between continuou features and target feature
continuous_features=[feature for feature in numerical_features if len(df[feature].unique())>=25]
df[continuous_features]
for feature in continuous_features:
    data=df.copy()
    data.groupby(feature)['count'].median().plot.bar()
    plt.title(feature)
    plt.xlabel(feature)
    plt.ylabel('count')
    plt.show() 
    
 #get histplot
for feature in continuous_features:
    data=df.copy()
    data[feature].hist(bins=25)
    plt.title(feature)
    plt.xlabel(feature)
    plt.ylabel('count')
    plt.show() 
       
#get categorical features
cat_features=[feature for feature in df.columns if df[feature].dtype=='O']
print('Number of catgorical features: {}'.format(len(cat_features)))
df[cat_features]

#now convert categorical feature to dateformat
df['datetime_new']=pd.to_datetime(df['datetime'])
df.sample(5)
df['year']=df['datetime_new'].map(lambda x:x.year)
df['month']=df['datetime_new'].map(lambda x:x.month)
df['day']=df['datetime_new'].map(lambda x:x.day)
df['hour']=df['datetime_new'].map(lambda x:x.hour)
df.sample(5)

#define hourly plot for working and non working
df.groupby(['hour','workingday'])['count'].sum().unstack().plot.bar(width=0.9)

#define hourly plot for working and non working in 2011, 2012
def define_hourly_working_plot(df, year=None, agg='sum'):
    data=df[df.year==year]
    hourly_data=data.groupby(['hour','workingday'])['count'].agg(agg).unstack()
    hourly_plot=hourly_data.plot(kind='bar',ylim=(0,110000),
                                 figsize=(15,5),
                                 width=0.9,
                                 title='Year {}'.format(year))
    return hourly_plot
    


define_hourly_working_plot(df,year=2011)
define_hourly_working_plot(df,year=2012)


#define hourly plot

def hourly_plot(df, year=None, agg='sum'):
    data=df[df.year==year]
    hourly_data=data.groupby(['hour'])['count'].agg(agg)
    hourly_plot=hourly_data.plot(kind='bar',width=0.9, 
                                 figsize=(15,5),
                                 ylim=(0,110000),
                                 title='Year {}'.format(year))
    
    return hourly_plot


hourly_plot(df,year=2011)
hourly_plot(df,year=2012)

#Comparison Year to Year Data
def define_yearly_comparison_plot(attr,agg,title):
    data=df.copy()
    yearly_data=data.groupby([attr,'year'])['count'].agg(agg).unstack()
    yearly_plot=yearly_data.plot(kind='bar',width=0.9,
                                 ylim=(0,110000),
                                 figsize=(15,5),
                                 title=title)
    return yearly_plot

define_yearly_comparison_plot('hour','sum',"Rent bikes per hour in 2011 and 2012")
define_yearly_comparison_plot('month','sum',"Rent bikes per month in 2011 and 2012")

#daywise count for specific hour
days={}
data=df.copy()
data1=data[(data['year']==2011)& (data['month']==1)]
for day in range(len(data['day'].unique())):
    days[day]=data1[(data1.day==day)&(data1.hour==0)]['count'].values
    

plt.figure(figsize=(15,5))
for key,val in days.items():
    plt.bar(key,val)
    plt.bar(key, val)
    plt.xticks(range(0,20))
    plt.xlabel('Day')
    plt.ylabel('count')
    plt.title('bikes rent at 1st hour of January, 2011')

#yearwise hourly count using boxplot

def yearwise_hourly_boxplot(df, message=''):
    data=df.copy()
    hours={}
    
    for hour in range(24):
        hours[hour]=data[data.hour==hour]['count'].values
    
    plt.figure(figsize=(15,5))
    plt.xlabel('hours')
    plt.ylabel('count')
    plt.title('count vs hours\n'+message)
    plt.boxplot([hours[hour] for hour in range(24)])
    
    axis=plt.gca()
    axis.set_ylim([0,1100])


yearwise_hourly_boxplot(df[df['year']==2011],'year 2011')
yearwise_hourly_boxplot(df[df['year']==2012],'year 2012')


#yearwise hourly count using boxplot for working 
yearwise_hourly_boxplot(df[df['workingday']==1],'working day')
yearwise_hourly_boxplot(df[df['workingday']==0],'non working day')


# average bike demand based on the hour 
figure,axes = plt.subplots(figsize = (10, 5))
hours = df.groupby(["hour"]).agg("mean")["count"]  
hours.plot(kind="line", ax=axes) 
plt.title('Hours VS Counts')
axes.set_xlabel('Time in Hours')
axes.set_ylabel('Average of the Bike Demand')
plt.show()


































    
    
    
    