#File neighbors.py untuk initial state random dan move (swap, relocate, rotate)
#move dibuat salinan, tidak akan mengubah state asli
#Hasil move yang tidak valid langsung dibuang
import random
import copy
from models import Vehicle, HORIZONTAL, VERTICAL, Ship, State
from objective import is_valid

#Fungsi move_rotate untuk mengubah orientasi dari kendaraan random dan cek valid atau tidak
def move_rotate(state):
    new = state.copy()
    inside = new.vehicles_inside()
    if not inside:
        return None
    vid = random.choice(inside)
    new.vehicles[vid].orientation = HORIZONTAL if new.vehicles[vid].orientation == VERTICAL else VERTICAL
    return new if is_valid(new) else None

#Fungsi move_relocate untuk memindahkan posisi satu kendaraan random ke tempat random yang berbeda dengan initial state
def move_relocate(state):
    new = state.copy()
    vid = random.choice(list(new.vehicles.keys()))  #ini berlaku untuk semua kendaraan yang diluar maupun didalam
    x = random.randint(0, new.ship.width - 1)
    y = random.randint(0, new.ship.length - 1)
    if (x,y) == new.positions[vid]:
        return None
    new.positions[vid] = (x,y)
    if is_valid(new):
        return new
    return None

#Fungsi move_swap untuk menukar posisi satu kendaraan random dengan kendaraan lain 
def move_swap(state):
    new = state.copy()
    idv = list(new.vehicles.keys()) #idv variabel penanda untuk kendaraan
    if len(idv) < 2:
        return None
    vid1, vid2 = random.sample(idv, 2)
    if new.positions[vid1] is None and new.positions[vid2] is None:
        return None
    new.positions[vid1], new.positions[vid2] = new.positions[vid2], new.positions[vid1]
    if is_valid(new):
        return new
    return None

#Fungsi random_initial_state untuk membuat state awal dari kapal dan dimana diletakkan setiap kendaraan
#Kalau setelah maksimum percobaan tetap gagal, biarkan None
#Note: vehicles -> list objek Vehicle
def random_initial_state(ship, vehicles, max_tries=20):
    state = State(
        ship,
        {v.id: copy.deepcopy(v) for v in vehicles},
        {v.id: None for v in vehicles}
    )
    order = list(state.vehicles.keys())
    random.shuffle(order)
    for vid in order:
        for _ in range (max_tries):
            state.vehicles[vid].orientation = random.choice([HORIZONTAL, VERTICAL])
            x = random.randint(0, ship.width - 1)
            y = random.randint(0, ship.length - 1)
            state.positions[vid] = (x, y)
            if is_valid(state):
                break
            state.positions[vid] = None
    return state


#List untuk menyimpan semua fungsi move (rotate, relocate, swap)
MOVES = [move_rotate, move_relocate, move_swap]

#Fungsi random_neighbor untuk mencari tetangga berikutnya yang valid secara random setelah initial state
#Dilakukan berulang dengan batasan (max_tries) untuk mencari tetangga yang valid
def random_neighbor(state, max_tries=100):
    for _ in range(max_tries):
        move = random.choice(MOVES)
        result = move(state)
        if result is not None:
            return result
    return None

if __name__ == "__main__":
    ship = Ship(10, 10, 500)
    a = Vehicle("A", 2, 2, HORIZONTAL, 10, 1, 1)
    b = Vehicle("B", 2, 3, HORIZONTAL, 20, 1, 1)
    s = State(ship, {"A": a, "B": b}, {"A": (0, 0), "B": None})

    for _ in range(50):
        n = random_neighbor(s)
        assert n is not None
        assert is_valid(n)
        assert s.positions == {"A": (0, 0), "B": None}   # asli utuh

    buntu = State(Ship(1, 1, 500), {"A": a}, {"A": None})
    assert random_neighbor(buntu, max_tries=20) is None

    print("random_neighbor OK")

    ship = Ship(10, 10, 500)
    vs = [Vehicle("A", 3, 4, HORIZONTAL, 60, 5, 3),
          Vehicle("B", 2, 2, HORIZONTAL, 30, 2, 1),
          Vehicle("C", 5, 5, HORIZONTAL, 40, 3, 2)]
    for _ in range(30):
        s = random_initial_state(ship, vs)
        assert is_valid(s)
        assert set(s.positions.keys()) == {"A", "B", "C"}
    assert vs[0].orientation == HORIZONTAL   # daftar asli tidak tersentuh

    s = random_initial_state(Ship(1, 1, 500), vs)
    assert s.vehicles_inside() == []

    print("random_initial_state OK")