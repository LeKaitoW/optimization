import random
from agent import Agent

N = 2 #2, 4, 8, 16, 32
population_size = 20
precision = 4
max_counter = 1000
function = "sphere"

population = []
intermediate_population = []
#random.seed(234547)
#random.seed(9996)

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
	#second_parent=0
	for j, agent in enumerate(population):
		distance = 0
		for index, x in enumerate(agent.values):
			distance += pow(x-parents[0].values[index],N)
		distance = pow(distance,1/N)
		if distance>max_distance:
			max_distance = distance
			second_parent = j
		#else:
		#	print(0)
	parents.append(population.pop(second_parent))
	return parents


def arithmetical_crossing(parents):
	u_first = random.random()
	u_second = random.random()
	x_first = []
	x_second = []
	for i in range(N):
		x_first.append(round(u_first*parents[0].values[i]+(1-u_first)*parents[1].values[i], precision))
		x_second.append(round(u_second*parents[1].values[i]+(1-u_second)*parents[0].values[i], precision))
	new_first_agent = Agent(N, x_first)
	new_second_agent = Agent(N, x_second)
	rates = {}
	for parent in parents:
		rates.update({parent.rate : parent})
	rates.update({new_first_agent.rate : new_first_agent})
	rates.update({new_second_agent.rate : new_second_agent})
	keys = sorted(rates.keys())
	intermediate_population.append(rates.get(keys[0]))
	intermediate_population.append(rates.get(keys[1]))


def mutation_Michalewicz(agent, counter):
	b=5
	seq = [1, -1]
	u_first = random.choice(seq)
	r = random.random()
	delta = 0.1*(1-pow(r, (pow(1-(counter/max_counter),b)))) #интервал |[x-;x+]|=2
	x_new = []
	for value in agent.values:
		x_new.append(round(value+u_first*delta, precision))
	new_agent = Agent(N, x_new)
	if new_agent.rate<agent.rate:
		intermediate_population.append(new_agent)
	else:
		intermediate_population.append(agent)


def can_stop(population):
	for agent in population:
		if agent.rate<1:
			print(agent.values)
			return True
	return False

		
def find_best(population):
	rates = []
	for agent in population:
		rates.append(agent.rate)
	print('best=', min(rates))


population = init_population(population_size, 10, precision)

counter = 1

while ((not can_stop(population)) and (counter < max_counter)):
#while counter < 10:
	print('it = ', counter)
	for i in range(population_size//20):
		arithmetical_crossing(selection(population))
	for j in range(len(population)):
		mutation_Michalewicz(population[j], counter)
	population = intermediate_population[:]
	find_best(population)
	del intermediate_population[:]
	counter+=1
	for agent in population:
		print(agent.rate)

print(len(population))
