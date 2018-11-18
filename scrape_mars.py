import os
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd




def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return browser = Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()
    listings = {}

    listings["nasa"] = nasa()
    listings["jpl"] = jpl()
    listings["weather"] = weather()
    listings["facts"] = facts()
    listings["hemisphere"]= hemisphere()

    return listings

def nasa():
    browser = init_browser()
    nasanews = {}
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')
    results = soup.find('div', class_='list_text')

    news_title = results.find('div', class_='content_title').text
    news_p = results.find('div', class_='article_teaser_body').text

    nasanews["title"] = news_title
    nasanews["para"] = news_p

    return nasanews


def jpl():
    browser = init_browser()
    jplresults = {}
    jplurl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jplurl)
    html = browser.html
    soup = bs(html, 'html.parser')
    results = soup.find('article', class_='carousel_item')
    featured_image_url = 'https://www.jpl.nasa.gov' + results.find('a', class_="button fancybox")['data-fancybox-href']



    jplresults["url"] = featured_image_url

    return jplresults




def weather():
    browser = init_browser()
    latestweather = {}
    twitterurl = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitterurl)
    html = browser.html
    soup = bs(html, 'html.parser')

    results = soup.find('div', class_='js-tweet-text-container')
    mars_weather = results.find('p').text

    latestweather["weather"] = mars_weather

    return latestweather


def facts():

    browser = init_browser()
    marsfacts = {}
    marsfactsurl = 'https://space-facts.com/mars/'
    browser.visit(marsfactsurl)

    html = browser.html
    soup = bs(html, 'html.parser')
    results = soup.find_all('table')[0]


    df = pd.read_html(str(results))
    df = df[0]
    df.columns = ['x', 'Measurement']
    df.set_index('x', inplace=True)



    marsfacts = df.to_html()


    return marsfacts

facts()

def hemisphere():
    browser = init_browser()
    astrourl = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(astrourl)

    html = browser.html
    soup = bs(html, 'html.parser')

    results = soup.find_all('div', class_='description')
    hemisphere_image_urls = []
    for result in results:
        suburl = 'https://astrogeology.usgs.gov' + result.find('a')['href']
        browser.visit(suburl)
        html = browser.html
        soup = bs(html, 'html.parser')

        title = result.find('a').text


        subresult = soup.find('div', class_='downloads')
        img_url = subresult.find('a')['href']

        hemisphere_image_urls.append({"title": title, "img_url": img_url})


    return hemisphere_image_urls
