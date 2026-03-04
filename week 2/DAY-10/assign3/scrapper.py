from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 15)
driver.get("https://webscraper.io/test-sites/e-commerce/static/computers/laptops")

data=[]
while True:
        # Wait for product cards to load
        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class,'thumbnail')]")
            )
        )

        # Get all products on current page
        products = driver.find_elements(
            By.XPATH, "//div[contains(@class,'thumbnail')]"
        )

        for product in products:
            # Product Name (relative XPath)
            name = product.find_element(
                By.XPATH, ".//a[contains(@class,'title')]"
            ).text

            # Product Price
            price_text = product.find_element(
                By.XPATH, ".//h4[contains(@class,'price')]"
            ).text

            # Convert price to float
            price_value = float(price_text.replace("$", ""))

            # Filter products above $500
            if price_value > 500:
                data.append({
                    "Product Name": name,
                    "Price ($)": price_value
                })
        #next button 
        try:
            next_button = driver.find_element(
                By.XPATH, "//li[@class='next']/a"
            )
            next_button.click()
            time.sleep(3)
            
        except:
            break 
driver.quit()
df = pd.DataFrame(data)
df.to_csv("filtered_products.csv", index=False)
print("\n scrapping done successfully!\n")
