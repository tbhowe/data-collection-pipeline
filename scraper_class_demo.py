# Import libraries

import requests # import the requests library
from bs4 import BeautifulSoup as bs # import Beautiful Soup
import re # import the python default regex library

# =====  Define Scraper class and add constructor + methods. =====
class Scraper():

        def __init__(self,ntokens):
            self.scrape_url='https://www.coingecko.com' #website url
            self.ntokens=ntokens # number of tokens to scrape
        
        def get_webpage(self):
            page = requests.get(self.scrape_url) #get the website frontpage
            html = page.text # Get the content of the webpage
            soup = bs(html, 'html.parser') # Convert that into a BeautifulSoup object that contains methods to make the tag searcg easier
            return(soup)

        def process_elements_into_array(self,soup):
            My_table = soup.find("table",{"class":"table"})
            token_rows = My_table.find_all('tr')
            token_data=[]
            for row in token_rows:
                cols = row.find_all('td') # find all table boxes in a given row
                cols = [ele.text.strip() for ele in cols] # get the text for that element
                token_data.append([ele for ele in cols if ele]) # Get rid of empty values
            return(token_data)

        def create_list_of_dicts(self,token_data):
            token_dicts=[]
            for itoken in range(1,self.ntokens):
                
                name_field_split=re.split("\n", token_data[itoken][1])
                thisdict={'name': name_field_split[0], 
                            'abbrev': name_field_split[-1], 
                            'price': token_data[itoken][2],
                            'vol24h': token_data[itoken][6],
                            'mcap': token_data[itoken][7],
                            }
                token_dicts.append(thisdict)
            return(token_dicts)

# ===== Create and instance of Scraper and run the code ======
scraper_instance = Scraper(30)
soup = scraper_instance.get_webpage()
token_data = scraper_instance.process_elements_into_array(soup)
token_dictionary=scraper_instance.create_list_of_dicts(token_data)

# print an example token from the list, to confirm functionality
print(token_dictionary[0])

print(token_dictionary[1])

print(token_dictionary[2])

