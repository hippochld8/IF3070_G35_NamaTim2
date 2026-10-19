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
        success = (x >= 0 and y >= 0 and x + w <= state.ship.width and y + l <= state.ship.length) #variabel success menjadi penanda yang menyimpan semua constraint
        if not success:
            return False
    return True

#Fungsi no_overlap untuk check tidak ada kendaraan yang ada di tempat yang sama pada kapal
#Bandingkan panjang list dengan panjang set dari list itu (set membuang duplikat)
def no_overlap(state):
    all = []                                                    #all variabel list kosong untuk menyimpan pasangan vehicle, x, dan y
    for vid in state.vehicles_inside():
        x, y = state.positions[vid]
        all.extend(occupied_cells(state.vehicles[vid], x, y))   #extend digunakan untuk menambahkan banyak elemen sekaligus ke all
    return len(all) == len(set(all))                            #set membuang duplikat kalau len(all) panjangnya sama dengan len(set(all)) berarti tidak ada duplikat

#Fungsi is_valid untuk check semua fungsi yang mencakup constraint valid
#within_bounds dipanggil terlebih dahulu supaya jika kendaraan diluar kapal, tidak perlu kerjakan fungsi lain
def is_valid(state):
    return within_bounds(state) and no_overlap(state) and within_capacity(state)