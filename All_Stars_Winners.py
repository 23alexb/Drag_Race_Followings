#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A more basic exploratory model using the Wikipedia_Web_Scrape dataset

Machine learning model to predict which contestants are selected for an
All Stars season based on main season metrics.

Machine learning model to predict which contestants win an All Stars season 
based on main season metrics.
"""

import Wikipedia_Web_Scrape as wiki
import pandas as pd
from sklearn.linear_model import LogisticRegression as lr
from sklearn.model_selection import train_test_split as tts

def get_all_stars_summary(all_stars_metrics):
    # For all stars, get dataframe of contestant/season and whether they were a winner/finalist
    all_stars_summary = pd.DataFrame(columns=['Contestant', 'All Stars Season', 'Winner', 'Finalist', 'Competed'])
    for season in list(all_stars_metrics['Season'].unique()):
        season_subset = all_stars_metrics[all_stars_metrics['Season']==season]
        
        for index, row in season_subset.iterrows():
            new_row = [row['Contestant'], row['Season'], row['Season Winner']==1, row['Season Runner-Up']==1, True]
            all_stars_summary.loc[all_stars_summary.shape[0] + 1] = new_row
            
    return all_stars_summary
    
def normalize_series_contestant_data(season_metrics):
    # Summarise main_season metrics to merge queens that appear twice, normalize names, etc.
    
    # Normalize names for queens that appear more than once
    names_replace_dict = { 'Shangela Laquifa Wadley' : 'Shangela',
                           'Trinity Taylor' : 'Trinity the Tuck' }
    season_metrics['Contestant'] = season_metrics['Contestant'].replace(names_replace_dict)
        
    # Get list of contestants that appear twice, merge records and use most recent season
    queens_appearing_twice = list(set(list(pd.concat(c for _, c in season_metrics.groupby('Contestant') if len(c) > 1)['Contestant'])))
    for contestant in queens_appearing_twice:
        row_indices = season_metrics.loc[season_metrics['Contestant']==contestant].index.tolist()
        keep_row = max(row_indices)
        for row_no in row_indices:
            if row_no != keep_row:
                for col in ['Win', 'High', 'Safe', 'Low', 'Bottom', 'Eliminated', 'Guest', 'Season Winner', 'Season Runner-Up', 'Season Miss Congeniality', 'Total Appearances']:
                    season_metrics.loc[keep_row, col] = season_metrics.loc[row_no, col] + season_metrics.loc[keep_row, col]
                season_metrics = season_metrics.drop(row_no)
        season_metrics = season_metrics.reset_index(drop=True)
        
    return season_metrics
    
def add_most_recent_contestant_appearance(prior_season_metrics, season_data):
    prior_season_metrics = pd.merge(prior_season_metrics, season_data, on='Season', how='left').fillna(False)
    prior_season_metrics = prior_season_metrics.drop([_ for _ in list(season_data.columns) if _ not in ['Season', 'Year']], 1)
    
    return prior_season_metrics

def get_all_stars_season_selection(all_stars_season, season_data, wiki_metrics):
    # Get list of eligible seasons to select contestants from for the specified season
    all_stars_season = 'All Stars Season ' + str(all_stars_season)
    season_list = list(season_data[season_data[all_stars_season]==True]['Season'])
    
    # Divide into main and all stars seasons 
    all_stars_metrics = wiki_metrics[wiki_metrics['Season']==all_stars_season].reset_index(drop=True)
    prior_season_metrics = wiki_metrics[wiki_metrics['Season'].isin(season_list)].reset_index(drop=True)
    
    # Get summary of all stars results and normalized main season results and get year of most recent prior appearance
    all_stars_summary = get_all_stars_summary(all_stars_metrics)
    prior_season_metrics = normalize_series_contestant_data(prior_season_metrics)
    prior_season_metrics = add_most_recent_contestant_appearance(prior_season_metrics, season_data)
    model_data = pd.merge(prior_season_metrics, all_stars_summary, on='Contestant', how='left').fillna(False)
    model_data['All Stars Season'] = all_stars_season

    # Get number of years between last appearance and selection round
    all_stars_season_year = int(season_data[season_data['Season']==all_stars_season]['Year'])
    model_data['Year'] = all_stars_season_year - model_data['Year']
    model_data['Year'] = model_data['Year'].astype(int)
    #model_data.rename({ 'Year' : 'Years Since Last Competed' })
 
    return model_data
    
def get_all_stars_selection_model_data(all_stars_seasons):
    # Get base metrics
    season_data = pd.read_csv('Season_Info.csv')
    wiki_metrics = wiki.get_episode_metrics(display_progress_alerts=False)
    model_data = pd.DataFrame(columns=['Contestant', 'Season', 'Win', 'High', 'Safe', 'Low', 'Bottom',
                                       'Eliminated', 'Guest', 'Season Winner', 'Season Runner-Up',
                                       'Season Miss Congeniality', 'Total Appearances', 'Year',
                                       'All Stars Season', 'Winner', 'Finalist', 'Competed'])
    
    # Get selection metrics for each all stars season
    for _ in all_stars_seasons : model_data = pd.concat([model_data, get_all_stars_season_selection(_, season_data, wiki_metrics)])
    model_data = model_data.rename(columns={'Year' : 'Years Since Last Competed'})
    
    return model_data

## Get data to train model on, adjust boolean parameters to integer
#model_data = get_all_stars_selection_model_data(range(1,5))
#for col_name in ['Winner', 'Finalist', 'Competed'] : model_data[col_name] = (model_data[col_name]==True).astype(int)

# Get features and outcome
feature_cols = [ 'Win', 'High', 'Safe', 'Low', 'Bottom', 'Eliminated', 'Guest', 
                 'Season Winner', 'Season Runner-Up', 'Season Miss Congeniality',
                 'Total Appearances', 'Years Since Last Competed' ]
X = model_data[feature_cols]
y = model_data['Competed']

# Split into train and test set
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.25,random_state=0)



















