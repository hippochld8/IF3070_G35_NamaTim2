#File visualization.py untuk fungsi yang menggambar state dan plot hasil eksperimen
#Menggunakan matplotlib untuk visualisasi
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from models import effective_size

#Fungsi draw_state untuk menggambarkan visualisasi kapal dan kendaraan di dalamnya
def draw_state(state, value=None, title="State", save_path=None):
    fig, ax= plt.subplots(figsize=(6,6))
    for i, vid in enumerate(state.vehicles_inside()):
        x, y = state.positions[vid]
        w, l = effective_size(state.vehicles[vid])
        ax.add_patch(Rectangle((x, y), w, l, facecolor=plt.cm.tab20(i % 20), edgecolor="black"))
        ax.text(x + w / 2, y + l / 2, vid, ha="center", va="center")
    ax.set_xlim(0, state.ship.width)
    ax.set_ylim(0, state.ship.length)
    ax.invert_yaxis()
    ax.set_aspect("equal")
    ax.set_xticks(range(state.ship.width + 1))
    ax.set_yticks(range(state.ship.length + 1))
    ax.grid(True)
    outside = [
        f"{vid} ({state.vehicles[vid].width}x{state.vehicles[vid].length}, fee {state.vehicles[vid].shipping_fee})"
        for vid in state.vehicles_outside()
    ]
    ax.set_xlabel("Di luar kapal " + (", ".join(outside) if outside else "-"))
    if value is not None:
        title = f"{title}\nTotal Shipping Fee: {value} juta rupiah"
        ax.set_title(title)
    if save_path is not None:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

#Fungsi plot_cuve untuk plot nilai objective terhadap iterasi yang dipakai hill climbing dan simulated annealing
def plot_curve(history, title="Objective vs Iterasi", save_path=None):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(range(len(history)), history)
    ax.set_xlabel("Iterasi")
    ax.set_ylabel("Total ShippingFee (juta rupiah)")
    ax.set_title(title)
    ax.grid(True)
    if save_path is not None:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

#Fungsi plot_sa_probability untuk plot probabilitas penerimaan e^(dE/T) terhadap iterasi (khusus SA)
#prob_history = list angka, panjang = iterations (satu nilai per iterasi, tanpa nilai awal)
#Catatan: 1.0 untuk neighbor lebih baik, 0.0 untuk iterasi tanpa neighbor valid
def plot_sa_probability(prob_history, title="SA: e^(dE/T) vs Iterasi", save_path=None):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(range(1, len(prob_history) + 1), prob_history)
    ax.set_xlabel("Iterasi")
    ax.set_ylabel("e^(dE/T)")
    ax.set_title(title)
    ax.grid(True)
    if save_path is not None:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
