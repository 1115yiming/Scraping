import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define the URL and proxies
url = "https://www.acga-web.org/current-gift-annuity-rates"

# Fetch the page content using requests
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# # Function to parse the table and return as a DataFrame
# def parse_table(table):
#     rows = table.find_all('tr')
#     data = []
#     for row in rows:
#         cols = row.find_all('td')
#         cols = [col.text.strip() for col in cols]
#         data.append(cols)
#     return data
#
# # Locate the specific table
# headings = soup.find_all('h3')
# for heading in headings:
#     if 'Single Life Suggested Maximum Gift Annuity Rates' in heading.get_text():
#         table = heading.find_next('table')
#         if table:
#             data = parse_table(table)
#             # The table data has columns Age and Rate duplicated for each half of the table
#             # We'll combine them into a single list
#             combined_data = []
#             for row in data:
#                 if len(row) >= 2:
#                     combined_data.append([row[0], row[1]])
#                 if len(row) >= 5:
#                     combined_data.append([row[3], row[4]])
#
#             # Create DataFrame and clean up
#             df = pd.DataFrame(combined_data, columns=['Age', 'Rate'])
#             df = df[df['Age'] != 'Age']  # Remove header rows
#
#             # Output to check
#             # print(df)
#
#             # Save to Excel
#             df.to_excel('single_life_annuity_rates.xlsx', index=False)
#             break
# else:
#     print("Heading not found.")
#
# # Transform the scraped data into the desired format
#
# # Read the original Excel file
# df = pd.read_excel('single_life_annuity_rates.xlsx')
#
# # Create a new DataFrame to store the revised data
# revised_data = []
#
# # Add initial ages 0 to 4 with rate 0.0%
# for age in range(0, 5):
#     revised_data.append([age, '0.0%'])
#
# # Function to expand the age ranges
# def expand_age_ranges(age_range, rate):
#     if '-' in age_range:
#         start, end = map(int, age_range.split('-'))
#         for age in range(start, end + 1):
#             revised_data.append([age, f'{rate}%'])
#     elif '90+' in age_range:
#         revised_data.append([90, f'{rate}%'])
#         for age in range(91, 111):
#             revised_data.append([age, f'{rate}%'])
#     else:
#         revised_data.append([int(age_range), f'{rate}%'])
#
# # Expand each row in the original DataFrame
# for _, row in df.iterrows():
#     expand_age_ranges(row['Age'], row['Rate'])
#
# # Convert the revised data to a DataFrame
# revised_df = pd.DataFrame(revised_data, columns=['Age', 'Single Life Max Rate'])
#
# # Ensure all ages up to 110 are included
# for age in range(5, 111):
#     if age not in revised_df['Age'].values:
#         revised_df = revised_df.append({'Age': age, 'Single Life Max Rate': '0.0%'}, ignore_index=True)
#
# # Sort the DataFrame by age
# revised_df = revised_df.sort_values(by='Age').reset_index(drop=True)
#
# # Save the revised DataFrame to a new Excel file
# revised_df.to_excel('revised_single_life_annuity_rates.xlsx', index=False)
#
# # Output to check
# print(revised_df)


