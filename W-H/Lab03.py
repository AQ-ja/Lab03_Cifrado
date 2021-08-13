import numpy as np
from skimage.data import camera     # estas librerías solo se usan para
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


seed1 = np.random.randint(1, 30000)
seed2 = np.random.randint(1, 30000)
seed3 = np.random.randint(1, 30000)
semillas = [seed1, seed2, seed3]


I = camera()
J = Image.fromarray(I)
J = J.resize((J.size[0]//2, J.size[1]//2), Image.LANCZOS)
I = np.array(J)
plt.figure()
plt.imshow(I, cmap='gray')
plt.show()

print("aqi")
bitsImage = img2bits(I)
print("aqi")

tam = len(bitsImage)
print("aqi")

s2 = Wichmann_Hill(semillas, tam)
print("aqi")

# s = np.random.choice(2, size=len(bitsImage))
# s2 = ''
# for i in range(0, len(s)):
#     s2 = s2 + str(s[i])

print(len(bitsImage))


# print((s2))
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
