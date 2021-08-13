import random
import numpy as np
from skimage.data import camera
from PIL import Image
import matplotlib.pyplot as plt
import re


def bits2img(x, shape):

    m, n = shape
    I = np.zeros(m*n).astype(np.uint8)
    bts = re.findall('........', x)
    for i in range(0, len(bts)):
        I[i] = int(bts[i], 2)
    I = I.reshape(m, n)
    return I


def img2bits(I):

    m, n = I.shape
    s = ''
    for i in range(0, m):
        for j in range(0, n):
            s = s + '{0:08b}'.format(I[i, j])
    return s


def Wichmann_Hill(seedlst, listlength):
    seed1 = seedlst[0]
    seed2 = seedlst[1]
    seed3 = seedlst[2]

    numlist = []
    for i in range(listlength):

        seed1 = (171 * seed1) % 30269
        seed2 = (172 * seed2) % 30307
        seed3 = (170 * seed3) % 30323

        numlist.append((((seed1)/30269) + ((seed2) /
                       30307) + ((seed3)/30323)) % 1)

    # print(numlist[0:50])
        for i in range(len(numlist)):
            if numlist[i] <= 0.5:
                numlist.remove(numlist[i])
                numlist.append(0)
            if numlist[i] > 0.5:
                numlist.remove(numlist[i])
                numlist.append(1)
    numlist = "".join([str(_) for _ in numlist])

    return numlist


def xor(a, b):
    m = len(a)
    n = len(b)
    maxx = max(m, n)
    if (m < n):
        a = a + (n-m)*'0'
    if (n < m):
        b = b + (m-n)*'0'

    c = ''
    for i in range(0, maxx):
        c = c + str(int(a[i]) ^ int(b[i]))
    return c


def LCG(a, b, N):
    bc = ''
    t = 16
    k = 8

    try:
        parse = list(map(int, [a, b, N]))
        a = parse[0]
        b = parse[1]
        N = parse[2]
    except:
        return "Como que no funciona"

    x = round(random.random() * 200) % N

    for i in range(t):
        x = (a*x + b) % N  # Segun la formula del lab
        binary = bin(x).replace('b', '').zfill(k)
        bc += binary

    return bc


def xorLFSR(temp_list1, inp_leng, tap_positions, temp_list2):
    xorLFSR = temp_list1[inp_leng-1]
    for i in range(len(tap_positions)-1):
        xorLFSR = temp_list1[tap_positions[i]] ^ xorLFSR
    temp_list2.append(xorLFSR)
    return temp_list2


def LFSR(bits, tap_positions, inp_data, op_bits):

    tap_positions = [int(i) for i in tap_positions]

    inp_data.insert(0, inp_data[len(inp_data)-1])
    inp_data.pop()

    output = [0]
    inp_leng = len(inp_data)
    temp_list1 = inp_data
    temp_list2 = []
    for i in range(int(op_bits)):
        output.insert(0, temp_list1[inp_leng-1])
        xorLFSR(temp_list1, inp_leng, tap_positions, temp_list2)
        for i in range(inp_leng - 1):
            temp_list2.append(temp_list1[i])

        temp_list1 = temp_list2
        temp_list2 = []

    output.pop()
    output.reverse()
    output_data = ''.join(str(x) for x in output)
    return output_data


I = camera()
J = Image.fromarray(I)
J = J.resize((J.size[0]//2, J.size[1]//2), Image.LANCZOS)
I = np.array(J)
plt.figure()
plt.imshow(I, cmap='gray')
plt.show()
bitsImage = img2bits(I)

bits = np.random.randint(1, 30000)
tap_positions = [np.random.randint(1, 30000)]
inp_data = [1, 0, 1, 0, 1]
inp_data = [int(i) for i in inp_data]
op_bits = len(bitsImage)

s2 = LFSR(bits, tap_positions, inp_data, op_bits)
s3 = xor(bitsImage, s2)

I2 = bits2img(s2, I.shape)
I3 = bits2img(s3, I.shape)
I1 = bits2img(xor(s2, s3), I.shape)

plt.figure(figsize=(15, 8))
plt.subplot(1, 2, 1)
plt.imshow(I2, cmap='gray')
plt.subplot(1, 2, 2)
plt.imshow(I3, cmap='gray')
plt.show()

plt.figure(figsize=(15, 8))
plt.subplot(1, 2, 1)
plt.imshow(I1, cmap='gray')
plt.subplot(1, 2, 2)
plt.imshow(I3-I2, cmap='gray')
plt.show()
