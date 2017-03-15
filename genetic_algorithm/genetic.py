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
	for j, agent in enumerate(population):
		distance = 0
		for index, x in enumerate(agent.values):
			distance += pow(x-parents[0].values[index],N)
		distance = pow(distance,1/N)
		if distance>max_distance:
			max_distance = distance
			second_parent = j
	parents.append(population.pop(second_parent))
	intermediate_population.extend(parents)
	return parents


def arithmetical_crossing(parents):
	u_first = random.random()
	u_second = random.random()
	x_first = []
	x_second = []
	for i in range(N):
		x_first.append(round(u_first*parents[0].values[i]+(1-u_first)*parents[1].values[i], precision))
		x_second.append(round(u_second*parents[1].values[i]+(1-u_second)*parents[0].values[i], precision))
	intermediate_population.append(Agent(N, x_first))
	intermediate_population.append(Agent(N, x_second))


def test_selection(intermediate_population, population):
		for i in range(population_size):
			population.append(intermediate_population[i])


def can_stop(population):
	for agent in population:
		if agent.rate<5:
			print(agent.values)
			return True


def encoding(population):
	encoding_population = []
	for value in population:
		encoding_population.append((u'%.2f'%value).replace('.', ''))
	print(encoding_population)		
		
population = init_population(population_size, 5, precision)

counter = 0
while not can_stop(population):
	print(counter)
	for i in range(population_size//2):
		arithmetical_crossing(selection(population))
	test_selection(intermediate_population,population)
	counter+=1
	
print(population)
