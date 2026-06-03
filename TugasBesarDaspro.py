# ============================================================
#   SISTEM MANAJEMEN PEMINJAMAN KENDARAAN
#   Mata Kuliah : Dasar Pemrograman
#   Kelompok    : - Steven Theodor               (2572015)
#                 - Roland Michael Febrian        (2572017)
#                 - Gabriele Sebastien De Fretes  (2572054)
# ============================================================


# ============================================================
#   DEKLARASI ARRAY GLOBAL (PARALLEL ARRAYS)
# ============================================================

# --- Data Kendaraan ---
kendaraan_id     = []   # int
kendaraan_nama   = []   # str
kendaraan_jenis  = []   # str  (Motor / Mobil / Truk)
kendaraan_plat   = []   # str
kendaraan_harga  = []   # int  (per hari)
kendaraan_status = []   # str  (Tersedia / Dipinjam)

# --- Data Peminjaman ---
pinjam_id           = []  # int
pinjam_id_kendaraan = []  # int  (FK -> kendaraan_id)
pinjam_nama         = []  # str
pinjam_hari         = []  # int
pinjam_total        = []  # int
pinjam_status       = []  # str  (Aktif / Selesai)

counter_kendaraan = [1]
counter_pinjam    = [1]


# ============================================================
#   FUNGSI UTILITAS
# ============================================================

def garis(karakter="-", lebar=70):
    print(karakter * lebar)

def format_rupiah(nominal):
    s = str(nominal)
    hasil = ""
    hitung = 0
    for i in range(len(s) - 1, -1, -1):
        if hitung > 0 and hitung % 3 == 0:
            hasil = "." + hasil
        hasil = s[i] + hasil
        hitung += 1
    return "Rp " + hasil

def format_id_k(n):
    return f"K{str(n).zfill(3)}"

def format_id_p(n):
    return f"P{str(n).zfill(3)}"

def cari_idx_kendaraan(id_cari):
    for i in range(len(kendaraan_id)):
        if kendaraan_id[i] == id_cari:
            return i
    return -1

def input_angka(pesan):
    while True:
        try:
            return int(input(pesan))
        except ValueError:
            print("  [!] Masukkan angka bulat yang valid.")

def input_teks(pesan):
    while True:
        val = input(pesan).strip()
        if val:
            return val
        print("  [!] Input tidak boleh kosong.")

def tekan_enter():
    input("\n  [ Tekan ENTER untuk lanjut... ]")


# ============================================================
#   FUNGSI TAMPIL DATA & PENCARIAN
# ============================================================

def tampilkan_tabel_kendaraan(filter_status="semua", filter_jenis=None):
    judul = "SEMUA KENDARAAN"
    if filter_status != "semua":
        judul = f"KENDARAAN — {filter_status.upper()}"
    if filter_jenis:
        judul += f" | JENIS: {filter_jenis.upper()}"

    LEBAR = 70
    print()
    garis("=", LEBAR)
    print(f"  {judul}")
    garis("-", LEBAR)
    print(f"  {'ID':<6}  {'Nama':<20}  {'Jenis':<7}  {'Plat':<12}  {'Harga/Hari':>13}   Status")
    garis("-", LEBAR)

    ada_data = False
    for i in range(len(kendaraan_id)):
        if filter_status != "semua" and kendaraan_status[i] != filter_status:
            continue
        if filter_jenis and kendaraan_jenis[i].lower() != filter_jenis.lower():
            continue

        id_str     = format_id_k(kendaraan_id[i])
        nama_str   = kendaraan_nama[i]
        jenis_str  = kendaraan_jenis[i]
        plat_str   = kendaraan_plat[i]
        harga_str  = format_rupiah(kendaraan_harga[i])
        status_str = kendaraan_status[i]
        tanda      = "[v]" if status_str == "Tersedia" else "[-]"

        print(f"  {id_str:<6}  {nama_str:<20}  {jenis_str:<7}  {plat_str:<12}  {harga_str:>13}  {tanda} {status_str}")
        ada_data = True

    if not ada_data:
        print("  (Tidak ada data yang sesuai.)")
    garis("=", LEBAR)
    return ada_data


