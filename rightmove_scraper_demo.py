#%%

from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
driver = webdriver.Chrome()
driver.get("https://www.rightmove.co.uk/")

# input data:
property_area='Mevagissey'

# finds the inputfield on the front page!
search_box_path = driver.find_element(by=By.XPATH, value='//*[@name="typeAheadInputField"]')

# finds the for sale button
for_sale_button_path =driver.find_element(by=By.XPATH,value='//*[@id="_3OuiRnbltQyS534SB4ivLV"]')

#fill in search box
search_box_path.send_keys(property_area)
search_box_path.send_keys(Keys.ENTER)
# for_sale_button_path.execute_script("arguments[0].click();", l)


#house price button is:

# print(search_box_path)
# print('searchbox_done')
# print(for_sale_button_path)
# print('for sale button done')
# %%
