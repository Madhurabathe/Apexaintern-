from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)

driver.get("https://www.imdb.com/chart/top/")

# wait until movie rows appear
wait.until(EC.presence_of_all_elements_located(
    (By.XPATH, "//li[contains(@class,'ipc-metadata-list-summary-item')]")
))

movies = driver.find_elements(
    By.XPATH, "//li[contains(@class,'ipc-metadata-list-summary-item')]"
)

data = []

for movie in movies:

    title = movie.find_element(
        By.XPATH, ".//h3"
    ).text

    rating = movie.find_element(
        By.XPATH, ".//span[contains(@class,'ipc-rating-star--rating')]"
    ).text

    data.append({
        "Title": title,
        "IMDb Rating": rating
    })

driver.quit()

df = pd.DataFrame(data)
df.to_csv("rank_movies.csv", index=False)

print(df)