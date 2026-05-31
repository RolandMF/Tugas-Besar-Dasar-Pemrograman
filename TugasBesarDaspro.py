# ============================================================
#        SISTEM MANAGEMENT PEMINJAMAN KENDARAAN 
#        Mata Kuliah : Dasar Pemrograman
#        Kelompok    : -Steven Theodor ( 2572015 )
#                      -Roland Michael Febrian ( 2572017 )
#                      -Gabriele Sebastien De Fretes ( 2572054 )
# ============================================================

# ============================================================
#    DEKLARASI ARRAY GLOBAL (PARALLEL ARRAYS)
#    *** JANGAN DIHAPUS, DIPAKAI SEMUA MENU ***
# ============================================================

# --- Array Data Kendaraan (Dipakai Menu 1 & 2) ---
kendaraan_id     = []   # int
kendaraan_nama   = []   # str
kendaraan_jenis  = []   # str
kendaraan_plat   = []   # str
kendaraan_harga  = []   # int
kendaraan_status = []   # str

# --- Array Data Peminjaman (Mulai diisi di Menu 2) ---
pinjam_id            = []  # int
pinjam_id_kendaraan = []  # int (merujuk ke kendaraan_id)
pinjam_nama          = []  # str
pinjam_hari          = []  # int
pinjam_total         = []  # int
pinjam_status        = []  # str

# --- Counter ID (menggunakan list agar mutable) ---
counter_kendaraan = [1]
counter_pinjam    = [1]


# ============================================================
#           FUNGSI UTILITAS / HELPER (TANPA INPUT)
#           *** DIPAKAI OLEH MENU 1 & 2 ***
# ============================================================

def cetak_garis():
    print("-" * 60)

def format_rupiah(nominal):
    """Format sederhana: 100000 -> Rp 100.000"""
    s = str(nominal)
    hasil = ""
    hitung = 0
    for i in range(len(s) - 1, -1, -1):
        if hitung > 0 and hitung % 3 == 0:
            hasil = "." + hasil
        hasil = s[i] + hasil
        hitung += 1
    return "Rp " + hasil

def cari_index_kendaraan(id_cari):
    """Mengembalikan index jika ditemukan, -1 jika tidak."""
    for i in range(len(kendaraan_id)):
        if kendaraan_id[i] == id_cari:
            return i
    return -1

def format_id_k(id_num): return "K" + str(id_num).zfill(3)

# CATATAN: Fungsi cari_index_peminjaman dan format_id_p dihapus 
# karena hanya dipakai Menu 3 & 4 


# ============================================================
#        FUNGSI TAMPIL DATA (PROSES OUPUT SAJA)
# ============================================================

def tampilkan_tabel_kendaraan(filter_status="semua"):
    """DIPAKAI MENU 1 & 2"""
    print("\n--- DAFTAR KENDARAAN ---")
    found = False
    print("ID\    | Nama             | Plat       | Harga/Hari  | Status")
    cetak_garis()
    for i in range(len(kendaraan_id)):
        if filter_status == "semua" or kendaraan_status[i] == filter_status:
            txt_id = format_id_k(kendaraan_id[i])
            txt_nama = kendaraan_nama[i].ljust(16)
            txt_plat = kendaraan_plat[i].ljust(10)
            txt_harga = format_rupiah(kendaraan_harga[i]).rjust(11)
            print(f"{txt_id} | {txt_nama} | {txt_plat} | {txt_harga} | {kendaraan_status[i]}")
            found = True
    if not found:
        print(" (Tidak ada data)")
    cetak_garis()

# CATATAN: Fungsi tampilkan_tabel_peminjaman dihapus 
# karena dipakai Menu 3 & 4 


# ============================================================
#        FUNGSI LOGIKA PROSES (TERIMA ARGUMEN, TANPA INPUT)
# ============================================================

# --- LOGIKA MENU 1 ---
def proses_tambah_kendaraan(nama, jenis, plat, harga):
    # Cek duplikat plat
    for p in kendaraan_plat:
        if p == plat:
            return False, "Nomor plat sudah terdaftar."

    # Simpan
    kendaraan_id.append(counter_kendaraan[0])
    kendaraan_nama.append(nama)
    kendaraan_jenis.append(jenis)
    kendaraan_plat.append(plat)
    kendaraan_harga.append(harga)
    kendaraan_status.append("Tersedia")
    
    counter_kendaraan[0] += 1
    return True, "Kendaraan berhasil ditambahkan."

