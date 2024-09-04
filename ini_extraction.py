# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 23:42:42 2024

@author: Pokhr002 """


# =============================================================================
# 
# THIS IS THE PIECE OF CODE TO EXTRACT THE FORCING AND MODEL FILES FOR SPECIFIC YEAR AND DATE TO RUN THE INITIAL CONDITION EFFECT ON THE MODEL RESULT
# 
# The output formats for the results are different as sometimes they are in 0000.000 format and sometimes they are in 000.000 and sometimes M00.00 (if it is monthly)
# 
# Therefore, there are different piece of code for each format.
# 
# =============================================================================


#%%

import pandas as pd
import shutil
import os
import re

dir_forcing = 'C:/SPHY_input/forcing/'
dir_model = 'C:/Users/pokhr002/OneDrive - Universiteit Utrecht/03Model/04_final_calib/results/'   # for baser a new model was ran because initially baser was not extracted as output
dir_output = 'C:/Users/pokhr002/OneDrive - Universiteit Utrecht/06Programming/01Python/04initial_conditions/processed_data/'
dir_extracted_forcing = 'C:/Users/pokhr002/OneDrive - Universiteit Utrecht/06Programming/01Python/04initial_conditions/raw_data/forcing_sel_yr/'
dir_renamed_forcing = 'C:/Users/pokhr002/OneDrive - Universiteit Utrecht/06Programming/01Python/04initial_conditions/processed_data/forcing_sel_yr/'

#%%

##########################  code to create df for the file names in SPHY based when the time step for simulation is daily ###############################


# Create a date range from '1991-01-01' to '2022-12-31'
dates = pd.date_range(start='1991-01-01', end='2022-12-31')

# Generate the filenames in the specified format
filenames = []
for i in range(12):
    for j in range(1, 1001):
        if j < 1000:
            filenames.append(f'{i:04d}.{j:03d}')
        else:
            i += 1
            filenames.append(f'{i:04d}.000')
            

# Combine dates and filenames as per the length of dates
combined_data = list(zip(dates, filenames[:len(dates)]))

# Create a DataFrame from the combined data
df = pd.DataFrame(combined_data, columns=['Dates', 'Filenames'])

# Filter for only the last day of February
df_last_day_feb = df[
    (df['Dates'].dt.month == 2) &  # Month is February
    (df['Dates'] == df['Dates'] + pd.offsets.MonthEnd(0))  # Date is the last day of the month
]

print(df_last_day_feb)
    
# # ############### Filter the DataFrame for all the dates in year 2018 which is the year we selected for the simulation ###############
###### Not needed in this code as below you can find the range for the years #######################
# df_sel = df[df['Dates'].dt.year == 2018]

#%%

############################################ to extract the forcing files ##################################################################

for year in range(2018, 2019):

    # Define the desired date range (March 1, 2018 to February end 2019)
    start_date = pd.to_datetime(f"{year}-03-01")
    end_date = pd.to_datetime(f"{year+1}-02-28")  # Includes February end
    
    # Filter the DataFrame for the desired date range
    df_filtered = df[(df['Dates'] >= start_date) & (df['Dates'] <= end_date)]
    
    
    # Mention the parameter that you want to extract from the files
    prefixes = ["prec", "tmax", "tmin", "tavg"]
    
    # Create directory for the extracted files (year as folder name)
    year_folder = os.path.join(dir_extracted_forcing , str(year))
    os.makedirs(year_folder, exist_ok=True) 
    
    # Iterate over each row in the DataFrame
    for prefix in prefixes:
        for index, row in df_filtered.iterrows():
            # Constructing the filename pattern
            filename_pattern = prefix + row["Filenames"]
            # Check if the file exists in the dir_forcing directory
            source_file = os.path.join(dir_forcing, filename_pattern)
            if os.path.exists(source_file):
                # If the file exists, copy it to the destination directory
                destination_file = os.path.join(year_folder, filename_pattern)
                shutil.copyfile(source_file, destination_file)
                print(f"File {filename_pattern} copied to {destination_file}")
            else:
                print(f"File {filename_pattern} not found in {dir_forcing}")
            
    
    # Specify the directory containing the destination files
    destination_dir = year_folder
    
    # Initialize an empty list to store filenames
    destination_filenames = []
    
    # Iterate over the files in the destination directory
    for filename in os.listdir(destination_dir):
        # Check if the file is a regular file (not a directory)
        if os.path.isfile(os.path.join(destination_dir, filename)):
            # Add the filename to the list
            destination_filenames.append(filename)
            
    print(f"Extraction for year {year} completed!")
            
print("Extraction for all years completed!")

# # Fill in any missing values with 0 to match the row counts
# if len(destination_filenames) < len(df_2004):
#     num_missing_rows = len(df_2004) - len(destination_filenames)
#     destination_filenames.extend([0] * num_missing_rows)

# # Add the list as a new column named "check" to the DataFrame df_2004
# df_2004['check'] = destination_filenames

# # Display the updated DataFrame
# print(df_2004)



#%% 

###### code to Rename the forcing for the selected year starting at 000.001 #####################


# Regular expression pattern to match the old file names
prefixes = ["prec", "tmax", "tmin", "tavg"]

# Regular expression pattern to dynamically match the prefixes
old_pattern_template = r'({prefix})\d{{4}}\.\d{{3}}'

# New filename parts initialization
new_part2_counter = 1
new_part1 = "0000"

for year in range(2018, 2019):  # Adjust the range as needed
    year_folder = os.path.join(dir_extracted_forcing, str(year))
    dest_year_folder = os.path.join(dir_renamed_forcing, str(year))
    
    # Check if the year folder exists in the source directory
    if os.path.exists(year_folder):
        # Create the same year folder in the destination directory if it doesn't exist
        os.makedirs(dest_year_folder, exist_ok=True)
        
        for prefix in prefixes:
            old_pattern = old_pattern_template.format(prefix=prefix)
            
            # Reset counters for each prefix
            new_part2_counter = 1
            new_part1 = "0000"
            
            for file in os.listdir(year_folder):
                if file.startswith(prefix):
                    # Construct the full source file path
                    src_file_path = os.path.join(year_folder, file)
                    
                    match = re.match(old_pattern, file)
                    if match:
                        new_part2 = str(new_part2_counter).zfill(3)
                        new_filename = f"{prefix}{new_part1}.{new_part2}"  # Assuming .tif extension
                        
                        # Update the counter for new_part2
                        new_part2_counter += 1
                        
                        # Construct the full destination file path with the new filename
                        dest_file_path = os.path.join(dest_year_folder, new_filename)
                        
                        # Copy or move the file to the new location with the new name
                        os.rename(src_file_path, dest_file_path)
                        print(f"Renamed and moved: {file} to {new_filename}")

print("Processing completed.")



#%% ################################################ Extracting the model outputs for initial conditions ##############################################


# Mention the parameter that you want to extract from the files with 0000.000  format
prefix = 'Subw'
directory = 'Subw/'

# Iterate over each row in the DataFrame
for index, row in df_last_day_feb.iterrows():
    # Constructing the filename pattern
    filename_pattern = prefix + row["Filenames"]
    # Check if the file exists in the dir_forcing directory
    source_file = os.path.join(dir_model, filename_pattern)
    if os.path.exists(source_file):
        # If the file exists, copy it to the destination directory
        destination_file = os.path.join(dir_output+directory, filename_pattern)
        shutil.copyfile(source_file, destination_file)
        print(f"File {filename_pattern} copied to {destination_file}")
    else:
        print(f"File {filename_pattern} not found in {dir_model}")
        
        
        
        
#%% ###################  For model files whose file patern is different  #####################################        

        ################# that was for groundwater, root water, baser and snow storage with 000.000  format ###############################
        
        
        ##### we are initialising the dataframe for the dates and file name as the format is different ######
        
# Generate the filenames in the specified format
filenames = []
for i in range(12):
    for j in range(1, 1001):
        if j < 1000:
            filenames.append(f'{i:03d}.{j:03d}')
        else:
            i += 1
            filenames.append(f'{i:03d}.000')
            

# Combine dates and filenames as per the length of dates
combined_data = list(zip(dates, filenames[:len(dates)]))

# Create a DataFrame from the combined data
df_changedformat = pd.DataFrame(combined_data, columns=['Dates', 'Filenames'])

# Filter for only the last day of February
df_last_day_feb_changedformat = df_changedformat[
    (df_changedformat['Dates'].dt.month == 2) &  # Month is February
    (df_changedformat['Dates'] == df_changedformat['Dates'] + pd.offsets.MonthEnd(0))  # Date is the last day of the month
]

print(df_last_day_feb_changedformat)        


#%%
# Mention the parameter that you want to extract from the files
prefix = 'Baser'
directory = 'Baser/'

# Iterate over each row in the DataFrame
for index, row in df_last_day_feb_changedformat.iterrows():
    # Constructing the filename pattern
    filename_pattern = prefix + row["Filenames"]
    # Check if the file exists in the dir_forcing directory
    source_file = os.path.join(dir_model, filename_pattern)
    if os.path.exists(source_file):
        # If the file exists, copy it to the destination directory
        destination_file = os.path.join(dir_output+directory, filename_pattern)
        shutil.copyfile(source_file, destination_file)
        print(f"File {filename_pattern} copied to {destination_file}")
    else:
        print(f"File {filename_pattern} not found in {dir_model}")
        
        

#%%

# =============================================================================
# Extraction of the monthly maps from the output 

## Why am I transferring the BaserM files not the daily? Am I supposed to run with the monthly file?
# =============================================================================

# List files in the output directory
files = os.listdir(dir_model)
# Filter filenames that start with "BaserM"
baserm_files = [filename for filename in files if filename.startswith('BaserM')]


# Define the number of times to repeat the pattern in this case 32 as there is 32 years
repeat_times = 32


selected_files = []
start_index = 1 # Define the initial index

# Iterate to select filenames for the specified number of times
for _ in range(repeat_times):
    # Select the filenames for the specified indices
    indices = range(start_index, start_index + 1)
    selected_files.extend([baserm_files[i] for i in indices])
    
    # Update the start index for the next iteration
    start_index += 12

# Create a DataFrame to store the selected filenames
baserM_df = pd.DataFrame({'BaserM_Files': selected_files})
df_last_day_feb.loc[:, 'BaserM_Files'] = baserM_df['BaserM_Files'].values


#%%

# Mention the parameter that you want to extract from the files
prefix = 'BaserM'
directory = 'BaserM/'

# Iterate over each row in the DataFrame
for index, row in baserM_df.iterrows():
    # Constructing the filename pattern
    filename_pattern = row["BaserM_Files"]
    # Check if the file exists in the dir_forcing directory
    source_file = os.path.join(dir_model, filename_pattern)
    if os.path.exists(source_file):
        # If the file exists, copy it to the destination directory
        destination_file = os.path.join(dir_output,directory,filename_pattern)
        shutil.copyfile(source_file, destination_file)
        print(f"File {filename_pattern} copied to {destination_file}")
    else:
        print(f"File {filename_pattern} not found in {dir_model}")
        
        
        
        
        

