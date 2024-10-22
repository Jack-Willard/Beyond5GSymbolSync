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
        else:
            return 2

# If the index found was not the index of where the preamble was actually placed a 2 is returned
    else:
        return 0


#-------------------------------------------------------------------------------------------------------------

#Testing Section

# Establishes a prompt to either plot a graph of accuracy vs noise or the bits after the preamble 
print("1. Locating the Preamble on a given Accuracy Threshold \n2. Exploring the relationship between Bits Flipped and accuracy at a given threshold\n3. Exploring the relationshiip between Bits Flipped and accuracy at four given thresholds \n4. Exploring the false positives and false negative cases at a given noise level")
Decision = input("Enter the number corresponding to the desired function you want this program to run: ")

# If decision is 1 prompts the user to input percentage of bits flipped, a threshold for accuracy and prints the bitstream with the preamble inserted
# Next the outcome is printed with the bits after the preamble if "found"
if (Decision == '1'):
    Percent = int(input('Enter Desired Percentage of Bits Flipped (0 - 100): '))
    newBits, index = preInsert(bitstream, bitstreamLen, preamble)   # Places the preamble in the bitstream
    newBits = bitFlip(newBits, len(newBits), Percent) # Flips Bits
    threshold = int(input("Enter the Desired Accuracy Threshold (0-100): ")) # Prompts the user to enter desired accuracy threshold
    inaccThreshold = 100 - threshold # Calculates innacuracy threshold
    print("The following is the bitstream with the preamble inserted")  
    print(newBits)
    print("The following result is the outcome of the simulation:")
    expected = newBits[(index + preLength):] # Finds expected location of preamble
    result = findData(newBits, preamble, inaccThreshold, expected) # Determines whether preamble found correctly
    
    # Prints whether preamble found correctly
    if(result == 1):
        print("Successful\nResult-")
        print(expected)
    else:
        print("Unsuccessful, output not found correctly")

# If decision is 2, prompts the user to enter a desired accuracy threshold and ranges the noise from 15 percent on either side of the innaccuracy threshold equivalent
# The accuracy after repeated random simulations is then graphed
elif (Decision == '2'):
    threshold = int(input("Enter the Desired Accuracy Threshold (0-100): "))  # Prompts the user to enter desired accuracy threshold
    x = []
    y = []
    inaccThreshold = 100 - threshold # Calculates innacuracy threshold
    upperBound = 100 
    lowerBound = 0

    # Calculates accuracy bounds for the simulation
    if inaccThreshold - 15 > 0:
        lowerBound = inaccThreshold - 15
    if inaccThreshold + 16 < 100:
        upperBound = inaccThreshold + 16
    
    # Calculates the number of correct preamble locations for each noise level at a certain accuracy threshold
    for noise in range(lowerBound, upperBound):
        x.append(noise)
        numCorrect = 0
        for i in range(250):
            newBits, index = preInsert(bitstream, bitstreamLen, preamble) # Places the preamble in the bitstream
            newBits = bitFlip(newBits, len(newBits), noise) # Flips Bits
            expected = newBits[(index + preLength):] # Finds expected location of preamble
            if(findData(newBits, preamble, inaccThreshold, expected) == 1): 
                numCorrect += 1
        y.append(numCorrect)
        print("Num Correct:")
        print(numCorrect)
    
    # Plots the collected data
    plt.plot(x, y)
    plt.xlabel('Noise Level')
    plt.ylabel('Number of Correct Results')
    plt.title('Correct Results vs. Noise Level')
    plt.show()
    
