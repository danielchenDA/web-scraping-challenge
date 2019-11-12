from splinter import Browser
from bs4 import BeautifulSoup
from pprint import pprint

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path":"chromedriver.exe"}
    return Browser('chrome', **executable_path, headless = False)

def scrape():
    browser = init_browser()
    mars = {}
    # define url and launch url in chrome
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # convert browser to html and parse using BeautifulSoup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # use BeautifulSoup to find news title and paragraph and save to dictionary
    mars["news_title"] = soup.find('li', class_='slide').find('div', class_='content_title').a.text
    mars["news_p"] = soup.find('div', class_='article_teaser_body').text

    ### JPL Mars Space Images - Featured Image
    # define url and launch url in chrome
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # convert browser to html and parse using BeautifulSoup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    base_url = 'https://www.jpl.nasa.gov'

    # use BeautifulSoup to find required texts
    img_path = soup.find('footer').a['data-fancybox-href']

    #save to dictionary
    mars["featured_image_url"] = base_url + img_path

    ### Mars Weather
    # define url and launch url in chrome
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    # convert browser to html and parse using BeautifulSoup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # add to dictionary
    mars["mars_weather"] = soup.find('p', class_ = 'tweet-text').contents[0]

    ### Mars Facts
    # define url
    url = 'https://space-facts.com/mars/'
    # Use pandas to scrape any tabular data from the url
    import pandas as pd
    tables = pd.read_html(url)

    # Grab first table, rename columns, and reset the index
    df = tables[0]
    df.columns = ['FAQs', 'Mars Planet Profile']
    df.set_index('FAQs', inplace=True)

    # Convert the df to a html table
    html_table = df.to_html()
    mars_soup = BeautifulSoup(html_table, 'html.parser')

    # Loop through html and add to dictionary
    ct = 1
    for th, td in zip(mars_soup.tbody.select('th'), mars_soup.tbody.select('td')):
        mars[f'table_title_{ct}'] = th.text.strip()
        mars[f'table_info_{ct}'] = td.text.strip()
        ct = ct + 1
    ### Mars Hemispheres
    # define url and launch url in chrome
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # convert browser to html and parse using BeautifulSoup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    products_html = soup.find_all('div',class_='item')
    counter = 0
    #loop through each product result
    for tag in products_html:
        counter = counter + 1
        #click on appropriate link
        browser.click_link_by_partial_text(tag.h3.text)
        #define html to scrape
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        #add values to dictionary
        mars[f'hemisphere{counter}_image_urls'] = {"title": soup.find('h2', class_ = 'title').text.strip("Enhanced").strip(" "),
                    "img_url": soup.ul.a["href"]}
        #return to previous url
        browser.back()

    # listings["headline"] = soup.find("a", class_="result-title").get_text()
    # listings["price"] = soup.find("span", class_="result-price").get_text()
    # listings["hood"] = soup.find("span", class_="result-hood").get_text()
    return mars
