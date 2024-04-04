import numpy as np
import random as r
import math as m

# Expected Preamble
#WLAN = Enter WLAN preamble here
Ethernet = '10101010101010101010101010101010101010101010101010101010'

# Preamble Manipulation
preamble = Ethernet
preLength = len(preamble)
Percent = int(input('Enter Desired Percentage of Bits Flipped (0 - 100): '))

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

# Function to flip a certain percentage of the bits by subtracting each element by 1
# and changing the -1 indexes to 0
# 'bits' is the bitstream with the preamble inserted, 'percent' is the percent of bits to be flipped
def bitFlip(bits, bitLen, percent):
    numBits = m.floor((percent / 100) * bitLen)
    bitIdxs = r.sample(range(bitLen), numBits)

    bits = list(bits)

    for bit in bitIdxs:
        x = int(bits[bit])
        x = x - 1

        if (x == -1):
            x = 1
        
        bits[bit] = str(x)

    bits = "".join(element for element in bits)

    return(bits)

# Function to find optimal Accuracy Threshold
# 'bits' is the bitstream with the preamble inserted, 'pre' is the expected preamble
def preambleBitstreamOptim(bits, pre):
    print('Pre')

# Function to find and report Data for Troy
def findData(bits, pre):
    print('Data')

#-------------------------------------------------------------------------------------------------------------

#Testing Section

newBits = preInsert(bitstream, bitstreamLen, preamble)   # Places the preamble in the bitstream
newBits2 = bitFlip(newBits, len(newBits), Percent)
