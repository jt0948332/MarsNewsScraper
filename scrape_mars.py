def scrape():
        #dependencies
    from bs4 import BeautifulSoup as bs
    import splinter
    import requests
    from splinter import Browser
    import time
    import pandas as pd
    from selenium import webdriver
    import os
    import pymongo
    import json

    #The dictionary
    mars_facts_data={}

    #1
    #emulate the browser and get the html
    executable_path = {'executable_path': 'C:/chromedriver/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)
    #url to visit
    url='https://mars.nasa.gov/news/'
    #we need to use the browser to visit the page because there are many elements that do not load until the page is loaded.
    #requests would only get the raw html.
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    news_p =soup.select_one("div.rollover_description_inner")
    news_title = soup.select_one("div.content_title")
    news_p = news_p.text
    news_title = news_title.text
    mars_facts_data['news_title'] = news_title
    mars_facts_data['news_paragraph'] = news_p

    #2
    executable_path = {'executable_path': 'C:/chromedriver/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser.visit(url)

    browser.click_link_by_id('full_image')
    time.sleep(3)
    browser.click_link_by_partial_text('more info')
    time.sleep(3)

    time.sleep(3)
    browser.click_link_by_partial_href('/spaceimages/images/')
    #Download the image and Store
    response = requests.get(browser.url)
    if response.status_code == 200:
        linkname= (browser.url.rsplit('/', 1)[-1])
        SaveFile = (f'Resources/{linkname}')
        with open(SaveFile, 'wb') as f:
            f.write(response.content)
    print(browser.url)
    Space_image_dict = {}
    Space_image_dict['Url'] = browser.url
    mars_facts_data['featured_image'] = browser.url
    #collection.insert_one(Space_image_dict)

    #3
    mars_weather_dict = {}
    url='https://twitter.com/marswxreport?lang=en'
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    mars_weather = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    mars_weather =mars_weather.strip()
    mars_facts_data['weather'] = mars_weather
    mars_facts_data
    #collection.insert_one(mars_weather_dict)

    #4
    url = 'https://space-facts.com/mars/'
    df = pd.read_html(url)
    #df = pd.DataFrame(df)
    df= df[0]
    df.columns = ['Category', 'Measure']
    df.set_index('Category',inplace = True)
    mars_html_table = df.to_html()
    mars_html_table = mars_html_table.replace("\n","")
    mars_facts_data['mars_facts_table'] = mars_html_table
    return mars_facts_data