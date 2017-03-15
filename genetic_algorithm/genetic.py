import random
from agent import Agent

N = 2 #2, 4, 8, 16, 32
population_size = 10
precision = 2
population = []
intermediate_population = []

def init_population(population_size, max, precision):
	for index in range(population_size):
		values = []
		for x in range(N):
			values.append(round(random.random()*max, precision))
		population.append(Agent(N, values))
	return population


def selection(population):
	parents = []
	parents.append(population.pop(random.randrange(len(population))))
	max_distance = 0
	for agent in population:
		distance = 0
		for index, x in enumerate(agent.values):
			distance += pow(x-parents[0].values[index],N)
		distance = pow(distance,1/N)
		print(distance)
		if distance>max_distance:
			max_distance = distance
			second_parent = index
	parents.append(population.pop(second_parent))
	intermediate_population.extend(parents)
	return parents


def arithmetical_crossing(parents):
	u = random.random()
	x_first = []
	x_second = []
	for i in range(N):
		x_first.append(round(u*parents[0].values[i]+(1-u)*parents[1].values[i], precision))
		x_second.append(round(u*parents[1].values[i]+(1-u)*parents[0].values[i], precision))
	intermediate_population.append(Agent(N, x_first))
	intermediate_population.append(Agent(N, x_second))


def encoding(population):
	encoding_population = []
	for value in population:
		encoding_population.append((u'%.2f'%value).replace('.', ''))
	print(encoding_population)		
		
population = init_population(population_size, 10, precision)
arithmetical_crossing(selection(population))
