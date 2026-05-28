class Produk:
    def __init__(self, nama, harga, stok):
        self.nama = nama
        self.harga = harga
        self.stok = stok

    def __str__(self):
        return f"Produk: {self.nama} | Harga: Rp{self.harga} | Stok: {self.stok}"
    # Perbandingan berdasarkan harga
    def __eq__(self, other):
        return self.harga == other.harga

    def __lt__(self, other):
        return self.harga < other.harga

    def __gt__(self, other):
        return self.harga > other.harga


# =========================
# Instansiasi Objek
# =========================
produk1 = Produk("Laptop", 8000000, 10)
produk2 = Produk("Smartphone", 5000000, 20)
produk3 = Produk("Tablet", 5000000, 15)

# =========================
# Menampilkan Objek (__str__)
# =========================
print(produk1)
print(produk2)
print(produk3)

print("\n=== Perbandingan Produk ===")

# =========================
# Pengujian Perbandingan
# =========================
print(f"Apakah {produk1.nama} lebih mahal dari {produk2.nama}? {produk1 > produk2}")
print(f"Apakah {produk2.nama} lebih murah dari {produk1.nama}? {produk2 < produk1}")
print(f"Apakah {produk2.nama} harganya sama dengan {produk3.nama}? {produk2 == produk3}")