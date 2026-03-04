from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# start browser
driver = webdriver.Chrome()
driver.get("https://books.toscrape.com/")
#explicit wait for elements to load
wait = WebDriverWait(driver, 10)

all_books = []

while True:
    
    # wait for books to load
    wait.until(EC.presence_of_element_located(
        (By.XPATH, "//article[@class='product_pod']")
    ))
    
    books = driver.find_elements(By.XPATH, "//article[@class='product_pod']")
    
    for book in books:
        title = book.find_element(By.XPATH, ".//h3/a").get_attribute("title")
        price = book.find_element(By.XPATH, ".//p[@class='price_color']").text
        
        all_books.append({
            "Title": title,
            "Price": price
        })
    
    print(f"Scraped {len(all_books)} books so far...")
    
    # try clicking next page
    try:
        next_button = driver.find_element(By.XPATH, "//li[@class='next']/a")
        next_button.click()
        time.sleep(2)
    except:
        break

df = pd.DataFrame(all_books)
df.to_csv("all_books.csv", index=False)
driver.quit()
print("All books scraped successfully!")