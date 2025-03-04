###Libraties
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

### Data Preprocessing
data = pd.read_excel("EDGAR_2024_GHG_booklet_2024.xlsx", sheet_name="GHG_totals_by_country")

#Create a list of countries in Europe, EU27 & Global
europe_list = [
    "ALB", "AUT", "BLR", "BEL", "BIH", "BGR", "HRV",
    "CZE", "DNK", "EST", "FIN", "FRA", "DEU", "GRC", "HUN",
    "ISL", "IRL", "ITA", "XKX", "LVA", "LTU", "LUX", "MLT", "MDA",
    "MNE", "NLD", "MKD", "NOR", "POL", "PRT", "ROU", "SRB", "SVK", "SVN",
    "ESP", "SWE", "CHE", "UKR", "GBR", "SCG"
]

european_union_list = ["EU27"]
global_list = ["GLOBAL TOTAL"]
europe = data[data["EDGAR Country Code"].isin(europe_list)]
european_union = data[data["Country"].isin(european_union_list)]
worldwide = data[data["Country"].isin(global_list)]

# Calculate the total emissions of Europe
europe.loc[37]=["EU", "EU", *europe.iloc[:,2:].sum().values]
europe_tot = pd.DataFrame(europe.iloc[37]).T

# Extract the emission data --> set y
europe_emissions = europe_tot.iloc[:,2:] 
european_union_emissions = european_union.iloc[:,2:] 
worldwide_emissions = worldwide.iloc[:,2:] 

# Extract years as a list --> set x
years = data.columns[2:].tolist() #list

# Turn all into arrays
europe = np.array(europe_emissions) #2d array
eu27 = european_union_emissions.to_numpy() #2d array
worldwide = worldwide_emissions.to_numpy() #2d array
year = np.array(years) #1d array

# Convert 2d arrays into 1d
europe = europe.flatten()
eu27 = eu27.flatten()
worldwide = worldwide.flatten()

# Assuming `year`, `europe`, `eu27`, and `worldwide` are defined arrays
year = np.array(year, dtype=np.int64)
europe = np.array(europe, dtype=np.float64)
eu27 = np.array(eu27, dtype=np.float64)
worldwide = np.array(worldwide, dtype=np.float64)

# Select every 2nd year the corresponding data
year_filtered = year[::2]
europe_filtered = europe[::2]
eu27_filtered = eu27[::2]
worldwide_filtered = worldwide[::2]

### Create the stacked bar chart
fig = plt.subplots(figsize=(12, 6))

#b_w_filtered = np.add(europe_filtered, eu27_filtered)

plt.bar(year_filtered-0.6, eu27_filtered, 0.7, label="EU27")
plt.bar(year_filtered, europe_filtered, 0.7,   label="EU")
plt.bar(year_filtered+0.6, worldwide_filtered, 0.7 ,label="Global")

# 1. EU27 Trend Line
coeff_eu27 = np.polyfit(year_filtered, eu27_filtered, 1)  # Linear fit (degree=1)
trend_eu27 = np.poly1d(coeff_eu27)
plt.plot(year_filtered, trend_eu27(year_filtered), linestyle="--", color="blue", label="EU27 Trend")

# 2. EU Trend Line
coeff_eu = np.polyfit(year_filtered, europe_filtered, 1)
trend_eu = np.poly1d(coeff_eu)
plt.plot(year_filtered, trend_eu(year_filtered), linestyle="--", color="red", label="EU Trend")

# 3. Global Trend Line
coeff_global = np.polyfit(year_filtered, worldwide_filtered, 1)
trend_global = np.poly1d(coeff_global)
plt.plot(year_filtered, trend_global(year_filtered), linestyle="--", color="green", label="Global Trend")

# Axis labels and title
plt.xlabel("Year")
plt.ylabel("GHG Emissions (Mt CO\u2082eq)")

# X,Y-axis ticks
plt.xticks(ticks=year[::2], labels=year[::2],rotation=45)  
plt.yticks(ticks= np.arange(0, 55000, 5000) )
plt.xlim(1968.5, 2023.5)
plt.grid(axis='y', linestyle='--', linewidth=0.7, alpha=0.1, color='black')

# Leg
plt.legend()

plt.savefig('evolution_of_ghg.png', dpi=300, bbox_inches='tight')

# Show the plot
plt.tight_layout()
plt.show()
