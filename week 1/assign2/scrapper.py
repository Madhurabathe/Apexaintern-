import pandas as pd
import requests

"""Fetch the population-by-country table without a browser.
Columns scraped: 2, 3, 4 and the last column (world share).
Use a real user-agent header to avoid HTTP 403.
"""

url = "https://www.worldometers.info/world-population/population-by-country/"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

resp = requests.get(url, headers=headers)
if resp.status_code != 200:
    print(f"failed to fetch page: status {resp.status_code}")
    resp.raise_for_status()

# pandas can accept the HTML string directly; warning about future deprecation
# is harmless for now, so we're skipping the StringIO step.
try:
    tables = pd.read_html(resp.text)
except Exception as e:
    print("failed to parse table:", e)
    raise

if not tables:
    print("no tables found on page")
    raise SystemExit(1)

# first table contains the desired data
df = tables[0]

# pick columns 2,3,4 and the last column
# pandas uses zero-based indexing
df = df.iloc[:, [1, 2, 3, -1]]
df.columns = ["Country", "Population", "Yearly Change", "World Share"]

out_file = "world_population.csv"
df.to_csv(out_file, index=False)
print("Scraping Completed Successfully!")
print(f"saved {len(df)} rows to {out_file}")