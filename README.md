# Drag_Race_Followings
Development of machine learning models to:
  - Predict follower count of RuPaul's Drag Race contestants based on in-show metrics
  - Predict whether or not a contestant is selected for/wins RuPaul's Drag Race All Stars based on in-show metrics
Including web scrapers for collection of data from Instagram and Wikipedia.
All code written in Python with Spyder and Jupyter.

Components uploaded so far:
  - Web scraper (Python with selenium) to download follower count for a given Instagram handle ('Instagram_Web_Scrape.py')
  - Web scraper (Python with BeautifulSoup) to download episode metrics ('Wikipedia_Web_Scrape.py')
  - Functions to normalize and prepare data for All Stars analysis ('All_Stars_Data_Prep.py')
  - Functions to explore data and get common statistical output, such as correlations, p-values, and confusion matrices
    ('Explore_Data.py')
  - Jupyter Notebook for All Stars analysis ('What Makes an All Star?.ipynb')
