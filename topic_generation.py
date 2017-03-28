import urllib2

from bs4 import BeautifulSoup
 
from censor import filter_strings

mirror_url = 'http://www.mirror.co.uk/news/weird-news/'
huff_url = 'https://twitter.com/HuffPostWeird'

def fetch_url(url):
  return urllib2.urlopen(url).read()

def get_headlines(url):
  soup = BeautifulSoup(fetch_url(url), 'lxml')
  headlines = []

  if url == mirror_url:
    for result in soup.find_all('strong'):
      headline = result.select('a')[0].get_text()
      headlines.append(headline)

  elif url == huff_url:
    for result in soup.find_all('p', class_="tweet-text"):
      text = result.get_text()
      headlines.append(text[:text.find('http')-1] + '.')

  return filter_strings(headlines)

def get_topics():
  return get_headlines(huff_url) #+ get_headlines(mirror_url)

if __name__ == '__main__':
  for topic in get_topics():
    print('topic', topic)
