import requests
import pandas as pd
from lxml import html as lh
from datetime import datetime

url = "https://www.paloaltonetworks.com/services/support/end-of-life-announcements/end-of-life-summary"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
page = lh.fromstring(response.content)

tables = page.xpath("//table")

data = []

def convert_date(date_text):
    try:
        return datetime.strptime(date_text.strip(), "%B %d, %Y").strftime("%Y-%m-%d")
    except:
        return ""

for table in tables:

    software = table.xpath("./ancestor::div[1]/preceding-sibling::*[self::h2 or self::h3][1]/text()")
    software_name = software[0].strip() if software else "Unknown"

    rows = table.xpath(".//tbody/tr")

    for r in rows:
        cols = r.xpath(".//td")

        if len(cols) >= 3:

            version = cols[0].text_content().strip()
            release = convert_date(cols[1].text_content().strip())
            eol = convert_date(cols[2].text_content().strip())

            data.append([
                software_name,
                version,
                eol,
                release
            ])

df = pd.DataFrame(data, columns=[
    "Software Name",
    "version",
    "EOL Date",
    "Release Date"
])

df.to_csv("paloalto_software_eol1.csv", index=False)

print("Software CSV downloaded successfully")