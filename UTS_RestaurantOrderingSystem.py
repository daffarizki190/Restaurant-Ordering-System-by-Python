# Nama  : Daffa Rizki Ariyanto
# NIM   : 24130300001
# Kelas : Prog5
# UTS Fundamental Programming - Restaurant Ordering System

# ---- data menu restoran ----
daftar_menu = {
    "Makanan": [
        {"id": "M1", "nama": "Nasi Goreng Spesial", "harga": 35000},
        {"id": "M2", "nama": "Mie Goreng Seafood",  "harga": 32000},
        {"id": "M3", "nama": "Ayam Bakar Madu",     "harga": 45000},
        {"id": "M4", "nama": "Soto Ayam Lamongan",  "harga": 28000},
        {"id": "M5", "nama": "Gado-Gado Betawi",    "harga": 25000},
    ],
    "Minuman": [
        {"id": "D1", "nama": "Es Teh Manis",    "harga": 8000},
        {"id": "D2", "nama": "Es Jeruk Peras",  "harga": 12000},
        {"id": "D3", "nama": "Jus Alpukat",     "harga": 18000},
        {"id": "D4", "nama": "Air Mineral",     "harga": 5000},
        {"id": "D5", "nama": "Kopi Susu Aren",  "harga": 22000},
    ],
    "Dessert": [
        {"id": "P1", "nama": "Es Campur",           "harga": 20000},
        {"id": "P2", "nama": "Puding Cokelat",      "harga": 15000},
        {"id": "P3", "nama": "Pisang Goreng Keju",  "harga": 18000},
    ],
}

# pajak 10%
PAJAK = 0.10

# diskon berdasarkan total belanja (pakai tuple biar ga keubah)
DISKON = (
    (200000, 0.15),
    (100000, 0.10),
    (50000, 0.05),
)

# riwayat semua pesanan yang sudah dibayar
riwayat = []


# ---- fungsi bantu ----

def rupiah(angka):
    # format angka jadi Rp xxx.xxx
    return "Rp {:,.0f}".format(angka).replace(",", ".")


def cari_item(id_item):
    # cari item di semua kategori berdasarkan id
    id_item = id_item.upper()
    for kategori, items in daftar_menu.items():
        for item in items:
            if item["id"] == id_item:
                return item
    return None


def hitung_subtotal(keranjang):
    total = 0
    for item in keranjang:
        total += item["harga"] * item["qty"]
    return total


def cek_diskon(subtotal):
    for batas, persen in DISKON:
        if subtotal >= batas:
            return persen
    return 0


def hitung_total(keranjang):
    subtotal = hitung_subtotal(keranjang)
    diskon = subtotal * cek_diskon(subtotal)
    setelah_diskon = subtotal - diskon
    pajak = setelah_diskon * PAJAK
    return setelah_diskon + pajak


# ---- fungsi tampilkan ----

def tampilkan_menu():
    print("\n" + "="*50)
    print("         MENU RESTORAN NUSANTARA")
    print("="*50)
    for kategori, items in daftar_menu.items():
        print(f"\n  [{kategori}]")
        print(f"  {'ID':<5}  {'Nama':<25}  {'Harga':>10}")
        print("  " + "-"*44)
        for item in items:
            print(f"  {item['id']:<5}  {item['nama']:<25}  {rupiah(item['harga']):>10}")
    print("="*50)


def tampilkan_keranjang(keranjang, nama_pelanggan):
    print("\n" + "="*50)
    print(f"  Pesanan atas nama: {nama_pelanggan}")
    print("="*50)

    if len(keranjang) == 0:
        print("  Belum ada pesanan.")
        return

    print(f"  {'No':<4}  {'Item':<25}  {'Qty':>4}  {'Subtotal':>10}")
    print("  " + "-"*47)

    for i in range(len(keranjang)):
        item = keranjang[i]
        sub = item["harga"] * item["qty"]
        print(f"  {i+1:<4}  {item['nama']:<25}  {item['qty']:>4}  {rupiah(sub):>10}")

    subtotal = hitung_subtotal(keranjang)
    persen_diskon = cek_diskon(subtotal)

    print("  " + "-"*47)
    print(f"  Subtotal : {rupiah(subtotal)}")

    if persen_diskon > 0:
        print(f"  Diskon   : {int(persen_diskon * 100)}% (-{rupiah(subtotal * persen_diskon)})")

    print(f"  Pajak    : 10%")
    print(f"  TOTAL    : {rupiah(hitung_total(keranjang))}")
    print("="*50)


# ---- fungsi kelola keranjang ----

def tambah_pesanan(keranjang):
    tampilkan_menu()

    while True:
        id_input = input("\n  Masukkan ID menu (ketik 'batal' untuk keluar): ").strip()

        if id_input.lower() == "batal":
            break

        item = cari_item(id_input)

        if item == None:
            print(f"  Menu '{id_input}' tidak ditemukan, coba lagi.")
            continue

        # validasi jumlah
        while True:
            try:
                qty = int(input(f"  Berapa porsi '{item['nama']}'? "))
                if qty <= 0:
                    print("  Jumlah harus lebih dari 0.")
                    continue
                break
            except ValueError:
                print("  Input tidak valid, masukkan angka.")

        # kalau item sudah ada di keranjang, tambah qty nya aja
        sudah_ada = False
        for x in keranjang:
            if x["id"] == item["id"]:
                x["qty"] += qty
                sudah_ada = True
                print(f"  Qty '{item['nama']}' jadi {x['qty']}.")
                break

        if not sudah_ada:
            keranjang.append({
                "id": item["id"],
                "nama": item["nama"],
                "harga": item["harga"],
                "qty": qty,
            })
            print(f"  '{item['nama']}' x{qty} ditambahkan!")

        lagi = input("  Mau tambah lagi? (y/n): ").strip().lower()
        if lagi != "y":
            break


