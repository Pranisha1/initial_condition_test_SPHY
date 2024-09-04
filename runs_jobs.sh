# This is the code to run the jobs for the model. The link is made in such a way that this code has to be in the main folder of the SPHY model files.

#!/bin/bash
sphyroot=/scratch/depfg/pokhr002/SPHY3.0/SPHY3.0

#source activate sphy

# Iterate through years and construct commands for parallel execution
for index in {1..32}; do
  echo "Starting experiment: ${index}"
  cd "$sphyroot"
  
  year=$((1990 + index))
  config_filename="sphy_config_${index}_${year}.cfg"
  full_command="srun -n1 -N1 -c 8 -J $index python /scratch/depfg/pokhr002/SPHY3.0/SPHY3.0/sphy.py /scratch/depfg/pokhr002/SPHY3.0/SPHY3.0/$config_filename"

  # Display steps by printing the full command and its output
  echo "** Executing command: $full_command"

  # Execute the command and capture its output in a variable
  output=$(eval "$full_command" 2>&1)

  echo "$output"

  # Wait for the command to finish
  wait 

done

# Wait for any remaining background jobs
wait
