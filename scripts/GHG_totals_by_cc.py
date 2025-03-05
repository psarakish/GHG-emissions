### Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

### Data preprocessing
data = pd.read_excel("EDGAR_2024_GHG_booklet_2024.xlsx", sheet_name="GHG_totals_by_country")
# In order to assign each country its respective continent label,
# a list of country and continent codes was obtained from 
# this github repo -> https://gist.github.com/stevewithington/20a69c0b6d2ff846ea5d35e5fc47f26c#file-country-and-continent-codes-list-csv-csv
data1 = pd.read_csv("country-and-continent-codes-list-csv.csv")
data1=data1[['Three_Letter_Country_Code', 'Continent_Name']]
data1=data1[data1['Three_Letter_Country_Code'].notna()]

merged = data.merge(data1[['Three_Letter_Country_Code', 'Continent_Name']],
                   left_on='EDGAR Country Code',
                   right_on='Three_Letter_Country_Code',
                   how='left')

merged=merged.drop(columns=['EDGAR Country Code', 'Three_Letter_Country_Code'])

# Update the continent of Russia to Asia
merged.loc[merged['Country'] == 'Russia', 'Continent_Name'] = 'Asia'

cols = merged.columns.tolist()
last_col = cols.pop()
cols.insert(1, last_col)
merged = merged[cols]
merged=merged[merged['Continent_Name'].notna()]

global_list = ["GLOBAL TOTAL"]
worldwide = data[data["Country"].isin(global_list)]
worldwide_emissions = worldwide.iloc[:,2:] # worldwide emissions
worldwide = worldwide_emissions.to_numpy() #2
worldwide = worldwide.flatten()
world_emissions = merged.iloc[:, 2:].sum(axis=0)
merged['Total Country Emissions']=merged.iloc[:,2:].sum(axis=1)
continent_emissions = merged.groupby('Continent_Name')['Total Country Emissions'].sum()
merged['Country Contribution'] = (merged['Total Country Emissions'] / world_emissions.sum()) * 100
continent_contribution = (continent_emissions / world_emissions.sum()) * 100

merged_filtered = merged[merged['Country Contribution'] > 2.5]

# Sort the data for countries and continents by their respective contributions
merged_filtered_sorted = merged_filtered.sort_values(by='Country Contribution')
continent_contribution_sorted = continent_contribution.sort_values()

### Create the bar chart
plt.figure(figsize=(12, 6))

# Plot the sorted countries and their contributions
plt.bar(merged_filtered_sorted['Country'], merged_filtered_sorted['Country Contribution'], label='Countries', 
        color='coral', alpha=1)

# Plot the sorted continents and their contributions
plt.bar(continent_contribution_sorted.index, continent_contribution_sorted, label='Continents', 
        color='brown', alpha=1)

# Axis labels and title
plt.xlabel('Countries & Continents')
plt.xticks(rotation=45)
plt.ylabel('Contribution to Total GHG Emissions (%)')
plt.yticks(ticks=np.arange(0, 55, 5))
plt.grid(axis='y', linestyle='--', linewidth=0.7, alpha=0.1, color='black')
plt.legend()

plt.savefig('contibution.png', dpi=300, bbox_inches='tight')


plt.tight_layout()
plt.show()


