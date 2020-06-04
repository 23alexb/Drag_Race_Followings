#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 20:00:07 2020

@author: alexbrebner
"""

import pandas as pd
from scipy.stats.stats import pearsonr
from imblearn import over_sampling as imbsample
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics

def print_accuracy_and_recall (cnf, percent_dp=2):
    
    accuracy = (cnf[0][0] + cnf[1][1]) / (sum(cnf[0]) + sum(cnf[1]))
    recall_1 = cnf[0][0] / sum(cnf[0])
    recall_2 = cnf[1][1] / sum(cnf[1])
    
    print('Accuracy = ' + str(round(accuracy * 100, percent_dp)))
    print('Recall 1 = ' + str(round(recall_1 * 100, percent_dp)))
    print('Recall 2 = ' + str(round(recall_2 * 100, percent_dp)))
    
    return
    
def print_accuracy_and_recall_2 (cnf):
    
    accuracy = round(((cnf[0][0] + cnf[1][1]) * 100 / (sum(cnf[0]) + sum(cnf[1]))), 2)
    recall_1 = round(((cnf[0][0] * 100 / sum(cnf[0]))), 2)
    recall_2 = round(((cnf[1][1] * 100 / sum(cnf[1]))), 2)
    
    print('The overall accuracy with the oversampled data is ' + str(accuracy) + \
          '%, with a recall of ' + str(recall_2) + '% for the group that were ' + \
          'selected to compete and ' + str(recall_1) + '% for the group that were not selected.')
    
    return

def get_oversampled_df (model_data, feature_columns, dependent_variable, sampling_strategy=0.5, seed_val=0):

    X = model_data[feature_columns]
    y = model_data[dependent_variable]
    oversample_obj = imbsample.RandomOverSampler(sampling_strategy=sampling_strategy, random_state=seed_val)
    X_over, y_over = oversample_obj.fit_resample(X, y)
    
    oversampled_df = X_over
    oversampled_df['Competed'] = y_over
    
    return oversampled_df

def get_pearson_correlations (model_data, dv, feature_columns):

    # Create output dataframe
    df = pd.DataFrame(columns=['Independent Variable', 'Correlation', 'P-Value'])
    
    # For each independent variable in the feature columns, get Pearson 
    # correlation/p-value and add to dataframe
    for iv in feature_columns:
        [corr, pval] = pearsonr(model_data[iv], model_data[dv])
        new_row = [iv, corr, pval]
        df.loc[df.shape[0] + 1] = new_row

    # Sort by p-value
    df = df.sort_values(by=['P-Value'])

    return df
    
def get_confusion_matrix (model_data, feature_cols, dependent_variable, seed_val=0, test_size=0.25, 
                          solver='liblinear', oversample_training_data=False, sampling_strategy=0.5):  
    
    # Split into independent and dependent variables
    X = model_data[feature_cols]
    y = model_data[dependent_variable]
    
    # Split into train and test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=seed_val)
    
    # Oversample training data if specified
    oversample_obj = imbsample.RandomOverSampler(sampling_strategy=sampling_strategy, random_state=seed_val)
    X_train, y_train = oversample_obj.fit_resample(X_train, y_train)
    
    # Instantiate the model
    lr = LogisticRegression(solver=solver)
    lr.fit(X_train, y_train)
    y_pred = lr.predict(X_test)
    cnf_matrix = metrics.confusion_matrix(y_test, y_pred)
    
    return cnf_matrix
    
