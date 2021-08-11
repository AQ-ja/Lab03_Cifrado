import random

print("Ingrese el valor de a:")
a = input()
print("Ingrese el valor de b:")
b = input()
print("Ingrese el valor de N:")
N = input()



def LCG(a, b, N):
	bc = '' 
	t = 8 
	k = 8 


	try:
		parse = list(map(int,[a, b, N])) 
		a = parse[0]
		b = parse[1]
		N = parse[2]
	except:
		return "Como que no funciona"
	
	x = random.randrange(200)%N

	for i in range(t): 
		x = (a*x + b)%N # Segun la formula del lab
		binary = bin(x).replace('b','').zfill(k)
		bc += binary

	return bc


print(LCG(a,b,N))


# Referncias del codigo
# https://physik.uni-graz.at/~pep/CompOriPhys/Python/LCG_histogram.py


 
 