def cari_kendaraan(keyword):
    LEBAR = 70
    print()
    garis("=", LEBAR)
    print(f"  HASIL PENCARIAN UNTUK: '{keyword}'")
    garis("-", LEBAR)
    print(f"  {'ID':<6}  {'Nama':<20}  {'Jenis':<7}  {'Plat':<12}  {'Harga/Hari':>13}   Status")
    garis("-", LEBAR)

    ada_data = False
    keyword_lower = keyword.lower()

    for i in range(len(kendaraan_id)):
        if (keyword_lower in kendaraan_nama[i].lower() or 
            keyword_lower in kendaraan_plat[i].lower() or 
            keyword_lower in kendaraan_jenis[i].lower()):
            
            id_str     = format_id_k(kendaraan_id[i])
            nama_str   = kendaraan_nama[i]
            jenis_str  = kendaraan_jenis[i]
            plat_str   = kendaraan_plat[i]
            harga_str  = format_rupiah(kendaraan_harga[i])
            status_str = kendaraan_status[i]
            tanda      = "[v]" if status_str == "Tersedia" else "[-]"

            print(f"  {id_str:<6}  {nama_str:<20}  {jenis_str:<7}  {plat_str:<12}  {harga_str:>13}  {tanda} {status_str}")
            ada_data = True

    if not ada_data:
        print(f"  (Tidak ada kendaraan yang cocok dengan kata kunci '{keyword}')")
    garis("=", LEBAR)


# ============================================================
#   FUNGSI LOGIKA PROSES
# ============================================================

def proses_tambah_kendaraan(nama, jenis, plat, harga):
    for p in kendaraan_plat:
        if p.upper() == plat.upper():
            return False, "Nomor plat sudah terdaftar."
    kendaraan_id.append(counter_kendaraan[0])
    kendaraan_nama.append(nama)
    kendaraan_jenis.append(jenis)
    kendaraan_plat.append(plat.upper())
    kendaraan_harga.append(harga)
    kendaraan_status.append("Tersedia")
    counter_kendaraan[0] += 1
    return True, "Kendaraan berhasil ditambahkan."

def proses_edit_harga(id_k, harga_baru):
    idx = cari_idx_kendaraan(id_k)
    if idx == -1:
        return False, "ID Kendaraan tidak ditemukan."
    kendaraan_harga[idx] = harga_baru
    return True, "Harga berhasil diperbarui."

def proses_hapus_kendaraan(id_k):
    idx = cari_idx_kendaraan(id_k)
    if idx == -1:
        return False, "ID Kendaraan tidak ditemukan."
    if kendaraan_status[idx] == "Dipinjam":
        return False, "Kendaraan sedang dipinjam, tidak bisa dihapus."
    kendaraan_id.pop(idx)
    kendaraan_nama.pop(idx)
    kendaraan_jenis.pop(idx)
    kendaraan_plat.pop(idx)
    kendaraan_harga.pop(idx)
    kendaraan_status.pop(idx)
    return True, "Kendaraan berhasil dihapus."

def proses_catat_peminjaman(id_k, nama_p, durasi):
    idx_k = cari_idx_kendaraan(id_k)
    if idx_k == -1:
        return False, "ID Kendaraan tidak ditemukan.", 0
    if kendaraan_status[idx_k] != "Tersedia":
        return False, "Kendaraan tidak tersedia.", 0
    total = kendaraan_harga[idx_k] * durasi
    pinjam_id.append(counter_pinjam[0])
    pinjam_id_kendaraan.append(id_k)
    pinjam_nama.append(nama_p)
    pinjam_hari.append(durasi)
    pinjam_total.append(total)
    pinjam_status.append("Aktif")
    kendaraan_status[idx_k] = "Dipinjam"
    counter_pinjam[0] += 1
    return True, "Peminjaman berhasil dicatat.", total

def proses_pengembalian(idx_pinjam):
    if pinjam_status[idx_pinjam] == "Selesai":
        return False, "Transaksi ini sudah selesai."
        
    # Ubah status peminjaman jadi Selesai
    pinjam_status[idx_pinjam] = "Selesai"
    
    # Balikin status kendaraan jadi Tersedia lagi
    id_k = pinjam_id_kendaraan[idx_pinjam]
    idx_k = cari_idx_kendaraan(id_k)
    if idx_k != -1:
        kendaraan_status[idx_k] = "Tersedia"
        
    return True, "Kendaraan berhasil dikembalikan dan siap disewa lagi."


# ============================================================
#   ISI DATA AWAL (DUMMY)
# ============================================================

def isi_data_dummy():
    data_kendaraan = [
        ("Honda Beat",       "Motor", "D-1234-AB",  85_000),
        ("Yamaha Nmax",      "Motor", "D-5678-CD", 110_000),
        ("Honda Vario 160",  "Motor", "D-1111-ZZ", 100_000),
        ("Toyota Avanza",    "Mobil", "D-9012-EF", 350_000),
        ("Honda Brio",       "Mobil", "D-3456-GH", 300_000),
        ("Mitsubishi L300",  "Truk",  "D-7890-IJ", 550_000),
        ("Suzuki Carry",     "Truk",  "D-2345-KL", 450_000),
    ]
    for nama, jenis, plat, harga in data_kendaraan:
        proses_tambah_kendaraan(nama, jenis, plat, harga)
        
    # Tambah dummy peminjaman biar menu 3 bisa langsung dites
    proses_catat_peminjaman(1, "Budi Santoso",  3)
    proses_catat_peminjaman(4, "Siti Rahayu",   2)


