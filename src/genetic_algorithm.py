# File genetic_algorithm.py untuk algoritma Genetic Algorithm pada kasus kendaraan dan kapal
# Mengembalikan dictionary hasil: Algorithm, Initial State, Final State, History Max, History Average, Duration, Iterations, Population Size
import random
import copy
import time
from models import State
from objective import objective, is_valid
from neighbors import random_initial_state, random_neighbor

# Fungsi init_population untuk membuat populasi awal berisi state acak yang valid
def init_population(ship, vehicles, pop_size):
    return [random_initial_state(ship, vehicles) for _ in range(pop_size)]

# Fungsi tournament_selection untuk memilih satu parent dari populasi
def tournament_selection(population, fitness=None, k=3):
    if fitness is None:
        fitness = [objective(s) for s in population]
    k=min(k, len(population))
    participants = random.sample(range(len(population)), k)
    winner = max(participants, key=lambda i: fitness[i])
    return population[winner]

# Fungsi mutate untuk mengubah state sedikit dengan peluang mutation_rate
def mutate(state, mutation_rate=0.2):
    if random.random() < mutation_rate:
        neighbor = random_neighbor(state)
        if neighbor is not None:
            return neighbor
    return state

# Fungsi crossover untuk membuat satu child dari dua parent
# Tiap kendaraan diambil dari salah satu parent, lalu diperbaiki (repair):
# kendaraan yang membuat state tidak valid dikembalikan ke None (tidak diangkut)
def crossover(parent1, parent2):
    child = State(
        parent1.ship, copy.deepcopy(parent1.vehicles),
        {vid: None for vid in parent1.vehicles},
    )
    order = list(child.vehicles.keys())
    random.shuffle(order)
    for vid in order:
        parent = random.choice([parent1, parent2])
        if parent.positions[vid] is None:
            continue
        child.vehicles[vid].orientation = parent.vehicles[vid].orientation
        child.positions[vid] = parent.positions[vid]
        if not is_valid(child):
            child.positions[vid] = None
    return child

# Fungsi genetic_algorithm sebagai fungsi utama
def genetic_algorithm(ship, vehicles, pop_size, iterations, mutation_rate=0.2):
    start = time.perf_counter()

    population = init_population(ship, vehicles, pop_size)
    fitness = [objective(s) for s in population]
    best_index = max(range(len(population)), key=lambda i: fitness[i])
    initial = population[best_index].copy()
    history_max = []
    history_avg = []

    for _ in range(iterations):
       history_max.append(max(fitness))
       history_avg.append(sum(fitness) / len(fitness))

       best_index = max(range(len(population)), key=lambda i: fitness[i])
       new_population = [population[best_index].copy()]
       while len(new_population) < pop_size:
           a = tournament_selection(population, fitness)
           b = tournament_selection(population, fitness)
           child = crossover(a, b)
           child = mutate(child, mutation_rate)
           new_population.append(child)
       population = new_population
       fitness = [objective(s) for s in population]

    best_index = max(range(len(population)), key=lambda i: fitness[i])
    final = population[best_index]
    duration = time.perf_counter() - start
    return {
        "Algorithm": "Genetic Algorithm",
         "Initial State": initial,
        "Final State": final,
        "History Max": history_max,
        "History Average": history_avg,
        "Duration": duration,
        "Iterations": iterations,
        "Population Size": pop_size,
    }

