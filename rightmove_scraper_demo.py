#%%

from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


def get_initial_search_page(property_area):
    driver = webdriver.Chrome()
    driver.get("https://www.rightmove.co.uk/")

    

    # finds the inputfield on the front page!
    search_box_path = driver.find_element(by=By.XPATH, value='//*[@name="typeAheadInputField"]')

    # finds the for sale button
    for_sale_button_path =driver.find_element(by=By.XPATH,value='//*[@id="_3OuiRnbltQyS534SB4ivLV"]')

    #fill in search box
    search_box_path.send_keys(property_area)
    search_box_path.send_keys(Keys.ENTER)
    return(driver.current_url)
    
    



# input data:
property_area='Mevagissey'
search_page_url=get_initial_search_page(property_area)

#%%
# let's explore the search page now:
driver = webdriver.Chrome()
driver.get(search_page_url)

min_price="200,000"
max_price="700,000"
property_type='Houses'
min_bedrooms="2"
# finds the inputfields - TIDY THIS INTO LOOP when sorted
min_price_dropdown = Select(driver.find_element(by=By.XPATH, value='//*[@name="minPrice"]'))
max_price_dropdown = Select(driver.find_element(by=By.XPATH, value='//*[@name="maxPrice"]'))
property_type_dropdown = Select(driver.find_element(by=By.XPATH, value='//*[@name="displayPropertyType"]'))
min_bedrooms_dropdown = Select(driver.find_element(by=By.XPATH, value='//*[@name="minBedrooms"]'))
# select by visible text
min_price_dropdown.select_by_visible_text(min_price)
max_price_dropdown.select_by_visible_text(max_price)
property_type_dropdown.select_by_visible_text(property_type)
min_bedrooms_dropdown.select_by_visible_text(min_bedrooms)

# find submit button
submit_button=driver.find_element(by=By.XPATH, value='//*[@id="submit"]')
submit_button.click()

# %%
