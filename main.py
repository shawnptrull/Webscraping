import re

class Content:
    def __init__(self, topic, url, title, body):
        self.topic = topic
        self.url = url
        self.title = title
        self.body = body

    def print(self):
        print(f'New article found for topic: {self.topic.capitalize()}')
        print(f'URL: {self.url}')
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

import requests
from bs4 import BeautifulSoup
import lxml

class Crawler:

    def getPage(self, url):
        #Returns a BeautifulSoup object
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'lxml')

    def safeGet(self, pageObj, selector):
        #Returns the text from selected tag
        childObj = pageObj.select(selector)
        if childObj is not None and len(childObj) > 0:
            if childObj[0].get_text() == "Discover Thomson Reuters":
                return childObj[3].get_text()
            return childObj[0].get_text()
        return ''

    def search(self, topic, site):

        #Creates BeautifulSoup object that uses search-bar url to look up topic
        bs = self.getPage(site.searchUrl + topic)

        # Creates a list of "results/sections" from a url
        searchResults = bs.select(site.resultListing)

        # Iterates through each item on list of "results/sections"
        for result in searchResults:

            # Create a var that is the attribute 'href' of the first <a> tag from "result/section"
            url = result.select(site.resultUrl)[0].attrs['href']

            # Checks to see if it is relative url or absolute. If relative, adds base url to beginning. If none, prints something then returns nothing.
            if(site.absoluteUrl):
                bs = self.getPage(url)
            else:
                bs = self.getPage(site.url + url)
            if bs is None:
                print('Something was wrong with that page or URL. Skipping!')
                return

            # Puts 2 returned strings into variables
            title = self.safeGet(bs, site.titleTag)
            body = self.safeGet(bs, site.bodyTag)

            global t_lst
            global b_lst

            # Checks variables to see if they have anything. If they do, it prints the topic, url, title, and body.
            if title != '' and body != '':
                if title not in t_lst or body not in b_lst:
                    t_lst.append(title)
                    b_lst.append(body)
                    content = Content(topic, url, title, body)
                    content.print()

t_lst = []
b_lst = []

crawler = Crawler()

siteData = [['Reuters', 'https://www.reuters.com', 'https://www.reuters.com/search/news?sortBy=&dateRange=&blob=', 'div.search-result-indiv', 'h3.search-result-title a', False, 'h1', 'p']]

sites = []
for row in siteData:
    sites.append(Website(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

topics = ['python', 'data science']
for topic in topics:
    print('           ---------GETTING INFO ABOUT: ' + topic.capitalize() + '---------         ' + '\n')
    for targetSite in sites:
        crawler.search(topic, targetSite)