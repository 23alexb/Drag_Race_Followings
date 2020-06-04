#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A model using the Wikipedia_Web_Scrape dataset

Machine learning model to predict which contestants are selected for an
All Stars season based on main season metrics.

Machine learning model to predict which contestants win an All Stars season 
based on main season metrics.
"""

import pandas as pd
from scipy.stats.stats import pearsonr
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics
#import All_Stars_Data_Prep as all_stars_prep

# Get data to train model on, adjust boolean parameters to integer
#model_data = all_stars_prep.get_all_stars_selection_model_data(range(1,5))

# Get features and outcome
feature_cols = [ 'Win', 'High', 'Safe', 'Low', 'Bottom', 'Eliminated', 'Guest', 
                 'Season Winner', 'Season Runner-Up', 'Season Miss Congeniality',
                 'Total Appearances', 'Years Since Last Competed' ]

feature_cols_selected = [ 'High', 'Safe', 'Guest', 'Season Winner', 'Season Runner-Up', 
                          'Season Miss Congeniality', 'Years Since Last Competed' ]

dependent_variable = 'Competed'
#test_size = 0.25
#seed_val = 0
#                        
#X = model_data[feature_cols]
#y = model_data[dependent_variable]
#
## Split into train and test set
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=seed_val)
#
## Instantiate the model
#lr = LogisticRegression(solver='liblinear')
#lr.fit(X_train, y_train)
#y_pred = lr.predict(X_test)
#cnf_matrix = metrics.confusion_matrix(y_test, y_pred)
#
#print(cnf_matrix)


    
oversampled_df = get_oversampled_df (model_data, feature_cols, dependent_variable)


























