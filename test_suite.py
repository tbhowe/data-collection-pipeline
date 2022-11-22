#%%

import unittest
import rm_scraper
import requests
import time
import os
import pickle
import shutil


class ScraperTestCase(unittest.TestCase):
    '''Test suite for rm_scraper'''
    
    def setUp(self):
        self.property_search=rm_scraper.GetProperties('mevagissey')
        with open('test_property_dictionary.pickle', 'rb') as handle:
            self.example_property_data=pickle.load(handle)
            print(self.example_property_data[3]['id'])
        
        

    def test_get_searchpage(self):
        '''Test for the get_searchpage method
        
        Checks that the returned url is a string, has length >20 and is reachable'''
        self.property_search.get_search_page()
        print(self.property_search.listings_url)
        assert isinstance(self.property_search.listings_url, str)
        assert len(self.property_search.listings_url) >20
        assert self.__url_reachable(self.property_search.listings_url)
        self.__wait_and_close()

    def test_return_properties(self):
        # TODO: How to make this into a unit test not an integration test?
        self.property_search.get_search_page()
        self.property_search.property_info=[]
        assert not self.property_search.property_info
        self.property_search.return_properties()
        assert isinstance(self.property_search.property_info,list)
        assert isinstance(self.property_search.property_info[0],dict)
        assert isinstance(self.property_search.property_info[0]['id'],int)
        assert len(str(self.property_search.property_info[0]['id'])) >=8
        assert isinstance(self.property_search.property_info[0]['price'],int)
        self.__wait_and_close()

    def test_get_expanded_property_data(self):
        '''test for the get_expanded_property_data method'''
        test_property_number=3
        self.property_search.property_info = self.example_property_data
        entries_to_remove = ['price_history','address','image_url','record_timestamp']
        self.__remove_entries_from_dict(entries_to_remove,self.property_search.property_info)
        self.property_search.get_expanded_property_data(test_property_number)
        assert 'price_history' in self.property_search.property_info[test_property_number] # is price history returned?
        assert isinstance(self.property_search.property_info[test_property_number]["price_history"], list) # is price_history a list?
        assert isinstance(self.property_search.property_info[test_property_number]["price_history"][0], dict) # is the first entry in price_history a dict?
        assert 'address' in self.property_search.property_info[test_property_number] # check reverse geocode occurs
        assert isinstance(self.property_search.property_info[test_property_number]["address"], str) # check reverse geocode produces an address string
        assert isinstance(self.property_search.property_info[test_property_number]['image_url'],str) # check an image url is written to the info dict
        assert self.__url_reachable(self.property_search.property_info[test_property_number]['image_url']) # assert that the image url is reachable
        assert os.path.isfile( 'raw_data/property_images/property_'+ str(self.property_search.property_info[test_property_number]['id'])+'.jpeg') 
        assert isinstance(self.property_search.property_info[test_property_number]['record_timestamp'],str)
        self.__wait_and_close()

    def test_get_price_history(self):
        '''Test that the get_price_history method returns a dict'''
        test_property_number=1
        self.property_search.property_info = self.example_property_data
        entries_to_remove = ["price_history"]
        print( self.property_search.property_info[test_property_number].keys() )
        # self.__remove_entries_from_dict(entries_to_remove,self.property_search.property_info)
        self.property_search.driver.get(self.property_search.property_url_base + str(self.property_search.property_info[test_property_number]['id']))
        self.property_search.get_price_history(test_property_number)
        assert "price_history" in self.property_search.property_info[test_property_number]
        assert isinstance(self.property_search.property_info[test_property_number]["price_history"], list)
        assert isinstance(self.property_search.property_info[test_property_number]["price_history"][0], dict)
        self.__wait_and_close()

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

    def test_get_property_images(self):
        test_property_number=3
        self.property_search.property_info = self.example_property_data
        entries_to_remove = ['image_url']
        self.__remove_entries_from_dict(entries_to_remove,self.property_search.property_info)
        if os.path.exists("raw_data/property_images/"):
            shutil.rmtree("raw_data/property_images/")

        test_property_ID=self.property_search.property_info[test_property_number]["id"]
        self.property_search.driver.get(self.property_search.property_url_base + str(self.property_search.property_info[test_property_number]['id']))
        self.property_search.get_property_images(test_property_ID,test_property_number)
        assert isinstance(self.property_search.property_info[test_property_number]['image_url'],str) # check an image url is written to the info dict
        assert self.__url_reachable(self.property_search.property_info[test_property_number]['image_url']) # assert that the image url is reachable
        assert os.path.isfile( 'raw_data/property_images/property_'+ str(self.property_search.property_info[test_property_number]['id'])+'.jpeg') 
        self.__wait_and_close()

    def __wait_and_close(self):
        time.sleep(3)
        self.property_search.driver.quit()


    @staticmethod
    def __url_reachable(url):
        '''tests that a given URL is reachable - ie. returns status code 200'''
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

    @staticmethod
    def __remove_entries_from_dict(entries_to_remove,example_property_data):
        '''static method to remove entries from dict, given a dict and a list of keys'''
        for k in entries_to_remove:
            example_property_data[3].pop(k)



unittest.main(argv=[''], verbosity=0, exit=False)
# %%



# %%
