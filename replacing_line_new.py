import os
import pandas as pd

####### ----- This code is use to replace the line and create a new config files ---------########

###### First all the file names is read and stored as df so that the names can be added into config files #####

###### The config files are made in C drive and then added in eejit for the simulation ##############################

# Get the directory of the current Python script
os.chdir("C:\\SPHY3.0")

modeldir = "C:\\SPHY3.0"
inputdir = "/scratch/depfg/pokhr002/SPHY3.0/input/"
outputdir = "/scratch/depfg/pokhr002/SPHY3.0/"
configdir = os.path.join(os.getcwd(), "config_all")
Snowdir = os.path.join(os.getcwd(), "SnowS")
Gwdir = os.path.join(os.getcwd(), "GrndW")
Rootwddir = os.path.join(os.getcwd(), "Rootw")
Subwddir = os.path.join(os.getcwd(), "Subw")
Baserdir = os.path.join(os.getcwd(), "Baser")

# Define parameters
params = ['SnowIni', 'GrndW', 'RootWater', 'SubWater', "Baser"]

# List of years
years = range(1991, 2023)

# Create DataFrame with year as index and parameters as columns
df = pd.DataFrame(index=years, columns=params)

def get_file_names(directory, param_name):
  file_names = []
  for filename in os.listdir(directory):
    if os.path.isfile(os.path.join(directory, filename)):
      file_names.append(filename)
  df[param_name] = file_names


# Loop through each parameter directory
for param, directory in zip(params, [Snowdir, Gwdir, Rootwddir, Subwddir, Baserdir]):
  get_file_names(directory, param)
  
# Reset the index and name the column 'years'
df = df.reset_index(drop=False).rename(columns={'index': 'year'})

# Print the DataFrame with filenames
print(df)

#%%

########## <<< This part of the code is to replace line. The values that do not need to be replaced is made as comment  >>>>> #######

# Loop over parameter combinations
for i, row in df.iterrows():
    # Existing config file path (modify as needed)
    config_file = os.path.join(configdir, "sphy_config.cfg")

    # Read the config file lines
    with open(config_file, 'r') as file:
        config_lines = file.readlines()
        
        
    # Replacing "inputdir" in config_lines
    for idx, line in enumerate(config_lines):
        if "inputdir" in line:
            config_lines[idx] = f"inputdir = {inputdir}\n"
            break
    
    folder_prefix = 'output_Baser/'
    # Create output directory if not exists
    output_dir = os.path.join(outputdir,folder_prefix + f"output_{row['year']}")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Replacing "outputdir" (adjust if different)
    for idx, line in enumerate(config_lines):
        if "outputdir" in line:
            # Use the previously defined output_dir variable
            config_lines[idx] = f"outputdir = {output_dir}/\n"
            break
        
    # # Replace SnowIni value directly in the config lines
    # new_value = row['SnowIni']
    # for idx, line in enumerate(config_lines):
    #     if line.startswith("SnowIni"):
    #         config_lines[idx] = f"SnowIni = SnowS/{new_value}\n"
    #         break


    # Replace Baser which is initial base routed runoff value directly in the config lines
    new_value = row['Baser']
    for idx, line in enumerate(config_lines):
        if line.startswith("BaseR "):
            config_lines[idx] = f"BaseR = Baser/{new_value}\n"
            break
        
    # # Replace GrndWdir value directly in the config lines
    # new_value = row['Gw']
    # for idx, line in enumerate(config_lines):
    #     if line.startswith("Gw              ="):
    #         config_lines[idx] = f"Gw              = Gw/{new_value}\n"
    #         break
        
######## Replace rootwater and subwater value in the config files for SOIL MOISTURE RUNS

    # # Replace Rootwater value directly in the config lines
    # new_value = row['RootWater']
    # for idx, line in enumerate(config_lines):
    #     if line.startswith("RootWater       = "):
    #         config_lines[idx] = f"RootWater       = Rootw/{new_value}\n"
    #         break
    
    # # Replace Subwater value directly in the config lines
    # new_value = row['SubWater']
    # for idx, line in enumerate(config_lines):
    #     if line.startswith("SubWater        ="):
    #         config_lines[idx] = f"SubWater        = Subw/{new_value}\n"
    #         break
                             
    # Create a new config file with the modified lines in the output directory
    new_config_file = os.path.join(configdir, f"sphy_config_{i+1}_{row['year']}.cfg")
    with open(new_config_file, 'w') as new_file:
        new_file.writelines(config_lines)

print("All SPHY model config files made.")

#%%  ####### This is to replace lines for the forcing data #######


for i, row in df.iterrows():
    # Existing config file path (modify as needed)
    config_file = os.path.join(configdir, "sphy_config.cfg")

    # Read the config file lines
    with open(config_file, 'r') as file:
        config_lines = file.readlines()
        
        # Replacing "inputdir" in config_lines
        for idx, line in enumerate(config_lines):
            if "inputdir" in line:
                config_lines[idx] = f"inputdir = /scratch/depfg/pokhr002/SPHY3.0/{inputdir}\n"
                break

        # Create output directory if not exists
        output_dir = os.path.join(outputdir, f"output_{row['year']}")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Replacing "outputdir" (adjust if different)
        for idx, line in enumerate(config_lines):
            if "outputdir" in line:
                # Use the previously defined output_dir variable
                config_lines[idx] = f"outputdir = /scratch/depfg/pokhr002/SPHY3.0/{output_dir}/\n"
                break
        
        # Replacing "Tmin" (adjust if different)
        for idx, line in enumerate(config_lines):
            if "Tmin" in line:
                # Use the previously defined output_dir variable
                config_lines[idx] = f"Tmin = forcing/{row['year']}/tmin\n"
                break
            
        # Replacing "Tmax" (adjust if different)
        for idx, line in enumerate(config_lines):
            if "Tmax" in line:
                # Use the previously defined output_dir variable
                config_lines[idx] = f"Tmax = forcing/{row['year']}/tmax\n"
                break
        
        # Replacing "Tavg" (adjust if different)
        for idx, line in enumerate(config_lines):
            if "Tair" in line:
                # Use the previously defined output_dir variable
                config_lines[idx] = f"Tair = forcing/{row['year']}/tavg\n"
                break
        
                 
        for idx, line in enumerate(config_lines):
            if line.startswith("Prec         	="):
                config_lines[idx] = f"Prec  = forcing/{row['year']}/prec\n"
                break
            
        # Create a new config file with the modified lines in the output directory
        new_config_file = os.path.join(configdir, f"sphy_config_{i+1}_{row['year']}.cfg")
        with open(new_config_file, 'w') as new_file:
            new_file.writelines(config_lines)

print("All SPHY model config files made.")

        