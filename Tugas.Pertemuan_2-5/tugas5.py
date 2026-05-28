class DompetDigital:
    def __init__(self, nama_pengguna, id_pengguna, pin, saldo):
        # Atribut privat
        self.__nama_pengguna = nama_pengguna
        self.__id_pengguna = id_pengguna
        self.__pin = pin
        self.__saldo = saldo
        # Getter untuk mengambil data secara aman
    def get_nama_pengguna(self):
        return self.__nama_pengguna

    def get_id_pengguna(self):
        return self.__id_pengguna

    # Method validasi untuk melihat saldo
    def cek_saldo(self, pin):
        if pin == self.__pin:
            return f"Saldo Anda: Rp{self.__saldo}"
        else:
            return "PIN salah! Akses ditolak."

    # Method validasi untuk tarik tunai
    def tarik_tunai(self, pin, jumlah):
        if pin == self.__pin:
            if jumlah <= self.__saldo:
                self.__saldo -= jumlah
                return f"Tarik tunai berhasil. Sisa saldo: Rp{self.__saldo}"
            else:
                return "Saldo tidak mencukupi."
        else:
            return "PIN salah! Transaksi dibatalkan."

    # Method validasi untuk ubah PIN
    def ubah_pin(self, pin_lama, pin_baru):
        if pin_lama == self.__pin:
            self.__pin = pin_baru
            return "PIN berhasil diubah."
        else:
            return "PIN lama salah! Gagal mengubah PIN."


# =========================
# INSTANSIASI OBJECT
# =========================

akun1 = DompetDigital(
    "Aayong",
    "USR001",
    "123456",
    500000
)

# =========================
# PENGUJIAN GETTER
# =========================

print("=== DATA PENGGUNA ===")
print("Nama Pengguna :", akun1.get_nama_pengguna())
print("ID Pengguna   :", akun1.get_id_pengguna())

# =========================
# PENGUJIAN AKSES LANGSUNG
# =========================

# Baris berikut akan ERROR karena atribut bersifat private
# print(akun1.__saldo)

# =========================
# PENGUJIAN VALIDASI SALDO
# =========================

print("\n=== CEK SALDO ===")
print("PIN Salah :", akun1.cek_saldo("111111"))
print("PIN Benar :", akun1.cek_saldo("123456"))

# =========================
# PENGUJIAN TARIK TUNAI
# =========================

print("\n=== TARIK TUNAI ===")
print("PIN Salah :", akun1.tarik_tunai("000000", 100000))
print("PIN Benar :", akun1.tarik_tunai("123456", 100000))

# =========================
# PENGUJIAN UBAH PIN
# =========================

print("\n=== UBAH PIN ===")
print("PIN Lama Salah :", akun1.ubah_pin("999999", "654321"))
print("PIN Lama Benar :", akun1.ubah_pin("123456", "654321"))

# Tes PIN baru
print("\n=== CEK SALDO DENGAN PIN BARU ===")
print(akun1.cek_saldo("654321"))