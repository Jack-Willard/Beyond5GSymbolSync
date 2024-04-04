import numpy as np

# Expected Preamble

# File IO
file = input('Enter file name: ')

with open(file, 'r') as fid:
    fid = fid.readlines()
    print(fid)


