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


'''
- Blundering homeowner hunting for keys accidentally traps his own arm in a toilet in bizarre video
  - handles: hunting for keys, trapped in toilet

- There's a crisp that looks just like Harambe \u2013 and it's selling for a staggering sum
  - chip like Harambe, selling for a lot

- New footage shows mystery green flash of light appear in sky leaving hundreds of residents baffled
  - flash of light
  - residents baffled

- Man allowed to take 30lbs of pancakes onto flight - because they were a present for his mum
  - 30lbs of pancakes, flight

- Dad has transformed his loft into an amazing shrine of Star Wars memorabilia from At-Ats to autographs
  - dad, shrine of star wars

- UK weather: Stunned onlookers film man swimming in giant waves as Storm Doris batters coast
  - swimming in giant waves

- Tiny frog last seen in 1962 found in the mountains of Zimbabwe.

- Enormous black hole chews star for a decade.

- Just some guys in England driving a tank to a gas station.

- This paper legit has a \u2018Squirrel of the month\u2019 and we\u2019re diggin\u2019 it.

- Everyone made the same joke about election night d\xe9j\xe0 vu after the Super Bowl.

- Steve Urkel\u2019s young neighbor on \u2018Family Matters\u2019 is all grown up.

- You'll never unlearn how many germs are on your water bottle.

- Bernie sanders responds to \u2018bizarre\u2019 fashion collection he inspired.

- A Cheeto that looks like Harambe is on eBay and can be yours for the low, low price of $100k.

-
'''
