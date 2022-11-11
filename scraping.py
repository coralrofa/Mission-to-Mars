# Import Splinter and BeautifulSoup
import datetime as dt

import pandas as pd
from bs4 import BeautifulSoup as soup
from matplotlib.pyplot import title
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

# Set up function to hold dictionaries

def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    news_title, news_paragraph = mars_news(browser)
    hemisphere_image_urls = []
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": mars_hemispheres(browser),
        "last_modified": dt.datetime.now()
     }
    
    browser.quit()
    return data


def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        slide_elem.find('div', class_='content_title')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


# ## JPL Space Images Featured Image

def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    # try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None
    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url
    

# ## Mars Facts

def mars_facts():
    # try/except for error handling
    try:
        # scrae into df
        df = pd.read_html('http://space-facts.com/mars/')[0]
        
    except BaseException:
        return None
    
    # Assigning columns, and set 'description' as index 
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    #Convert back to HTML format, add bootstrap
    return df.to_html()

    # end the automated browsing session
    browser.quit() 


def mars_hemispheres(browser):
    # Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    
    # Create a list to hold the images and titles.
    hemisphere_image_urls = []
    
    for i in range (4):
        hemispheres = {}
        mars_hem_elem = browser.find_by_css('a.product-item h3')[i]
        mars_hem_elem.click()
        full_image_elem = browser.find_by_text('Sample')
        image_url = full_image_elem['href']
        title = browser.find_by_css('h2.title').text
        hemispheres["image_url"] = image_url
        hemispheres["title"] = title
        hemisphere_image_urls.append(hemispheres)
        browser.back()

        # Print the list that holds the dictionary of each image url and title
        return  hemisphere_image_urls

        # Quit the browser
        browser.quit()

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())

# Quit the browser
browser.quit()
   