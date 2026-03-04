from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time


# Function to start the browser
def start_browser():
    driver = webdriver.Chrome()
    driver.get("https://books.toscrape.com")
    return driver


# Function to click the genre
def click_genre(driver, wait):
    genre = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[contains(text(),'Historical Fiction')]")
    ))
    genre.click()


# scrape books from one page
def scrape_books(driver):
    books_data = []

    books = driver.find_elements(By.XPATH, "//article[@class='product_pod']")

    for book in books:
        title = book.find_element(By.XPATH, ".//h3/a").get_attribute("title")
        price = book.find_element(By.XPATH, ".//p[@class='price_color']").text

        books_data.append({
            "Title": title,
            "Price": price
        })

    return books_data


# handle pagination
def pages(driver, wait):
    all_books = []

    while True:
        wait.until(EC.presence_of_element_located(
            (By.XPATH, "//article[@class='product_pod']")
        ))

        books = scrape_books(driver)
        all_books.extend(books)

        try:
            next_button = driver.find_element(By.XPATH, "//li[@class='next']/a")
            next_button.click()
            time.sleep(2)

        except:
            break

    return all_books


# csv save data
def save_data(books_data):
    df = pd.DataFrame(books_data)
    df.to_csv("historical_fiction_books.csv", index=False)



def main():
    driver = start_browser()
    wait = WebDriverWait(driver, 20)

    click_genre(driver, wait)

    books_data = pages(driver, wait)

    save_data(books_data)

    driver.quit()

    print("Scraping Completed Successfully!")


main()