import pandas as pd

""" 
business_df = pd.read_json('business.json', lines=True)

categories_df = business_df['categories'].str.split(', ', expand=True).stack().reset_index(level=1, drop=True).rename('category')
category_counts = categories_df.value_counts()
print(category_counts)

business_df['categories'].fillna('Unknown', inplace=True)

food_and_restaurants_df = business_df[business_df['categories'].str.contains('Food|Restaurants')]

food_and_restaurants_df.to_json('filtered_data.json', orient='records', lines=True)
food_and_restaurants_df.to_csv('filtered_data.csv', index=False)

filtered_data = pd.read_json('filtered_data.json', lines=True)
Veg_df = filtered_data[filtered_data['categories'].str.contains('Vegetarian|Vegan', case=False, na=False)]
Veg_df.to_csv('Veg_data.csv', index=False)

STATE Wise:
state_counts = Veg_df['state'].value_counts()
print(state_counts)

PA    480
FL    267
LA    132
TN    129
MO    106
IN     95
NJ     90
AZ     77
AB     72
CA     63
NV     55
ID     34
DE     24
IL      5
"""

"""
CITY Wise
veg_data = pd.read_csv('Veg_data.csv')

pa_veg_data = veg_data[veg_data['state'] == 'PA']

city_counts_pa_veg = pa_veg_data['city'].value_counts()
print(city_counts_pa_veg)

Philadelphia    277
Doylestown       10
Malvern           8
Ardmore           8
Bryn Mawr         7
               ...
Dresher           1
Morrisville       1
Roslyn            1
Blue Bell         1
Stowe             1
"""
"""
Extracting the csv just for the Philadelphia city.

veg_data = pd.read_csv('Veg_data.csv')

philadelphia_veg_data = veg_data[veg_data['city'] == 'Philadelphia']

philadelphia_veg_data.to_csv('Philadelphia_Veg_data.csv', index=False)

veg_data = pd.read_csv('Veg_data.csv')

philadelphia_veg_data = veg_data[veg_data['city'] == 'Philadelphia']

philadelphia_veg_data.to_csv('Philadelphia_Veg_data.csv', index=False)

"""

"""
missing_values = philadelphia_veg_data.isnull().sum()
print("Missing Values:\n", missing_values)
Missing Values:
business_id      0
name             0
address          1
city             0
state            0
postal_code      0
latitude         0
longitude        0
stars            0
review_count     0
is_open          0
attributes       2
categories       0
hours           20
"""
philadelphia_veg_data = pd.read_csv('Philadelphia_Veg_data.csv')
philadelphia_veg_data.fillna('NA', inplace=True)
#Replacing missing values with NA for the moment.

#duplicates = philadelphia_veg_data[philadelphia_veg_data.duplicated()]
#print(duplicates)
#No duplicates, the variable "duplicates" is empty
"""
Optional: 
sorted_data = philadelphia_veg_data.sort_values(by=['postal_code', 'stars'])
print(sorted_data)
sorted_data.to_csv('Philadelphia_Veg_data_sorted.csv', index=False)
"""
"""

review_df_head = pd.read_json('review.json', lines=True, chunksize=5)

for chunk in review_df_head:
    column_names = chunk.columns
    print(column_names)
    break 
    
Index(['review_id', 'user_id', 'business_id', 'stars', 'useful', 'funny',
       'cool', 'text', 'date'],
      dtype='object')
"""

unique_postal_codes = philadelphia_veg_data['postal_code'].unique()
#print(len(unique_postal_codes)) : 35!


# Splitting the DataFrame and save to separate CSV files based on postal codes
""""
for postal_code in unique_postal_codes:
    subset_data = philadelphia_veg_data[philadelphia_veg_data['postal_code'] == postal_code]
    output_filename = f'veg_data_{postal_code}.csv'
    subset_data.to_csv(output_filename, index=False)
"""
