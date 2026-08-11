import streamlit as st
from abc import ABC, abstractmethod
from datetime import datetime, date
import pandas as pd

# ============================================================
# CUSTOM EXCEPTIONS
# ============================================================
class WeddingRentalError(Exception): pass
class StokTidakCukupError(WeddingRentalError): pass
class InputTidakValidError(WeddingRentalError): pass
class TransaksiError(WeddingRentalError): pass

# ============================================================
# UTILITAS
# ============================================================
class Utilitas:
    @staticmethod
    def rupiah(nominal):
        return f"Rp{nominal:,.0f}".replace(",", ".")

# ============================================================
# USER & ADMIN (INHERITANCE & ENCAPSULATION)
# ============================================================
class User:
    def __init__(self, username, nama):
        self.__username = username
        self.__nama = nama

    @property
    def username(self): return self.__username
    @property
    def nama(self): return self.__nama

class Admin(User):
    def __init__(self, username, nama, password):
        super().__init__(username, nama)
        self.__password = password

    def cek_password(self, password):
        return self.__password == password

# ============================================================
# PELANGGAN
# ============================================================
class Pelanggan:
    def __init__(self, id_pelanggan, nama, telepon, alamat):
        self.__id_pelanggan = id_pelanggan
        self.nama = nama
        self.telepon = telepon
        self.alamat = alamat

    @property
    def id_pelanggan(self): return self.__id_pelanggan

    def __str__(self):
        return f"{self.nama} ({self.id_pelanggan})"

# ============================================================
# PERLENGKAPAN (POLYMORPHISM)
# ============================================================
class Perlengkapan(ABC):
    def __init__(self, kode, nama, stok, harga_sewa):
        self.__kode = kode
        self.nama = nama
        self.stok = stok
        self.harga_sewa = harga_sewa

    @property
    def kode(self): return self.__kode

    def kurangi_stok(self, jumlah):
        if jumlah > self.stok:
            raise StokTidakCukupError(f"Stok {self.nama} hanya {self.stok}.")
        self.stok -= jumlah

    def tambah_stok(self, jumlah):
        self.stok += jumlah

    @abstractmethod
    def biaya_tambahan(self, subtotal): pass

    @property
    @abstractmethod
    def kategori(self): pass

    def hitung_biaya(self, jumlah, lama_hari):
        subtotal = self.harga_sewa * jumlah * lama_hari
        return subtotal + self.biaya_tambahan(subtotal)

    def __str__(self):
        return f"[{self.kode}] {self.nama} (Stok: {self.stok})"

class StrukturArea(Perlengkapan):
    @property
    def kategori(self): return "Struktur & Area Luar Ruangan"
    def biaya_tambahan(self, subtotal): return subtotal * 0.05

class Furnitur(Perlengkapan):
    @property
    def kategori(self): return "Furnitur"
    def biaya_tambahan(self, subtotal): return 0

class Dekorasi(Perlengkapan):
    @property
    def kategori(self): return "Dekorasi & Estetika"
    def biaya_tambahan(self, subtotal): return subtotal * 0.08

class Katering(Perlengkapan):
    @property
    def kategori(self): return "Peralatan Katering & Penyajian Makanan"
    def biaya_tambahan(self, subtotal): return subtotal * 0.03

class PakaianRias(Perlengkapan):
    @property
    def kategori(self): return "Pakaian & Rias"
    def biaya_tambahan(self, subtotal): return subtotal * 0.10

class AudioHiburan(Perlengkapan):
    @property
    def kategori(self): return "Sistem Suara & Hiburan"
    def biaya_tambahan(self, subtotal): return subtotal * 0.05

# ============================================================
# PEMBAYARAN
# ============================================================
class Pembayaran(ABC):
    @abstractmethod
    def proses(self, total): pass

class PembayaranTunai(Pembayaran):
    def proses(self, total): return f"TUNAI: {Utilitas.rupiah(total)}"

class PembayaranTransfer(Pembayaran):
    def __init__(self, bank):
        self.bank = bank
    def proses(self, total): return f"TRANSFER ({self.bank}): {Utilitas.rupiah(total)}"

