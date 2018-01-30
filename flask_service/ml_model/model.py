import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle

from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.model_selection import train_test_split


def get_model():
    """
        get model from pretrained files
    """    
    
    with open('/flask_service/ml_model/logmodel.pkl', 'rb') as pkl_file:
        clf = pickle.load(pkl_file)
        
    with open('/flask_service/ml_model/columns.pkl', 'rb') as pkl_file:
        features = pickle.load(pkl_file)
        
    new_vector = np.zeros(len(features))
    f_importances = list(zip(features, clf.feature_importances_))
       
    return clf, features


def get_feature_importances_fig(clf, features, prediction):
    """Create matplotlib figure of the feature importances.

    This function will generate a bar plot figure where the x axis
    contains the labels of the features and y axis the importances.
    
    Returns:
        matplotlib.figure.Figure: Figure object of the plot of the
            features importance as bar plots.
    """
   
    price_imp = list(zip(features, [int(fi*prediction) for fi in clf.feature_importances_]))

    importances_name = np.array([f[0] for f in price_imp])
    importances_value = np.array([f[1] for f in price_imp])
    indices = np.argsort(importances_value)

    std = np.std([clf.feature_importances_,], axis=0)

    fig = plt.figure()
    plt.bar(range(len(indices)), importances_value[indices], width=0.3, color="#AEA79F",
            yerr=std[indices], ecolor="#DD4814", align="center")
    plt.xticks(range(len(indices)), importances_name[indices], rotation=45)
    plt.grid(color='gray', linestyle='-', linewidth=0.5)
    
    return fig