# ============================================================
#   MENU 1 — MANAJEMEN DATA KENDARAAN
# ============================================================

def pilih_jenis():
    print("  Jenis :  1) Motor   2) Mobil   3) Truk")
    while True:
        pj = input("  >> Pilih jenis [1/2/3]: ").strip()
        if pj == "1":   return "Motor"
        elif pj == "2": return "Mobil"
        elif pj == "3": return "Truk"
        print("  [!] Pilih angka 1, 2, atau 3.")

def menu_kendaraan():
    while True:
        print("\n")
        garis("=", 44)
        print("      MANAJEMEN DATA KENDARAAN")
        garis("=", 44)
        print("  1. Lihat Semua Kendaraan")
        print("  2. Kendaraan Tersedia")
        print("  3. Kendaraan Sedang Dipinjam")
        print("  4. Filter Berdasarkan Jenis")
        print("  ─────────────────────────────────────")
        print("  5. Tambah Kendaraan Baru")
        print("  6. Edit Harga Sewa")
        print("  7. Hapus Kendaraan")
        print("  ─────────────────────────────────────")
        print("  0. Kembali ke Menu Utama")
        garis("-", 44)
        sub = input("  >> Pilih: ").strip()

        if sub == "1":
            tampilkan_tabel_kendaraan()
            tekan_enter()
        elif sub == "2":
            tampilkan_tabel_kendaraan("Tersedia")
            tekan_enter()
        elif sub == "3":
            tampilkan_tabel_kendaraan("Dipinjam")
            tekan_enter()
        elif sub == "4":
            print("\n  [ FILTER BERDASARKAN JENIS ]")
            jenis_cari = pilih_jenis()
            tampilkan_tabel_kendaraan("semua", jenis_cari)
            tekan_enter()
        elif sub == "5":
            print("\n  [ TAMBAH KENDARAAN BARU ]")
            garis("-", 44)
            nama  = input_teks("  Nama Kendaraan  : ")
            jenis = pilih_jenis()
            plat  = input_teks("  Nomor Plat      : ").upper()
            harga = input_angka("  Harga Sewa/Hari : Rp ")

            garis("-", 44)
            print("  Ringkasan data :")
            print(f"    Nama  : {nama}")
            print(f"    Jenis : {jenis}")
            print(f"    Plat  : {plat}")
            print(f"    Harga : {format_rupiah(harga)}/hari")
            garis("-", 44)
            konfirmasi = input("  Simpan data ini? (y/n): ").strip().lower()

            if konfirmasi == "y":
                ok, msg = proses_tambah_kendaraan(nama, jenis, plat, harga)
                if ok:
                    id_baru = format_id_k(counter_kendaraan[0] - 1)
                    print(f"  [v] {msg}  →  ID diberikan: {id_baru}")
                else:
                    print(f"  [x] Gagal: {msg}")
            else:
                print("  [i] Penambahan dibatalkan.")
            tekan_enter()
        elif sub == "6":
            print("\n  [ EDIT HARGA SEWA ]")
            tampilkan_tabel_kendaraan()
            if not kendaraan_id:
                tekan_enter()
                continue
            id_in = input_angka("  Masukkan ID (angka saja): K")
            idx   = cari_idx_kendaraan(id_in)
            if idx == -1:
                print("  [x] ID tidak ditemukan.")
            else:
                print(f"  Kendaraan  : {kendaraan_nama[idx]}  ({kendaraan_plat[idx]})")
                print(f"  Harga Lama : {format_rupiah(kendaraan_harga[idx])}/hari")
                harga_baru = input_angka("  Harga Baru : Rp ")
                konfirmasi = input(f"  Ubah ke {format_rupiah(harga_baru)}/hari? (y/n): ").strip().lower()
                if konfirmasi == "y":
                    ok, msg = proses_edit_harga(id_in, harga_baru)
                    print(f"  [v] {msg}" if ok else f"  [x] {msg}")
                else:
                    print("  [i] Edit dibatalkan.")
            tekan_enter()
        elif sub == "7":
            print("\n  [ HAPUS KENDARAAN ]")
            tampilkan_tabel_kendaraan("Tersedia")
            if kendaraan_status.count("Tersedia") == 0:
                print("  [!] Tidak ada kendaraan yang bisa dihapus saat ini.")
                tekan_enter()
                continue
            id_in = input_angka("  Masukkan ID (angka saja): K")
            idx   = cari_idx_kendaraan(id_in)
            if idx == -1:
                print("  [x] ID tidak ditemukan.")
            else:
                print(f"  Kendaraan : {format_id_k(kendaraan_id[idx])} | {kendaraan_nama[idx]} | {kendaraan_plat[idx]}")
                konfirmasi = input("  Yakin ingin menghapus? (y/n): ").strip().lower()
                if konfirmasi == "y":
                    ok, msg = proses_hapus_kendaraan(id_in)
                    print(f"  [v] {msg}" if ok else f"  [x] {msg}")
                else:
                    print("  [i] Penghapusan dibatalkan.")
            tekan_enter()
        elif sub == "0":
            break
        else:
            print("  [!] Pilihan tidak valid.")


