import random
import copy
import time
from models import State
from objective import objective, is_valid
from neighbors import random_initial_state, random_neighbor

def init_population(ship, vehicles, popu_size):
    return [random_initial_state(ship, vehicles) for _ in range(popu_size)]

def tournament_selection(population, k=3):
    k=min(k, len(population))
    peserta = random.sample(population, k)
    return max(peserta, key=objective)

def mutate(state, mutation_rate=0.2):
    if random.random() < mutation_rate:
        hasil = random_neighbor(state)
        if hasil is not None:
            return hasil
    return state

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

def genetic_algorithm(ship, vehicles, popu_size, iterations, mutation_rate=0.2):
    start = time.perf_counter()

    population = init_population(ship, vehicles, popu_size)
    best = max(population, key=objective)
    initial = best.copy()
    history_max = []
    history_avg = []

    for _ in range(iterations):
       values = [objective(s) for s in population]
       history_max.append(max(values))
       history_avg.append(sum(values) / len(values))

       best = max(population, key=objective)
       new_population = [best.copy()]
       while len(new_population) < popu_size:
           a = tournament_selection(population)
           b = tournament_selection(population)
           child = crossover(a, b)
           child = mutate(child, mutation_rate)
           new_population.append(child)
       population = new_population

    final = max(population, key=objective)
    duration = time.perf_counter() - start
    return {
         "initial_state": initial,
        "final_state": final,
        "history_max": history_max,
        "history_avg": history_avg,
        "duration": duration,
        "iterations": iterations,
        "popu_size": popu_size,
    }

