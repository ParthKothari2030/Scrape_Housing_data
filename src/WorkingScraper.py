url2 = "https://www.realestateindia.com/ahmedabad-property/new-projects.htm"
path_to_file = "/home/User/Documents/Deep_learning_folder/Scrape_Housing_data/"


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
# import pandas as pd
import time



# Using gecko 0.36.0 for the firefox
service = Service(executable_path="/home/User/Documents/Deep_learning_folder/Scrape_Housing_data/geckodriver_latest/geckodriver")
driver = webdriver.Firefox(service=service)



driver.maximize_window()
driver.get(url2)

print("new code start with 48 scrolls")

# wait time for scroll
scroll_pause_time = 2

scroll_no = 0
while True:

    # scrolling down
    driver.execute_script(f"window.scrollBy(0,500);")
    

    time.sleep(scroll_pause_time) # Pause time between next scroll

    try:    
        load_more_button = WebDriverWait(driver, 4).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/section[2]/div/div/div[1]/div[4]/a"))
        )

        
        time.sleep(4)

        if load_more_button.is_displayed() == True:
            # time.sleep(60)            
            load_more_button.click()
            scroll_no += 1
            time.sleep(2)
        # else:
        #     time.sleep(60)
    
    except Exception as e:
        print('Button not Found')
    
    # time.sleep(60)
    
    # End of page check (scroll break)
    if (scroll_no == 2):
        break
    else:
        print(f"No. of scrolls: {scroll_no}")

page_source = driver.page_source

# saving the scraped page to a text file
f = open(path_to_file+"source.txt","w",encoding="utf-8")
f.write(page_source)
f.close() 