def proses_edit_harga(id_k, harga_baru):
    idx = cari_index_kendaraan(id_k)
    if idx == -1:
        return False, "ID Kendaraan tidak ditemukan."
    
    kendaraan_harga[idx] = harga_baru
    return True, "Harga berhasil diupdate."

def proses_hapus_kendaraan(id_k):
    idx = cari_index_kendaraan(id_k)
    if idx == -1:
        return False, "ID Kendaraan tidak ditemukan."
    if kendaraan_status[idx] == "Dipinjam":
        return False, "Gagal. Kendaraan sedang dipinjam."
    
    # Hapus dari semua array
    kendaraan_id.pop(idx)
    kendaraan_nama.pop(idx)
    kendaraan_jenis.pop(idx)
    kendaraan_plat.pop(idx)
    kendaraan_harga.pop(idx)
    kendaraan_status.pop(idx)
    return True, "Kendaraan berhasil dihapus."

# --- LOGIKA MENU 2 ---
def proses_catat_peminjaman(id_k, nama_p, durasi):
    idx_k = cari_index_kendaraan(id_k)
    
    # Validasi logika
    if idx_k == -1:
        return False, "ID Kendaraan tidak ditemukan.", 0
    if kendaraan_status[idx_k] == "Dipinjam":
        return False, "Kendaraan sedang tidak tersedia.", 0
    
    # Hitung total
    total = kendaraan_harga[idx_k] * durasi
    
    # Simpan transaksi
    pinjam_id.append(counter_pinjam[0])
    pinjam_id_kendaraan.append(id_k)
    pinjam_nama.append(nama_p)
    pinjam_hari.append(durasi)
    pinjam_total.append(total)
    pinjam_status.append("Aktif")
    
    # Update status kendaraan
    kendaraan_status[idx_k] = "Dipinjam"
    
    counter_pinjam[0] += 1
    return True, "Peminjaman berhasil dicatat.", total

# CATATAN: Fungsi proses_pengembalian, hitung_statistik, dan isi_data_dummy 
# dihapus


# ============================================================
#           VALIDATOR INPUT SIMPEL (DIPAKAI DI MAIN)
# ============================================================

def input_angka(pesan):
    while True:
        try:
            return int(input(pesan))
        except ValueError:
            print("[!] Masukkan angka bulat.")

def input_teks(pesan):
    while True:
        teks = input(pesan).strip()
        if teks:
            return teks
        print("[!] Input tidak boleh kosong.")


# ============================================================
#           ENTRY POINT (HANYA MENU 1 & 2)
# ============================================================

