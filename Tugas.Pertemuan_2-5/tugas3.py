# main.py

class Karyawan:
    def __init__(self, nama, jabatan, gaji):
        self.nama = nama
        self.jabatan = jabatan
        self.gaji = gaji

    # Instance Method 1
    def tampilkan_info(self):
        print(f"Nama: {self.nama}, Jabatan: {self.jabatan}, Gaji: Rp{self.gaji}")

    # Instance Method 2
    def naik_gaji(self, persentase):
        kenaikan = self.gaji * (persentase / 100)
        self.gaji += kenaikan
        print(f"Gaji {self.nama} setelah naik {persentase}% menjadi Rp{self.gaji}")

    # Static Method
    @staticmethod
    def perusahaan():
        print("Perusahaan: PT Maju Jaya Lancar Sejahtera")


# Instansiasi Object
karyawan1 = Karyawan("Andi", "Programmer", 5000000)
karyawan2 = Karyawan("Budi", "Designer", 4500000)

# Pemanggilan Instance Method
karyawan1.tampilkan_info()
karyawan1.naik_gaji(10)

print()  # pemisah

karyawan2.tampilkan_info()
karyawan2.naik_gaji(5)

print()  # pemisah

# Pemanggilan Static Method
Karyawan.perusahaan()      # melalui class
karyawan1.perusahaan()     # melalui object