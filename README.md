# RuPaul's Drag Race: What Makes an All Star?
Development of machine learning models to predict whether or not a contestant is selected for/wins RuPaul's Drag Race All Stars based on in-show metrics

Includes web scrapers for collection of data from Instagram and Wikipedia.
All code written in Python with Spyder and Jupyter.

Components uploaded so far:
  - Web scraper (Python with selenium) to download follower count for a given Instagram handle ('Instagram_Web_Scrape.py')
  - Web scraper (Python with BeautifulSoup) to download episode metrics ('Wikipedia_Web_Scrape.py')
  - Functions to normalize and prepare data for All Stars analysis ('All_Stars_Data_Prep.py')
  - Functions to explore data and get common statistical output, such as correlations, p-values, and confusion matrices
    ('Explore_Data.py')
  - Jupyter Notebook for All Stars analysis ('What Makes an All Star?.ipynb')

To view the analysis, read the "What Makes an All Star?.ipynb" Jupyter Notebook. This was compiled shortly after the cast of All Stars Season 5 was announced.
The analysis is supplemented by provided .csv files, as well as the Python modules used to scrape data from the web.
Issues may occur over time as people edit the Wikipedia page in a way that the 'Wikipedia_Web_Scrape.py' module was not designed to process.
