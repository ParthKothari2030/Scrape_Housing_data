from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
from bs4 import BeautifulSoup 

url1 = "https://www.realestateindia.com/ahmedabad-property/new-projects.htm"
url2 = "https://www.scrapethissite.com/pages/simple/"
path_to_file = "/home/user/Documents/Deep_learning_folder/Scrape_Housing_data/"

mode = "scrape" # mode = extract/scrape/""



# Choosing webbrowser and giving target link
driver = webdriver.Chrome()
driver.maximize_window()
driver.get(url1)

# wait time for scroll
Intial_screen_height = driver.execute_script("return window.screen.height;")



while True:
    
    load_more_button = driver.find_element(By.XPATH, "/html/body/section[2]/div/div/div[1]/div[4]/a")
    
    if load_more_button.is_displayed():
        
        
        load_more_button.click()
        time.sleep(4)
        
    # scrolling down
    driver.execute_script(f"window.scrollBy(0,1000);")
    
    # Pause time between next scroll
    time.sleep(2) 

    # End of page check (scroll break)
    new_height = driver.execute_script("return document.body.scrollHeight;")

    if (new_height == Intial_screen_height):
        load_more_button = driver.find_element(By.XPATH, "/html/body/section[2]/div/div/div[1]/div[4]/a")
        
        if load_more_button.is_displayed():
        
            load_more_button.click()
            time.sleep(4)



# saving the page after scraping 
page_source = driver.page_source

# saving the scraped page to a text file
f = open(path_to_file+"source.txt","w",encoding="utf-8")
f.write(page_source)
f.close() 

