import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

census = pd.read_csv("census1900-2000.csv")

# Create histogram with age buckets of 0-4, 5-9, 10-14, ..., 90+
age_bins = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 
            55, 60, 65, 70, 75, 80, 85, 90, 94]
age_labels = ['0-4', '5-9', '10-14', '15-19', '20-24', 
              '25-29', '30-34', '35-39', '40-44', '45-49', 
              '50-54', '55-59', '60-64', '65-69', '70-74', 
              '75-79', '80-84', '85-89', '90+']

# Further split into either 1900 or 2000
census_1900 = census.loc[census['Year'] == 1900, ["Age", "People"]]
census_2000 = census.loc[census['Year'] == 2000, ["Age", "People"]]

# Plot w/ side-by-side bars for 1900 and 2000
plt.figure(figsize=(10, 6))
plt.hist([census_1900["Age"], census_2000["Age"]],
         bins=age_bins,
         weights=[census_1900["People"], census_2000["People"]],
         label=["1900", "2000"],
         alpha=0.5)
bin_centers = [(age_bins[i] + age_bins[i + 1]) / 2 for i in range(len(age_bins) - 1)]
plt.xticks(bin_centers, age_labels, rotation=45)

plt.xlabel("Age")
plt.ylabel("Number of people")
plt.title("Age distribution, 1900 vs 2000")
plt.legend()

# Save plot as .png file in folder
plt.savefig("age_distribution_1900_vs_2000.png")
