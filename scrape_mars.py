# Dependencies and Setup
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd

# Mac
executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
browser = Browser("chrome", **executable_path, headless=False)

# Windows
#executable_path = {"executable_path": "/Users/connor.roemelt/Downloads/chromedriver"}
# browser = Browser("chrome", **executable_path)

def scrape_info():
    mars_news()
    mars_image()
    mars_weather()
    mars_facts()
    mars_hemispheres()


def mars_news():
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    news_title = soup.find_all('div', class_='content_title')[1].get_text()
    news_p = soup.find('div', class_='article_teaser_body').get_text()
    output = [news_title, news_p]
    return output

def mars_image():
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    pic = soup.find('img', class_='thumb').get('src')
    pic_url = f'https://www.jpl.nasa.gov{pic}'
    return pic_url

def mars_weather():
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    mars_weather = soup.find("span", class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0").text
    return mars_weather

def mars_facts():
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    facts_table = pd.read_html(facts_url)
    mars_facts = facts_table[0]
    mars_facts.columns=['Description', 'Value']
    mars_facts.set_index("Description", inplace=True)
    return mars_facts

def mars_hemispheres():
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    hemisphere_image_urls = []

    page_list = soup.find('div', class_='result-list')
    pictures = page_list.find_all('div',class_='item')

    for picture in pictures:
        title = picture.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = picture.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup=bs(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_image_urls.append({"title": title, "img_url": image_url})

    return hemisphere_image_urls
