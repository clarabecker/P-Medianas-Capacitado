#!/usr/bin/python3
import os
import sys
import subprocess
import random

# Get the parameters as command line arguments
configuration_id = sys.argv[1]
instance_id = sys.argv[2]
seed = sys.argv[3]
instance = ' '.join(sys.argv[4:7])
conf_params = ' '.join(sys.argv[7:])

# Create execution command
fixed_params = '--max_iterations 1000'
command = f'python3 ./src/ig.py --instance {instance} {fixed_params} {conf_params}'

# Define the stdout and stderr files
r = str(random.randint(1, 999999))
out_file = './c' + str(configuration_id) + '-' + str(instance_id) + '-' + r + '.stdout'
err_file = './c' + str(configuration_id) + '-' + str(instance_id) + '-' + r + '.stderr'

# Execute
outf = open(out_file, "w")
errf = open(err_file, "w")
return_code = subprocess.call(command, stdout = outf, stderr = errf, shell = True)
outf.close()
errf.close()

# Check return code
if return_code != 0:
    print('Command returned code <' + str(return_code) + '>.')
    sys.exit(1)

# Check output file
if not os.path.isfile(out_file):
    print('Output file <' + out_file  + '> not found.')
    sys.exit(1)

# Get result and print it
result = open(out_file).readlines()[-1]
result = int(result.replace('\n', ''))
print(result)

# Clean files and exit
os.remove(out_file)
os.remove(err_file)
sys.exit(0)
