#File run_sa.py untuk menjalankan Simulated Annealing sebanyak 3x dan menyimpan hasil ke output
#Dijalankan dari root repo: python src/run_sa.py
import json
from data import SHIP, VEHICLES
from simulated_annealing import simulated_annealing
from visualization import draw_state, plot_curve, plot_sa_probability

RUNS = 3
summary = []

for run in range(1, RUNS + 1):
    r = simulated_annealing(SHIP, VEHICLES, initial_temp=100.0, cooling_rate=0.998, min_temp=0.01, max_iterations=10000)
    draw_state(r["Initial State"], r["Initial Value"], f"SA Run {run} - State Awal", f"output/sa_run{run}_initial.png")
    draw_state(r["Final State"], r["Final Value"], f"SA Run {run} - State Akhir", f"output/sa_run{run}_final.png")
    plot_curve(r["History"], f"SA Run {run}", f"output/sa_run{run}_curve.png")
    plot_sa_probability(r["Prob History"], f"SA Run {run}: e^(dE/T) vs Iterasi", f"output/sa_run{run}_prob.png")
    summary.append({
        "run": run,
        "Initial Value": r["Initial Value"],
        "Final Value": r["Final Value"],
        "Iterations": r["Iterations"],
        "Duration": round(r["Duration"], 4),
        "Stuck Count": r["Stuck Count"],
    })
    print(summary[-1])

with open("output/sa_summary.json", "w") as f:json.dump(summary, f, indent=2)
