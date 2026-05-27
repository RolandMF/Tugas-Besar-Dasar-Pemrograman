# ============================================================
#        SISTEM MANAGEMENT PEMINJAMAN KENDARAAN 
#        Mata Kuliah : Dasar Pemrograman
# ============================================================
# File : TugasBesarDaspro.py 
# Penulis : - Steven Theodore Alden ( 2572015 )
#           - Roland Michael Febrian ( 2572017 )
#           - Gabrielle Sebastien De Fretes ( 2572054 )
# Tujuan Program : Sistem Peminjaman Kendaraan
# Kamus Data  :


def main():
    
    print("="*60)
    print("     SELAMAT DATANG DI SISTEM RENTAL KENDARAAN")
    print("="*60)

    while True:
        print("=== MENU UTAMA ===")
        print("1. Manajemen Data Kendaraan")
        print("2. Transaksi Pinjam Kendaraan")
        print("3. Transaksi Kembalikan Kendaraan")
        print("4. Lihat Riwayat Peminjaman")
        print("5. Laporan Statistik Sederhana")
        print("0. Keluar")
        
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

if __name__ == '__main__':    
    main()   
