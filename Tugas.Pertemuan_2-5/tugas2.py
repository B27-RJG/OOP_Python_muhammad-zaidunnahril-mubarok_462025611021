# main.py

# Membuat Class
class Hewan:
    def __init__(self, nama, jenis, umur):
        self.nama = nama
        self.jenis = jenis
        self.umur = umur

    def tampilkan_info(self):
        return f"Nama: {self.nama}, Jenis: {self.jenis}, Umur: {self.umur} tahun"


# Membuat Object
hewan1 = Hewan("Kiko", "Kucing", 2)
hewan2 = Hewan("Bruno", "Anjing", 4)

# Menampilkan ke console (1 print untuk 1 object)
print(hewan1.tampilkan_info())
print(hewan2.tampilkan_info())