# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 14:57:48 2024

@author: Pokhr002
"""

### This is the code to read the results from the 32 runs made for the average year. 

import os
import pandas as pd
from datetime import datetime

base_dir = "/scratch/depfg/pokhr002/SPHY3.0/output_baser/"
output_dir = "/scratch/depfg/pokhr002/SPHY3.0/xx"
prefix = "Baser" 

# Station number for modeled QTot (adjust as needed)
stn_number = 7

# List of desired output dataframes (modify names as needed)
stations = [
    "Karnali Chisapani",
    "Mugu-Humla Karnali confluence 1000",
    "Humla Karnali 2000",
    "West Seti Confluence",
    "Seti 2000",
    "Bheri Confluence",
    "Thuli Bheri 2000",
]

# Create a dictionary to store dataframes for each station
dataframes = {station: pd.DataFrame() for station in stations}

# Create datetime index for a year (adjust start date if needed)
start_date = datetime(2018, 1, 1)
end_date = datetime(2018, 12, 31)
date_range = pd.date_range(start=start_date, end=end_date, freq='D')


# Loop through output folders (output_1991 to output_2022)
for year in range(1991, 2023):
  result_dir = os.path.join(base_dir, f"output_{year}")
  if not os.path.exists(result_dir):
    continue  # Skip if directory doesn't exist

  # Find QALLDTS.tss file
  discharge_file = [f for f in os.listdir(result_dir) if f.startswith("QAllDTS.tss")][0]
  discharge_path = os.path.join(result_dir, discharge_file)

  # Read discharge data
  discharge_data = pd.read_table(discharge_path, skiprows=stn_number+3, header=None, delim_whitespace=True)
  discharge_data = discharge_data.iloc[:, 1:]
  
  # Set datetime index and rename first column
  discharge_data.insert(loc=0, column='Dates', value=date_range)
   
  for i, station in enumerate(stations):
        df = pd.DataFrame()
        df[str(discharge_data.columns[i+1]) + '_' + str(year)] = discharge_data[i+1]
        dataframes[station] = pd.concat([dataframes[station], df], axis=1)
        
        
#%%  

variance_df = pd.DataFrame()
 
# Print the dataframes for each station
for station, df in dataframes.items():
    df = df.set_index(date_range)
    df_monthly_average = df.resample('M').mean()
    variance = df_monthly_average.var(axis=1)
    variance_df[station] = variance
    
    print(f"Dataframe for {station}:")
    print(df)
    
    df.to_csv(os.path.join(output_dir, f"{station}_{prefix}.csv"))
    # print(f"Dataframe for {station} saved to {os.path.join(output_dir, f'{station}.csv')}")
    df_monthly_average.to_csv(os.path.join(output_dir, f"{station}_monthly_average_{prefix}.csv"))
    print(f"Monthly avg dataframe for {station} saved to {os.path.join(output_dir, f'{station}_monthly_average_{prefix}.csv')}")
    

print("Processing completed!")     
 


