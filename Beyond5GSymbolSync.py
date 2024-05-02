import numpy as np
import random as r
import math as m
import matplotlib.pyplot as plt

# Expected Synchronization Bit Stream 
WLAN = '01111110111011001110100010100100111110011001010110001100001001011110101010000010110101110010001110000000111100010000110100110110'
Ethernet = '10101010101010101010101010101010101010101010101010101010'
Fibonacci = '101100011111000000001111111111111000000000000000000000111111111111111111111111111111111100000000000000000000000000000000000000'
Alternating = '101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010'

# Preamble Manipulation
preamble = WLAN
preLength = len(preamble)

#-------------------------------------------------------------------------

# File IO, Accepts Text File Name and reads the lines of the file
bitstreamFile = input('Enter file name: ')
with open(bitstreamFile, 'r') as fid:
    fid = fid.readlines()

# Sets the read lines to a variable
bitstream = fid[0]

# Measures the length of the bitstream and reports it's length
bitstreamLen = len(bitstream)

#--------------------------------------------------------------------------

# Inserts the preamble somwhere randomly into the bitstream
def preInsert(bits, bitLen, pre):
    idx = r.randint(1, (bitLen - 2))
    return(bits[0:idx] + pre + bits[(idx):(bitLen)], idx)

#---------------------------------------------------------------------------

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

#-------------------------------------------------------------------------

# Finds the Synchronization part of the preamble after it is hidden bits are flipped in the bitstream
def findData(bits, pre, threshold, expected):
    thresholdMet = False
    stream = []

# Creates an array of the bitstream  
    for bit in bits:
        stream += [int(bit)]

    preamble = []

# Create an array of the preamble synchronization bitstream
    for bit in pre:
        preamble += [int(bit)]

# Sets the frame size to the length of the preamble
    frame = stream[:preLength]
    frame = np.array(frame)
    preamble = np.array(preamble)

# Sets the next index to the preamble length
    nextIndex = preLength

# Sets initial accuracy score to 100
    score = 100

# While frame is moved through the bitstream with the preamble inserted the differences are evaluated 
    while(nextIndex < bitstreamLen + preLength):
        frame = np.delete(frame, 0)
        frame = np.append(frame, stream[nextIndex])
        differenceArr = np.abs(frame - preamble)
        #print(differenceArr)
        score = np.sum(differenceArr) * 100 / preLength
        nextIndex += 1

# If threshold is met the loop will break because the preamble is found
        if(score <= threshold):
            thresholdMet = True
            break   

# If the index found is equal to the index of where the preamble was actually placed a 1 is returned       
    result = bits[nextIndex:]
    if(thresholdMet):
        if(result == expected):
            return 1

# If the index found was not the index of where the preamble was actually placed a -1 is returned
    return -1   
#-------------------------------------------------------------------------------------------------------------

#Testing Section

# Establishes a prompt to either plot a graph of accuracy vs noise or the bits after the preamble 
print("1. Locating the Preamble on a given Accuracy Threshold \n2. Exploring the relationship between Bits Flipped and accuracy at a given threshold\n3. Exploring the relationshiip between Bits Flipped and accuracy at four given thresholds")
Decision = input("Enter the number corresponding to the desired function you want this program to run: ")

# If decision is 1 prompts the user to input percentage of bits flipped, a threshold for accuracy and prints the bitstream with the preamble inserted
# Next the outcome is printed with the bits after the preamble if "found"
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

# If decision is 2, prompts the user to enter a desired accuracy threshold and ranges the noise from 15 percent on either side of the innaccuracy threshold equivalent
# The accuracy after repeated random simulations is then graphed
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
        for i in range(250):
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
    
# If value entered for decision is 3 then the following prompt is returned
elif (Decision == '3'):
    threshold1 = int(input("Enter the Desired Accuracy Threshold 1 (0-100): "))
    threshold2 = int(input("Enter the Desired Accuracy Threshold 2 (0-100): "))
    threshold3 = int(input("Enter the Desired Accuracy Threshold 3 (0-100): "))
    threshold4 = int(input("Enter the Desired Accuracy Threshold 4 (0-100): "))

    x = []
    y1 = []
    y2 = []
    y3 = []
    y4 = []

    inaccThreshold1 = 100 - threshold1
    inaccThreshold2 = 100 - threshold2
    inaccThreshold3 = 100 - threshold3
    inaccThreshold4 = 100 - threshold4 

    upperBound = 100
    lowerBound = 0

    inaccThresholdlist = [inaccThreshold1, inaccThreshold2, inaccThreshold3, inaccThreshold4]
    list.sort(inaccThresholdlist)

    if inaccThresholdlist[0] - 15 > 0:
        lowerBound = inaccThresholdlist[0] - 15
    if inaccThresholdlist[2] + 16 < 100:
        upperBound = inaccThresholdlist[3] + 16
        
    for noise in range(lowerBound, upperBound):
        x.append(noise)
        numCorrect1 = 0
        numCorrect2 = 0
        numCorrect3 = 0
        numCorrect4 = 0

        for i in range(1000):
            newBits, index = preInsert(bitstream, bitstreamLen, preamble)   # Places the preamble in the bitstream
            newBits = bitFlip(newBits, len(newBits), noise)
            expected = newBits[(index + preLength):]
            if(findData(newBits, preamble, inaccThresholdlist[0], expected) == 1):
                numCorrect1 += 1
            if(findData(newBits, preamble, inaccThresholdlist[1], expected) == 1):
                numCorrect2 += 1
            if(findData(newBits, preamble, inaccThresholdlist[2], expected) == 1):
                numCorrect3 += 1
            if(findData(newBits, preamble, inaccThresholdlist[3], expected) == 1):
                numCorrect4 += 1

        y1.append(numCorrect1)
        y2.append(numCorrect2)
        y3.append(numCorrect3)
        y4.append(numCorrect4)
        print("Num Correct 1:")
        print(numCorrect1)
        print("Num Correct 2:")
        print(numCorrect2)
        print("Num Correct 3:")
        print(numCorrect3)
        print("Num Correct 4:")
        print(numCorrect4)
        

    plt.plot(x, y1)
    plt.plot(x, y2)
    plt.plot(x, y3)
    plt.plot(x, y4)
    plt.xlabel('Noise Level')
    plt.ylabel('Number of Correct Results')
    plt.title('Correct Results vs. Noise Level')
    plt.legend([str(100 - inaccThresholdlist[0]) + '% Threshold', str(100 - inaccThresholdlist[1]) + '% Threshold', str(100 - inaccThresholdlist[2]) + '% Threshold', str(100 - inaccThresholdlist[3]) + '% Threshold'])
    plt.show()

# If value entered for decision is neither 1, 2, nor 3 then the following prompt is returned
else:
    print("Decision selected was not one of the options")