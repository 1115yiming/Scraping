# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
# from openpyxl import Workbook
#
# # Define the URL of the page to scrape
# url = "https://www.acga-web.org/current-gift-annuity-rates"
#
# # Fetch the page content
# response = requests.get(url)
# soup = BeautifulSoup(response.content, 'html.parser')
# # print(soup)
#
# # # Function to parse the table and return as a DataFrame
# # def parse_table(table):
# #     rows = table.find_all('tr')
# #     data = []
# #     for row in rows:
# #         cols = row.find_all(['td', 'th'])
# #         cols = [col.text.strip() for col in cols]
# #         data.append(cols)
# #     return pd.DataFrame(data[1:], columns=data[0])
# #
# # # Parse Single Life table
# # single_life_table = soup.find('table', {'summary': 'Single Life Suggested Maximum Gift Annuity Rates'})
# # single_life_df = parse_table(single_life_table)
# # single_life_df.columns = ['Age', 'Rate']
# # single_life_df['Age'] = single_life_df['Age'].apply(lambda x: int(x.split('-')[0]) if '-' in x else int(x))
# #
# # # Parse Two Lives table
# # two_lives_table = soup.find('table', {'summary': 'Two Lives - Joint and Survivor Suggested Maximum Gift Annuity Rates'})
# # two_lives_df = parse_table(two_lives_table)
# # two_lives_df.columns = ['Younger Age', 'Older Age', 'Rate']
# #
# # # Extract Two Lives Same Age rates
# # two_lives_same_age_df = two_lives_df[two_lives_df['Younger Age'] == two_lives_df['Older Age']]
# #
# # # Prepare the final DataFrame for Excel
# # excel_df = pd.DataFrame()
# # excel_df['Age'] = single_life_df['Age']
# # excel_df['Single Life Max Rate'] = single_life_df['Rate']
# # excel_df['Two Lives Same Age Max Rate'] = two_lives_same_age_df['Rate'].reset_index(drop=True)
# # excel_df['Age_'] = excel_df['Age']  # To keep 'Age' column in sync across the sheet
# #
# # # Create the matrix for Two Lives rates
# # two_lives_matrix_df = pd.DataFrame(index=excel_df['Age'], columns=excel_df['Age'])
# # for _, row in two_lives_df.iterrows():
# #     younger_age = int(row['Younger Age'].split('-')[0])
# #     older_age = int(row['Older Age'].split('-')[0])
# #     rate = row['Rate']
# #     two_lives_matrix_df.at[younger_age, older_age] = rate
# #
# # # Merge the matrix to the main DataFrame
# # final_df = pd.concat([excel_df, two_lives_matrix_df], axis=1)
# #
# # # Write to Excel file
# # with pd.ExcelWriter('gift_annuity_rates.xlsx', engine='openpyxl') as writer:
# #     final_df.to_excel(writer, index=False, sheet_name='Rates')
# #
# # print("Data has been successfully written to gift_annuity_rates.xlsx")
#
# # Function to parse the table and return as a DataFrame
# def parse_table(table):
#     rows = table.find_all('tr')
#     data = []
#     for row in rows:
#         cols = row.find_all('td')
#         cols = [col.text.strip() for col in cols]
#         data.append(cols)
#     return pd.DataFrame(data, columns=['Age', 'Rate'])
#
# # Find the table using more precise CSS selectors
# center_div = soup.find('div', style=lambda value: 'text-align: center;' in value if value else False)
# single_life_table = center_div.find('table') if center_div else None
#
# if single_life_table:
#     single_life_df = parse_table(single_life_table)
#     # Convert age ranges and rates
#     single_life_df['Age'] = single_life_df['Age'].apply(lambda x: int(x.split('-')[0]) if '-' in x else int(x))
#
#     # Write the DataFrame to an Excel file
#     single_life_df.to_excel('single_life_annuity_rates.xlsx', index=False)
#
#     print("Data has been successfully written to single_life_annuity_rates.xlsx")
# else:
#     print("Table not found. Check the website structure.")

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import pandas as pd
#
# # Setup Selenium WebDriver
# options = webdriver.ChromeOptions()
# options.headless = True  # Optional: if you do not want the browser window to appear
# driver = webdriver.Chrome(options=options)  # Ensure that the path to the ChromeDriver is correct or it's in PATH
#
# url = "https://www.acga-web.org/current-gift-annuity-rates"
# driver.get(url)
#
# try:
#     # Wait for the page to load and ensure the table is present
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, "h3 + div table"))
#     )
#
#     # Select the table directly below the <h3> tag containing the specific text
#     table = driver.find_element(By.CSS_SELECTOR, "h3 + div table")
#
#     # Extract data from the table
#     rows = table.find_elements(By.TAG_NAME, "tr")
#     data = []
#     for row in rows:
#         cols = row.find_elements(By.TAG_NAME, "td")
#         if cols:
#             age = cols[0].text.strip()
#             rate = cols[1].text.strip()
#             data.append([age, rate])
#
#     df = pd.DataFrame(data, columns=['Age', 'Rate'])
#
#     # Output to check
#     print(df)
#
#     # Save to Excel
#     df.to_excel('single_life_annuity_rates.xlsx', index=False)
#
# finally:
#     driver.quit()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Setup Selenium WebDriver
options = webdriver.ChromeOptions()
options.headless = True  # Optional: if you do not want the browser window to appear
driver = webdriver.Chrome(options=options)  # Ensure that the path to the ChromeDriver is correct or it's in PATH

url = "https://www.acga-web.org/current-gift-annuity-rates"
driver.get(url)

try:
    # Wait for the page to load and ensure the table is present
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "h3 + div table"))
    )

    # Select the table directly below the <h3> tag containing the specific text
    table = driver.find_element(By.CSS_SELECTOR, "h3 + div table")

    # Extract data from the table
    rows = table.find_elements(By.TAG_NAME, "tr")
    data = []
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) >= 2:
            age1 = cols[0].text.strip()
            rate1 = cols[1].text.strip()
            data.append([age1, rate1])
        if len(cols) >= 4:
            age2 = cols[3].text.strip()
            rate2 = cols[4].text.strip()
            data.append([age2, rate2])

    df = pd.DataFrame(data, columns=['Age', 'Rate'])

    # Remove any header rows that may have been included
    df = df[df['Age'] != 'Age']

    # Output to check
    print(df)

    # Save to Excel
    df.to_excel('single_life_annuity_rates.xlsx', index=False)

finally:
    driver.quit()
