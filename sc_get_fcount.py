# Import libraries

import requests # import the requests library
from bs4 import BeautifulSoup as bs # import Beautiful Soup
import re

# base URL to scrape
soundcloud_url='https://www.soundcloud.com/'


# list of artists to scrape data for
artists=['rrritalin','kanji','dave-shades','yeahhbuzz','samplejunkie']


# artist number - iterate in future version!
artist_number=3
# construct current artist URL
artist_url=str(soundcloud_url+artists[artist_number])

print(artists[artist_number])

# get webpage 
page = requests.get(artist_url)
html = page.text # Get the content of the webpage
soup = bs(html, 'html.parser') # Convert that into a BeautifulSoup object that contains methods to make the tag searcg easier
test=soup.find_all("script")
test2=re.search('\"followers_count\":[0-9]+',str(test[-8]))
follower_count=re.search('[0-9]+',test2.group()).group()
# print(test.dtype)
# test2=re.search('followers_count', test)
#  test2=test.find('\"followers_count\":[0-9]+')
# artist_info = soup.find_all("td")
print(follower_count)

# %%
