import random
import numpy as np
from skimage.data import camera
from PIL import Image
import matplotlib.pyplot as plt
import re

# Funcion de convertir bits a imagen


def bits2img(x, shape):

    m, n = shape
    I = np.zeros(m*n).astype(np.uint8)
    bts = re.findall('........', x)
    for i in range(0, len(bts)):
        I[i] = int(bts[i], 2)
    I = I.reshape(m, n)
    return I

# Funcion de convertir imagen a bits


def img2bits(I):

    m, n = I.shape
    s = ''
    for i in range(0, m):
        for j in range(0, n):
            s = s + '{0:08b}'.format(I[i, j])
    return s

# Generador pseudo aleatorio Wichmann_Hill


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

# Funcion XOR de dos cadenas


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

# Funcion de generador pseudo aleatorio LCG


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

# Funcion XOR de LFSR


def xorLFSR(temp_list1, inp_leng, tap_positions, temp_list2):
    xorLFSR = temp_list1[inp_leng-1]
    for i in range(len(tap_positions)-1):
        xorLFSR = temp_list1[tap_positions[i]] ^ xorLFSR
    temp_list2.append(xorLFSR)
    return temp_list2

# Funcion de generador de LFSR


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
# Imagen Original
plt.show()
bitsImage = img2bits(I)
# Numero aleatorio para la funcion LFSR
bits = np.random.randint(1, 30000)
# Numero aleatorio para la funcion LFSR
tap_positions = [np.random.randint(1, 30000)]
# Arreglo cambiante
# Numero aleatorio del tamano de la semilla fuente para la funcioon LFSR
# Cambiar para que cambie la imagen
sizeinp_data = np.random.randint(1, 10)
# Genera una lista de bits de longitud aleatoria para poder usarse en el generador de LFSR
inp_data = np.random.randint(2, size=sizeinp_data)
inp_data = [int(i) for i in inp_data]
op_bits = len(bitsImage)
# Llama a la funcion LFSR
s2 = LFSR(bits, tap_positions, inp_data, op_bits)
print("Se pobro con la semilla ", inp_data, "con el generador LFSR")
# Realiza un XOR entre la cadena de bits de la imagen y la cadina de bits del generador
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
