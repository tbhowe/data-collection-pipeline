# Data Collection Pipeline

This project is about scraping data from the property website rightmove.co.uk.


## Milestone 1-3

The first milestone of the project is the development of the central data scraping tool. The Selenium python package is used to control the Chrome browser via ChromeDriver. Selenium provides direct control over the browser, allowing us to fill in and submit forms, click on dropdown menus and navigate to pages. 

The data scraping tool is created as a class, and all of the functions for each step of the process are then created as methods of the class. 

The class has the following methods:

 - get_search_page() - takes our selection parameters and uses them to drive a property search. Default search parameters are included in the class initialiser method, aside from the area to search, which is a necessary attribute when instantiating the class. The search parameters will be assigned to an options dictionary in a future iteration. 

 Selenium is used to navigate to the various fields on the search page and complete them using our initial paramters. Different approaches are required depending on whether the fields are free text input or menu dropdowns.

 The method stores the search results URL as an attribute of the class, and then returns.

 - return_properties() - this method takes the search results and scrapes a variety of data on each property on the page. The property search results are listed on the results page as "property cards", with fields populated by a java script from a .json. Rather than scraping the data directly from the HTML, a handy shortcut is to simply access the json using the json.loads method, and parse the data inside.

 From the json file we get the following data:
   -- Property ID
   -- number of bedrooms
   -- number of bathrooms
   -- Property location in lat/long co-ordinates. In a future iteration we will use the geopy library to retrieve the postcode  and address from these co-ordinates. 

These data are compiled into a dictionary for each property, and the method returns a list of dictionaries, one per property. This is stored in the property_info attribute of the class.

-  nav_to_property_page(prop_ID) - As there are additional relevant data on the individual property pages that are not present in the json on the search results page, it is necessary to navigate to each property page individually. This method provides the functionality for this, given the property ID.

- accept_cookies() - This method is used to accept the GDPR cookies on the individual property pages. It is not strictly necessary for the rightmove.co.uk site, as the cookie popup is neither a field nor an alert, so does not hinder crawler functionality. It was implemented purely as an exercise. The method uses the webdriver.wait() method from the Selenium package to wait for the cookie element to appear, and then pause again until the "accept cookies" button is ready to be clicked. If the cookie element fails to appear,for example after the first page has already been crawled and the GDPR cookies have been accepted, the NoSuchElement exception is handled in a try/except statement.

- get_expanded_property_data(): This method collects additional data from each page in the search results inside a for loop. The individual property url is compiled from the property ID in the property_info attribute, and nav_to_property_page is called to navigate to the url. The Selenium webdrive is used to click a dropdown button to open the price history, and the price history data are scraped from the table this reveals, and added to the property_info dictionary.

