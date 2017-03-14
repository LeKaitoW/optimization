import random

N = 2 #2, 4, 8, 16, 32
F = 0

def init_population(population_size, max, precision):
	population = []
	for index in range(population_size):
		for x in range(N):
			population.append(round(random.random()*max, precision))
	print(population)
	return population

def encoding(population):
	encoding_population = []
	for value in population:
		encoding_population.append((u'%.2f'%value).replace('.', ''))
	print(encoding_population)
	

def sphere_function():
	for i in range(1, N+1):
		F += pow(generation[i-1],2)
		
population = init_population(4, 100, 2)
