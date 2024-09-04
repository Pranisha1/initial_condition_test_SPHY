# Model Workflow for Hydrological Simulations

This document describes the steps for running hydrological simulations with different initial conditions by configuring snow storage (SnowS), baseflow runoff (Baser), subsoil storage (Subw), and meteorological data (P, T) for a representative average year, and examining the flow conditions at various locations in the basin.

## Steps Overview

### STEP 1: Selecting an Average Representative Year
- Begin by selecting an average representative year for the simulation. This year will act as the base for running future tests. In this case the selected average year is 2018 so the hydrological period runs from Mar 2018 to Feb 2019.

### STEP 2: Analyze Snowfall Trend and Shift the Start Date
- Snow conditions peak around March rather than January. Therefore, the simulation should not begin in January. The starting point is set to March to better align with peak snow conditions.

### STEP 3: Run the Model for 32 Transient Years
- The model is run to simulate transient conditions over 32 years.
- Outputs are generated for each of these 32 years with various parameters like snow storage, baseflow runoff, and subsoil storage.

### STEP 4: Extract Initial Conditions for SnowS, Baser, and Subw
- For each year, extract maps of SnowS, Baser, and Subw at the end of February.
- These maps will later serve as initial conditions for running the average representative year simulation 32 times.

### STEP 5: Adjust Meteorological Data and Run the Representative Year
- The model running for a year with selected representative yearis initialised with different meteorological data (precipitation, temperature) extraced from 1991-2022.
- The model is run 32 times, starting from March 1 to the end of February, each time with different met conditions.
- The forcing data is renamed to start from `000.000` on March 1 to ensure alignment with the simulation timeline.

### STEP 6: Create Configuration Files for Initial Conditions
- Configuration files (`sphy_config`) are created for each year with specific initial conditions.
    - **SnowS**: For each configuration file, the initial snow storage is assigned based on the extracted SnowS map for the end of February for that year. The entry in the config file is:
      ``` 
      Initial Snow Storage (scalar map with initial snow storage (mm)): 
      SnowIni = SnowS/SnowS001.155
      ```
    - **Met Data**: The forcing folder path is linked to the meteorological conditions for the specific years.


### STEP 7: Parallel runs
- If the model is allowed to run one by one it takes forever. Therefore parallel runs was performed where temporary directory of SPHy was created to run selected 1 year with 32 config settings.

---
By following these steps, the simulation for different basin conditions can be properly configured, ensuring accurate representation of snow, runoff, and subsoil storage along with corresponding meteorological inputs.


## Codes that I have in this repository

### `ini_extraction.py`
- This script is used to extract the necessary files and configurations for running the initial condition tests.
- The following files are extracted:
  - **Forcing file**: The forcing file for the selected average year is extracted, and the filenames are renamed starting from `000.001` for March 1 to `000.365` for February 28 of the following year.
  - **Model outputs**: The script extracts model outputs from the calibrated model run, including daily maps for subsoil water (Subw), baseflow runoff (Baser), snow storage (SnowS), and meteorological data (Met). Also the forcing files for each year is also extracted to change the initial condition in the meteorology. 
  - **Map files**: Then from these outputs the maps for the last day of February for each year is extracted, where February 19th is used for leap years.

- For soil moisture, both **RootWater** and **SubWater** maps are extracted, and corresponding changes are made in the configuration file.

#### Configuration File Line Numbers for Updates:
- **RootWater & SubWater**: Line 160 and 163
- **SnowIni**: Line 405
- **BaseR**: Line 256

#### Map Files Extracted for Each Year:
| Date       | Filename for Each Parameter |
|------------|-----------------------------|
| 2/28/1991  | 0.059                       |
| 2/29/1992  | 0.425                       |
| 2/28/1993  | 0.79                        |
| 2/28/1994  | 1.155                       |
| 2/28/1995  | 1.52                        |
| 2/29/1996  | 1.886                       |
| 2/28/1997  | 2.251                       |
| 2/28/1998  | 2.616                       |
| 2/28/1999  | 2.981                       |
| 2/29/2000  | 3.347                       |
| 2/28/2001  | 3.712                       |
| 2/28/2002  | 4.077                       |
| 2/28/2003  | 4.442                       |
| 2/29/2004  | 4.808                       |
| 2/28/2005  | 5.173                       |
| 2/28/2006  | 5.538                       |
| 2/28/2007  | 5.903                       |
| 2/29/2008  | 6.269                       |
| 2/28/2009  | 6.634                       |
| 2/28/2010  | 6.999                       |
| 2/28/2011  | 7.364                       |
| 2/29/2012  | 7.73                        |
| 2/28/2013  | 8.095                       |
| 2/28/2014  | 8.46                        |
| 2/28/2015  | 8.825                       |
| 2/29/2016  | 9.191                       |
| 2/28/2017  | 9.556                       |
| 2/28/2018  | 9.921                       |
| 2/28/2019  | 10.286                      |
| 2/29/2020  | 10.652                      |
| 2/28/2021  | 11.017                      |
| 2/28/2022  | 11.382                      |

---

#### `replacing_line.py`
- This script is designed to update the `sphy_config` configuration file by replacing specific lines with the required initial map names and setting different output folder paths for each run.
- The script identifies the required lines in the config file, makes the necessary replacements, and saves the modified configuration file for each run.
- For each run, the updated config file is saved with a unique year number appended to the filename, ensuring that the configuration files are versioned and organized per year.

---

### `rreading_results.py`
- This script is responsible for reading and processing the results from each model run.
- It navigates to the output folder where the results are stored for each run.
- The script specifically reads the `QallDTS.tss` file, which contains the model's output data.
- After reading the data, it calculates the variance of the results across different runs.
- The results are saved as a **DataFrame (df)** for further analysis or reporting.

---

### `parallel_runs.sh`
- This shell script is used to automate and run multiple instances of the SPHY model in parallel.
- It creates temporary directories for each run to store intermediate files and results.
- The script executes the SPHY model with different configuration settings in parallel, significantly speeding up the execution time.
- Once each run completes, the results are saved in their respective output directories, allowing for efficient management of multiple configurations and results.

---

### ERRORS encountered:
There was discrepancy between the extracted files and the files for the last day of the Feb because of the numbering system. So the model was once again ran from the beginning to ensure everything is right. 