# ============================================================
#   ENTRY POINT (MENU UTAMA)
# ============================================================

def main():
    isi_data_dummy()

    garis("=", 70)
    print("        SISTEM MANAJEMEN PEMINJAMAN KENDARAAN")
    print("        Dasar Pemrograman  —  Kelompok 2572015/017/054")
    garis("=", 70)

    while True:
        print("\n  ──────  MENU UTAMA  ──────")
        print("  1. Manajemen Data Kendaraan")
        print("  2. Transaksi Pinjam Kendaraan")
        print("  3. Transaksi Kembalikan Kendaraan")
        print("  4. Riwayat Peminjaman")
        print("  5. Cari Kendaraan")
        print("  6. Laporan & Statistik")
        print("  0. Keluar")
        garis("-", 34)
        pilihan = input("  >> Pilih Menu: ").strip()

        if pilihan == "1":
            menu_kendaraan()
            
        elif pilihan == "3":
            print("\n  [ TRANSAKSI PENGEMBALIAN KENDARAAN ]")
            garis("-", 70)
            
            # Cari transaksi yang masih aktif aja
            aktif_indices = [i for i in range(len(pinjam_id)) if pinjam_status[i] == "Aktif"]
            
            if not aktif_indices:
                print("  [!] Tidak ada peminjaman aktif saat ini.")
                tekan_enter()
                continue
                
            # Bikin tabel rapi biar enak dilihat
            print(f"  {'No':<4} {'ID Pinjam':<10} {'Nama Penyewa':<20} {'Kendaraan (ID)':<17} {'Total'}")
            garis("-", 70)
            
            for nomor, idx in enumerate(aktif_indices, start=1):
                id_p = format_id_p(pinjam_id[idx])
                nama = pinjam_nama[idx]
                id_k = format_id_k(pinjam_id_kendaraan[idx])
                total = format_rupiah(pinjam_total[idx])
                
                print(f"  {nomor:<4} {id_p:<10} {nama:<20} {id_k:<17} {total}")
            garis("-", 70)

            # Input pilih urutan nomor (bukan K)
            pilihan_kembali = input_angka("  >> Pilih nomor urut transaksi yang dikembalikan: ")
            
            if 1 <= pilihan_kembali <= len(aktif_indices):
                idx = aktif_indices[pilihan_kembali - 1]
                
                konfirmasi = input(f"  Yakin selesaikan transaksi {format_id_p(pinjam_id[idx])}? (y/n): ").strip().lower()
                
                if konfirmasi == "y":
                    sukses, pesan = proses_pengembalian(idx)
                    if sukses:
                        print(f"  [v] {pesan}")
                    else:
                        print(f"  [x] {pesan}")
                else:
                    print("  [i] Pengembalian dibatalkan.")
            else:
                print("  [!] Pilihan tidak valid.")
            tekan_enter()
            
        elif pilihan == "5":
            print("\n  [ CARI KENDARAAN ]")
            keyword = input_teks("  Masukkan nama/plat/jenis kendaraan: ")
            cari_kendaraan(keyword)
            tekan_enter()
            
        # Pilihan 3 udah dihapus dari list pengembangan
        elif pilihan in ["2", "4", "6"]:
            print("\n  [!] Fitur ini sedang dalam pengembangan.")
            tekan_enter()
            
        elif pilihan == "0":
            garis("=", 70)
            print("  Terima kasih telah menggunakan sistem ini. Sampai jumpa!")
            garis("=", 70)
            break
            
        else:
            print("  [!] Pilihan menu tidak valid.")

if __name__ == "__main__":
    main()
