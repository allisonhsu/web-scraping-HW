from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
# import time


def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    #NASA Mars News

    url_1 = 'https://mars.nasa.gov/news/'
    browser.visit(url_1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    articles = soup.find_all('div', class_='list_text')

    for article in articles:
        news_title = article.find('div', class_= 'content_title').text
        news_p = article.find('div', class_= 'article_teaser_body').text

    #JPL Mars Space Images - Featured Image

    url_2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_2)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    pictures = soup.find_all('div', class_='img')

    for picture in pictures:
        link = picture.find('img')
        src = link['src']
        featured_image_url = 'https://www.jpl.nasa.gov/'+ src

    
    #Mars Weather

    url_3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_3)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    weathers = soup.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')

    for weather in weathers:
        mars_weather = weather.text
    
    #Mars Facts

    url_4 = 'https://space-facts.com/mars/'
    tables = pd.read_html(url_4)
    df = tables[0]
    df.columns = ['description','values']
    df.set_index ('description')
    html_table = df.to_html('mars facts')

    #Mars Hemispheres
    url_5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_5)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    hemispheres = soup.find_all('div', class_='item')
    hemisphere_image_urls = []

    for hemisphere in hemispheres:
        title = hemisphere.find('h3').text
        title = title.replace('Enhanced','')
        full_img_link = 'https://astrogeology.usgs.gov/' + hemisphere.find('a')['href']   
        browser.visit(full_img_link)
        html = browser.html
        soup=BeautifulSoup(html, 'html.parser')
        downloads = soup.find('div', class_='wide-image-wrapper')
        src_2 = downloads.find('img', class_ ='wide-image')['src']
        img_url = 'https://astrogeology.usgs.gov/' + src_2
        
        hemisphere_image_urls.append({"title": title, "img_url": img_url})


    mars_dict = {"news_title":news_title,"news_p":news_p,"featured_image_url":featured_image_url,
    "mars_weather":mars_weather,"html_table":html_table,"hemisphere_image_urls":hemisphere_image_urls}

    browser.quit()

    return mars_dict