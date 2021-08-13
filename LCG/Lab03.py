import random

def LCG(a, b, N):
	bc = '' 
	t = 16 
	k = 8

	try:
		parse = list(map(int,[a, b, N])) 
		a = parse[0]
		b = parse[1]
		N = parse[2]
	except:
		return "Como que no funciona"
	
	x = round(random.random() * 200) % N

	for i in range(t): 
		x = (a*x + b) % N  # Segun la formula del lab
		binary = bin(x).replace('b','').zfill(k)
		bc += binary

	return bc

print(LCG(2, 4, 1000))


# Referncias del codigo
# https://physik.uni-graz.at/~pep/CompOriPhys/Python/LCG_histogram.py


 
 