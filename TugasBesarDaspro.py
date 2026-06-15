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

kendaraan_id     = []  
kendaraan_nama   = []   
kendaraan_jenis  = []   
kendaraan_plat   = []  
kendaraan_harga  = []   
kendaraan_status = []   


pinjam_id           = []  
pinjam_id_kendaraan = []  
pinjam_nama         = [] 
pinjam_hari         = []  
pinjam_total        = []  
pinjam_status       = []  
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
    if n < 10:
        return f"K00{n}"
    elif n < 100:
        return f"K0{n}"
    else:
        return f"K{n}"

def format_id_p(n):
    if n < 10:
        return f"P00{n}"
    elif n < 100:
        return f"P0{n}"
    else:
        return f"P{n}"

def cari_idx_kendaraan(id_cari):
    for i in range(len(kendaraan_id)):
        if kendaraan_id[i] == id_cari:
            return i
    return -1

def input_angka(pesan):
    selesai = False
    while not selesai:
        teks = hapus_spasi(input(pesan))
        if teks != "":
            angka_benar = True
            for karakter in teks:
                if karakter < '0' or karakter > '9':
                    angka_benar = False
            if angka_benar:
                return int(teks)
        print("  [!] Masukkan angka bulat yang valid.")

def hapus_spasi(teks):
    awal = 0
    while awal < len(teks) and teks[awal] in " \t\n\r":
        awal += 1
    akhir = len(teks) - 1
    while akhir >= awal and teks[akhir] in " \t\n\r":
        akhir -= 1
    return teks[awal:akhir + 1]

def input_teks(pesan):
    while True:
        val = hapus_spasi(input(pesan))
        if val:
            return val
        print("  [!] Input tidak boleh kosong.")

def beri_spasi_kanan(teks, lebar):
    hasil = teks
    while len(hasil) < lebar:
        hasil = hasil + " "
    return hasil

def ubah_ke_besar(teks):
    tabel = {
        'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D', 'e': 'E',
        'f': 'F', 'g': 'G', 'h': 'H', 'i': 'I', 'j': 'J',
        'k': 'K', 'l': 'L', 'm': 'M', 'n': 'N', 'o': 'O',
        'p': 'P', 'q': 'Q', 'r': 'R', 's': 'S', 't': 'T',
        'u': 'U', 'v': 'V', 'w': 'W', 'x': 'X', 'y': 'Y', 'z': 'Z'
    }
    hasil = ""
    for huruf in teks:
        hasil += tabel.get(huruf, huruf)
    return hasil

def ubah_ke_kecil(teks):
    tabel = {
        'A': 'a', 'B': 'b', 'C': 'c', 'D': 'd', 'E': 'e',
        'F': 'f', 'G': 'g', 'H': 'h', 'I': 'i', 'J': 'j',
        'K': 'k', 'L': 'l', 'M': 'm', 'N': 'n', 'O': 'o',
        'P': 'p', 'Q': 'q', 'R': 'r', 'S': 's', 'T': 't',
        'U': 'u', 'V': 'v', 'W': 'w', 'X': 'x', 'Y': 'y', 'Z': 'z'
    }
    hasil = ""
    for huruf in teks:
        hasil += tabel.get(huruf, huruf)
    return hasil

def tekan_enter():
    input("\n  [ Tekan ENTER untuk lanjut... ]")


# ============================================================
#   FUNGSI UTILITAS TAMPIL & PENCARIAN
# ============================================================

def tampilkan_tabel_kendaraan(filter_status="semua", filter_jenis=None):
    judul = "SEMUA KENDARAAN"
    if filter_status != "semua":
        judul = f"KENDARAAN — {ubah_ke_besar(filter_status)}"
    if filter_jenis:
        judul += f" | JENIS: {ubah_ke_besar(filter_jenis)}"

    LEBAR = 70
    print()
    garis("=", LEBAR)
    print(f"  {judul}")
    garis("-", LEBAR)
    print("  " + beri_spasi_kanan("ID", 6) + "  " + beri_spasi_kanan("Nama", 20) + "  " + beri_spasi_kanan("Jenis", 7) + "  " + beri_spasi_kanan("Plat", 12) + "  " + "Harga/Hari".rjust(13) + "   Status")
    garis("-", LEBAR)

    ada_data = False
    for i in range(len(kendaraan_id)):
        cocok_status = filter_status == "semua" or kendaraan_status[i] == filter_status
        cocok_jenis  = not filter_jenis or ubah_ke_kecil(kendaraan_jenis[i]) == ubah_ke_kecil(filter_jenis)

        if cocok_status and cocok_jenis:
            id_str     = format_id_k(kendaraan_id[i])
            nama_str   = kendaraan_nama[i]
            jenis_str  = kendaraan_jenis[i]
            plat_str   = kendaraan_plat[i]
            harga_str  = format_rupiah(kendaraan_harga[i])
            status_str = kendaraan_status[i]
            tanda      = "[v]" if status_str == "Tersedia" else "[-]"

            print("  " + beri_spasi_kanan(id_str, 6) + "  " + beri_spasi_kanan(nama_str, 20) + "  " + beri_spasi_kanan(jenis_str, 7) + "  " + beri_spasi_kanan(plat_str, 12) + "  " + harga_str.rjust(13) + "  " + tanda + " " + status_str)
            ada_data = True

    if not ada_data:
        print("  (Tidak ada data yang sesuai.)")
    garis("=", LEBAR)
    return ada_data

