import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys
import glob
import errno
url = "https://www.economist.com/"

try:
    # Use existing html if it exists
    soup = BeautifulSoup(open("economist-homepage.html"), "html.parser")
except Exception:
    # Scrape page if html does not exist
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    with open("economist-homepage.html", "w") as file:
        file.write(str(soup))


class Article:
    """
    An article from The Economist.
    -All headline text with class = flytitle-and-title__title is scrapped and
    saved in headline variable.
    -Headline url with class = teaser__link is scrspped and saved in
    article_url variable.
    -Image url is scrapped and saved in img_url variable if it exists.
    """

    def __init__(self, html):
        self.headline = html.find(
            class_='flytitle-and-title__title').get_text()
        self.article_url = url+html.find(class_='teaser__link')['href']
        try:
            self.img_url = html.find('img')['src']
        except Exception:
            self.img_url = None

    def get_article(self):
        return {
            "headline": self.headline,
            "url": self.article_url,
            "image": self.img_url
        }


headlines = []

for html in soup.find_all(class_='teaser'):
    article = Article(html)
    headlines.append(article.get_article())

pd.DataFrame(headlines).to_csv("economist-homepage.csv", index=False)
