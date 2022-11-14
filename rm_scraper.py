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


import requests
import shutil
import json
import time
import os
import datetime

# import geopy - will need this for a later method.


class GetProperties:

    def __init__(self, property_area,opts=None): 
        # required: property_area (string) - place or postcode of search area
        #optional: opts (dict with elements: min_price, max_price, property_type, min_bedrooms )
        self.property_area=property_area
        self.property_url_base='https://www.rightmove.co.uk/properties/'
        self.base_url='https://www.rightmove.co.uk/'
        self.opts={'min_price' :'200,000', 
                'max_price' : '700,000',
                'property_type' : 'Houses',
                'min_bedrooms' : 2,
                }
        accepted_opts=list(self.opts.keys())
        if opts:
            for opt in opts:
                if opt in accepted_opts:
                    self.opts[opt]=opts[opt]

                else:
                    raise ValueError(f"Invalid Option: {opt}")

            self.opts.update(opts)

        self.driver=None
        self.listings_url=None
        self.property_ids=None
        self.property_info=None
        if __name__ == "__main__" :
            
            self.get_search_page()
            self.return_properties()
            self.get_expanded_property_data()
            self.save_property_data()

        

    def get_search_page(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.base_url)
        time.sleep(1)
        # finds the inputfield on the front page
        search_box_path = self.driver.find_element(by=By.XPATH, value='//*[@name="typeAheadInputField"]')
        search_box_path.send_keys(self.property_area)
        search_box_path.send_keys(Keys.ENTER)
        # finds the inputfields - TIDY THIS INTO LOOP when sorted
        min_price_dropdown = Select(self.driver.find_element(by=By.XPATH, value='//*[@name="minPrice"]'))
        max_price_dropdown = Select(self.driver.find_element(by=By.XPATH, value='//*[@name="maxPrice"]'))
        property_type_dropdown = Select(self.driver.find_element(by=By.XPATH, value='//*[@name="displayPropertyType"]'))
        min_bedrooms_dropdown = Select(self.driver.find_element(by=By.XPATH, value='//*[@name="minBedrooms"]'))
        # select by visible text
        min_price_dropdown.select_by_visible_text(self.opts['min_price'])
        max_price_dropdown.select_by_visible_text(self.opts['max_price'])
        property_type_dropdown.select_by_visible_text(self.opts['property_type'])
        min_bedrooms_dropdown.select_by_visible_text(self.opts['min_bedrooms'])
        # find submit button
        submit_button=self.driver.find_element(by=By.XPATH, value='//*[@id="submit"]')
        submit_button.click()
        self.listings_url=self.driver.current_url
        

    # Function to acquire basid info regarding the properties on the search page, and store them in a dictionary
    def return_properties(self):
        r = requests.get(self.listings_url)
        if r.status_code == 200: # checks request completed successfully
            # This code parses the json on each property page and stores the infromation in a list of dictionaries
            search_term = '<script>window.jsonModel = '
            body = r.content.decode('utf-8')
            left_idx = body.find(search_term)
            right_idx = body.find('</script>', left_idx)
            offset = len(search_term)
            data_str = body[left_idx + offset:right_idx]
            data = json.loads(data_str)
            property_array = data['properties']
            properties_dict=[]
            for entry in property_array:
                id = entry['id']
                price = entry['price']['amount']
                bedrooms=entry['bedrooms']
                bathrooms=entry['bathrooms']
                location=entry['location']
                properties_dict.append({ "id" : id, "price" : price , "bedrooms" : bedrooms, "bathrooms" : bathrooms, "location" : location})

            self.property_info=properties_dict

    # Function for navigating to the page of an individual property
    def nav_to_property_page(self,property_ID):
        self.driver.get(self.property_url_base + str(property_ID) )
        print( "navigating to: " + str(self.driver.current_url))
        return()

    # Function to accept cookies on individual property page
    def accept_cookies(self):
        delay = 5
        try:
            WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@class="optanon-alert-box-wrapper  "]')))
            print("cookiebox Ready!")
            try:
                accept_cookies_button = self.driver.find_element(by=By.XPATH, value='//button[@title="Allow all cookies"]') # finds accept cookies button
                WebDriverWait(self.driver, delay).until(EC.element_to_be_clickable((By.XPATH, '//button[@title="Allow all cookies"]'))) # wait until clickable
                self.driver.execute_script("arguments[0].click();", accept_cookies_button)
                time.sleep(1)

            except NoSuchElementException:
                print("cookie button not present")
            
        except TimeoutException:
            print("No GDPR cookie box appeared!")
    
    
    # Function to scrape the price history from a property page
    def get_price_history(self,list_index):
        price_history_button=self.driver.find_element(by=By.XPATH, value='//*[@id="root"]/main/div/div[2]/div/div[14]/button')
        price_history_button.click()
        time.sleep(4)
        try:
            price_history_table=self.driver.find_element(by=By.TAG_NAME, value='table') 
            price_history=[]

            for row in price_history_table.find_elements(by=By.CSS_SELECTOR, value='tr')[1:]:
                price_history_element=row.find_elements(by=By.TAG_NAME, value='td')
                price_history.append({price_history_element[0].text : price_history_element[1].text})

            self.property_info[list_index]['price_history']= price_history

        except NoSuchElementException:
                print('no sale price history')
        
    
    # Function to navigate to an individual property page, and get the property image and price history.
    def get_expanded_property_data(self):
        print( 'properties found: ' + str(len(self.property_info )))
        for property_number in range(4): # range(len(self.property_info )):
            print('extracting more data for property: '+ str(property_number))
            property_ID=self.property_info[property_number]["id"]
            print('property ID: ' + str(property_ID))
            self.nav_to_property_page(property_ID)
            self.get_price_history(property_number)
            self.get_property_images(property_ID,property_number)

    # def get_property_image(self):
    def get_property_images(self,property_ID,list_index):
        self.nav_to_property_page(property_ID)
        self.driver.find_element(by=By.XPATH, value='//*[@id="root"]/main/div/article/div/div[1]/div[1]/section').click()
        time.sleep(2)
        first_image_url=self.driver.find_element(by=By.XPATH, value='//img').get_attribute("src")
        print(first_image_url)
        self.property_info[list_index]['image_url']= first_image_url
        self.property_info[list_index]['record_timestamp']=datetime.datetime.fromtimestamp(time.time()).strftime('%c')
        image_data = requests.get(first_image_url, stream = True)
        if os.path.exists("raw_data/property_images/")==False:
            os.makedirs("raw_data/property_images/")

        image_file_name=str("raw_data/property_images/property_" + str(property_ID) + ".jpeg")
        if image_data.status_code == 200:
            with open(image_file_name,'wb') as f:
                shutil.copyfileobj(image_data.raw, f)

            print('Image sucessfully Downloaded: ', image_file_name)

        else:
            print('Image Couldn\'t be retrieved')
    
    def save_property_data(self):

        if os.path.exists("raw_data/property_data/")==False:
            os.makedirs("raw_data/property_data/")

        for property_number in range(len(self.property_info )):
            property_ID=self.property_info[property_number]["id"]
            dict_file_path=str("raw_data/property_data/property_" + str(property_ID) + ".json")
            with open(dict_file_path, 'w+') as f:
                json.dump(self.property_info[property_number], f, sort_keys=True, indent=4)
            
    


# RUN CODE

opts={'min_price' :'300,000', 
    'max_price' : '700,000',
    'property_type' : 'Houses',
    'min_bedrooms' : '2',
    }
    
property_search=GetProperties('mevagissey',opts)





# %%
