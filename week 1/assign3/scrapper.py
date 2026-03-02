from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

# Setup Chrome
options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 15)

url = "https://webscraper.io/test-sites/e-commerce/static/computers/laptops"

data = []

try:
    driver.get(url)

    while True:
        # Wait until products load
        wait.until(EC.presence_of_element_located(
            (By.XPATH, "//div[contains(@class,'thumbnail')]")
        ))

        products = driver.find_elements(
            By.XPATH, "//div[contains(@class,'thumbnail')]"
        )

        for product in products:
            try:
                # Extract product name
                name = product.find_element(
                    By.XPATH, ".//a[contains(@class,'title')]"
                ).text

                # Extract price
                price_text = product.find_element(
                    By.XPATH, ".//h4[contains(@class,'price')]"
                ).text

                # Clean price
                price_value = float(price_text.replace("$", ""))

                # Apply filter (Price > 500)
                if price_value > 500:
                    data.append({
                        "Product Name": name,
                        "Price ($)": price_value
                    })

            except:
                continue

        # Pagination handling
        try:
            next_button = driver.find_element(
                By.XPATH, "//li[@class='next']/a"
            )
            next_button.click()
            time.sleep(2)
        except:
            break  # No more pages

    # Create DataFrame
    df = pd.DataFrame(data)

    # Export to CSV
    df.to_csv("filtered_products.csv", index=False)

    print("\nCSV created successfully!\n")
    print(df)

finally:
    driver.quit()