#%%
# import libraries
from geopy.geocoders import Nominatim
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import datetime
import json
import os
import requests
import shutil
import time



# import geopy - will need this for a later method.


class GetProperties:
    '''Collect property listings for a location on Rightmove.co.uk
        
    This module runs a property search on rightmove.co.uk, 
    using the location specified in the "property_area" argument. It collects 
    data on each property listing in the search results, and downloads the data on each 
    property into a dictionary, which is writtento a .json file. 
    The first image on each property page is also saved as a jpeg with filename "property_"+[property_id]+".jpeg".

    Example output:

        {
        "address": "Harbour Reach, Tregoney Hill, Mevagissey, Cornwall, England, PL26 6RD, United Kingdom",
        "bathrooms": 2,
        "bedrooms": 4,
        "id": 127546982,
        "image_url": "https://media.rightmove.co.uk/248k/247442/127546982/247442_HSA-13055831_IMG_14_0000.jpeg",
        "location": {
            "latitude": 50.270049,
            "longitude": -4.787646
        },
        "price": 450000,
        "price_history": [
            {"2015": "210,000"},
            {"2010": "200,000"}
        ],
        "record_timestamp": "Mon Nov 14 14:26:16 2022"
        }
   
    Search options can be supplied in the form of a dictionary, with fields
    {min_price,max_price,property_type,min_bedrooms}. In the case where no 
    option is supplied, internal defaults will be used.



        
        
        
        '''

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
        '''Method to open the search page on rightmove.co.uk '''
        self.driver = webdriver.Chrome()
        self.driver.get(self.base_url)
        time.sleep(1)
        # finds the inputfield on the front page
        search_box_path = self.driver.find_element(by=By.XPATH, value='//*[@name="typeAheadInputField"]')
        search_box_path.send_keys(self.property_area)
        search_box_path.send_keys(Keys.ENTER)
        # finds the inputfields - TIDY THIS INTO LOOP when sorted
        self.find_and_fill_webform()
        self.listings_url=self.driver.current_url

    def find_and_fill_webform(self):
        '''Method to fill in the property search form on rightmove.co.uk '''

        data_names={'min_price': "minPrice", 
                    "max_price": "maxPrice", 
                    "property_type": "displayPropertyType", 
                    "min_bedrooms": "minBedrooms"
                    }
        for field_element in data_names.keys():
            print(data_names[field_element])
            Select(self.driver.find_element(by=By.XPATH, value="//*[@name='" +data_names[field_element]+"']")).select_by_visible_text(self.opts[field_element])

        self.driver.find_element(by=By.XPATH, value='//*[@id="submit"]').click()
        
    def return_properties(self):
        '''Method to collect the property listings from the search page on rightmove.co.uk '''

        r = requests.get(self.listings_url)
        if r.status_code == 200: # checks request completed successfully
            # This code parses the json on each property page and stores the infromation in a list of dictionaries
            search_term = '<script>window.jsonModel = '
            body = r.content.decode('utf-8')
            left_idx = body.find(search_term)
            right_idx = body.find('</script>', left_idx)
            offset = len(search_term)
            data_string = body[left_idx + offset:right_idx]
            data = json.loads(data_string)
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

        
    def get_expanded_property_data(self):
        '''Method to scrape additional data from the individual propety pages. '''

        print( 'properties found: ' + str(len(self.property_info )))
        for property_number in range(len(self.property_info )):
            print('extracting more data for property: '+ str(property_number))
            property_ID=self.property_info[property_number]["id"]
            self.nav_to_property_page(property_ID)
            # self.accept_cookies()
            self.get_price_history(property_number)
            self.reverse_geocode_address(property_number)
            self.get_property_images(property_ID,property_number)

    
    def nav_to_property_page(self,property_ID):
        '''Method to navigate to an individual property's url, given its ID '''

        self.driver.get(self.property_url_base + str(property_ID) )
        print( "navigating to: " + str(self.driver.current_url))
        return()

    
    def accept_cookies(self):
        '''Method to accept the GFPR cookies on an individual property page '''

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
    
    
    
    def get_price_history(self,list_index):
        '''Method to accept the price history from an individual property page '''

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
    
    def reverse_geocode_address(self,property_number):
        '''Method to retrieve postal address from Lat and Long data '''

        locator = Nominatim(user_agent='OSM')
        coordinates = str(self.property_info[property_number]["location"]["latitude"]) +','+str(self.property_info[property_number]["location"]["longitude"])
        location = locator.reverse(coordinates)
        self.property_info[property_number]["address"]=location.address

    def get_property_images(self,property_ID,list_index):
        '''Method to retrieve the first image associated with each property listing '''
        
        self.nav_to_property_page(property_ID)
        self.driver.find_element(by=By.XPATH, value='//*[@id="root"]/main/div/article/div/div[1]/div[1]/section').click()
        time.sleep(2)
        first_image_url=self.driver.find_element(by=By.XPATH, value='//img').get_attribute("src")
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
        '''Method to save the scraped data dictionary for each property as a .json '''

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
