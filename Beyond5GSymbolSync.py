import numpy as np

# Expected Preamble
#WLAN = Enter WLAN preamble here
Ethernet = '10101010101010101010101010101010101010101010101010101010'

# Preamble Manipulation
preamble = Ethernet
preLength = len(preamble)

#-------------------------------------------------------------------------

# File IO
bitstreamFile = input('Enter file name: ')

with open(bitstreamFile, 'r') as fid:
    fid = fid.readlines()

bitstream = fid[0]
bitstreamLen = len(bitstream)
#--------------------------------------------------------------------------

# Function to find optimal Accuracy Threshold
def preambleBitstreamOptim():
    print('Hello World')

# Function to find and report Data
def findData():
    print('Data')
    
# Function to flip a certain percentage of the bits