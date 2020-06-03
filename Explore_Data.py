#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 20:00:07 2020

@author: alexbrebner
"""

import pandas as pd
from scipy.stats.stats import pearsonr
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics

def get_pearson_correlations (model_data, dv, feature_columns):

    # Create output dataframe
    df = pd.DataFrame(columns=['Independent Variable', 'Correlation', 'P-Value'])
    
    # For each independent variable in the feature columns, get Pearson 
    # correlation/p-value and add to dataframe
    for iv in feature_columns:
        [corr, pval] = pearsonr(model_data[iv], model_data[dv])
        new_row = [iv, corr, pval]
        df.loc[df.shape[0] + 1] = new_row

    return df
    
def get_confusion_matrix (model_data, feature_cols, dependent_variable, seed_val=0, test_size=0.25):                
    X = model_data[feature_cols]
    y = model_data[dependent_variable]
    
    # Split into train and test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=seed_val)
    
    # Instantiate the model
    lr = LogisticRegression()
    lr.fit(X_train, y_train)
    y_pred = lr.predict(X_test)
    cnf_matrix = metrics.confusion_matrix(y_test, y_pred)
    
    return cnf_matrix
    