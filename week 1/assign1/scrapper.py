from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# start browser
driver = webdriver.Chrome()
driver.get("https://books.toscrape.com")

# Increase timeout and add implicit wait for stability
wait = WebDriverWait(driver, 20)
driver.implicitly_wait(10)

# click on Historical Fiction category using XPath
# Using contains for more flexible text matching
category = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//a[contains(text(), 'Historical Fiction')]")
))
category.click()

books_data = []

while True:
    
    # wait for books to load
    wait.until(EC.presence_of_element_located(
        (By.XPATH, "//article[@class='product_pod']")
    ))

    # get all books on page
    books = driver.find_elements(By.XPATH, "//article[@class='product_pod']")

    for book in books:
        title = book.find_element(By.XPATH, ".//h3/a").get_attribute("title")
        price = book.find_element(By.XPATH, ".//p[@class='price_color']").text
        
        books_data.append({
            "Title": title,
            "Price": price
        })

    # check if next button exists
    try:
        next_button = driver.find_element(By.XPATH, "//li[@class='next']/a")
        next_button.click()
        time.sleep(2)
    except:
        break

# convert to dataframe
df = pd.DataFrame(books_data)

# save to csv
df.to_csv("historical_fiction_books.csv", index=False)

driver.quit()

print("Scraping Completed Successfully!")