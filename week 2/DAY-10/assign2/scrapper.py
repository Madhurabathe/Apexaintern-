from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Start browser
driver = webdriver.Chrome()
driver.get("https://www.worldometers.info/world-population/population-by-country/")

wait = WebDriverWait(driver, 20)

# Wait for table to load
wait.until(EC.presence_of_element_located((By.XPATH, "//table")))

# Get all rows
rows = driver.find_elements(By.XPATH, "//table/tbody/tr")

data = []

for row in rows:
    try:
        country = row.find_element(By.XPATH, "./td[2]").text
        population = row.find_element(By.XPATH, "./td[3]").text
        yearly_change = row.find_element(By.XPATH, "./td[4]").text
        world_share = row.find_element(By.XPATH, "./td[last()]").text

        data.append({
            "Country": country,
            "Population": population,
            "Yearly Change": yearly_change,
            "World Share": world_share
        })
    except:
        break 

driver.quit()

# Convert to DataFrame
df = pd.DataFrame(data)

# Save to CSV
file = "world_population.csv"
df.to_csv(file, index=False)

print("Scraping Completed Successfully!")
