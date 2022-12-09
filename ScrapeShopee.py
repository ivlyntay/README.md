import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import random

class ScrapeData():
    def __init__(self):
        pass

    def get_url(self, product):
        product = product.replace(" ",'%20')
        template = 'https://shopee.com.my/search?keyword={}'
        url = template.format(product)
        return url

    def main(self, product ,no_prod):
        url = self.get_url(product) # since the file is a class, we add a "self." to call the function within the same class
        driver = webdriver.Chrome(executable_path="C:\vscode-cpp-samples\my_project\chromedriver.exe")
        driver.get(url)
        driver.maximize_window()
        time.sleep(3)
    

        btn = driver.find_element("xpath",'//*[@id="modal"]/div[1]/div[1]/div/div[3]/div[1]/button') #language button
        btn.click()
        sleep_time = random.randint(5,7) 
        time.sleep(sleep_time) 

        btn = driver.find_element("xpath", '//*[@id="main"]/div/div[2]/div/div/div[2]/div[2]/div[1]/div[1]/div[3]') #click to top sales
        btn.click()
        sleep_time = random.randint(5,7) 
        time.sleep(sleep_time) 
        records=[]
        scraped_count = 0

        #for i in range (1,51):
        while True:
            #Define an initial value
            temp_height=0
    
            while True:
            #Looping down the scroll bar
                driver.execute_script("window.scrollBy(0,1000)")
            #sleep and let the scroll bar react
                sleep_time = random.randint(3,6) 
                time.sleep(sleep_time) 
            #Get the distance of the current scroll bar from the top
                check_height = driver.execute_script("return document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;")
            #If the two are equal to the end
                if check_height==temp_height:
                    break
                temp_height=check_height
                sleep_time = random.randint(2,4) 
                time.sleep(sleep_time) 
            
            product_cards = driver.find_elements(By.CLASS_NAME,'col-xs-2-4')
            
            for item in product_cards:
                pImg = item.find_element(By.TAG_NAME,'img')
                product_image = pImg.get_attribute('src')

                product_name = item.find_element(By.CLASS_NAME,'Cve6sh').text.encode(encoding='ascii',errors= 'ignore').decode()
                
                product_price = item.find_element(By.CLASS_NAME,'ZEgDH9').text.strip()

                try:
                    product_sold = item.find_element(By.CLASS_NAME,'r6HknA').text.strip()
                except AttributeError:
                    product_sold = '0 sold'
                    
                pLink =item.find_element(By.TAG_NAME,'a')
                product_buy_link = pLink.get_attribute('href')
            
            
                records.append(
                        (product_image, product_name, product_price, product_sold, product_buy_link)
                    )
                scraped_count += 1
                print("scrapped_count",  scraped_count)
                print("no_prod",  no_prod)
                if scraped_count == int(no_prod):
                    print('done')
                    driver.quit()
                    return records
            # btn = driver.find_element("xpath",'//*[@id="main"]/div/div[2]/div/div/div[2]/div[2]/div[3]/div/button[8]')
            # btn.click()
            # sleep_time = random.randint(5,7) 
            # time.sleep(sleep_time)

    
    def data(self,product,no_prod):
        records = self.main(product, no_prod) 
        col = ['Product_Image','Product_Name','Product_Price','Product_Sold', 'Product_Buy_Link']
        shopee_data = pd.DataFrame(records ,columns=col)
        shopee_data.to_csv('ShopeeData.csv')   