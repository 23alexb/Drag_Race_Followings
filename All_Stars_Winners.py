#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A model using the Wikipedia_Web_Scrape dataset

Machine learning model to predict which contestants are selected for an
All Stars season based on main season metrics.

Machine learning model to predict which contestants win an All Stars season 
based on main season metrics.
"""

import All_Stars_Data_Prep as all_stars_prep

# Get data to train model on, adjust boolean parameters to integer
model_data = all_stars_prep.get_all_stars_selection_model_data(range(1,5))

# Get features and outcome
feature_cols = [ 'Win', 'High', 'Safe', 'Low', 'Bottom', 'Eliminated', 'Guest', 
                 'Season Winner', 'Season Runner-Up', 'Season Miss Congeniality',
                 'Total Appearances', 'Years Since Last Competed' ]



























