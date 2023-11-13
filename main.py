import requests
import lxml
from bs4 import BeautifulSoup

class Content:
    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = body

def getPage(url):
    req = requests.get(url)
    return BeautifulSoup(req.text, 'lxml')

def scrapeToscrape(url):
    bs = getPage(url)
    titles = bs.select('h2')
    title = [title.text for title in titles]
    paragraphs = bs.select('p')
    body = [paragraph.text for paragraph in paragraphs]
    return Content(url, title, body)

url = 'https://toscrape.com'
content = scrapeToscrape(url)
print(content.title[0], '\n', content.body[0])
print('\n')
print(content.title[1], '\n', content.body[1])
