#File data.py untuk data eeksperimen yang dipakai bersama untuk ketiga algoritma
#File ini digunakan agar perbandingan adil
from models import Ship, Vehicle, HORIZONTAL

SHIP = Ship(10, 20, 500) #kapal ukuran 10x20, kapasitas maks 500 unit
VEHICLES = [
    Vehicle("V01", 3, 4, HORIZONTAL, 60, 40, 3),
    Vehicle("V02", 2, 2, HORIZONTAL, 45, 15, 1),
    Vehicle("V03", 5, 7, HORIZONTAL, 90, 80, 4),
    Vehicle("V04", 5, 6, HORIZONTAL, 75, 70, 2),
    Vehicle("V05", 4, 6, HORIZONTAL, 55, 60, 5),
    Vehicle("V06", 4, 5, HORIZONTAL, 50, 55, 3),
    Vehicle("V07", 3, 6, HORIZONTAL, 40, 50, 2),
    Vehicle("V08", 4, 4, HORIZONTAL, 38, 45, 4),
    Vehicle("V09", 3, 5, HORIZONTAL, 30, 40, 1),
    Vehicle("V10", 3, 6, HORIZONTAL, 28, 35, 3),
    Vehicle("V11", 2, 4, HORIZONTAL, 35, 25, 2),
    Vehicle("V12", 2, 2, HORIZONTAL, 40, 12, 1),
    Vehicle("V13", 1, 3, HORIZONTAL, 18, 10, 5),
    Vehicle("V14", 1, 2, HORIZONTAL, 22, 8, 2),
]