Beyond 5G Symbol Sync


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


preamble