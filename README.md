Beyond 5G Symbol Sync:
This code was meant to explore the operation of symbol synchronization. While the code is not optimized, this was not the point of the project. This code serves four purposes. 
1. Locating the Preamble on a given Accuracy Threshold
2. Exploring the relationship between Bits Flipped and accuracy at a given threshold
3. Exploring the relationshiip between Bits Flipped and accuracy at four given thresholds
4. Exploring the false positives and false negative cases at a given noise level
These are all functions of the code and can operate on various predefined preambles including the current synchronization part of the WLAN 802.11 preamble. The code to determine the synchronization portion of the
802.11 WLAN preamble is given below and was developed in MATLAB. 

Matlab Code to Develop 802.11 Preamble (128 bits)

x1 = 1;
x2 = 1;
x3 = 0;
x4 = 1;
x5 = 1;
x6 = 0;
x7 = 0;

arr1 = [x1, x2, x3, x4];
arr2 = [x5, x6, x7];

feed = [1];

preamble = '';
s = 128;

for c = 0:127
    A = xor(x4, x7);
    B = xor(A, feed);
    preamble = strcat(preamble, int2str(B));
    x7 = x6;
    x6 = x5;
    x5 = x4;
    x4 = x3;
    x3 = x2;
    x2 = x1;
    x1 = B;
end
