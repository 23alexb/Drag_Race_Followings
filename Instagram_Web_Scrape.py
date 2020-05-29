# -*- coding: utf-8 -*-

'''
Dependencies:
    - selenium installed with Chromedriver file located at '/usr/local/bin/chromedriver'
'''

from selenium import webdriver
from selenium.common import exceptions 
import pandas as pd

insta_handles_csv = 'Instagram_Handles.csv'

def get_follower_count_from_handle(insta_handle, browser):
    # Returns follower count for a given Instagram handle (insta_handle)
    
    # Get and navigate to URL
    url = 'https://www.instagram.com/' + insta_handle + '/'
    browser.get(url)
    
    # Get follower count displayed text (e.g. '931k', '1.1m')
    elems = browser.find_elements_by_tag_name("a")
    for elem in elems:
        follower_count_text = elem.text
        if follower_count_text.endswith(' followers') : break
        follower_count_text = ''
    # Return -1 for error if not found
    if follower_count_text == '' : return -1
    follower_count_text = follower_count_text[:len(follower_count_text) - len(' followers')]
    
    # Used displayed text to find actual underlying follower count (e.g. '931,083', '1,103,473')
    elems = browser.find_elements_by_tag_name('span')
    for elem in elems:
        try:
            if elem.text==follower_count_text : follower_count = elem.get_attribute('title')
        except exceptions.StaleElementReferenceException:
            return -2
    # Return -1 for error if not found
    if follower_count is None : return -1
        
    # Convert to integer and return
    follower_count = int(follower_count.replace(',', ''))
    return follower_count

def get_follower_counts(insta_handles):
    # Returns the follower counts for a list of Instagram handles as a data frame
    
    # Initialise Instagram URL and browser object
    browser = webdriver.Chrome('/usr/local/bin/chromedriver')
    max_attempts = 10
    
    # Initialise output dataframe
    df = pd.DataFrame(columns=['Instagram Handle', 'Follower Count'])
    
    # Get follower count for each Instagram handle and add to dataframe
    for insta_handle in insta_handles:
        # Loop until follower count successfully scraped or maximum number of attempts reached
        follower_count = -2
        i = 0
        while follower_count == -2:
            follower_count = get_follower_count_from_handle(insta_handle, browser)
            if i == max_attempts : follower_count = -1
            
        # Add to dataframe
        new_row = [insta_handle, follower_count]
        df.loc[df.shape[0] + 1] = new_row
    
    # Tidy up and return
    browser.quit()
    return df
    
def get_follower_counts_from_csv_list():
    # Using the pre-set csv list, returns a dataframe of contestant, handle, and follower count
    
    # Get list of Instagram handles from csv file
    df_in = pd.read_csv(insta_handles_csv)
    handles = list(df_in['Instagram Handle'])
    
    # Get follower count from Instagram handles
    df_out = pd.merge(df_in, get_follower_counts(handles), on='Instagram Handle')
    
    return df_out
    
def add_handle_to_csv(contestant_name, handle):
    # Adds the specified contestant and their Instagram handle to the csv file
    
    # Retrieve csv data as data frame
    df = pd.read_csv(insta_handles_csv)
    
    # Create and add new row
    new_row = [contestant_name, handle]
    df.loc[df.shape[0] + 1] = new_row

    # Save and return
    df.to_csv(insta_handles_csv, index=False)
    return