def tampilkan_tabel_peminjaman(filter_status="semua"):
    print("\n--- RIWAYAT PEMINJAMAN ---")
    found = False
    print("ID   | ID Kendaraan | Nama Peminjam    | Hari | Total        | Status")
    garis("-", 70)
    for i in range(len(pinjam_id)):
        if filter_status == "semua" or pinjam_status[i] == filter_status:
            txt_id   = format_id_p(pinjam_id[i])
            txt_id_k = format_id_k(pinjam_id_kendaraan[i])
            txt_nama = pinjam_nama[i] + " " * (16 - len(pinjam_nama[i]))
            txt_hari = " " * (4 - len(str(pinjam_hari[i]))) + str(pinjam_hari[i])
            txt_total = " " * (12 - len(format_rupiah(pinjam_total[i]))) + format_rupiah(pinjam_total[i])
            print(f"{txt_id} | {txt_id_k}       | {txt_nama} | {txt_hari} | {txt_total} | {pinjam_status[i]}")
            found = True
    if not found:
        print(" (Tidak ada data)")
    garis("-", 70)


# ============================================================
#   FUNGSI LOGIKA PROSES
# ============================================================

def proses_tambah_kendaraan(nama, jenis, plat, harga):
    global kendaraan_id, kendaraan_nama, kendaraan_jenis, kendaraan_plat, kendaraan_harga, kendaraan_status, counter_kendaraan
    for p in kendaraan_plat:
        if p == plat:
            return False, "Nomor plat sudah terdaftar."
    kendaraan_id     = kendaraan_id     + [counter_kendaraan[0]]
    kendaraan_nama   = kendaraan_nama   + [nama]
    kendaraan_jenis  = kendaraan_jenis  + [jenis]
    kendaraan_plat   = kendaraan_plat   + [plat]
    kendaraan_harga  = kendaraan_harga  + [harga]
    kendaraan_status = kendaraan_status + ["Tersedia"]
    counter_kendaraan[0] += 1
    return True, "Kendaraan berhasil ditambahkan."

def proses_edit_harga(id_k, harga_baru):
    idx = cari_idx_kendaraan(id_k)
    if idx == -1:
        return False, "ID Kendaraan tidak ditemukan."
    kendaraan_harga[idx] = harga_baru
    return True, "Harga berhasil diperbarui."

def proses_hapus_kendaraan(id_k):
    global kendaraan_id, kendaraan_nama, kendaraan_jenis, kendaraan_plat, kendaraan_harga, kendaraan_status
    idx = cari_idx_kendaraan(id_k)
    if idx == -1:
        return False, "ID Kendaraan tidak ditemukan."
    if kendaraan_status[idx] == "Dipinjam":
        return False, "Kendaraan sedang dipinjam, tidak bisa dihapus."
    kendaraan_id     = kendaraan_id[:idx]     + kendaraan_id[idx + 1:]
    kendaraan_nama   = kendaraan_nama[:idx]   + kendaraan_nama[idx + 1:]
    kendaraan_jenis  = kendaraan_jenis[:idx]  + kendaraan_jenis[idx + 1:]
    kendaraan_plat   = kendaraan_plat[:idx]   + kendaraan_plat[idx + 1:]
    kendaraan_harga  = kendaraan_harga[:idx]  + kendaraan_harga[idx + 1:]
    kendaraan_status = kendaraan_status[:idx] + kendaraan_status[idx + 1:]
    return True, "Kendaraan berhasil dihapus."

def proses_catat_peminjaman(id_k, nama_p, durasi):
    global pinjam_id, pinjam_id_kendaraan, pinjam_nama, pinjam_hari, pinjam_total, pinjam_status, counter_pinjam
    idx_k = cari_idx_kendaraan(id_k)
    if idx_k == -1:
        return False, "ID Kendaraan tidak ditemukan.", 0
    if kendaraan_status[idx_k] != "Tersedia":
        return False, "Kendaraan tidak tersedia.", 0
    total               = kendaraan_harga[idx_k] * durasi
    pinjam_id           = pinjam_id           + [counter_pinjam[0]]
    pinjam_id_kendaraan = pinjam_id_kendaraan + [id_k]
    pinjam_nama         = pinjam_nama         + [nama_p]
    pinjam_hari         = pinjam_hari         + [durasi]
    pinjam_total        = pinjam_total        + [total]
    pinjam_status       = pinjam_status       + ["Aktif"]
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