def ubah_qty(keranjang):
    if len(keranjang) == 0:
        print("  Keranjang kosong.")
        return

    tampilkan_keranjang(keranjang, "")

    while True:
        try:
            pilih = int(input("  Pilih nomor item yang mau diubah (0 = batal): "))
            if pilih == 0:
                return
            if pilih < 1 or pilih > len(keranjang):
                print(f"  Masukkan angka 1 sampai {len(keranjang)}.")
                continue
            break
        except ValueError:
            print("  Input tidak valid.")

    item = keranjang[pilih - 1]

    while True:
        try:
            qty_baru = int(input(f"  Qty baru untuk '{item['nama']}' (sekarang {item['qty']}): "))
            if qty_baru <= 0:
                print("  Qty minimal 1, kalau mau hapus pakai menu hapus.")
                continue
            item["qty"] = qty_baru
            print(f"  Berhasil diubah jadi {qty_baru}.")
            break
        except ValueError:
            print("  Input tidak valid.")


def hapus_item(keranjang):
    if len(keranjang) == 0:
        print("  Keranjang kosong.")
        return

    tampilkan_keranjang(keranjang, "")

    while True:
        try:
            pilih = int(input("  Pilih nomor item yang mau dihapus (0 = batal): "))
            if pilih == 0:
                return
            if pilih < 1 or pilih > len(keranjang):
                print(f"  Masukkan angka 1 sampai {len(keranjang)}.")
                continue
            break
        except ValueError:
            print("  Input tidak valid.")

    dihapus = keranjang.pop(pilih - 1)
    print(f"  '{dihapus['nama']}' dihapus dari pesanan.")


def bayar(keranjang, nama_pelanggan):
    if len(keranjang) == 0:
        print("  Keranjang masih kosong!")
        return False

    tampilkan_keranjang(keranjang, nama_pelanggan)
    total = hitung_total(keranjang)

    print(f"\n  Total yang harus dibayar: {rupiah(total)}")

    while True:
        try:
            bayaran = input("  Masukkan nominal pembayaran (0 = batal): Rp ").strip()

            if bayaran == "0":
                print("  Pembayaran dibatalkan.")
                return False

            bayaran = float(bayaran.replace(".", "").replace(",", ""))

            if bayaran < total:
                kurang = total - bayaran
                print(f"  Kurang {rupiah(kurang)}, coba lagi.")
                continue

            kembalian = bayaran - total
            print("\n" + "="*50)
            print(f"  Bayar     : {rupiah(bayaran)}")
            print(f"  Total     : {rupiah(total)}")
            print(f"  Kembalian : {rupiah(kembalian)}")
            print("="*50)
            print("  Pembayaran berhasil! Terima kasih :)")
            print("="*50)

            # simpan ke riwayat
            riwayat.append({
                "nama": nama_pelanggan,
                "total": total,
                "pesanan": list(keranjang),
            })

            return True

        except ValueError:
            print("  Input tidak valid, masukkan angka.")


def lihat_riwayat():
    print("\n" + "="*50)
    print("         RIWAYAT PESANAN")
    print("="*50)

    if len(riwayat) == 0:
        print("  Belum ada transaksi.")
        return

    for i in range(len(riwayat)):
        r = riwayat[i]
        print(f"\n  [{i+1}] {r['nama']} - {rupiah(r['total'])} ({len(r['pesanan'])} item)")

    print("="*50)


# ---- program utama ----

def main():
    print("="*50)
    print("   Selamat datang di Restoran Nusantara!")
    print("="*50)

    nama = ""
    while nama == "":
        nama = input("  Nama kamu: ").strip()
        if nama == "":
            print("  Nama tidak boleh kosong.")

    print(f"\n  Halo {nama}! Silakan pesan makanan/minuman.\n")

    keranjang = []

    while True:
        print("\n" + "-"*50)
        if len(keranjang) > 0:
            print(f"  Keranjang: {len(keranjang)} item | Total: {rupiah(hitung_total(keranjang))}")
        print("  [1] Lihat Menu")
        print("  [2] Tambah Pesanan")
        print("  [3] Lihat Keranjang")
        print("  [4] Ubah Jumlah Item")
        print("  [5] Hapus Item")
        print("  [6] Bayar")
        print("  [7] Riwayat Pesanan")
        print("  [0] Keluar")
        print("-"*50)

        pilihan = input("  Pilih: ").strip()

        if pilihan == "1":
            tampilkan_menu()

        elif pilihan == "2":
            tambah_pesanan(keranjang)

        elif pilihan == "3":
            tampilkan_keranjang(keranjang, nama)

        elif pilihan == "4":
            ubah_qty(keranjang)

        elif pilihan == "5":
            hapus_item(keranjang)

        elif pilihan == "6":
            sukses = bayar(keranjang, nama)
            if sukses:
                keranjang.clear()
                lagi = input("\n  Mau pesan lagi? (y/n): ").strip().lower()
                if lagi == "y":
                    nama = ""
                    while nama == "":
                        nama = input("  Nama pelanggan baru: ").strip()
                        if nama == "":
                            print("  Nama tidak boleh kosong.")
                    print(f"  Halo {nama}!")

        elif pilihan == "7":
            lihat_riwayat()

        elif pilihan == "0":
            print("\n  Sampai jumpa!")
            break

        else:
            print("  Pilihan tidak valid.")


main()
