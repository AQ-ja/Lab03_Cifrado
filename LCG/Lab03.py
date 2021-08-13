import random

def LCG(a, b, m, N):
	bc = '' 
	t = 500000 
	k = 8

	try:
		parse = list(map(int,[a, b, m, N])) 
		a = parse[0]
		b = parse[1]
		m = parse[2]
		N = parse[3]
	except:
		return "Como que no funciona"
	
	x = round(random.random() * 100) % N

	for i in range(t): 
		x = (a*x + b) % N  # Segun la formula del lab
		binary = bin(x).replace('b','').zfill(k)
		bc += binary

	return bc

print(LCG(2, 4, 5, 10))


# Referncias del codigo
# https://physik.uni-graz.at/~pep/CompOriPhys/Python/LCG_histogram.py


 
 