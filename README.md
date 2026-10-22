# IF3070_G35_NamaTim2

Tugas Besar 1 IF3070 Dasar Inteligensi Artifisial 2026/2027.
Optimasi penataan kendaraan di geladak kapal kargo dengan algoritma local search
(Stochastic Hill-Climbing, Simulated Annealing, Genetic Algorithm).

## Deskripsi Singkat

Sistem menentukan kendaraan mana yang diangkut serta posisi dan orientasinya di geladak
(grid 2D) untuk memaksimalkan total ShippingFee, dengan constraint: tidak overlap,
berada dalam batas geladak, dan total berat tidak melebihi kapasitas kapal.

- State awal: random (valid)
- Move: tukar dua kendaraan, pindahkan kendaraan, ubah orientasi
- Visualisasi: Matplotlib (disimpan sebagai PNG di `output/`)

## Struktur Repository

```
src/    source code
docs/   laporan (PDF)
output/ hasil run algoritma (PNG dan JSON)
```

File utama di `src/`:

| File | Isi |
|---|---|
| `models.py` | Vehicle, Ship, State, fungsi geometri |
| `objective.py` | objective function dan constraint checker |
| `neighbors.py` | move, random_neighbor, random_initial_state |
| `data.py` | data eksperimen bersama (SHIP, VEHICLES) |
| `hill_climbing.py` | Stochastic Hill-Climbing |
| `simulated_annealing.py` | Simulated Annealing |
| `genetic_algorithm.py` | Genetic Algorithm |
| `visualization.py` | fungsi gambar state dan plot |
| `run_hc.py`, `run_sa.py`, `run_ga.py` | skrip eksperimen |

## Setup

Prasyarat: Python 3.9 atau lebih baru.

```bash
git clone https://github.com/hippochld8/IF3070_G35_NamaTim2.git
cd IF3070_G35_NamaTim2
pip install matplotlib
```

## Cara Menjalankan

Jalankan dari root repository:

```bash
python src/run_hc.py   # Stochastic Hill-Climbing, 3 run
python src/run_sa.py   # Simulated Annealing, 3 run
python src/run_ga.py   # Genetic Algorithm, variasi populasi dan iterasi
```

Hasil (gambar state awal/akhir, kurva objective, ringkasan JSON) tersimpan di `output/`.

TODO: tulis estimasi durasi tiap skrip (terutama GA).

## Parameter

| Algoritma | Parameter utama |
|---|---|
| Stochastic HC | `max_iterations`, `max_no_improve` |
| SA | `initial_temp`, `cooling_rate`, `min_temp`, `max_iterations` |
| GA | `pop_size`, `iterations`, `mutation_rate` |

## Pembagian Tugas

| NIM | Nama | Tugas |
| --- | --- | --- |
| 18224041 | Irghi Satya Priangga | 1. Membuat file:<br>&nbsp;&nbsp;&nbsp;&nbsp;- `src/data.py`<br>&nbsp;&nbsp;&nbsp;&nbsp;- `src/hill_climbing.py`<br>&nbsp;&nbsp;&nbsp;&nbsp;- `src/models.py`<br>&nbsp;&nbsp;&nbsp;&nbsp;- `src/neighbors.py`<br>&nbsp;&nbsp;&nbsp;&nbsp;- `src/objective.py`<br>&nbsp;&nbsp;&nbsp;&nbsp;- `src/run_hc.py`<br>&nbsp;&nbsp;&nbsp;&nbsp;- `src/visualization.py`<br>&nbsp;&nbsp;&nbsp;&nbsp;- `README.md`<br>2. Membuat repository dan semua folder di dalamnya<br>3. Merapikan dan menyusun dokumen terutama bagian stochastic hill climbing<br>4. Menjalankan eksperimen Stochastic Hill Climbing sebanyak 3 kali dan menyimpan hasilnya di `output/`<br>5. Testing keseluruhan kode |
| 18224039 | Lutfi Al Pasha | 1. Membuat file:<br>&nbsp;&nbsp;&nbsp;&nbsp;- `src/genetic_algorithm.py`<br>&nbsp;&nbsp;&nbsp;&nbsp;- `src/run_ga.py`<br>2. Menyusun dokumen laporan terutama bagian implementasi algoritma dan hasil eksperimen genetic algorithm<br>3. Menambahkan fungsi `plot_ga_curve` pada `src/visualization.py` |
| 182240109 | Kyan Saktya Diraya | 1. Membuat file:<br>&nbsp;&nbsp;&nbsp;&nbsp;- `src/simulated_annealing.py`<br>&nbsp;&nbsp;&nbsp;&nbsp;- `src/run_sa.py`<br>2. Menambahkan fungsi `plot_sa_probability` pada `src/visualization.py.`<br>3. Menjalankan eksperimen Simulated Annealing sebanyak 3 kali dan menyimpan hasilnya di `output/`.<br>4. Menyusun bagian Simulated Annealing pada dokumen laporan. |

## Catatan

- Penggunaan Generative AI dicantumkan pada lampiran laporan (`docs/`).