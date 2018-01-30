"""
This module generate data
and train model
and dump them with pickle to use later

"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mpl_toolkits
import seaborn as sns
from datetime import datetime

from populate_db import generate

from sklearn.cross_validation import train_test_split
from sklearn import ensemble

import pickle


max_values = 10000
# generate amount of data
generate(max_values)

# read data
data = pd.read_csv("data.csv")

# split data
labels = data['price']
train1 = data.drop(['price'],axis=1)

# split datasets train / test
x_train, x_test, y_train, y_test = train_test_split(train1, labels, test_size = 0.10, random_state =2)

# use GradientBoostingRegressor algoritm
# -15min on 1M entries (20.5mb csv)
dt1 = datetime.now()
clf = ensemble.GradientBoostingRegressor(
    n_estimators = 400, max_depth = 5,
    min_samples_split = 2,
    learning_rate = 0.1, loss = 'ls')
dt2 = datetime.now()
#print(dt2-dt1)

# fit and score data
clf.fit(x_train, y_train)
clf.score(x_test,y_test)


# dump model to use later
with open('logmodel.pkl', 'wb') as f:
    pickle.dump(clf, f, 2)
    
#Create a Dataframe with only the dummy variables
features = dict(zip(train1.columns,range(train1.shape[1])))
with open('columns.pkl', 'wb') as f:
    pickle.dump(features, f, 2)








