import numpy as np
import random as r
import math as m


# Expected Preamble
WLAN = '01111110111011001110100010100100111110011001010110001100001001011110101010000010110101110010001110000000111100010000110100110110'
Ethernet = '10101010101010101010101010101010101010101010101010101010'

# Preamble Manipulation
preamble = WLAN
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
def findData(bits, pre, threshold):
    thresholdMet = False
    stream = []
    for bit in bits:
        stream += [int(bit)]
    
    preamble = []
    for bit in pre:
        preamble += [int(bit)]

    frame = stream[:preLength]
    frame = np.array(frame)
    preamble = np.array(preamble)

    nextIndex = preLength
    score = 100
    while(nextIndex < bitstreamLen):
        frame = np.delete(frame, 0)
        frame = np.append(frame, stream[nextIndex])
        differenceArr = np.abs(frame - preamble)
        #print(differenceArr)
        score = np.sum(differenceArr) * 100 / preLength
        nextIndex += 1
        if(score <= threshold):
            thresholdMet = True
            break            

    if(thresholdMet):
        return bits[nextIndex:]

    return ("Threshold not met")   

#-------------------------------------------------------------------------------------------------------------

#Testing Section

print("1. Locating the Preamble on a given Inaccuracy Threshold \n2. Exploring the relationship between Bits Flipped and accuracy at a given threshold")
Decision = input("Enter the number corresponding to the desired function you want this program to run: ")

if (Decision == '1'):
    Percent = int(input('Enter Desired Percentage of Bits Flipped (0 - 100): '))
    newBits1 = preInsert(bitstream, bitstreamLen, preamble)   # Places the preamble in the bitstream
    newBits2 = bitFlip(newBits1, len(newBits1), Percent)
    threshold = input("Enter the Desired Inaccuracy Threshold (0-100): ")
    print("The following is the bitstream with the preamble inserted")
    print(newBits2)
    print("The following result is the outcome of the simulation:")
    result = findData(newBits2, preamble, int(threshold))
    print(result)

elif (Decision == '2'):
    threshold = input("Enter the Desired Accuracy Threshold (0-100): ")
    

else:
    print("Decision selected was not one of the options")




