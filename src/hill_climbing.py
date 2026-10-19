#File hill_climbing.py untuk tes Stochastic Hill Climbing pada kasus kendaraan dan kapal
#Mengembalikan format hasil yang terdiri dari:
#initial_state, final_state, history, duration, iterations
import time
from objective import objective
from neighbors import random_initial_state, random_neighbor

#Fungsi stochastic_hil_climbing untuk tes kasus dengan algoritma stochastic hill climbing
def stochastic_hill_climbing(ship, vehicles, max_iterations=1000, max_no_improve=200):
    start = time.perf_counter()

    current = random_initial_state(ship, vehicles)
    initial = current.copy()
    current_value = objective(current)
    history = [current_value]
    no_improve = 0
    iterations = 0

    while iterations < max_iterations and no_improve < max_no_improve:
        iterations += 1
        neighbor = random_neighbor(current)
        if neighbor is None:
            no_improve += 1
            history.append(current_value)
            continue
        neighbor_value = objective(neighbor)
        if neighbor_value > current_value:
            current = neighbor
            current_value = neighbor_value
            no_improve = 0
        else:
            no_improve += 1
        history.append(current_value)
    
    duration = time.perf_counter() - start
    return{
        "initial_state": initial,
        "final_state": current,
        "history": history,
        "duration": duration,
        "iterations": iterations,
    }