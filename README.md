# Data Collection Pipeline

This is a web scraper, designed to gather property data from rightmove.co.uk. It was produced as part of the AiCore course, for project 3: data collection pipeline.

## Brief:
"An implementation of an industry grade data collection pipeline that runs scalably in the cloud. It uses Python code to automatically control your browser, extract information from a website, and store it on the cloud in a data warehouses and data lake. The system conforms to industry best practices such as being containerised in Docker and running automated tests."

# Installation instructions

## Standalone version (requires Python and Pip, or Conda):

Clone the Github repository onto the local machine, and either run 

pip install requirements.txt
Python rm_scraper.py

Or to create a conda environment to run the scraper:

conda env create -f rightmove_env.yml
conda activate rightmove_env
Python rm_scraper.py


## Containerised version (requires Docker):

 To use the containerised version, download the image from:

 https://hub.docker.com/repository/docker/tbhowe/rm_scraper

 Then run a container from the image using the following command:

docker container run -d -it -v [HOST_DL_PATH]:/raw_data tbhowe/rm_scraper --platform linux/amd64

Substituting "[HOST_DL_PATH]" with the desired path on the host machine for downloading the scraped data.

# Operation of the scraper

To change the parameters of the scraper, open rm_scraper.py in a text editor. The area to search can be changed by altering the first argument in the instance creation on line 282:

property_search=GetProperties('mevagissey',opts)

Search options can be altered by changing the values of the search options dictionary on line 276. If the GetProperties instance is created with a single argument, the default search options will be used.


# Development history


## Milestones 1-4 - Data Scraper

The core of the project is the development of a data scraping tool. The Selenium python package is used to control the Chrome browser via ChromeDriver. Selenium provides direct control over the browser, allowing the scraper to fill in and submit forms, click on dropdown menus and navigate to pages. 

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

- get_price_history() - This method collects the price history data from the individual property page. 

- reverse_geocode_address() - This method takes the scraped lattitude and longitude data and returns a street address. It utilises the Geopy package.



## Milestone 5 - Testing

Unit tests for all public-facing methods are contained in test_suite.py. The unit tests utilise the unittest python module. For some of the tests, example data are loaded from the file: test_property_dictionary.pickle. 

The tests themselves are relatively rudimentary, and assess whether the data are returned, and if they in the correct format. For web scrapers, it is difficult to apply strict unit testing which covers all edge cases, due to the evanescent nature of a given webpage design. These tests serve more to demonstrate the concept of unit testing as part of the exercise.

To run the unit tests in terminal:

 python test_suite.py

## Milestone 6 - Containerisation

 The full package is available as a containerised image, generating using Docker. The scraper is configured to run in headless mode inside the container. 

## Miletsone 7 - CI/CD Pipeline
 
 A github action is used to ensure that all updates to the codebase are pushed to the Docker image. Every commit to the main branch of the repository triggers an action that rebuilds the docker image and pushes it to the dockerhub repository.