class PembayaranQRIS(Pembayaran):
    def proses(self, total): return f"QRIS: {Utilitas.rupiah(total)}"

# ============================================================
# TRANSAKSI
# ============================================================
class DetailPeminjaman:
    def __init__(self, barang, jumlah, lama_hari):
        self.barang = barang
        self.jumlah = jumlah
        self.lama_hari = lama_hari
        self.total = barang.hitung_biaya(jumlah, lama_hari)

class Peminjaman:
    DENDA_PER_HARI = 50000

    def __init__(self, id_transaksi, pelanggan, tgl_pinjam, tgl_kembali):
        self.__id_transaksi = id_transaksi
        self.__pelanggan = pelanggan
        self.__tgl_pinjam = tgl_pinjam
        self.__tgl_kembali = tgl_kembali
        self.detail = []
        self.status = "DIPINJAM"
        self.denda = 0
        self.metode = "-"

    @property
    def id_transaksi(self): return self.__id_transaksi
    @property
    def pelanggan(self): return self.__pelanggan
    
    def tambah_detail(self, barang, jumlah):
        lama_hari = (self.__tgl_kembali - self.__tgl_pinjam).days + 1
        barang.kurangi_stok(jumlah)
        self.detail.append(DetailPeminjaman(barang, jumlah, lama_hari))

    def hitung_total_sewa(self):
        return sum(item.total for item in self.detail)
    
    def hitung_total_akhir(self):
        return self.hitung_total_sewa() + self.denda

    def bayar(self, pembayaran):
        if isinstance(pembayaran, PembayaranTransfer):
            self.metode = f"Transfer {pembayaran.bank}"
        elif isinstance(pembayaran, PembayaranQRIS):
            self.metode = "QRIS"
        else:
            self.metode = "Tunai"
        return pembayaran.proses(self.hitung_total_akhir())

    def kembalikan(self, tgl_aktual):
        if self.status == "DIKEMBALIKAN":
            raise TransaksiError("Sudah dikembalikan.")
        
        for item in self.detail:
            item.barang.tambah_stok(item.jumlah)
            
        terlambat = (tgl_aktual - self.__tgl_kembali).days
        self.denda = max(0, terlambat * self.DENDA_PER_HARI)
        self.status = "DIKEMBALIKAN"


# ============================================================
# WEB UI - STREAMLIT APP
# ============================================================
def init_session():
    if "admin" not in st.session_state:
        st.session_state.admin = Admin("admin", "Administrator", "admin123")
        st.session_state.logged_in = False
        st.session_state.pelanggan = [
            Pelanggan("PL001", "Budi Santoso", "081234567890", "Ponorogo"),
            Pelanggan("PL002", "Siti Aminah", "081298765432", "Madiun")
        ]
        st.session_state.barang = [
            StrukturArea("SA001", "Tenda Pernikahan", 25, 500000),
            Furnitur("F001", "Kursi Futura", 1000, 15000),
            Dekorasi("D001", "Dekorasi Bunga", 10, 200000),
            Katering("K001", "Wadah Prasmanan Stainless", 10, 25000),
            PakaianRias("P001", "Kebaya Akad Nikah", 100, 250000),
            AudioHiburan("A001", "Sound System Set", 55, 1000000),
        ]
        st.session_state.transaksi = []
        st.session_state.cart = []

def generate_id(prefix, data, attr_name):
    maks = 0
    for item in data:
        val = getattr(item, attr_name)
        try:
            num = int(val.replace(prefix, ""))
            maks = max(maks, num)
        except: pass
    return f"{prefix}{maks + 1:03d}"

