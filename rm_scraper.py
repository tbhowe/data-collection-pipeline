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
# from bs4 import BeautifulSoup as bs # import Beautiful Soup - no longer needed. Delete later.
import requests
import json
import time
# import geopy - will need this for a later method.

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
        
        if __name__ == "__main__" :
            self.get_search_page()
            self.return_properties()
            self.get_expanded_property_data()
            pass
        else:
            pass
        

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
        delay = 5
        try:
            WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@class="optanon-alert-box-wrapper  "]')))
            print("cookiebox Ready!")
            
            try:
                # self.driver.switch_to.alert('//*[@class="optanon-alert-box-wrapper  "]') # throws noAlertPresent exception
                accept_cookies_button = self.driver.find_element(by=By.XPATH, value='//button[@title="Allow all cookies"]') # finds accept cookies button
                #print(accept_cookies_button.get_attribute("class")) # proves correct element selected
                # accept_cookies_button.click() # this fails - ElementClickInterceptedException
                WebDriverWait(self.driver, delay).until(EC.element_to_be_clickable((By.XPATH, '//button[@title="Allow all cookies"]'))) # wait until clickable
                # accept_cookies_button.click() # still fails with ElementClickInterceptedException
                self.driver.execute_script("arguments[0].click();", accept_cookies_button)
                time.sleep(1)
            except NoSuchElementException:
                print("cookie button not present")
            
        except TimeoutException:
            print("No GDPR cookie box appeared!")
            return()
    
    def get_price_history(self,prop_elem):
        price_history_button=self.driver.find_element(by=By.XPATH, value='//*[@id="root"]/main/div/div[2]/div/div[14]/button')
        price_history_button.click()
        time.sleep(4)
        try:
            price_history_table=self.driver.find_element(by=By.TAG_NAME, value='table')
            # handle exception - NoSuchElementException 
            price_history=[]
        
            for row in price_history_table.find_elements(by=By.CSS_SELECTOR, value='tr')[1:]:
                price_history_element=row.find_elements(by=By.TAG_NAME, value='td')
                price_history.append({price_history_element[0].text : price_history_element[1].text})
            self.property_info[3]['price_history']= price_history
        except NoSuchElementException:
                print('no sale price history')
        return()
    
    def get_expanded_property_data(self):
        print( 'properties found: ' + str(len(self.property_info )))
        for property_number in range(len(self.property_info )):
            print('extracting more data for property: '+ str(property_number))
            prop_ID=self.property_info[property_number]["id"]
            print('property ID: ' + str(prop_ID))
            self.nav_to_property_page(prop_ID)
            # self.accept_cookies()
            self.get_price_history(property_number)
            time.sleep(2)
        return()

# RUN CODE
property_search=GetProperties('mevagissey')
# property_search.get_search_page()
# property_search.return_properties()
# property_search.get_expanded_property_data()


#%%