# Function to parse the table and return as a DataFrame
# Function to parse the joint life table and return as a DataFrame
# # Function to parse the table and return as a DataFrame
# def parse_joint_table(table):
#     rows = table.find_all('tr')
#     left_data = []
#     right_data = []
#     for row in rows:
#         cols = row.find_all('td')
#         cols = [col.text.strip() for col in cols]
#         if len(cols) >= 3:
#             left_data.append([cols[0], cols[1], cols[2]])
#         if len(cols) >= 6:
#             right_data.append([cols[4], cols[5], cols[6]])
#     return left_data, right_data
#
# # Locate the specific table for Two Lives
# headings = soup.find_all('h3')
# for heading in headings:
#     if 'Two Lives - Joint and Survivor Suggested Maximum Gift Annuity Rates' in heading.get_text():
#         table = heading.find_next('table')
#         if table:
#             left_data, right_data = parse_joint_table(table)
#             # Combine the left and right data correctly
#             combined_data_joint = left_data + right_data
#
#             # Create DataFrame and clean up
#             df_joint = pd.DataFrame(combined_data_joint, columns=['Younger Age', 'Older Age', 'Rate'])
#             df_joint = df_joint[df_joint['Younger Age'] != 'Younger Age']  # Remove header rows
#
#             # Output to check
#             print(df_joint)
#
#             # Save to Excel
#             df_joint.to_excel('two_lives_annuity_rates.xlsx', index=False)
#             break
# else:
#     print("Two Lives table heading not found.")
#
#
# # Read the original Excel file
# df_joint = pd.read_excel('two_lives_annuity_rates.xlsx')
#
# # Create a new DataFrame to store the revised data
# revised_data_joint = []
#
# # Add initial ages 0 to 4 with rate 0.0%
# for age in range(0, 5):
#     revised_data_joint.append([age, '0.0%'])
#
# # Function to expand the age ranges
# def expand_joint_age_ranges(younger_age, older_age, rate):
#     expanded_data = []
#     older_age = older_age.strip()  # Remove any extra spaces
#
#     if '-' in older_age:
#         start_age, end_age = map(int, older_age.replace('+', '').split('-'))
#     elif '95+' in older_age:
#         start_age, end_age = 95, 110
#     else:
#         start_age = end_age = int(older_age.replace('+', ''))
#
#     if younger_age.isdigit():
#         younger_age = int(younger_age)
#         if younger_age >= start_age and younger_age <= end_age:
#             expanded_data.append([younger_age, f'{rate}%'])
#     return expanded_data
#
# # Expand each row in the original DataFrame
# for _, row in df_joint.iterrows():
#     revised_data_joint.extend(expand_joint_age_ranges(row['Younger Age'], row['Older Age'], row['Rate']))
#
# # Convert the revised data to a DataFrame
# revised_df_joint = pd.DataFrame(revised_data_joint, columns=['Age', 'Same Age Max Rate'])
#
# # Ensure all ages up to 110 are included
# for age in range(5, 111):
#     if age not in revised_df_joint['Age'].values:
#         revised_df_joint = pd.concat([revised_df_joint, pd.DataFrame({'Age': [age], 'Same Age Max Rate': ['9.9%']})])
#
# # Sort the DataFrame by age
# revised_df_joint = revised_df_joint.sort_values(by='Age').reset_index(drop=True)
#
# # Save the revised DataFrame to a new Excel file
# revised_df_joint.to_excel('revised_same_age_max_rate.xlsx', index=False)
#
# # Output to check
# print(revised_df_joint)


# Read the original two lives annuity rates Excel file
df_joint = pd.read_excel('two_lives_annuity_rates.xlsx')

# Create a new DataFrame to store the revised data
matrix_data = [['' for _ in range(111)] for _ in range(111)]

# Initialize the rate for ages 0-4 to 0.0%
for age in range(5):
    for older_age in range(age, 111):
        matrix_data[age][older_age] = '0.0%'

# Initialize the rate for ages 95 and above to 9.9%
for age in range(95, 111):
    for older_age in range(age, 111):
        matrix_data[age][older_age] = '9.9%'

# Function to expand the age ranges and fill in the matrix data
def fill_matrix_data(younger_age, older_age_range, rate):
    rate_value = f'{rate}%'
    if '-' in older_age_range:
        start_age, end_age = older_age_range.split('-')
        start_age = int(start_age)
        end_age = 110 if '95+' in end_age else int(end_age)
    else:
        if '95+' in older_age_range:
            start_age = 95
            end_age = 110
        else:
            start_age = int(older_age_range)
            end_age = start_age

    for older_age in range(start_age, end_age + 1):
        if younger_age <= older_age:  # Fill only the top right half of the matrix
            matrix_data[younger_age][older_age] = rate_value

# Expand each row in the original DataFrame
for index, row in df_joint.iterrows():
    try:
        if '95+' in row['Younger Age']:
            younger_age = 95
            fill_matrix_data(younger_age, '95+', row['Rate'])
        else:
            younger_age = int(row['Younger Age'])
            older_age_range = row['Older Age']
            rate = row['Rate']
            fill_matrix_data(younger_age, older_age_range, rate)
    except ValueError as e:
        print(f"Error processing row {index}: {row}")
        raise e

# Convert the matrix data to a DataFrame
matrix_df = pd.DataFrame(matrix_data, columns=range(111), index=range(111))

# Save the matrix DataFrame to a new Excel file
matrix_df.to_excel('two_lives_annuity_matrix.xlsx')

# Output to check
print(matrix_df)
