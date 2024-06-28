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
            # print(df)

            # Save to Excel
            df.to_excel('single_life_annuity_rates.xlsx', index=False)
            break
else:
    print("Heading not found.")

# Transform the scraped data into the desired format

# Read the original Excel file
df = pd.read_excel('single_life_annuity_rates.xlsx')

# Create a new DataFrame to store the revised data
revised_data = []

# Add initial ages 0 to 4 with rate 0.0%
for age in range(0, 5):
    revised_data.append([age, '0.0%'])

# Function to expand the age ranges
def expand_age_ranges(age_range, rate):
    if '-' in age_range:
        start, end = map(int, age_range.split('-'))
        for age in range(start, end + 1):
            revised_data.append([age, f'{rate}%'])
    elif '90+' in age_range:
        revised_data.append([90, f'{rate}%'])
        for age in range(91, 111):
            revised_data.append([age, f'{rate}%'])
    else:
        revised_data.append([int(age_range), f'{rate}%'])

# Expand each row in the original DataFrame
for _, row in df.iterrows():
    expand_age_ranges(row['Age'], row['Rate'])

# Convert the revised data to a DataFrame
revised_df = pd.DataFrame(revised_data, columns=['Age', 'Single Life Max Rate'])

# Ensure all ages up to 110 are included
for age in range(5, 111):
    if age not in revised_df['Age'].values:
        revised_df = revised_df.append({'Age': age, 'Single Life Max Rate': '0.0%'}, ignore_index=True)

# Sort the DataFrame by age
revised_df = revised_df.sort_values(by='Age').reset_index(drop=True)

# Save the revised DataFrame to a new Excel file
revised_df.to_excel('revised_single_life_annuity_rates.xlsx', index=False)

# Output to check
print(revised_df)