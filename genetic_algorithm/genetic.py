import random
from agent import Agent

N = 2 #2, 4, 8, 16, 32
population_size = 20
precision = 4
max_counter = 1000
function = "sphere"

population = []
intermediate_population = []
random.seed(123)

def init_population(population, population_size, max, precision):
	for i in range(population_size):
		values = []
		for x in range(N):
			values.append(round(random.random()*max, precision))
		population.append(Agent(function, values))
	return population


def selection(population):
	parents = []
	first_parent = random.randrange(len(population))
	parents.append(population.pop(first_parent))
	max_distance = 0
	#second_parent=0
	for j, agent in enumerate(population):
		distance = 0
		for i, x in enumerate(agent.values):
			distance += pow(x-parents[0].values[i],N)
		distance = pow(distance,1/N)
		if distance>max_distance:
			max_distance = distance
			second_parent = j
	parents.append(population.pop(second_parent))
	return parents


def arithmetical_crossing(parents, population):
	u_first = random.random()
	u_second = random.random()
	x_first = []
	x_second = []
	for i in range(N):
		x_first.append(round(u_first*parents[0].values[i]+(1-u_first)*parents[1].values[i], precision))
		x_second.append(round(u_second*parents[1].values[i]+(1-u_second)*parents[0].values[i], precision))
	new_first_agent = Agent(function, x_first)
	new_second_agent = Agent(function, x_second)
	rates = {}
	for parent in parents:
		rates.update({parent.rate : parent})
	rates.update({new_first_agent.rate : new_first_agent})
	rates.update({new_second_agent.rate : new_second_agent})
	keys = sorted(rates.keys())
	population.append(rates.get(keys[0]))
	population.append(rates.get(keys[1]))
	return population


def mutation_Michalewicz(agent, counter, population):
	b=5
	interval = 0.2
	seq = [1, -1]
	u_first = random.choice(seq)
	r = random.random()
	delta = interval/2*(1-pow(r, (pow(1-(counter/max_counter),b))))
	x_new = []
	for value in agent.values:
		x_new.append(round(value+u_first*delta, precision))
	new_agent = Agent(function, x_new)
	if new_agent.rate<agent.rate:
		population.append(new_agent)
	else:
		population.append(agent)
	return population


def can_stop(population):
	for agent in population:
		if agent.rate<0.005:
			print(agent.values)
			return True
	return False

		
def find_best(population):
	rates = []
	for agent in population:
		rates.append(agent.rate)
	print('best=', min(rates))


population = init_population(population, population_size, 10, precision)

counter = 1

while ((not can_stop(population)) and (counter < max_counter)):
#while counter < 10:
	print('it = ', counter)
	for i in range(population_size//20):
		intermediate_population = arithmetical_crossing(selection(population),
		intermediate_population)
	for j in range(len(population)):
		intermediate_population = mutation_Michalewicz(population[j],
		counter, intermediate_population)
	population = intermediate_population[:]
	find_best(population)
	del intermediate_population[:]
	counter+=1

print(len(population))
