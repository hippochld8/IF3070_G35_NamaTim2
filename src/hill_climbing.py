#File hill_climbing.py untuk tes Stochastic Hill Climbing pada kasus kendaraan dan kapal
#Mengembalikan format hasil yang terdiri dari:
#1. Algorithm: Nama algoritma
#2. Initial State: state awal
#3. Final State: state akhir
#4. Initial Value: nilai objective state awal (dalam satuan juta rupiah)
#5. Final Value: nilai objective state akhir (dalam satuan juta rupiah)
#6. History: nilai objective tiap iterasi untuk plot
#7. Duration: durasi pencarian (dalam detik)
#8. Iterations: banyak iterasi hingga pencarian berhenti
import time
from objective import objective
from neighbors import random_initial_state, random_neighbor

#Fungsi stochastic_hil_climbing untuk tes kasus dengan algoritma stochastic hill climbing
def stochastic_hill_climbing(ship, vehicles, max_iterations=1000, max_no_improve=200):
    start = time.perf_counter()

    current = random_initial_state(ship, vehicles)  #cari random state awal yang valid
    initial = current.copy()                        #kerjakan di salinan agar state awal tidak berubah
    current_value = objective(current)              #nilai objective dari state awal
    history = [current_value]                       #nilai objective sebelum iterasi pertama (indeks = 0)
    no_improve = 0
    iterations = 0

    while iterations < max_iterations and no_improve < max_no_improve:
        iterations += 1
        neighbor = random_neighbor(current)         #cari random neighbor yang ingin dibandingkan dengan state awal
        if neighbor is None:                        #jika tidak ada neighbor yang valid, dihitung sebagai iterasi tanpa perbaikan (perpindahan)
            no_improve += 1
            history.append(current_value)
            continue
        neighbor_value = objective(neighbor)
        if neighbor_value > current_value:          #stocahstic hill climbing akan menerima neighbor jika nilainya lebih baik (kalau nilainya sama ditolak)
            current = neighbor
            current_value = neighbor_value
            no_improve = 0
        else:                                       #jika neighbor nilainya sama atau lebih buruk, tetap di current state dan dihitung sebagai iterasi tanpa perbaikan (perpindahan)
            no_improve += 1
        history.append(current_value)
    
    duration = time.perf_counter() - start
    return{
        "Algorithm": "Stochastic Hill Climbing",
        "Initial State": initial,
        "Final State": current,
        "Initial Value": history[0],
        "Final Value": current_value,
        "History": history,
        "Duration": duration,
        "Iterations": iterations,
    }