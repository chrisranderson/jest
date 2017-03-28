import urllib2

from bs4 import BeautifulSoup

def fetch_url(url):
  return urllib2.urlopen(url).read()

def get_soup(url):
  return BeautifulSoup(fetch_url(url), 'lxml')

soup = get_soup('http://www.newsmax.com/Jokes/1785/')
