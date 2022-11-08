#%%
# import libraries
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import re
from bs4 import BeautifulSoup as bs # import Beautiful Soup
import requests
import json
import pprint

class GetProperties:
    def __init__(self,property_area):
        self.property_area=property_area
        self.base_url="https://www.rightmove.co.uk/"
        self.min_price="200,000"
        self.max_price="700,000"
        self.property_type='Houses'
        self.min_bedrooms="2"
        self.driver=None
        self.listings_url=None
        self.property_ids=None
        self.property_url_base="https://www.rightmove.co.uk/properties/"
        

    def get_search_page(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.base_url)

        # finds the inputfield on the front page!
        search_box_path = self.driver.find_element(by=By.XPATH, value='//*[@name="typeAheadInputField"]')
        # finds the for sale button
        for_sale_button_path =self.driver.find_element(by=By.XPATH,value='//*[@id="_3OuiRnbltQyS534SB4ivLV"]')
        #fill in search box
        search_box_path.send_keys(self.property_area)
        search_box_path.send_keys(Keys.ENTER)
        
        # finds the inputfields - TIDY THIS INTO LOOP when sorted
        min_price_dropdown = Select(self.driver.find_element(by=By.XPATH, value='//*[@name="minPrice"]'))
        max_price_dropdown = Select(self.driver.find_element(by=By.XPATH, value='//*[@name="maxPrice"]'))
        property_type_dropdown = Select(self.driver.find_element(by=By.XPATH, value='//*[@name="displayPropertyType"]'))
        min_bedrooms_dropdown = Select(self.driver.find_element(by=By.XPATH, value='//*[@name="minBedrooms"]'))
        # select by visible text
        min_price_dropdown.select_by_visible_text(self.min_price)
        max_price_dropdown.select_by_visible_text(self.max_price)
        property_type_dropdown.select_by_visible_text(self.property_type)
        min_bedrooms_dropdown.select_by_visible_text(self.min_bedrooms)

        # find submit button
        submit_button=self.driver.find_element(by=By.XPATH, value='//*[@id="submit"]')
        submit_button.click()
        self.listings_url=self.driver.current_url
        return()

    def return_property_ids(self):
        listings=self.driver.find_elements(by=By.XPATH, value="//a[contains(@href, 'properties')]")
        links = [elem.get_attribute('href') for elem in listings] # get hrefs from the <a> tags in listings
        property_id_list=[]
        for i in range(len(links)):
            property_id_list.append ( re.findall(r'\d+',links[i]) ) # make a list of all the numerical parts of each href

        property_ids=[x for x in property_id_list if len(x) < 2] #get rid of instances where there is more than one numeric
        self.property_ids=list(set([''.join(i) for i in property_ids]) )# return uniques
       


# RUN CODE
property_search=GetProperties('mevagissey')
property_search.get_search_page()
property_search.return_property_ids()

# test_property_url=str(property_search.property_url_base + property_search.property_ids[1])
test_property_url=property_search.listings_url
r = requests.get(test_property_url)
if r.status_code == 200:
    search_term = '<script>window.jsonModel = '
    body = r.content.decode('utf-8')
    left_idx = body.find(search_term)
    right_idx = body.find('</script>', left_idx)
    offset = len(search_term)
    data_str = body[left_idx + offset:right_idx]
    # data holds the 'data model' of the page. the prices are there as well
    data = json.loads(data_str)
    props = data['properties']
    properties_dict=[]
    counter=0
    for entry in props:
        id = entry['id']
        price = entry['price']['amount']
        bedrooms=entry['bedrooms']
        bathrooms=entry['bathrooms']
        location=entry['location']
        properties_dict.append({ "id" : id, "price" : price , "bedrooms" : bedrooms, "bathrooms" : bathrooms, "location" : location})
        
    print(properties_dict)