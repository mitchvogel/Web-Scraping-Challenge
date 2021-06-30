# Jupyter Notebook Conversion to Python Script

# Dependencies and Setup
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# Set Executable Path & Initialize Chrome Browser
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# NASA Mars News Site Web Scraper
def mars_news(browser):
    # Visit the NASA Mars News Site
    url = "https://redplanetscience.com/"
    browser.visit(url)

    html = browser.html
    news_soup = BeautifulSoup(html, "html.parser")

    # Scrape the Latest News Title
    news_title = news_soup.find("div", {"class":"content_title"}).get_text()

    news_p = data = news_soup.find("div", {"class":"article_teaser_body"}).get_text()

    return news_title, news_p


# NASA JPL Site Web Scraper
def featured_image(browser):
    # Visit the NASA JPL Site
    url = "https://spaceimages-mars.com"
    browser.visit(url)

    # Use splinter to navigate the site and find the image url for the current Featured Mars Image
    full_image_button = browser.find_by_tag('a')
    full_image_button.click()

    # Parse Results HTML with BeautifulSoup
    html = browser.html
    image_soup = BeautifulSoup(html, "html.parser")

    image_url = image_soup.find("img", {"class":"headerimage"}).get("src")
    image_url

   # Use Base URL to Create Absolute URL
    featured_image_url = f"https://spaceimages-mars.com{image_url}"
    return featured_image_url


# Mars Facts Web Scraper
def mars_facts():
    # Visit the Mars Facts Site Using Pandas to Read
    mars_facts = pd.read_html("https://galaxyfacts-mars.com")[0]

    return mars_facts.to_html()(classes="table table-striped")


# Mars Hemispheres Web Scraper
def hemisphere(browser):
    # Visit the astrogeology Site
    url = "https://marshemispheres.com/"
    browser.visit(url)

    html = browser.html
    hemisphere_soup = BeautifulSoup(html, "html.parser")

    hemisphere_scrape_links = hemisphere_soup.body.find('div', class_='collapsible results')
    hemisphere_links = hemisphere_scrape_links.find_all('a',class_='itemLink product-item')
    hemisphere_links
        
    hemisphere_scrape_links = hemisphere_soup.body.find('div',class_='collapsible results')
    hemisphere_links = hemisphere_scrape_links.find_all('a',class_="itemLink product-item")
    hemisphere_image = []
    for link in hemisphere_links:
        img_dict = {}
        if link.h3 is None:
            link_path = link["href"]
            browser.visit(url+link_path)
            html = browser.html
            hemisphere_soup = BeautifulSoup(html, 'html.parser')
            title = hemisphere_soup.body.find('h2',class_="title").text
            hem_image = hemisphere_soup.body.find('img',class_='wide-image')['src']
            img_dict["title"] = title
            img_dict["img_url"] = url+hem_image
            hemisphere_image.append(img_dict)

    hemisphere_image
    
    return hemisphere_image


#################################################
# Main Web Scraping Bot
#################################################
def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    news_title, news_p = mars_news(browser)
    featured_image_url = featured_image(browser)
    facts = mars_facts()
    hemisphere_image = hemisphere(browser)

    data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": featured_image_url,
        "facts": facts,
        "hemispheres": hemisphere_image,
    }
    browser.quit()
    return data 

if __name__ == "__main__":
    print(scrape_all())

