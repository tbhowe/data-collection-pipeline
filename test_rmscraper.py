#%%

import unittest
import rm_scraper
import requests
import time
import os
import pickle

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
        time.sleep(3)

    def test_return_properties(self):
        # ISSUE: How to make this into a unit test not an integration test?
        self.property_search.get_search_page()
        self.property_search.property_info=[]
        assert not self.property_search.property_info
        self.property_search.return_properties()
        assert isinstance(self.property_search.property_info,list)
        assert isinstance(self.property_search.property_info[0],dict)
        assert isinstance(self.property_search.property_info[0]['id'],int)
        assert len(str(self.property_search.property_info[0]['id'])) >=8
        assert isinstance(self.property_search.property_info[0]['price'],int)
        time.sleep(3)

    def test_get_expanded_property_data(self):
        test_property_number=3
        self.property_search.property_info = self.example_property_data
        print("ID is" + str ( self.property_search.property_info[test_property_number]['id']))
        entries_to_remove = ['price_history','address','image_url','record_timestamp']
        self.__remove_entries_from_dict(entries_to_remove,self.property_search.property_info)
        print(self.property_search.property_info[test_property_number].keys())
        self.property_search.get_expanded_property_data(test_property_number)
        assert 'price_history' in self.property_search.property_info[test_property_number] # is price history returned as a dict?
        assert 'address' in self.property_search.property_info[test_property_number] # check reverse geocode occurs
        assert isinstance(self.property_search.property_info[test_property_number]["address"], str) # check reverse geocode produces an address string
        assert isinstance(self.property_search.property_info[test_property_number]['image_url'],str) # check an image url is written to the info dict
        assert self.__url_reachable(self.property_search.property_info[test_property_number]['image_url']) # assert that the image url is reachable
        assert os.path.isfile( 'raw_data/property_images/property_'+ str(self.property_search.property_info[test_property_number]['id'])+'.jpeg') 
        assert isinstance(self.property_search.property_info[test_property_number]['record_timestamp'],str)



    def test_reverse_geocode_address(self):
        ''' Test that the reverse geocode function returns an address field to the property_info dict, formatted as str'''
        self.property_search.property_info=[{"location": {
        "latitude": 50.269928,
        "longitude": -4.788661
        },}]
        property_number=0
        self.property_search.reverse_geocode_address(property_number)
        # print(self.property_search.property_info)
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

    @staticmethod
    def __remove_entries_from_dict(entries_to_remove,example_property_data):
        for k in entries_to_remove:
            example_property_data[3].pop(k)



unittest.main(argv=[''], verbosity=0, exit=False)
# %%



# %%
