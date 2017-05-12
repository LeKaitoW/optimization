import random
import matplotlib.pyplot as plot
from agent import Agent


N = 2  # 2, 4, 8, 16, 32
population_size = 100
precision = 4
max_counter = 1000
function = 'Rastr'#'Rozen'#'sphere'#'Rastr'
stagnation_value = 1 / pow(10, precision)
stagnation_iterations = 50

current_population = []
intermediate_population = []
best_rates = []
iterations = []
#random.seed(83392)

counter = 1


def init_population(population, size, maximum, accuracy):
    for m in range(size):
        values = []
        for x in range(N):
            values.append(round(random.random() * 2*maximum, accuracy) - maximum)
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
    interval = 0.1
    seq = [1, -1]
    sign = random.choice(seq)
    r = random.random()
    delta = interval / 2 * (1 - pow(r, (pow(1 - (iteration / max_counter), b))))
    x_new = []
    for value in agent.values:
        x_new.append(round(value + sign * delta, precision))
    new_agent = Agent(function, x_new)
    rates = {new_agent.rate: new_agent, agent.rate: agent}
    population = pick_best(rates, population, 1)
    return population


def pick_best(rates, population, number):
    keys = sorted(rates.keys())
    for k in range(number):
        if number < len(keys):
            population.append(rates.get(keys[k]))
        else:
            population.append(rates.get(keys[0]))
    return population


def stagnation(best_values, iteration):
    i = 0
    for j in range(iteration - 1):
        if abs(best_values[iteration - j] - best_values[iteration - j - 1]) < stagnation_value:
            i += 1
            if i == stagnation_iterations:
                return True
    return False


def find_best(population, iteration):
    rates = []
    for agent in population:
        rates.append(agent.rate)
    best = min(rates)
    best_rates.append(best)
    iterations.append(iteration)
    return best


def make_points(population):
    x = []
    y = []
    for agent in population:
        x.append(agent.values[0])
        y.append(agent.values[1])
    return x, y


#graph_2.axis([-5, 5, -5, 5])


current_population = init_population(current_population, population_size, 5, precision)

while (not stagnation(best_rates, counter - 2)) and (counter < max_counter):
    for i in range(population_size//2):
        intermediate_population = arithmetical_crossing(selection(current_population), intermediate_population)
    for j in range(len(intermediate_population)):
        intermediate_population = mutation_michalewicz(intermediate_population[j], counter, intermediate_population)
    current_population = intermediate_population[:]
    x, y = make_points(current_population)

    find_best(current_population, counter)
    del intermediate_population[:]
    counter += 1

print(best_rates[counter - 2])
for agent in current_population:
    if agent.rate == best_rates[counter - 2]:
        print(agent.values)


figure_1 = plot.figure()
graph_1 = figure_1.add_subplot(111)
graph_1.plot(iterations, best_rates)
plot.xlabel('x1')
plot.ylabel('x2')

plot.show()
