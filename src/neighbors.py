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
    if not inside:                                                                                          #untuk cek kendaraan di dalam kapal atau tidak
        return None
    vid = random.choice(inside)                                                                             #untuk ambil random kendaraan
    new.vehicles[vid].orientation = HORIZONTAL if new.vehicles[vid].orientation == VERTICAL else VERTICAL   #ubah orientasi (rotate) kendaraan yang diambil secara random
    return new if is_valid(new) else None

#Fungsi move_relocate untuk memindahkan posisi satu kendaraan random ke tempat random yang berbeda dengan initial state
def move_relocate(state):
    new = state.copy()
    vid = random.choice(list(new.vehicles.keys()))  #ini berlaku untuk semua kendaraan yang diluar maupun didalam
    x = random.randint(0, new.ship.width - 1)       #randint digunakan agar batas awal dan akhir termasuk ke dalam angka random yang bisa dipilih
    y = random.randint(0, new.ship.length - 1)
    if (x,y) == new.positions[vid]:                 
        return None
    new.positions[vid] = (x,y)                      #pindahkan tampat kendaraan jika tidak None
    if is_valid(new):
        return new
    return None

#Fungsi move_swap untuk menukar posisi satu kendaraan random dengan kendaraan lain 
def move_swap(state):
    new = state.copy()
    idv = list(new.vehicles.keys())                                                     #idv variabel penanda untuk list kendaraan yang ditukar
    if len(idv) < 2:                                                                    #jika kurang dari 2 kendaraan tidak bisa ditukar
        return None
    vid1, vid2 = random.sample(idv, 2)                                                  #ambil 2 kendaraan sebagai sample dengan random
    if new.positions[vid1] is None and new.positions[vid2] is None:
        return None
    new.positions[vid1], new.positions[vid2] = new.positions[vid2], new.positions[vid1] #tukar tempat 2 kendaraan jika tidak None
    if is_valid(new):
        return new
    return None

#Fungsi random_initial_state untuk membuat state awal dari kapal dan dimana diletakkan setiap kendaraan
#Kalau setelah maksimum percobaan tetap gagal, biarkan None
#Note: vehicles -> list objek Vehicle
def random_initial_state(ship, vehicles, max_tries=20):
    state = State(
        ship,
        {v.id: copy.deepcopy(v) for v in vehicles},                                 #salinan dari dictionary id -> Vehicle, supaya daftar asli tidak rusak saat orientasi dirubah
        {v.id: None for v in vehicles}                                              #semua kendaraan disimpan di luar kapal pada state awal
    )
    order = list(state.vehicles.keys())                                             #list semua kendaraan
    random.shuffle(order)                                                           #list dishuffle agar tidak selalu kendaraan yang sama dapat tempat duluan
    for vid in order:
        for _ in range (max_tries):
            state.vehicles[vid].orientation = random.choice([HORIZONTAL, VERTICAL]) #pilih orientasi random untuk setiap kendaraan
            x = random.randint(0, ship.width - 1)
            y = random.randint(0, ship.length - 1)
            state.positions[vid] = (x, y)
            if is_valid(state):                                                     #perulangan berhenti jika  state sudah valid
                break
            state.positions[vid] = None
    return state


#List untuk menyimpan semua fungsi move (rotate, relocate, swap)
MOVES = [move_rotate, move_relocate, move_swap]

#Fungsi random_neighbor untuk mencari tetangga berikutnya yang valid secara random setelah initial state
#Dilakukan berulang dengan batasan (max_tries) untuk mencari tetangga yang valid
def random_neighbor(state, max_tries=100):
    for _ in range(max_tries):
        move = random.choice(MOVES)         #pilih secara random diantara ketiga fungsi move
        result = move(state)
        if result is not None:
            return result
    return None