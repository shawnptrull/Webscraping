import re
import requests
from bs4 import BeautifulSoup
import lxml

class Content:
    def __init__(self, topic, url, title, body, base_url):
        self.topic = topic
        self.url = url
        self.title = title
        self.body = body
        self.base_url = base_url


    def print(self):
        print(f'New article found for topic: {self.topic.capitalize()}')
        print(f'URL: {self.base_url}{self.url}')
        print(f'TITLE: {self.title}')
        print(f'BODY: {self.body}')

class Website:
    def __init__(self, name, url, searchUrl, resultListing, resultUrl, absoluteUrl, titleTag, bodyTag):
        self.name = name
        self.url = url
        self.searchUrl = searchUrl
        self.resultListing = resultListing
        self.resultUrl = resultUrl
        self.absoluteUrl = absoluteUrl
        self.titleTag = titleTag
        self.bodyTag = bodyTag

class Crawler:
    def __init__(self):
        self.visited = []

    # Returns a BeautifulSoup object
    def getPage(self, url):
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'lxml')

    # Returns the text from selected tag
    def safeGet(self, pageObj, selector):
        childObj = pageObj.select(selector)
        if childObj is not None and len(childObj) > 0:
            if childObj[0].get_text() == "Discover Thomson Reuters":
                return childObj[3].get_text()
            return childObj[0].get_text()
        return ''

    # The action
    def search(self, topic, site):
        bs = self.getPage(site.searchUrl + topic)

        # Selects individual articles (resultListing)
        searchResults = bs.select(site.resultListing)

        # Iterates through each article
        for result in searchResults:

            # Attribute 'href' of the first <a> tag from an article
            url = result.select(site.resultUrl)[0].attrs['href']

            # Absolute/Relative filter
            if(site.absoluteUrl):
                bs = self.getPage(url)
            else:
                bs = self.getPage(site.url + url)
            if bs is None:
                print('Something was wrong with that page or URL. Skipping!')
                return

            # Returned strings from page elements
            title = self.safeGet(bs, site.titleTag)
            body = self.safeGet(bs, site.bodyTag)
            base_url = site.url

            # Dust in the wind filter
            if title != '' and body != '':

                # Replication avoidance filter
                if title not in self.visited:
                    self.visited.append(title)
                    content = Content(topic, url, title, body, base_url)
                    content.print()

crawler = Crawler()

'''
To add websites with similar html layout, insert list into siteData.
To add topic of interest, insert into "topics" list.
'''

siteData = [['Reuters', 'https://www.reuters.com', 'https://www.reuters.com/search/news?sortBy=&dateRange=&blob=', 'div.search-result-indiv', 'h3.search-result-title a', False, 'h1', 'p']]

sites = []
for row in siteData:
    sites.append(Website(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

topics = ['python', 'data science']
for topic in topics:
    print('\n')
    print('           ---------GETTING INFO ABOUT: ' + topic.capitalize() + '---------         ' + '\n')
    for targetSite in sites:
        crawler.search(topic, targetSite)