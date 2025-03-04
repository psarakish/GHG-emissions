### Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

### Data preprocessing
data = pd.read_excel("EDGAR_2024_GHG_booklet_2024.xlsx", sheet_name="GHG_per_capita_by_country")
#Class -> Classification of countries based on their income group by The World Bank
# https://datahelpdesk.worldbank.org/knowledgebase/articles/906519-world-bank-country-and-lending-groups
data1 = pd.read_excel("CLASS.xlsx")
data1=data1[['Economy', 'Code', 'Income group']]
data1=data1[data1['Income group'].notna()]

merged = data.merge(data1[['Code', 'Income group']],
                   left_on='EDGAR Country Code',
                   right_on='Code',
                   how='left')

merged=merged[merged['Income group'].notna()]

summed_emission=merged.groupby('Income group').sum(numeric_only=True)
summed_emissions_transposed = summed_emission.T

### Create the plot
plt.figure(figsize=(12, 6))

for income_group in summed_emissions_transposed.columns:
    plt.plot(summed_emissions_transposed.index, summed_emissions_transposed[income_group], label=income_group)

plt.xlabel('Year')
plt.ylabel('GHG Emissions (t CO₂ eq / cap)')
plt.xticks(ticks=summed_emissions_transposed.index[::2], labels=summed_emissions_transposed.index[::2],rotation=45)  
plt.yticks(ticks= np.arange(0, 1600, 200) )

plt.grid(axis='y', linestyle='--', linewidth=0.7, alpha=0.1, color='black')
plt.xlim(1968.5, 2023.5)
plt.legend()
plt.savefig('evolution_of_ghgpc.png', dpi=300, bbox_inches='tight')
plt.tight_layout()

plt.show()
