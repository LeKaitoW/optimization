import random
from agent import Agent

N = 2 #2, 4, 8, 16, 32
population_size = 20
precision = 2
max_counter = 1000
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
	#second_parent=0 костыль
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


def mutation_Michalewicz(agent, counter):
	b=5
	seq = [1, -1]
	u_first = random.choice(seq)
	r = random.random()
	delta = 1*(1-pow(r, (pow(1-(counter/max_counter),b)))) #интервал |[x-;x+]|=2
	x_new = []
	for value in agent.values:
		x_new.append(round(value+u_first*delta, precision))
	intermediate_population.append(Agent(N, x_new))


def test_selection(intermediate_population, population):
		average = []
		for agent in intermediate_population:
			average.append(agent.rate)
		print(average)
		average = sorted(average)[:population_size]
		#random.shuffle(average)
		#del average[9:]
		print(average)
		for agent in intermediate_population:
			if agent.rate in average:
				population.append(agent)
			if len(population)>population_size-1:
				break
		del intermediate_population[:]


def can_stop(population):
	for agent in population:
		if agent.rate<1:
			print(agent.values)
			return True
	return False


def encoding(population):
	encoding_population = []
	for value in population:
		encoding_population.append((u'%.2f'%value).replace('.', ''))
	print(encoding_population)		
		
population = init_population(population_size, 100, precision)

counter = 1

while ((not can_stop(population)) and (counter < max_counter)):
#while counter < 10:
	print(counter)
	for i in range(population_size//3):
		arithmetical_crossing(selection(population))
	for agent in population:
		mutation_Michalewicz(agent, counter)
		population.remove(agent)
	test_selection(intermediate_population,population)
	counter+=1

print(len(population))