def tampilkan_tabel_peminjaman(filter_status="semua"):
    print("\n--- RIWAYAT PEMINJAMAN ---")
    found = False
    print("ID   | ID Kendaraan | Nama Peminjam    | Hari | Total        | Status")
    garis("-", 70)
    for i in range(len(pinjam_id)):
        if filter_status == "semua" or pinjam_status[i] == filter_status:
            txt_id = format_id_p(pinjam_id[i])
            txt_id_k = format_id_k(pinjam_id_kendaraan[i])
            txt_nama = pinjam_nama[i] + " " * (16 - len(pinjam_nama[i]))
            txt_hari = " " * (4 - len(str(pinjam_hari[i]))) + str(pinjam_hari[i])
            txt_total = " " * (12 - len(format_rupiah(pinjam_total[i]))) + format_rupiah(pinjam_total[i])
            print(f"{txt_id} | {txt_id_k}       | {txt_nama} | {txt_hari} | {txt_total} | {pinjam_status[i]}")
            found = True
    if not found:
        print(" (Tidak ada data)")
    garis("-", 70)

# ============================================================
#   MENU 6 — LAPORAN & STATISTIK
# ============================================================

def hitung_total_kendaraan():
    return len(kendaraan_id)


def hitung_kendaraan_per_status():
    total_tersedia = 0
    total_dipinjam = 0
    for i in range(len(kendaraan_status)):
        if kendaraan_status[i] == "Tersedia":
            total_tersedia = total_tersedia + 1
        else:
            total_dipinjam = total_dipinjam + 1
    return total_tersedia, total_dipinjam

def hitung_rincian_jenis():
    jenis_unik     = []
    jenis_jumlah   = []
    jenis_tersedia = []
    jenis_dipinjam = []

    for i in range(len(kendaraan_jenis)):
        jenis = kendaraan_jenis[i]
        idx   = -1
        for j in range(len(jenis_unik)):
            if jenis_unik[j] == jenis:
                idx = j

        if idx == -1:
            jenis_unik   = jenis_unik   + [jenis]
            jenis_jumlah = jenis_jumlah + [1]
            if kendaraan_status[i] == "Tersedia":
                jenis_tersedia = jenis_tersedia + [1]
                jenis_dipinjam = jenis_dipinjam + [0]
            else:
                jenis_tersedia = jenis_tersedia + [0]
                jenis_dipinjam = jenis_dipinjam + [1]
        else:
            jenis_jumlah[idx] = jenis_jumlah[idx] + 1
            if kendaraan_status[i] == "Tersedia":
                jenis_tersedia[idx] = jenis_tersedia[idx] + 1
            else:
                jenis_dipinjam[idx] = jenis_dipinjam[idx] + 1

    return jenis_unik, jenis_jumlah, jenis_tersedia, jenis_dipinjam

def hitung_total_transaksi():
    jumlah_aktif   = 0
    jumlah_selesai = 0
    for i in range(len(pinjam_status)):
        if pinjam_status[i] == "Aktif":
            jumlah_aktif = jumlah_aktif + 1
        else:
            jumlah_selesai = jumlah_selesai + 1
    return jumlah_aktif, jumlah_selesai


def hitung_pendapatan():
    pendapatan_selesai = 0
    pendapatan_aktif   = 0
    for i in range(len(pinjam_id)):
        if pinjam_status[i] == "Selesai":
            pendapatan_selesai = pendapatan_selesai + pinjam_total[i]
        else:
            pendapatan_aktif = pendapatan_aktif + pinjam_total[i]
    return pendapatan_selesai, pendapatan_aktif


def cari_kendaraan_populer():
    id_unik     = []
    jumlah_sewa = []

    for i in range(len(pinjam_id_kendaraan)):
        id_k = pinjam_id_kendaraan[i]
        idx  = -1
        for j in range(len(id_unik)):
            if id_unik[j] == id_k:
                idx = j

        if idx == -1:
            id_unik     = id_unik     + [id_k]
            jumlah_sewa = jumlah_sewa + [1]
        else:
            jumlah_sewa[idx] = jumlah_sewa[idx] + 1

    if not id_unik:
        return -1, 0

    idx_max = 0
    for i in range(1, len(jumlah_sewa)):
        if jumlah_sewa[i] > jumlah_sewa[idx_max]:
            idx_max = i

    return id_unik[idx_max], jumlah_sewa[idx_max]


