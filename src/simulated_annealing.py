#File simulated_annealing.py, algoritma Simulated Annealing untuk memaksimalkan objective (total shipping fee)
#Format hasil mengikuti kesepakatan tim: initial_state, final_state, history, duration, iterations + metrik khusus SA
import math
import random
import time
from objective import objective
from neighbors import random_initial_state, random_neighbor

#Fungsi simulated_annealing
#Parameter:
#   initial_temp     : suhu awal T0
#   cooling_rate     : faktor pendinginan geometrik (T = T * cooling_rate), 0 < cooling_rate < 1
#   min_temp         : suhu minimum, pencarian berhenti jika T < min_temp
#   max_iterations   : batas maksimum iterasi
#Karena kasusnya maksimasi, delta = neighbor_value - current_value
#   delta > 0  -> neighbor selalu diterima
#   delta <= 0 -> neighbor diterima dengan probabilitas e^(delta/T)
def simulated_annealing(ship, vehicles, initial_temp=100.0, cooling_rate=0.995,
                        min_temp=0.01, max_iterations=10000):
    start = time.perf_counter()

    current = random_initial_state(ship, vehicles)  #state awal random yang valid
    initial = current.copy()                        #salinan agar state awal tidak berubah
    current_value = objective(current)
    history = [current_value]                       #nilai objective sebelum iterasi pertama (indeks = 0)
    prob_history = []                               #nilai e^(delta/T) tiap iterasi (1.0 jika neighbor lebih baik / tidak ada neighbor)
    stuck_count = 0                                 #frekuensi 'stuck' di local optima (neighbor lebih buruk/sama ditolak)
    temp = initial_temp
    iterations = 0

    while iterations < max_iterations and temp > min_temp:
        iterations += 1
        neighbor = random_neighbor(current)
        if neighbor is None:                        #tidak ada neighbor valid -> tetap di current state, dihitung stuck
            stuck_count += 1
            prob_history.append(0.0)
            history.append(current_value)
            temp *= cooling_rate
            continue

        neighbor_value = objective(neighbor)
        delta = neighbor_value - current_value
        if delta > 0:                               #neighbor lebih baik -> selalu diterima
            prob = 1.0
            accept = True
        else:                                       #neighbor sama/lebih buruk -> diterima dengan probabilitas e^(delta/T)
            prob = math.exp(delta / temp)
            accept = random.random() < prob
            if not accept:
                stuck_count += 1

        if accept:
            current = neighbor
            current_value = neighbor_value
        prob_history.append(prob)
        history.append(current_value)
        temp *= cooling_rate                        #turunkan suhu

    duration = time.perf_counter() - start
    return {
        "initial_state": initial,
        "final_state": current,
        "history": history,
        "duration": duration,
        "iterations": iterations,
        "prob_history": prob_history,
        "stuck_count": stuck_count,
        "initial_temp": initial_temp,
        "cooling_rate": cooling_rate,
    }
