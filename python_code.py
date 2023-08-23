
import pandas as pd
import numpy as np


df = pd.read_excel(r"C:\Users\MAHALINGAMS\Downloads\New folder\Sindhu_8_17.xlsx")


#data preprocessing
# type 1 is police department. Since we can't distribute to legal department removing them and removing outof state orders
df2 = df[(df['type_1'] != 1) & (df['state'] == "Texas")]
#datetime format
df2 = df2.copy()
df2['date'] = pd.to_datetime(df2['date'])
df2['year'] = df2['date'].dt.year
df2['month'] = df2['date'].dt.month
#duplicates. several individuals from the same household can each make a request. One indivdual is limited to one order per month.
duplicates = ['first_name', 'last_name', 'street_address', 'city', 'state', 'zip_code','month']
df3 = df2.drop_duplicates(subset=duplicates, keep='first')


monthly_request = df2.groupby(['year', 'month']).size().reset_index(name='request_count')
pivot_table = monthly_request.pivot_table(index='month', columns='year', values='request_count')
plt.figure(figsize=(10, 6))

#yellow to green to blue (cmap='YlGnBu'), annot=True (annotate the cells with new numbers), fmt='.0f' no floating point
sns.heatmap(pivot_table, cmap='YlGnBu', annot=True, fmt='.0f')  
plt.title('Monthly Narcan Request Trends Over Years')
plt.xlabel('Year')
plt.ylabel('Month')
plt.show()



# Convert zip_code column to string
df['zip_code'] = df['zip_code'].astype(str)
# Extract 5-digit zip codes
zip_code_extract = df['zip_code'].str.extractall(r'(\b\d{5}\b)')[0]
# Count the frequency of zip codes
zip_code_freq= zip_code_extract.value_counts()


import matplotlib.pyplot as plt
# Plotting the top 20 zip codes by frequency
top_zip_codes = zip_code_freq.head(5)
#10- width and 6 height in inches
plt.figure(figsize=(10, 6))
top_zip_codes.plot(kind='bar')
plt.title('Top 5 Zip Codes by Frequency')
plt.xlabel('Zip Code')
plt.ylabel('Frequency')
#tick marks prevent overlapping
plt.xticks(rotation=45)
#prevent label, title cut off
plt.tight_layout()
plt.show()














# Rename the index column to "zipcode" and the value column to "frequency"
zip_code_freq = zip_code_freq.rename_axis('zip code').reset_index(name='frequency')


# Save zip_code_freq_by_year to a CSV file
zip_code_freq.to_csv('zip_code_freq_SM.csv', index=False)
































