# -*- coding: utf-8 -*-

from selenium import webdriver

def get_follower_count(insta_handle, browser):
    # Returns
    
    # Get and navigate to URL
    url = url_prefix + insta_handle + '/'
    browser.get(url)
    
    # Get follower count displayed text (e.g. '931k', '1.1m')
    elems = browser.find_elements_by_tag_name("a")
    for elem in elems:
        if elem.text.endswith(' followers') : follower_count_text = elem.text[:len(elem.text) - len(' followers')]
    
    # Used displayed text to find actual underlying follower count (e.g. '931,083', '1,103,473')
    elems = browser.find_elements_by_tag_name('span')
    for elem in elems:
        if elem.text==follower_count_text : follower_count = elem.get_attribute('title')
        
    # Convert to integer and return
    follower_count = int(follower_count.replace(',', ''))
    return (follower_count)

# Initialise Instagram URL and browser object
url_prefix = 'https://www.instagram.com/'
browser = webdriver.Chrome("/usr/local/bin/chromedriver")

# Test with final four from season 11
for insta_handle in ['oddlyyvie', 'bhytes', 'mizakeriachanel', 'silkyganache']:
    print(insta_handle + ': ' + str(get_follower_count(insta_handle, browser)))

# Tidy up
browser.quit()