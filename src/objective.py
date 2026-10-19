#File objective.py, untuk menilai state dan memeriksa apakah valid atau tidak (constraint checker)
#State yang is_valid nya False akan dibuang
#Semua fungsi objektif hanya akan memproses kapal yang bukan None (vehicles_inside)
from models import Vehicle, HORIZONTAL, VERTICAL, Ship, State, effective_size, occupied_cells

#Fungsi total_weight untuk mengembalikan total berat dari semua kendaraan di kapal
def total_weight(state):
    return sum(state.vehicles[vid].weight for vid in state.vehicles_inside())

#Fungsi objective untuk mengembalikan total biaya pengiriman dari semua kendaraan di kapal
def objective(state):
    return sum(state.vehicles[vid].shipping_fee for vid in state.vehicles_inside())

#Fungsi within_capacity untuk mengembalikan total berat kendaraan dengan kapasitas kapal
def within_capacity(state):
    return total_weight(state) <= state.ship.max_capacity

#Fungsi within_bounds untuk constraint checker
#Satu kendaraan dengan penempatan (x,y) dengan ukuran efektif (w,l) dapat berada di kapal dengan memenuhi constraint sebagai berikut:
#1. x >= 0 (tidak keluar dari sisi kiri)
#2. y >= 0 (tidak keluar dari sisi atas)
#3. x + w <= ship.width (tidak keluar dari sisi kanan)
#4. y + l <= ship.length (tidak keluar dari sisi bawah)
def within_bounds(state):
    for vid in state.vehicles_inside():
        x, y = state.positions[vid]
        w, l = effective_size(state.vehicles[vid])
        success = (x >= 0 and y >= 0 and x + w <= state.ship.width and y + l <= state.ship.length)
        if not success:
            return False
    return True

#Fungsi no_overlap untuk check tidak ada kendaraan yang ada di tempat yang sama pada kapal
#Bandingkan panjang list dengan panjang set dari list itu (set membuang duplikat)
def no_overlap(state):
    all = []
    for vid in state.vehicles_inside():
        x, y = state.positions[vid]
        all.extend( occupied_cells(state.vehicles[vid], x, y))
    return len(all) == len(set(all))

#Fungsi is_valid untuk check semua fungsi yang mencakup constraint valid
#within_bounds dipanggil terlebih dahulu supaya jika kendaraan diluar kapal, tidak perlu kerjakan fungsi lain
def is_valid(state):
    return within_bounds(state) and no_overlap(state) and within_capacity(state)

if __name__ == "__main__":
    ship = Ship(10, 20, 500)
    a = Vehicle("A", 3, 4, HORIZONTAL, 60, 5, 3)
    b = Vehicle("B", 2, 2, HORIZONTAL, 30, 2, 1)
    # overlap: B di (2,0) menabrak sel (2,0) milik A
    s = State(ship, {"A": a, "B": b}, {"A": (0, 0), "B": (2, 0)})
    assert not no_overlap(s)
    assert not is_valid(s)

    # bersebelahan tapi tidak overlap: A x 0..2, B mulai x=3
    s = State(ship, {"A": a, "B": b}, {"A": (0, 0), "B": (3, 0)})
    assert no_overlap(s)
    assert is_valid(s)

    # overlap parsial di sudut: A sel (2,3), B di (2,3)
    s = State(ship, {"A": a, "B": b}, {"A": (0, 0), "B": (2, 3)})
    assert not no_overlap(s)

    # kendaraan di luar tidak ikut dihitung
    s = State(ship, {"A": a, "B": b}, {"A": (0, 0), "B": None})
    assert no_overlap(s)
    assert is_valid(s)

    # tidak valid karena kapasitas, walau tidak overlap
    s = State(Ship(10, 20, 6), {"A": a, "B": b}, {"A": (0, 0), "B": (5, 5)})
    assert no_overlap(s)
    assert not is_valid(s)

    print("no_overlap & is_valid OK")