#File run_ga.py untuk menjalankan Genetic Algorithm pada dua eksperimen (masing-masing konfigurasi 3x) dan menyimpan hasil ke output
#Eksperimen 1: jumlah populasi tetap (kontrol), banyak iterasi divariasikan
#Eksperimen 2: banyak iterasi tetap (kontrol), jumlah populasi divariasikan
import json
from data import SHIP, VEHICLES
from genetic_algorithm import genetic_algorithm
from objective import objective
from visualization import draw_state, plot_curve, plot_ga_curve

RUNS = 3
BASE_POP = 30
BASE_ITER = 100
ITER_VARIATIONS = [50, 100, 200]
POP_VARIATIONS = [10, 30, 60]
summary = []

#Fungsi run_config untuk menjalankan satu konfigurasi sebanyak RUNS kali
def run_config(experiment, pop_size, iterations):
    for run in range(1, RUNS + 1):
        r = genetic_algorithm(SHIP, VEHICLES, pop_size, iterations)
        initial_value = objective(r["Initial State"])
        final_value = objective(r["Final State"])
        name = f"output/ga_{experiment}_pop{pop_size}_iter{iterations}_run{run}"
        label =  f"GA Pop {pop_size} Iter {iterations} Run {run}"
        draw_state(r["Initial State"], initial_value, f"{label} - State Awal", f"{name}_initial.png")
        draw_state(r["Final State"], final_value, f"{label} - State Akhir", f"{name}_final.png")
        plot_ga_curve(r["History Max"], r["History Average"], label, f"{name}_curve.png")
        summary.append({
            "experiment": experiment,
            "run": run,
            "Population Size": r["Population Size"],
            "Iterations": r["Iterations"],
            "Initial Value": initial_value,
            "Final Value": final_value,
            "Duration": round(r["Duration"], 4),
        })
        print(summary[-1])

#Eksperimen 1: populasi tetap, 3 variasi iterasi
for iterations in ITER_VARIATIONS:
    run_config("exp1", BASE_POP, iterations)

#Eksperimen 2: iterasi tetap, 3 variasi populasi
for pop_size in POP_VARIATIONS:
    run_config("exp2", pop_size, BASE_ITER)

with open("output/ga_summary.json", "w") as f: json.dump(summary, f, indent=2)