def main():
    # CATATAN: isi_data_dummy() dihapus agar mulai dari kosong (bisa ditambah via Menu 1)
    
    print("="*60)
    print("     SELAMAT DATANG DI SISTEM RENTAL KENDARAAN")
    print("="*60)

    while True:
        print("\n=== MENU UTAMA ===")
        print("1. Manajemen Data Kendaraan")
        print("2. Transaksi Pinjam Kendaraan")
        print("3. Transaksi Kembalikan Kendaraan")
        print("4. Lihat Riwayat Peminjaman")
        print("5. Laporan Statistik Sederhana")
        print("0. Keluar")
        cetak_garis()
        
        pilihan = input(">> Pilih Menu: ")

        # --------------------------------------------------------
        # MENU 1: MANAJEMEN KENDARAAN (SUB-MENU) 
        # --------------------------------------------------------
        if pilihan == "1":
            while True:
                print("\n  == SUB-MENU KENDARAAN ==")
                print("  1. Lihat Semua Kendaraan")
                print("  2. Tambah Kendaraan Baru")
                print("  3. Edit Harga Sewa")
                print("  4. Hapus Kendaraan")
                print("  0. Kembali")
                
                sub_pilih = input("  >> Pilih: ")

                if sub_pilih == "1":
                    tampilkan_tabel_kendaraan("semua")
                
                elif sub_pilih == "2":
                    print("\n  [INPUT DATA KENDARAAN BARU]")
                    nama = input_teks("  Masukkan Nama: ")
                    jenis = input_teks("  Masukkan Jenis (Motor/Mobil/Truk): ")
                    plat = input_teks("  Masukkan Plat Nomor: ").upper()
                    harga = input_angka("  Masukkan Harga/Hari: ")
                    
                    # Panggil fungsi proses
                    sukses, pesan = proses_tambah_kendaraan(nama, jenis, plat, harga)
                    if sukses:
                        print(f"  [v] {pesan}")
                    else:
                        print(f"  [x] Gagal: {pesan}")

                elif sub_pilih == "3":
                    tampilkan_tabel_kendaraan("semua")
                    if len(kendaraan_id) == 0: continue # Skip jika kosong

                    id_input = input_angka("  Masukkan Nomor ID Kendaraan yang akan diedit: K")
                    idx = cari_index_kendaraan(id_input)
                    
                    if idx != -1:
                        print(f"  Nama: {kendaraan_nama[idx]}, Harga Lama: {format_rupiah(kendaraan_harga[idx])}")
                        harga_baru = input_angka("  Masukkan Harga Baru: ")
                        konfirmasi = input(f"  Yakin ubah harga menjadi {format_rupiah(harga_baru)}? (y/n): ")
                        
                        if konfirmasi.lower() == 'y':
                            # Panggil fungsi proses
                            sukses, pesan = proses_edit_harga(id_input, harga_baru)
                            print(f"  [v] {pesan}")
                        else:
                            print("  [i] Edit dibatalkan.")
                    else:
                        print("  [x] ID tidak ditemukan.")

                elif sub_pilih == "4":
                    tampilkan_tabel_kendaraan("Tersedia")
                    if kendaraan_status.count("Tersedia") == 0: continue # Skip jika tidak ada yang bisa dihapus

                    id_input = input_angka("  Masukkan Nomor ID Kendaraan yang akan dihapus: K")
                    idx = cari_index_kendaraan(id_input)
                    
                    if idx != -1:
                        konfirmasi = input(f"  Yakin hapus '{kendaraan_nama[idx]}' ({kendaraan_plat[idx]})? (y/n): ")
                        if konfirmasi.lower() == 'y':
                            # Panggil fungsi proses
                            sukses, pesan = proses_hapus_kendaraan(id_input)
                            if sukses:
                                print(f"  [v] {pesan}")
                            else:
                                print(f"  [x] {pesan}")
                        else:
                            print("  [i] Penghapusan dibatalkan.")
                    else:
                        print("  [x] ID tidak ditemukan.")

                elif sub_pilih == "0":
                    break

        # --------------------------------------------------------
        # MENU 2: PINJAM KENDARAAN
        # --------------------------------------------------------
        elif pilihan == "2":
            print("\n[TRANSAKSI PEMINJAMAN]")
            tampilkan_tabel_kendaraan("Tersedia")
            
            # Cek apakah ada yang tersedia
            if kendaraan_status.count("Tersedia") == 0:
                print("[!] Maaf, tidak ada kendaraan yang bisa dipinjam saat ini.")
                continue

            id_k = input_angka("Masukkan Nomor ID Kendaraan yang dipilih: K")
            idx_k = cari_index_kendaraan(id_k)

            if idx_k != -1 and kendaraan_status[idx_k] == "Tersedia":
                nama_p = input_teks("Masukkan Nama Lengkap Peminjam: ")
                durasi = input_angka("Durasi Pinjam (Hari): ")
                
                # Kalkulasi total di main untuk konfirmasi
                estimasi_total = kendaraan_harga[idx_k] * durasi
                print(f"Estimasi Total Biaya: {format_rupiah(estimasi_total)}")
                
                konfirmasi = input("Konfirmasi Peminjaman? (y/n): ")
                if konfirmasi.lower() == 'y':
                    # Panggil fungsi proses
                    sukses, pesan, total_final = proses_catat_peminjaman(id_k, nama_p, durasi)
                    if sukses:
                        print(f"[v] {pesan} Total: {format_rupiah(total_final)}")
                    else:
                        print(f"[x] {pesan}")
                else:
                    print("[i] Transaksi dibatalkan.")
            else:
                print("[x] ID Kendaraan salah atau sedang dipinjam.")

        # --------------------------------------------------------
        # (Belum Ada Fitur)
        # --------------------------------------------------------
        elif pilihan in ["3", "4", "5"]:
            print("\n[!] Maaf, masih belum ada fiturnya.")

        elif pilihan == "0":
            print("\nTerima kasih. Sampai jumpa!")
            break
        else:
            print("[!] Pilihan menu tidak valid.")

if __name__ == "__main__":
    main()
