import random
from agent import Agent

N = 2 #2, 4, 8, 16, 32
population = []

def init_population(population_size, max, precision):
	for index in range(population_size):
		values = []
		for x in range(N):
			values.append(round(random.random()*max, precision))
		population.append(Agent(N, values))
	print(population)
	return population


def encoding(population):
	encoding_population = []
	for value in population:
		encoding_population.append((u'%.2f'%value).replace('.', ''))
	print(encoding_population)		
		
population = init_population(4, 100, 2)
