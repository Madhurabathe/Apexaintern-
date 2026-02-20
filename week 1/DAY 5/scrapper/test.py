import requests
import pandas as pd
from lxml import html as lh

url = "https://www.paloaltonetworks.com/services/support/end-of-life-announcements/hardware-end-of-life-dates"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
page = lh.fromstring(response.content)

# XPath to table rows
rows = page.xpath("//table//tbody/tr")

data = []

for r in rows:
    cols = r.xpath(".//td")

    if len(cols) >= 4:
        product = cols[0].text_content().strip()
        eol = cols[2].text_content().strip()
        replacement = cols[3].text_content().strip()

        # resource link
        link = cols[0].xpath(".//a/@href")
        resource = link[0] if link else url

        data.append([
            "Palo Alto",
            product,
            eol,
            resource,
            replacement
        ])

df = pd.DataFrame(data, columns=[
    "vendor",
    "productName",
    "EOL Date",
    "resource",
    "Recommended replacement"
])

df.to_csv("paloalto_eol1.csv", index=False)

print("CSV downloaded successfully")