#%%

from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By



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



# input data:
property_area='Mevagissey'
get_initial_search_page(property_area)