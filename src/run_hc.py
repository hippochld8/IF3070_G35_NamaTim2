#File run_hc.py untuk menjalankan Stochastic Hill-Climbing sebanyak 3x dan menyimpan hasil ke output
import json
from data import SHIP, VEHICLES
from hill_climbing import stochastic_hill_climbing
from visualization import draw_state, plot_curve

RUNS = 3
summary = []

for run in range(1, RUNS + 1):
    r = stochastic_hill_climbing(SHIP, VEHICLES)
    draw_state(r["Initial State"], r["Initial Value"], f"HC Run {run} - State Awal", f"output/hc_run{run}_initial.png")
    draw_state(r["Final State"], r["Final Value"], f"HC Run {run} - State Akhir", f"output/hc_run{run}_final.png")
    plot_curve(r["History"], f"HC Run {run}", f"output/hc_run{run}_curve.png")
    summary.append({
        "run": run,
        "Initial Value": r["Initial Value"],
        "Final Value": r["Final Value"],
        "Iterations": r["Iterations"],
        "Duration": round(r["Duration"], 4),
    })
    print(summary[-1])

with open("output/hc_summary.json", "w") as f:json.dump(summary, f, indent=2)