def main():
    st.set_page_config(page_title="Wedding Rental", layout="wide")
    init_session()

    # --- LOGIN SYSTEM ---
    if not st.session_state.logged_in:
        st.title("Sistem Peminjaman Perlengkapan Pernikahan")
        st.subheader("Login Admin")
        with st.form("login_form"):
            user = st.text_input("Username")
            pswd = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            if submitted:
                if user == st.session_state.admin.username and st.session_state.admin.cek_password(pswd):
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Username atau password salah!")
        return

    # --- SIDEBAR MENU ---
    st.sidebar.title(f"Halo, {st.session_state.admin.nama}")
    menu = st.sidebar.radio("Navigasi", [
        "Dashboard", "Kelola Pelanggan", "Kelola Barang", 
        "Peminjaman Baru", "Pengembalian", "Logout"
    ])

    if menu == "Logout":
        st.session_state.logged_in = False
        st.rerun()

    # --- DASHBOARD ---
    if menu == "Dashboard":
        st.title("Dashboard")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Pelanggan", len(st.session_state.pelanggan))
        col2.metric("Total Barang", len(st.session_state.barang))
        col3.metric("Transaksi Aktif", sum(1 for t in st.session_state.transaksi if t.status == "DIPINJAM"))
        col4.metric("Transaksi Selesai", sum(1 for t in st.session_state.transaksi if t.status == "DIKEMBALIKAN"))

    # --- KELOLA PELANGGAN ---
    elif menu == "Kelola Pelanggan":
        st.title("Kelola Pelanggan")
        with st.expander("Tambah Pelanggan Baru"):
            with st.form("tambah_pl"):
                nama = st.text_input("Nama")
                telepon = st.text_input("Telepon")
                alamat = st.text_area("Alamat")
                if st.form_submit_button("Simpan"):
                    new_id = generate_id("PL", st.session_state.pelanggan, "id_pelanggan")
                    st.session_state.pelanggan.append(Pelanggan(new_id, nama, telepon, alamat))
                    st.success("Berhasil ditambahkan!")
                    st.rerun()
        
        if st.session_state.pelanggan:
            df = pd.DataFrame([{
                "ID": p.id_pelanggan, "Nama": p.nama, 
                "Telepon": p.telepon, "Alamat": p.alamat
            } for p in st.session_state.pelanggan])
            st.dataframe(df, use_container_width=True)

    # --- KELOLA BARANG ---
    elif menu == "Kelola Barang":
        st.title("Kelola Perlengkapan")
        with st.expander("Tambah Barang Baru"):
            with st.form("tambah_brg"):
                kategori = st.selectbox("Kategori", [
                    "Struktur & Area Luar Ruangan", 
                    "Furnitur",
                    "Dekorasi & Estetika", 
                    "Peralatan Katering & Penyajian Makanan", 
                    "Pakaian & Rias", 
                    "Sistem Suara & Hiburan"
                ])
                nama = st.text_input("Nama Barang")
                stok = st.number_input("Stok", min_value=0, step=1)
                harga = st.number_input("Harga Sewa/Hari", min_value=0, step=1000)
                
                if st.form_submit_button("Simpan"):
                    mapping_data = {
                        "Struktur & Area Luar Ruangan": {"prefix": "SA", "class": StrukturArea},
                        "Furnitur": {"prefix": "F", "class": Furnitur},
                        "Dekorasi & Estetika": {"prefix": "D", "class": Dekorasi},
                        "Peralatan Katering & Penyajian Makanan": {"prefix": "K", "class": Katering},
                        "Pakaian & Rias": {"prefix": "P", "class": PakaianRias},
                        "Sistem Suara & Hiburan": {"prefix": "A", "class": AudioHiburan}
                    }
                    
                    prefix = mapping_data[kategori]["prefix"]
                    new_id = generate_id(prefix, st.session_state.barang, "kode")
                    kelas_objek = mapping_data[kategori]["class"]
                    
                    st.session_state.barang.append(kelas_objek(new_id, nama, stok, harga))
                    st.success("Berhasil ditambahkan!")
                    st.rerun()

        if st.session_state.barang:
            df = pd.DataFrame([{
                "Kode": b.kode, "Kategori": b.kategori, "Nama": b.nama, 
                "Stok": b.stok, "Harga/Hari": Utilitas.rupiah(b.harga_sewa)
            } for b in st.session_state.barang])
            st.dataframe(df, use_container_width=True)

    # --- PEMINJAMAN BARU ---
    elif menu == "Peminjaman Baru":
        st.title("Transaksi Peminjaman")
        
        col1, col2 = st.columns(2)
        with col1:
            pelanggan_terpilih = st.selectbox("Pilih Pelanggan", st.session_state.pelanggan)
            tgl_pinjam = st.date_input("Tanggal Pinjam", date.today())
            tgl_kembali = st.date_input("Rencana Kembali", date.today())
        
        with col2:
            st.subheader("Keranjang Barang")
            barang_terpilih = st.selectbox("Pilih Barang", st.session_state.barang)
            qty = st.number_input("Jumlah", min_value=1, max_value=max(1, barang_terpilih.stok))
            if st.button("Tambah ke Keranjang"):
                st.session_state.cart.append({"barang": barang_terpilih, "qty": qty})
                st.success(f"{barang_terpilih.nama} ditambahkan!")

            if st.session_state.cart:
                for idx, item in enumerate(st.session_state.cart):
                    st.write(f"- {item['barang'].nama} (x{item['qty']})")
                
                if st.button("Kosongkan Keranjang"):
                    st.session_state.cart.clear()
                    st.rerun()

        if st.session_state.cart:
            st.markdown("---")
            st.subheader("Metode Pembayaran")
            metode = st.radio("Pilih Metode Pembayaran", ["Tunai", "Transfer Bank", "QRIS"])
            
            bank_pilihan = None
            if metode == "Transfer Bank":
                bank_pilihan = st.selectbox("Pilih Bank", ["BCA (1234567890 a.n Wedding Organizer)", "BRI (0987654321 a.n Wedding Organizer)", "Mandiri (1122334455 a.n Wedding Organizer)"])
            elif metode == "QRIS":
                st.info("Silakan scan QRIS di bawah ini untuk melakukan pembayaran:")
                # Contoh placeholder gambar QRIS menggunakan URL gambar publik atau local file path
                st.image("https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=WeddingOrganizerQRIS", width=200, caption="Scan QRIS Pembayaran")

            if st.button("Proses Transaksi", type="primary"):
                try:
                    new_id = generate_id("TR", st.session_state.transaksi, "id_transaksi")
                    transaksi = Peminjaman(new_id, pelanggan_terpilih, tgl_pinjam, tgl_kembali)
                    
                    for item in st.session_state.cart:
                        transaksi.tambah_detail(item["barang"], item["qty"])
                    
                    if metode == "Tunai":
                        pembayaran = PembayaranTunai()
                    elif metode == "Transfer Bank":
                        nama_bank = bank_pilihan.split(" ")[0]
                        pembayaran = PembayaranTransfer(nama_bank)
                    else:
                        pembayaran = PembayaranQRIS()

                    transaksi.bayar(pembayaran)
                    
                    st.session_state.transaksi.append(transaksi)
                    st.session_state.cart.clear()
                    st.success(f"Transaksi {new_id} Berhasil!")
                except Exception as e:
                    st.error(f"Gagal: {e}")

    # --- PENGEMBALIAN ---
    elif menu == "Pengembalian":
        st.title("Pengembalian Barang")
        aktif = [t for t in st.session_state.transaksi if t.status == "DIPINJAM"]
        
        if not aktif:
            st.info("Tidak ada transaksi aktif yang perlu dikembalikan.")
            return

        transaksi_terpilih = st.selectbox("Pilih Transaksi", aktif, format_func=lambda x: f"{x.id_transaksi} - {x.pelanggan.nama}")
        tgl_aktual = st.date_input("Tanggal Dikembalikan", date.today())
        
        if st.button("Proses Pengembalian"):
            try:
                transaksi_terpilih.kembalikan(tgl_aktual)
                st.success(f"Pengembalian berhasil. Denda: {Utilitas.rupiah(transaksi_terpilih.denda)}")
                st.rerun()
            except Exception as e:
                st.error(e)

if __name__ == "__main__":
    main()