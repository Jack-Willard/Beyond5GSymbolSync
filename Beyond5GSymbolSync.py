import numpy as np
import random as r
import math as m
import matplotlib.pyplot as plt


# Expected Preamble
WLAN = '01111110111011001110100010100100111110011001010110001100001001011110101010000010110101110010001110000000111100010000110100110110'
Ethernet = '10101010101010101010101010101010101010101010101010101010'
Fibonacci = '101100011111000000001111111111111000000000000000000000111111111111111111111111111111111100000000000000000000000000000000000000'
#Alternating = 

# Preamble Manipulation
preamble = WLAN
preLength = len(preamble)
#Thresh = int(input('Enter Desired Preamble Accuracy Threshold (0 - 100): '))

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
    return(bits[0:idx] + pre + bits[(idx):(bitLen)], idx)

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
def findData(bits, pre, threshold, expected):
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
    while(nextIndex < bitstreamLen + preLength):
        frame = np.delete(frame, 0)
        frame = np.append(frame, stream[nextIndex])
        differenceArr = np.abs(frame - preamble)
        #print(differenceArr)
        score = np.sum(differenceArr) * 100 / preLength
        nextIndex += 1
        if(score <= threshold):
            thresholdMet = True
            break            

    result = bits[nextIndex:]
    if(thresholdMet):
        if(result == expected):
            return 1

    return -1   


#-------------------------------------------------------------------------------------------------------------

#Testing Section

print("1. Locating the Preamble on a given Accuracy Threshold \n2. Exploring the relationship between Bits Flipped and accuracy at a given threshold")
Decision = input("Enter the number corresponding to the desired function you want this program to run: ")

if (Decision == '1'):
    Percent = int(input('Enter Desired Percentage of Bits Flipped (0 - 100): '))
    newBits, index = preInsert(bitstream, bitstreamLen, preamble)   # Places the preamble in the bitstream
    newBits = bitFlip(newBits, len(newBits), Percent)
    threshold = int(input("Enter the Desired Accuracy Threshold (0-100): "))
    inaccThreshold = 100 - threshold
    print("The following is the bitstream with the preamble inserted")
    print(newBits)
    print("The following result is the outcome of the simulation:")
    expected = newBits[(index + preLength):]
    result = findData(newBits, preamble, inaccThreshold, expected)
    if(result == 1):
        print("Successful\nResult-")
        print(expected)
    else:
        print("Unsuccessful, output not found correctly")

elif (Decision == '2'):
    threshold = int(input("Enter the Desired Accuracy Threshold (0-100): "))
    x = []
    y = []
    inaccThreshold = 100 - threshold
    upperBound = 100
    lowerBound = 0
    if inaccThreshold - 15 > 0:
        lowerBound = inaccThreshold - 15

    if inaccThreshold + 16 < 100:
        upperBound = inaccThreshold + 16
        
    for noise in range(lowerBound, upperBound):
        x.append(noise)
        numCorrect = 0
        for i in range(1000):
            newBits, index = preInsert(bitstream, bitstreamLen, preamble)   # Places the preamble in the bitstream
            newBits = bitFlip(newBits, len(newBits), noise)
            expected = newBits[(index + preLength):]
            if(findData(newBits, preamble, inaccThreshold, expected) == 1):
                numCorrect += 1
        y.append(numCorrect)
        print("Num Correct:")
        print(numCorrect)

    plt.plot(x, y)

    plt.xlabel('Noise Level')
    plt.ylabel('Number of Correct Results')
    plt.title('Correct Results vs. Noise Level')

    plt.show()
    

else:
    print("Decision selected was not one of the options")
