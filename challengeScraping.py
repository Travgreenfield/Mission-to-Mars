# Import Splinter, BeautifulSoup, and Pandas
#%%
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from flask import Flask, render_template
from flask_pymongo import PyMongo

#%%
def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)

    hemisphere_title = hemisphere_info(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "title": hemisphere_title,
        "img_url": hemisphere_image(browser),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def hemisphere_info(browser): 
    # Visit the mars nasa news site
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    
    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    hemisphere_soup = soup(html, 'html.parser')

    hemisphere_title = []
    
    for link in hemisphere_soup.find_all('h3').get_text():
        hemisphere_title.append(link)

    return hemisphere_title

def hemisphere_image(browser): 
    # Visit URL
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    
    base_url = 'https://astrogeology.usgs.gov'

    #Empty list to populate with links into hemisphere details
    hemisphere_links = []
    hemisphere_pics = []

    html = browser.html
    hemisphere_soup = soup(html, 'html.parser')
    
    for link in hemisphere_soup.find_all('div', {'class': 'description'}):
        hemisphere_links.append(link.a['href'])

    for path in hemisphere_links:
        browser.visit(f'{base_url}{path}')
        
        # Parse the resulting html with soup
        html = browser.html
        img_soup = soup(html, 'html.parser')
        
        try:
            # find the relative image url
            img_url_rel = img_soup.select_one('div.downloads ul li a').get("href")
        except AttributeError:
            return None

    # Use the base url to create an absolute url
    hemisphere_image = f'{base_url}{img_url_rel}'
    hemisphere_pics.append(hemisphere_image)
    
    return hemisphere_pics