def tampilkan_laporan_statistik():
    LEBAR = 70
    print()
    garis("=", LEBAR)
    print("  LAPORAN & STATISTIK SISTEM")
    garis("=", LEBAR)

    total_kendaraan = hitung_total_kendaraan()
    total_tersedia, total_dipinjam = hitung_kendaraan_per_status()

    print("\n  [ DATA KENDARAAN ]")
    garis("-", LEBAR)
    print(f"  Total Kendaraan       : {total_kendaraan} unit")
    print(f"  Kendaraan Tersedia    : {total_tersedia} unit")
    print(f"  Kendaraan Dipinjam    : {total_dipinjam} unit")

    jenis_unik, jenis_jumlah, jenis_tersedia, jenis_dipinjam = hitung_rincian_jenis()

    print("\n  [ RINCIAN PER JENIS KENDARAAN ]")
    garis("-", LEBAR)
    if not jenis_unik:
        print("  (Belum ada data kendaraan.)")
    else:
        print("  " + beri_spasi_kanan("Jenis", 10) + beri_spasi_kanan("Total", 8) +
              beri_spasi_kanan("Tersedia", 10) + "Dipinjam")
        garis("-", LEBAR)
        for i in range(len(jenis_unik)):
            print("  " + beri_spasi_kanan(jenis_unik[i], 10) +
                  beri_spasi_kanan(str(jenis_jumlah[i]), 8) +
                  beri_spasi_kanan(str(jenis_tersedia[i]), 10) +
                  str(jenis_dipinjam[i]))

    # --- 3. Transaksi peminjaman ---
    jumlah_aktif, jumlah_selesai = hitung_total_transaksi()
    total_transaksi = jumlah_aktif + jumlah_selesai

    print("\n  [ TRANSAKSI PEMINJAMAN ]")
    garis("-", LEBAR)
    print(f"  Total Transaksi       : {total_transaksi} transaksi")
    print(f"  Transaksi Aktif       : {jumlah_aktif} transaksi")
    print(f"  Transaksi Selesai     : {jumlah_selesai} transaksi")

    # --- 4. Pendapatan ---
    pendapatan_selesai, pendapatan_aktif = hitung_pendapatan()
    total_pendapatan = pendapatan_selesai + pendapatan_aktif

    print("\n  [ PENDAPATAN ]")
    garis("-", LEBAR)
    print(f"  Pendapatan (Selesai)      : {format_rupiah(pendapatan_selesai)}")
    print(f"  Potensi Pendapatan (Aktif): {format_rupiah(pendapatan_aktif)}")
    print(f"  Total Keseluruhan         : {format_rupiah(total_pendapatan)}")

    # --- 5. Kendaraan paling populer ---
    print("\n  [ KENDARAAN PALING POPULER ]")
    garis("-", LEBAR)
    id_populer, jumlah_sewa = cari_kendaraan_populer()
    if id_populer == -1:
        print("  (Belum ada data peminjaman.)")
    else:
        idx_k = cari_idx_kendaraan(id_populer)
        if idx_k == -1:
            print("  (Data kendaraan tidak ditemukan.)")
        else:
            print(f"  ID          : {format_id_k(id_populer)}")
            print(f"  Nama        : {kendaraan_nama[idx_k]}")
            print(f"  Plat        : {kendaraan_plat[idx_k]}")
            print(f"  Jenis       : {kendaraan_jenis[idx_k]}")
            print(f"  Jumlah Sewa : {jumlah_sewa} kali")

    garis("=", LEBAR)
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
    indeks = 0
    while indeks < len(data_kendaraan):
        nama  = data_kendaraan[indeks][0]
        jenis = data_kendaraan[indeks][1]
        plat  = data_kendaraan[indeks][2]
        harga = data_kendaraan[indeks][3]
        proses_tambah_kendaraan(nama, jenis, plat, harga)
        indeks = indeks + 1

    proses_catat_peminjaman(1, "Budi Santoso", 3)
    proses_catat_peminjaman(4, "Siti Rahayu",  2)


# ============================================================
#   MENU UTAMA
# ============================================================

