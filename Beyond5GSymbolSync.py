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

