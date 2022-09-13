import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# loading dataset
dataset = pd.read_csv('train_bikes.csv')
df = dataset.copy()
print(df.head(5))

# Basic Statistic
print(df.shape)

# get data info
print(df.info())
#%%
print(df.describe().T)
#%%
# Numerical features
numerical_features = [feature for feature in df.columns if df[feature].dtype!='O']
print(df[numerical_features])

# get discreate feature

discreate_features = [feature for feature in df.columns if len(df[feature].unique())<25]
for feature in discreate_features:
    data=df.copy()
    data.groupby(feature)['count'].mean().plot.bar()
    plt.title(feature)
    plt.show()