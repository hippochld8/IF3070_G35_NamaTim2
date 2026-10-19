#File models.py, Struktur data inti (Vehicle, Ship, State)
#Fungsi tambahan untuk bantuan geometri (effective_size, occupied_cells)
from dataclasses import dataclass 
import copy
HORIZONTAL = "Horizontal"   #membuat konstanta orientasi horizontal lebih stabil, jika salah penulisan akan tidak jalan maka terjadi error
VERTICAL = "Vertical"       #membuat konstanta orientasi vertical lebih stabil, jika salah penulisan akan tidak jalan maka terjadi error

#Spesifikasi Entitas Vehicle
@dataclass
class Vehicle:
    id:str              #atribut id tipe data string
    width:int           #atribut dimensions width tipe data integer (grid)
    length:int          #atribut dimensions length tipe data integer (grid)
    orientation:str     #atribut orientation tipe data string (Vertical, Horizontal, bisa berubah saat pencarian)
    shipping_fee:int    #atribut shipping_fee tipe data integer (satuan juta rupiah)
    weight:int          #atribut weight tipe data integer (satuan unit)
    eta:int             #atribut ETA (Estimated Time of Arrival) tipe data integer (sisa hari, belum dipakai objective funtion) 

#Spesifikasi Entitas Ship
@dataclass(frozen=True) #pakai frozen=True karena data kapal tidak berubah
class Ship:
    width:int           #atribut dimensions width tipe data integer (grid)
    length:int          #atribut dimensions length tipe data integer (grid)
    max_capacity:int    #atribut max_capacity tipe data integer (satuan unit)

#Fungsi ukuran efektif
#Jika orientasinya horizontal maka grid (width, length)
#Jika orientasinya vertical maka grid (length, width)
def effective_size(vehicle):
    if vehicle.orientation == HORIZONTAL:
        return vehicle.width, vehicle.length
    return vehicle.length, vehicle.width

#Fungsi sel yang ditempati
#Parameter x,y itu pojok kiri atas dimulainya suatu kendaraan diletakkan di grid kapal
#x untuk kolom, y untuk baris, mulai dari (0,0)
def occupied_cells(vehicle, x, y):
    width, length = effective_size(vehicle)
    result = set()                              #set kosong untuk menyimpan x dan y (sel yang ditempati)
    for dx in range(width):                     #perulangan untuk setiap sel yang ditempati oleh x (kolomnya)
        for dy in range(length):                #perulangan untuk setiap sel yang ditempati oleh y (barisnya)
            result.add((x + dx, y + dy))        #tambah setiap hasil perulangan x dan y ke set yang awalnya kosong
    return result

#Spesifikasi Kelas State
class State:
    def __init__(self, ship, vehicles, positions):
        self.ship = ship            #atribut ship, kapal dan gridnya sesuai entitas Ship
        self.vehicles = vehicles    #atribut vehicles, id merujuk ke entitas Vehicle
        self.positions = positions  #atribut positions, id merujuk ke x,y pada occupied_cells, bisa juga None

#Fungsi copy untuk mengembalikan State baru
    def copy(self):
        return State(
            self.ship,                      #ship dapat langsung dibagikan karena frozen
            copy.deepcopy(self.vehicles),   #vehicles pakai deepcopy karerna bisa berubah
            dict(self.positions)            #positions pakai dict karena isinya tuple atau None
        )

#Fungsi vehicles_inside untuk mengembalikan kendaraan yang diangkut oleh kapal
    def vehicles_inside(self):
        return [vehicles_id for vehicles_id, pos in self.positions.items() if pos is not None]

##Fungsi vehicles_outside untuk mengembalikan kendaraan yang tidak diangkut oleh kapal
    def vehicles_outside(self):
        return [vehicles_id for vehicles_id, pos in self.positions.items() if pos is None]