# If value entered for decision is 3 then the following prompt is returned
elif (Decision == '3'):

    # Prompts user to enter 4 accuracy thresholds
    threshold1 = int(input("Enter the Desired Accuracy Threshold 1 (0-100): "))
    threshold2 = int(input("Enter the Desired Accuracy Threshold 2 (0-100): "))
    threshold3 = int(input("Enter the Desired Accuracy Threshold 3 (0-100): "))
    threshold4 = int(input("Enter the Desired Accuracy Threshold 4 (0-100): "))

    # Creates empty arrays for each
    x = []
    y1 = []
    y2 = []
    y3 = []
    y4 = []

    # Calculates innaccuracy thresholds 
    inaccThreshold1 = 100 - threshold1
    inaccThreshold2 = 100 - threshold2
    inaccThreshold3 = 100 - threshold3
    inaccThreshold4 = 100 - threshold4 

    upperBound = 100
    lowerBound = 0

    # Sorts innacuracy thresholds
    inaccThresholdlist = [inaccThreshold1, inaccThreshold2, inaccThreshold3, inaccThreshold4]
    list.sort(inaccThresholdlist)

    # Sets bounds for entire innacuracy threshold
    if inaccThresholdlist[0] - 15 > 0:
        lowerBound = inaccThresholdlist[0] - 15
    if inaccThresholdlist[2] + 16 < 100:
        upperBound = inaccThresholdlist[3] + 16

    # Calculates the number of correct preamble locations for each noise level at each accuracy threshold
    for noise in range(lowerBound, upperBound):
        x.append(noise)
        numCorrect1 = 0
        numCorrect2 = 0
        numCorrect3 = 0
        numCorrect4 = 0

        for i in range(1000):
            newBits, index = preInsert(bitstream, bitstreamLen, preamble)   # Places the preamble in the bitstream
            newBits = bitFlip(newBits, len(newBits), noise) # Flips Bits
            expected = newBits[(index + preLength):] # Finds expected location of preamble
            if(findData(newBits, preamble, inaccThresholdlist[0], expected) == 1):
                numCorrect1 += 1
            if(findData(newBits, preamble, inaccThresholdlist[1], expected) == 1):
                numCorrect2 += 1
            if(findData(newBits, preamble, inaccThresholdlist[2], expected) == 1):
                numCorrect3 += 1
            if(findData(newBits, preamble, inaccThresholdlist[3], expected) == 1):
                numCorrect4 += 1

        # Creates and prints each number of correct declarations
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
        
    # Prints all data 
    plt.plot(x, y1)
    plt.plot(x, y2)
    plt.plot(x, y3)
    plt.plot(x, y4)
    plt.xlabel('Noise Level')
    plt.ylabel('Number of Correct Results')
    plt.title('Correct Results vs. Noise Level')
    plt.legend([str(100 - inaccThresholdlist[0]) + '% Threshold', str(100 - inaccThresholdlist[1]) + '% Threshold', str(100 - inaccThresholdlist[2]) + '% Threshold', str(100 - inaccThresholdlist[3]) + '% Threshold'])
    plt.show()

elif (Decision == '4'):
    Percent = int(input('Enter Desired Percentage of Bits Flipped (0 - 100): ')) # Prompts user to enter percentage of bits flipped
    
    # Creates empty arrays for each preamble searching outcome
    x = []
    fnegy = []
    fposy = []
    numCy = []

    # Cycles through accuracy threshold range 60 to 100 to find number of false positives, false negatives, and correct preamble location
    for threshold in range(60, 100):
        x.append(threshold)
        fpos = 0
        fneg = 0
        numCorrect = 0 
        for i in range (250):
            newBits, index = preInsert(bitstream, bitstreamLen, preamble)   # Places the preamble in the bitstream
            newBits = bitFlip(newBits, len(newBits), Percent) # Flips Bits
            expected = newBits[(index + preLength):] # Finds expected location of preamble
            returnVal = findData(newBits, preamble, 100 - threshold, expected)
            if(returnVal == 2):
                fpos += 1
            elif (returnVal == 0):
                fneg += 1
            elif (returnVal == 1):
                numCorrect += 1
            else:
                numCorrect = numCorrect
    
        # Appends data
        numCy.append(numCorrect)
        fposy.append(fpos)
        fnegy.append(fneg)
        print("Num Correct:" + str(numCorrect) + "\nNum False Pos:" + str(fpos) + "\nNum False neg:" + str(fneg))

    # Plots data   
    plt.plot(x, numCy)
    plt.plot(x, fposy)
    plt.plot(x, fnegy)
    plt.xlabel('Accuracy Thresholad')
    plt.ylabel('Results')
    plt.title('Results vs. Accuracy Threshold')
    plt.legend(["Number Correct", "False Positives", "False Negatives"])
    plt.show()

# If value entered for decision is neither 1, 2, 3, nor 4 then the following prompt is returned
else:
    print("Decision selected was not one of the options")