def main():
    isi_data_dummy()
    selesai = False

    garis("=", 70)
    print("        SISTEM MANAJEMEN PEMINJAMAN KENDARAAN")
    print("        Dasar Pemrograman  —  Kelompok 2572015/017/054")
    garis("=", 70)

    while not selesai:
        print("\n  ──────  MENU UTAMA  ──────")
        print("  1. Manajemen Data Kendaraan")
        print("  2. Transaksi Pinjam Kendaraan")
        print("  3. Transaksi Kembalikan Kendaraan")
        print("  4. Riwayat Peminjaman")
        print("  5. Cari Kendaraan")
        print("  6. Laporan & Statistik")
        print("  0. Keluar")
        garis("-", 34)
        pilihan = hapus_spasi(input("  >> Pilih Menu: "))

        # ============================================================
        #   MENU 1 — MANAJEMEN DATA KENDARAAN
        # ============================================================
        if pilihan == "1":
            selesai_k = False
            while not selesai_k:
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
                sub = hapus_spasi(input("  >> Pilih: "))

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
                    print("  Jenis :  1) Motor   2) Mobil   3) Truk")
                    jenis_cari = None
                    while jenis_cari is None:
                        pj = hapus_spasi(input("  >> Pilih jenis [1/2/3]: "))
                        if pj == "1":   jenis_cari = "Motor"
                        elif pj == "2": jenis_cari = "Mobil"
                        elif pj == "3": jenis_cari = "Truk"
                        else:           print("  [!] Pilih angka 1, 2, atau 3.")
                    tampilkan_tabel_kendaraan("semua", jenis_cari)
                    tekan_enter()

                elif sub == "5":
                    print("\n  [ TAMBAH KENDARAAN BARU ]")
                    garis("-", 44)
                    nama  = input_teks("  Nama Kendaraan  : ")
                    print("  Jenis :  1) Motor   2) Mobil   3) Truk")
                    jenis = None
                    while jenis is None:
                        pj = hapus_spasi(input("  >> Pilih jenis [1/2/3]: "))
                        if pj == "1":   jenis = "Motor"
                        elif pj == "2": jenis = "Mobil"
                        elif pj == "3": jenis = "Truk"
                        else:           print("  [!] Pilih angka 1, 2, atau 3.")
                    plat  = input_teks("  Nomor Plat      : ")
                    harga = input_angka("  Harga Sewa/Hari : Rp ")

                    garis("-", 44)
                    print("  Ringkasan data :")
                    print(f"    Nama  : {nama}")
                    print(f"    Jenis : {jenis}")
                    print(f"    Plat  : {plat}")
                    print(f"    Harga : {format_rupiah(harga)}/hari")
                    garis("-", 44)
                    konfirmasi = ubah_ke_kecil(hapus_spasi(input("  Simpan data ini? (y/n): ")))

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
                    else:
                        id_in = input_angka("  Masukkan ID (angka saja): K")
                        idx   = cari_idx_kendaraan(id_in)
                        if idx == -1:
                            print("  [x] ID tidak ditemukan.")
                        else:
                            print(f"  Kendaraan  : {kendaraan_nama[idx]}  ({kendaraan_plat[idx]})")
                            print(f"  Harga Lama : {format_rupiah(kendaraan_harga[idx])}/hari")
                            harga_baru = input_angka("  Harga Baru : Rp ")
                            konfirmasi = ubah_ke_kecil(hapus_spasi(input(f"  Ubah ke {format_rupiah(harga_baru)}/hari? (y/n): ")))
                            if konfirmasi == "y":
                                ok, msg = proses_edit_harga(id_in, harga_baru)
                                if ok:   print(f"  [v] {msg}")
                                else:    print(f"  [x] {msg}")
                            else:
                                print("  [i] Edit dibatalkan.")
                        tekan_enter()

                elif sub == "7":
                    print("\n  [ HAPUS KENDARAAN ]")
                    tampilkan_tabel_kendaraan("Tersedia")
                    if kendaraan_status.count("Tersedia") == 0:
                        print("  [!] Tidak ada kendaraan yang bisa dihapus saat ini.")
                        tekan_enter()
                    else:
                        id_in = input_angka("  Masukkan ID (angka saja): K")
                        idx   = cari_idx_kendaraan(id_in)
                        if idx == -1:
                            print("  [x] ID tidak ditemukan.")
                        else:
                            print(f"  Kendaraan : {format_id_k(kendaraan_id[idx])} | {kendaraan_nama[idx]} | {kendaraan_plat[idx]}")
                            konfirmasi = ubah_ke_kecil(hapus_spasi(input("  Yakin ingin menghapus? (y/n): ")))
                            if konfirmasi == "y":
                                ok, msg = proses_hapus_kendaraan(id_in)
                                if ok:   print(f"  [v] {msg}")
                                else:    print(f"  [x] {msg}")
                            else:
                                print("  [i] Penghapusan dibatalkan.")
                        tekan_enter()

                elif sub == "0":
                    selesai_k = True

                else:
                    print("  [!] Pilihan tidak valid.")

        # ============================================================
        #   MENU 2 — TRANSAKSI PINJAM KENDARAAN
        # ============================================================
        elif pilihan == "2":
            print("\n  [ TRANSAKSI PINJAM KENDARAAN ]")
            ada_tersedia = tampilkan_tabel_kendaraan("Tersedia")

            if not ada_tersedia:
                print("  [!] Tidak ada kendaraan yang tersedia untuk dipinjam saat ini.")
                tekan_enter()
            else:
                id_in = input_angka("  Masukkan ID Kendaraan (angka saja): K")
                idx_k = cari_idx_kendaraan(id_in)

                if idx_k == -1:
                    print("  [x] ID Kendaraan tidak ditemukan.")
                    tekan_enter()
                elif kendaraan_status[idx_k] != "Tersedia":
                    print("  [x] Kendaraan tersebut sedang dipinjam, tidak bisa disewa.")
                    tekan_enter()
                else:
                    nama_p = input_teks("  Nama Peminjam : ")
                    durasi = input_angka("  Durasi Sewa (hari) : ")

                    while durasi <= 0:
                        print("  [!] Durasi minimal 1 hari.")
                        durasi = input_angka("  Durasi Sewa (hari) : ")

                    total = kendaraan_harga[idx_k] * durasi

                    garis("-", 70)
                    print("  Ringkasan Transaksi :")
                    print(f"    Kendaraan      : {kendaraan_nama[idx_k]}  ({kendaraan_plat[idx_k]})")
                    print(f"    Harga/Hari     : {format_rupiah(kendaraan_harga[idx_k])}")
                    print(f"    Nama Peminjam  : {nama_p}")
                    print(f"    Durasi         : {durasi} hari")
                    print(f"    Total Bayar    : {format_rupiah(total)}")
                    garis("-", 70)

                    konfirmasi = ubah_ke_kecil(hapus_spasi(input("  Konfirmasi peminjaman ini? (y/n): ")))

                    if konfirmasi == "y":
                        sukses, pesan, total_bayar = proses_catat_peminjaman(id_in, nama_p, durasi)
                        if sukses:
                            id_transaksi = format_id_p(counter_pinjam[0] - 1)
                            print(f"  [v] {pesan}  →  ID Transaksi: {id_transaksi}")
                            print(f"  [v] Total yang harus dibayar: {format_rupiah(total_bayar)}")
                        else:
                            print(f"  [x] Gagal: {pesan}")
                    else:
                        print("  [i] Peminjaman dibatalkan.")
                    tekan_enter()

        # ============================================================
        #   MENU 3 — TRANSAKSI KEMBALIKAN KENDARAAN
        # ============================================================
        elif pilihan == "3":
            print("\n  [ TRANSAKSI PENGEMBALIAN KENDARAAN ]")
            garis("-", 70)

            aktif_indices = []
            for i in range(len(pinjam_id)):
                if pinjam_status[i] == "Aktif":
                    aktif_indices = aktif_indices + [i]

            if not aktif_indices:
                print("  [!] Tidak ada peminjaman aktif saat ini.")
                tekan_enter()
            else:
                print("  " + beri_spasi_kanan("No", 4) + " " + beri_spasi_kanan("ID Pinjam", 10) + " " + beri_spasi_kanan("Nama Penyewa", 20) + " " + beri_spasi_kanan("Kendaraan (ID)", 17) + " " + "Total")
                garis("-", 70)

                for nomor, idx in enumerate(aktif_indices, start=1):
                    id_p  = format_id_p(pinjam_id[idx])
                    nama  = pinjam_nama[idx]
                    id_k  = format_id_k(pinjam_id_kendaraan[idx])
                    total = format_rupiah(pinjam_total[idx])
                    print("  " + beri_spasi_kanan(str(nomor), 4) + " " + beri_spasi_kanan(id_p, 10) + " " + beri_spasi_kanan(nama, 20) + " " + beri_spasi_kanan(id_k, 17) + " " + total)
                garis("-", 70)

                pilihan_kembali = input_angka("  >> Pilih nomor urut transaksi yang dikembalikan: ")

                if 1 <= pilihan_kembali <= len(aktif_indices):
                    idx        = aktif_indices[pilihan_kembali - 1]
                    konfirmasi = ubah_ke_kecil(hapus_spasi(input(f"  Yakin selesaikan transaksi {format_id_p(pinjam_id[idx])}? (y/n): ")))

                    if konfirmasi == "y":
                        sukses, pesan = proses_pengembalian(idx)
                        if sukses:   print(f"  [v] {pesan}")
                        else:        print(f"  [x] {pesan}")
                    else:
                        print("  [i] Pengembalian dibatalkan.")
                else:
                    print("  [!] Pilihan tidak valid.")
                tekan_enter()

        # ============================================================
        #   MENU 4 — RIWAYAT PEMINJAMAN
        # ============================================================
        elif pilihan == "4":
            lanjut_riwayat = True
            while lanjut_riwayat:
                print("\n  == RIWAYAT PEMINJAMAN ==")
                print("  1. Semua Riwayat")
                print("  2. Riwayat Aktif")
                print("  3. Riwayat Selesai")
                print("  0. Kembali")
                sub_pilih = hapus_spasi(input("  >> Pilih: "))

                if sub_pilih == "1":
                    tampilkan_tabel_peminjaman("semua")
                elif sub_pilih == "2":
                    tampilkan_tabel_peminjaman("Aktif")
                elif sub_pilih == "3":
                    tampilkan_tabel_peminjaman("Selesai")
                elif sub_pilih == "0":
                    lanjut_riwayat = False
                else:
                    print("  [!] Pilihan tidak valid.")
                tekan_enter()

        # ============================================================
        #   MENU 5 — CARI KENDARAAN
        # ============================================================
        elif pilihan == "5":
            print("\n  [ CARI KENDARAAN ]")
            keyword       = input_teks("  Masukkan nama/plat/jenis kendaraan: ")
            keyword_lower = ubah_ke_kecil(keyword)

            LEBAR = 70
            print()
            garis("=", LEBAR)
            print(f"  HASIL PENCARIAN UNTUK: '{keyword}'")
            garis("-", LEBAR)
            print("  " + beri_spasi_kanan("ID", 6) + "  " + beri_spasi_kanan("Nama", 20) + "  " + beri_spasi_kanan("Jenis", 7) + "  " + beri_spasi_kanan("Plat", 12) + "  " + "Harga/Hari".rjust(13) + "   Status")
            garis("-", LEBAR)

            ada_data = False
            for i in range(len(kendaraan_id)):
                if (keyword_lower in ubah_ke_kecil(kendaraan_nama[i]) or
                        keyword_lower in ubah_ke_kecil(kendaraan_plat[i]) or
                        keyword_lower in ubah_ke_kecil(kendaraan_jenis[i])):

                    id_str     = format_id_k(kendaraan_id[i])
                    nama_str   = kendaraan_nama[i]
                    jenis_str  = kendaraan_jenis[i]
                    plat_str   = kendaraan_plat[i]
                    harga_str  = format_rupiah(kendaraan_harga[i])
                    status_str = kendaraan_status[i]
                    tanda      = "[v]" if status_str == "Tersedia" else "[-]"

                    print("  " + beri_spasi_kanan(id_str, 6) + "  " + beri_spasi_kanan(nama_str, 20) + "  " + beri_spasi_kanan(jenis_str, 7) + "  " + beri_spasi_kanan(plat_str, 12) + "  " + harga_str.rjust(13) + "  " + tanda + " " + status_str)
                    ada_data = True

            if not ada_data:
                print(f"  (Tidak ada kendaraan yang cocok dengan kata kunci '{keyword}')")
            garis("=", LEBAR)
            tekan_enter()

        # ============================================================
        #   MENU 6 — LAPORAN & STATISTIK
        # ============================================================
        elif pilihan == "6":
            LEBAR = 70
            print()
            garis("=", LEBAR)
            print("  LAPORAN & STATISTIK SISTEM")
            garis("=", LEBAR)

            # --- Data Kendaraan ---
            total_kendaraan  = len(kendaraan_id)
            total_tersedia   = 0
            total_dipinjam_k = 0
            for i in range(len(kendaraan_status)):
                if kendaraan_status[i] == "Tersedia":
                    total_tersedia   = total_tersedia   + 1
                else:
                    total_dipinjam_k = total_dipinjam_k + 1

            print("\n  [ DATA KENDARAAN ]")
            garis("-", LEBAR)
            print(f"  Total Kendaraan       : {total_kendaraan} unit")
            print(f"  Kendaraan Tersedia    : {total_tersedia} unit")
            print(f"  Kendaraan Dipinjam    : {total_dipinjam_k} unit")

            # --- Rincian per jenis ---
            jenis_unik     = []
            jenis_jumlah   = []
            jenis_tersedia = []
            jenis_dipinjam = []

            for i in range(len(kendaraan_jenis)):
                jenis = kendaraan_jenis[i]
                idx   = -1
                for j in range(len(jenis_unik)):
                    if jenis_unik[j] == jenis:
                        idx = j

                if idx == -1:
                    jenis_unik     = jenis_unik     + [jenis]
                    jenis_jumlah   = jenis_jumlah   + [1]
                    if kendaraan_status[i] == "Tersedia":
                        jenis_tersedia = jenis_tersedia + [1]
                        jenis_dipinjam = jenis_dipinjam + [0]
                    else:
                        jenis_tersedia = jenis_tersedia + [0]
                        jenis_dipinjam = jenis_dipinjam + [1]
                else:
                    jenis_jumlah[idx] = jenis_jumlah[idx] + 1
                    if kendaraan_status[i] == "Tersedia":
                        jenis_tersedia[idx] = jenis_tersedia[idx] + 1
                    else:
                        jenis_dipinjam[idx] = jenis_dipinjam[idx] + 1

            print("\n  [ RINCIAN PER JENIS KENDARAAN ]")
            garis("-", LEBAR)
            if not jenis_unik:
                print("  (Belum ada data kendaraan.)")
            else:
                print("  " + beri_spasi_kanan("Jenis", 10) + beri_spasi_kanan("Total", 8) +
                      beri_spasi_kanan("Tersedia", 10) + "Dipinjam")
                garis("-", LEBAR)
                for i in range(len(jenis_unik)):
                    print("  " + beri_spasi_kanan(jenis_unik[i], 10) +
                          beri_spasi_kanan(str(jenis_jumlah[i]), 8) +
                          beri_spasi_kanan(str(jenis_tersedia[i]), 10) +
                          str(jenis_dipinjam[i]))

            # --- Transaksi ---
            jumlah_aktif   = 0
            jumlah_selesai = 0
            for i in range(len(pinjam_status)):
                if pinjam_status[i] == "Aktif":
                    jumlah_aktif   = jumlah_aktif   + 1
                else:
                    jumlah_selesai = jumlah_selesai + 1
            total_transaksi = jumlah_aktif + jumlah_selesai

            print("\n  [ TRANSAKSI PEMINJAMAN ]")
            garis("-", LEBAR)
            print(f"  Total Transaksi       : {total_transaksi} transaksi")
            print(f"  Transaksi Aktif       : {jumlah_aktif} transaksi")
            print(f"  Transaksi Selesai     : {jumlah_selesai} transaksi")

            # --- Pendapatan ---
            pendapatan_selesai = 0
            pendapatan_aktif   = 0
            for i in range(len(pinjam_id)):
                if pinjam_status[i] == "Selesai":
                    pendapatan_selesai = pendapatan_selesai + pinjam_total[i]
                else:
                    pendapatan_aktif   = pendapatan_aktif   + pinjam_total[i]
            total_pendapatan = pendapatan_selesai + pendapatan_aktif

            print("\n  [ PENDAPATAN ]")
            garis("-", LEBAR)
            print(f"  Pendapatan (Selesai)      : {format_rupiah(pendapatan_selesai)}")
            print(f"  Potensi Pendapatan (Aktif): {format_rupiah(pendapatan_aktif)}")
            print(f"  Total Keseluruhan         : {format_rupiah(total_pendapatan)}")

            # --- Kendaraan paling populer ---
            id_unik_pop = []
            jumlah_sewa = []

            for i in range(len(pinjam_id_kendaraan)):
                id_k = pinjam_id_kendaraan[i]
                idx  = -1
                for j in range(len(id_unik_pop)):
                    if id_unik_pop[j] == id_k:
                        idx = j
                if idx == -1:
                    id_unik_pop = id_unik_pop + [id_k]
                    jumlah_sewa = jumlah_sewa + [1]
                else:
                    jumlah_sewa[idx] = jumlah_sewa[idx] + 1

            print("\n  [ KENDARAAN PALING POPULER ]")
            garis("-", LEBAR)
            if not id_unik_pop:
                print("  (Belum ada data peminjaman.)")
            else:
                idx_max = 0
                for i in range(1, len(jumlah_sewa)):
                    if jumlah_sewa[i] > jumlah_sewa[idx_max]:
                        idx_max = i

                id_populer = id_unik_pop[idx_max]
                idx_k      = cari_idx_kendaraan(id_populer)
                if idx_k == -1:
                    print("  (Data kendaraan tidak ditemukan.)")
                else:
                    print(f"  ID          : {format_id_k(id_populer)}")
                    print(f"  Nama        : {kendaraan_nama[idx_k]}")
                    print(f"  Plat        : {kendaraan_plat[idx_k]}")
                    print(f"  Jenis       : {kendaraan_jenis[idx_k]}")
                    print(f"  Jumlah Sewa : {jumlah_sewa[idx_max]} kali")

            garis("=", LEBAR)
            tekan_enter()

        # ============================================================
        #   MENU 0 — KELUAR
        # ============================================================
        elif pilihan == "0":
            garis("=", 70)
            print("  Terima kasih telah menggunakan sistem ini. Sampai jumpa!")
            garis("=", 70)
            selesai = True

        else:
            print("  [!] Pilihan menu tidak valid.")


if __name__ == "__main__":
    main()
