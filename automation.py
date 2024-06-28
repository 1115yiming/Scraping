import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define the URL and proxies
url = "https://www.acga-web.org/current-gift-annuity-rates"

# Fetch the page content using requests
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Function to parse the table and return as a DataFrame
def parse_table(table):
    rows = table.find_all('tr')
    data = []
    for row in rows:
        cols = row.find_all('td')
        cols = [col.text.strip() for col in cols]
        data.append(cols)
    return data

# Locate the specific table
headings = soup.find_all('h3')
for heading in headings:
    if 'Single Life Suggested Maximum Gift Annuity Rates' in heading.get_text():
        table = heading.find_next('table')
        if table:
            data = parse_table(table)
            # The table data has columns Age and Rate duplicated for each half of the table
            # We'll combine them into a single list
            combined_data = []
            for row in data:
                if len(row) >= 2:
                    combined_data.append([row[0], row[1]])
                if len(row) >= 5:
                    combined_data.append([row[3], row[4]])

            # Create DataFrame and clean up
            df = pd.DataFrame(combined_data, columns=['Age', 'Rate'])
            df = df[df['Age'] != 'Age']  # Remove header rows

            # Output to check
            print(df)

            # Save to Excel
            df.to_excel('single_life_annuity_rates.xlsx', index=False)
            break
else:
    print("Heading not found.")