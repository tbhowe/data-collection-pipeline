#%%
# import libraries
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

import re
from bs4 import BeautifulSoup as bs # import Beautiful Soup
import requests
import json
import time

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
        self.property_info=None
        self.property_url_base="https://www.rightmove.co.uk/properties/"
        

    def get_search_page(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.base_url)
        time.sleep(1)

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

 # Function to acquire basid info regarding the properties on the search page
    def return_properties(self):
        r = requests.get(self.listings_url)
        if r.status_code == 200:
            search_term = '<script>window.jsonModel = '
            body = r.content.decode('utf-8')
            left_idx = body.find(search_term)
            right_idx = body.find('</script>', left_idx)
            offset = len(search_term)
            data_str = body[left_idx + offset:right_idx]
            # data holds the 'data model' of the page. All of the info to populate the "property card is in there"
            data = json.loads(data_str)
            property_array = data['properties']
            properties_dict=[]
            counter=0
            for entry in property_array:
                id = entry['id']
                price = entry['price']['amount']
                bedrooms=entry['bedrooms']
                bathrooms=entry['bathrooms']
                location=entry['location']
                properties_dict.append({ "id" : id, "price" : price , "bedrooms" : bedrooms, "bathrooms" : bathrooms, "location" : location})
            self.property_info=properties_dict
        return()

    def nav_to_property_page(self,prop_ID):
        self.driver.get(self.property_url_base + str(prop_ID) )
        print( "navigating to: " + str(self.driver.current_url))
        return()

    def accept_cookies(self):
        # driver=self.driver
        delay = 10
        try:
            WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@class="optanon-alert-box-wrapper  "]')))
            print("cookiebox Ready!")
            
            try:
                # self.driver.switch_to.alert('gdpr-consent-notice')
                accept_cookies_button = self.driver.find_element(by=By.XPATH, value='//button[@title="Allow all cookies"]')
                
                print(accept_cookies_button.get_attribute("class"))
                # accept_cookies_button.click()
                WebDriverWait(self.driver, delay).until(EC.element_to_be_clickable((By.XPATH, '//button[@title="Allow all cookies"]')))
                accept_cookies_button.click()
                time.sleep(1)
            except NoSuchElementException:
                print("box isn't there")
            
        except TimeoutException:
            print("Loading took too much time!")
            return()
        
        

# RUN CODE
property_search=GetProperties('mevagissey')
property_search.get_search_page()
property_search.return_properties()
prop_ID=property_search.property_info[1]["id"]
property_search.nav_to_property_page(prop_ID)
property_search.accept_cookies()

# price_history_button=property_search.driver.find_element(by=By.XPATH, value='//*[@id="root"]/main/div/div[2]/div/div[13]/button')
# price_history_button.click()
# price_history_div=property_search.driver.find_element(by=By.XPATH, value='//*[@id="root"]/main/div/div[2]/div/div[13]/div/div[2]/table/tbody')


# %%
