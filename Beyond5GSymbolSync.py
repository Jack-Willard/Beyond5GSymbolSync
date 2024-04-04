import numpy as np
import random as r

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

# Inserts the preamble somwhere randomly into the bitstream
def preInsert(bits, bitLen, pre):
    idx = r.randint(1, (bitLen - 2))
    return(bits[0:idx] + pre + bits[(idx):(bitLen)])

# Function to find optimal Accuracy Threshold
# 'bits' is the bitstream with the preamble inserted, 'pre' is the expected preamble
def preambleBitstreamOptim(bits, pre):
    print('Pre')

# Function to find and report Data
def findData(bits, pre):
    print('Data')

# Function to flip a certain percentage of the bits by subtracting each element by 1
# and changing the -1 indexes to 0
# 'bits' is the bitstream with the preamble inserted, 'percent' is the percent of bits to be flipped
def bitFlip(bits, percent):
    print('Flip')

newBits = preInsert(bitstream, bitstreamLen, preamble)
# percent = preambleBitstreamOptim(, preamble)