#%%

import unittest
import rm_scraper
import requests
import time


class ScraperTestCase(unittest.TestCase):
    '''Test suite for rm_scraper'''
    
    def setUp(self):
        self.property_search=rm_scraper.GetProperties('mevagissey')

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



unittest.main(argv=[''], verbosity=0, exit=False)
# %%



# %%
