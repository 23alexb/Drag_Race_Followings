#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import bs4
import requests
import pandas as pd

def find_table_by_header_list(soup, headers_list, table_class=None):
    
    # Get tables collection (with or without class)
    if table_class is None:
        tables = soup.findAll('table')
    else:
        tables = soup.findAll('table', { 'class' : table_class })
        
    # Check each table for matching headers
    for table in tables:
        # Compile list of headers
        this_headers_list = []
        for header in table.findAll('th') : this_headers_list.append(header.find(text=True).strip())
        #print(this_headers_list) # For testing/adjustments, to view possible header lists
        
        # If all headers in headers_list found in this_headers_list, return table object
        match = True
        for header in headers_list:
            if header not in this_headers_list : match = False
        if match : return (table)
    
    return None

def get_season_appearances_dataframe(season_number, all_stars=False):
    # Get url and season name
    if all_stars:
        url = 'https://en.wikipedia.org/wiki/RuPaul%27s_Drag_Race_All_Stars_(season_' + str(season_number) + ')'
        season_name = 'All Stars Season ' + str(season_number)
    else:
        url = 'https://en.wikipedia.org/wiki/RuPaul%27s_Drag_Race_(season_' + str(season_number) + ')'
        season_name = 'Season ' + str(season_number)
    print('Retrieving details for: ' + season_name + '.')
        
    # Get beautiful soup object
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    
    # Get results table and convert to data frame
    table = find_table_by_header_list(soup, ['Contestant', '1', '2', '3', '4'], 'wikitable')
    df_scraped = pd.read_html(str(table))[0]
    
    # Create scores data frame
    df = pd.DataFrame(columns=['Contestant', 'Season',
                               'Win', 'High', 'Safe',
                               'Low', 'Bottom', 'Eliminated',
                               'Guest',
                               'Season Winner', 'Season Runner-Up', 'Season Miss Congeniality',
                               'Total Appearances'])
    
    # Create dictionary to determine how each result is recorded in the final dataframe
    results_dict = { 'WIN' : 'Win',
                     'HIGH' : 'High',
                     'TOP2' : 'High',
                     'SAFE' : 'Safe',
                     'LOW' : 'Low',
                     'BTM2' : 'Bottom',
                     'BTM3' : 'Bottom',
                     'BTM4' : 'Bottom',
                     'BTM6' : 'Bottom',
                     'ELIM' : 'Eliminated',
                     'IN' : 'Win',
                     'OUT' : 'Eliminated',
                     'GUEST' : 'Guest',
                     'JUROR' : 'Guest',
                     'WINNER' : 'Season Winner',
                     'RUNNER-UP' : 'Season Runner-Up',
                     'ELIMINATED' : 'Eliminated',
                     'DISQ' : 'Eliminated',
                     'QUIT' : 'Eliminated',
                     'MISS C' : 'Season Miss Congeniality',
                     }
    
    # Convert scraped data to score tallies
    for row_no in range(1, df_scraped.shape[0]):
        
        # Add new row to the data frame for the contestant
        new_row = [df_scraped[0][row_no], season_name]
        for _ in range(2, df.shape[1]) : new_row.append(0)
        df.loc[df.shape[0] + 1] = new_row
        total_appearances = 0
        
        # Check each episode column and add result to dataframe
        for episode in range(1, df_scraped.shape[1]):
            result = str(df_scraped.loc[row_no][episode]).upper()
            if result in results_dict.keys():
                df.at[row_no, results_dict[result]] += 1
                total_appearances += 1
            elif result not in ['NAN']:
                print('Unclassified: ' + result)
                
        # Add number of total appearances to dataframe
        df.at[row_no, 'Total Appearances'] = total_appearances
    
    return df

df = None

season_details = [[1, False], [2, False], #[3, False], 
                  [4, False], 
                  [5, False], [6, False], [7, False], [8, False],
                  [9, False], [10, False], [11, False], [12, False], #[1, True], 
                  [2, True], [3, True], [4, True], ]

for season in season_details:
    df_new = get_season_appearances_dataframe(season[0], season[1])
    if df is None:
        df = df_new
    else:
        df = pd.concat([df, df_new])