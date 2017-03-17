import random
import matplotlib.pyplot as plot
from agent import Agent

N = 2  # 2, 4, 8, 16, 32
population_size = 20
precision = 4
max_counter = 1000
function = "sphere"

current_population = []
intermediate_population = []
best_rates = []
iterations = []
# random.seed(123)


def init_population(population, size, maximum, accuracy):
    for m in range(size):
        values = []
        for x in range(N):
            values.append(round(random.random()*maximum, accuracy))
        population.append(Agent(function, values))
    return population


def selection(population):
    parents = []
    first_parent = random.randrange(len(population))
    parents.append(population.pop(first_parent))
    max_distance = 0
    second_parent = 0
    for n, agent in enumerate(population):
        distance = 0
        for p, x in enumerate(agent.values):
            distance += pow(x - parents[0].values[p], N)
        distance = pow(distance, 1 / N)
        if distance > max_distance:
            max_distance = distance
            second_parent = n
    parents.append(population.pop(second_parent))
    return parents


def arithmetical_crossing(parents, population):
    u_first = random.random()
    u_second = random.random()
    x_first = []
    x_second = []
    for i in range(N):
        x_first.append(round(u_first * parents[0].values[i] + (1 - u_first) * parents[1].values[i], precision))
        x_second.append(round(u_second * parents[1].values[i] + (1 - u_second) * parents[0].values[i], precision))
    new_first_agent = Agent(function, x_first)
    new_second_agent = Agent(function, x_second)
    rates = {}
    for parent in parents:
        rates.update({parent.rate: parent})
    rates.update({new_first_agent.rate: new_first_agent})
    rates.update({new_second_agent.rate: new_second_agent})
    population = pick_best(rates, population, 2)
    return population


def mutation_michalewicz(agent, iteration, population):
    b = 5
    interval = 0.2
    seq = [1, -1]
    u_first = random.choice(seq)
    r = random.random()
    delta = interval / 2 * (1 - pow(r, (pow(1 - (iteration / max_counter), b))))
    x_new = []
    for value in agent.values:
        x_new.append(round(value + u_first * delta, precision))
    new_agent = Agent(function, x_new)
    rates = {new_agent.rate: new_agent, agent.rate: agent}
    population = pick_best(rates, population, 1)
    return population


def pick_best(rates, population, number):
    keys = sorted(rates.keys())
    for k in range(number):
        population.append(rates.get(keys[k]))
    return population


def can_stop(population):
    for agent in population:
        if agent.rate < 0.005:
            print(agent.values)
            return True
    return False


def find_best(population, iteration):
    rates = []
    for agent in population:
        rates.append(agent.rate)
    best = min(rates)
    print('best=', best)
    best_rates.append(best)
    iterations.append(iteration)
    return best


current_population = init_population(current_population, population_size, 10, precision)

counter = 1

while (not can_stop(current_population)) and (counter < max_counter):
    # while counter < 10:
    print('it = ', counter)
    for i in range(population_size // 20):
        intermediate_population = arithmetical_crossing(selection(current_population),
                                                        intermediate_population)
    for j in range(len(current_population)):
        intermediate_population = mutation_michalewicz(current_population[j],
                                                       counter, intermediate_population)
        current_population = intermediate_population[:]
    find_best(current_population, counter)
    del intermediate_population[:]
    counter += 1

print(len(current_population))
plot.plot(iterations, best_rates)
plot.xlabel('iterations')
plot.ylabel('best value')
plot.show()
