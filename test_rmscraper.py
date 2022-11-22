#%%

import unittest
import rm_scraper
import requests
import time
import pickle
import os
import datetime

class ScraperTestCase(unittest.TestCase):
    '''Test suite for rm_scraper'''
    
    def setUp(self):
        self.property_search=rm_scraper.GetProperties('mevagissey')
        self.test_listings_url='https://www.rightmove.co.uk/property-for-sale/find.html?searchType=SALE&locationIdentifier=REGION%5E17104&insId=1&radius=0.0&minPrice=200000&maxPrice=700000&minBedrooms=2&maxBedrooms=&displayPropertyType=houses&maxDaysSinceAdded=&_includeSSTC=on&sortByPriceDescending=&primaryDisplayPropertyType=&secondaryDisplayPropertyType=&oldDisplayPropertyType=&oldPrimaryDisplayPropertyType=&newHome=&auction=false'
        with open('test_property_dictionary.pickle', 'rb') as handle:
            self.example_property_data=pickle.load(handle)
            self.example_property_data=self.example_property_data[0:2]
            # print(self.example_property_data[0])
        
    def test_get_searchpage(self):
        '''Test for the get_searchpage method
        
        Checks that the returned url is a string, has length >20 and is reachable'''
        self.property_search.get_search_page()
        print(self.property_search.listings_url)
        assert isinstance(self.property_search.listings_url, str)
        assert len(self.property_search.listings_url) >20
        assert self.__url_reachable(self.property_search.listings_url)
        time.sleep(3)

    def test_return_properties(self):
        self.property_search.listings_url=self.test_listings_url
        self.property_search.property_info=[]
        assert self.__url_reachable(self.property_search.listings_url)
        assert not self.property_search.property_info
        self.property_search.return_properties()
        assert isinstance(self.property_search.property_info,list)
        assert isinstance(self.property_search.property_info[0],dict)
        assert isinstance(self.property_search.property_info[0]['id'],int)
        assert len(str(self.property_search.property_info[0]['id'])) >= 8
        assert isinstance(self.property_search.property_info[0]['price'],int)
        time.sleep(3)

    def test_get_expanded_property_data(self):
        self.property_search.get_search_page()
        self.property_search.return_properties()
        # self.property_search.property_info = self.example_property_data
        # # print('number of entries is'+ str( len(self.property_search.property_info )))
        # print("ID is" + str ( self.property_search.property_info[0]['id']))
        self.property_search.get_expanded_property_data()
        assert 'price_history' in self.property_search.property_info[0] # is price history returned as a dict?
        assert 'address' in self.property_search.property_info[0] # check reverse geocode occurs
        assert isinstance(self.property_search.property_info[0]["address"], str) # check reverse geocode produces an address string
        assert isinstance(self.property_search.property_info[0]['image_url'],str) # check an image url is written to the info dict
        assert self.__url_reachable(self.property_search.property_info[0]['image_url']) # assert that the image url is reachable
        assert os.path.isfile( 'raw_data/property_'+ str(self.property_search.property_info[0]['id'])+'.jpeg') 
        assert isinstance(self.property_search.property_info[0]['record_timestamp'],str)

    def test_reverse_geocode_address(self):
        ''' Test that the reverse geocode function returns an address field to the property_info dict, formatted as str'''
        self.property_search.property_info=[{"location": {
        "latitude": 50.269928,
        "longitude": -4.788661
        },}]
        property_number=0
        self.property_search.reverse_geocode_address(property_number)
        assert 'address' in self.property_search.property_info[0]
        assert isinstance(self.property_search.property_info[0]["address"], str)

    


    

    @staticmethod
    def __url_reachable(url):
        try:
            #Get Url
            get = requests.get(url)
            # if the request succeeds 
            if get.status_code == 200:
                return(True)
            else:
                return(False)

        except requests.exceptions.RequestException as e:
            # print URL with Errs
            raise SystemExit(f"{url}: is Not reachable \nErr: {e}")



unittest.main(argv=[''], verbosity=0, exit=False)
# %%



# %%
