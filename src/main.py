from repository.TransaksiRepository import TransaksiRepository
from datetime import datetime
import os


def clear_screen():
    """Clear terminal screen"""
    os.system("cls" if os.name == "nt" else "clear")


def print_header():
    """Print simple header"""
    clear_screen()
    print()
    print("=" * 60)
    print("APLIKASI PENCATATAN KEUANGAN".center(60))
    print("=" * 60)
    print()


def show_menu():
    """Display clean menu"""
    print()
    print("MENU UTAMA")
    print("-" * 20)
    print()
    print("  1. Lihat semua transaksi")
    print("  2. Statistik transaksi")
    print("  3. Filter transaksi per bulan")
    print("  4. Keluar")
    print()

    return input("Pilih menu (1-4): ")


def tampilkan_transaksi(transaksi_list, judul="Transaksi"):
    """Helper function untuk menampilkan daftar transaksi dengan tampilan bersih"""
    print()
    print(f"{judul.upper()}")
    print("=" * 50)

    if transaksi_list:
        print()
        print(f"{'No':<4} {'Nominal':<20} {'Tujuan':<20} {'Tanggal':<12}")
        print("-" * 60)

        for i, t in enumerate(transaksi_list, 1):
            nominal_str = f"Rp{t.nominal:,}".replace(",", ".") if t.nominal > 0 else "-"
            tujuan_str = (
                (t.tujuan[:17] + "...")
                if t.tujuan and len(t.tujuan) > 20
                else (t.tujuan or "-")
            )
            tanggal_str = t.tanggal or "-"

            print(f"{i:<4} {nominal_str:<20} {tujuan_str:<20} {tanggal_str:<12}")

        print("-" * 60)

        total = sum(t.nominal for t in transaksi_list if t.nominal > 0)
        print()
        print(f"TOTAL: Rp{total:,}".replace(",", "."))

    else:
        print()
        print(f"Tidak ada {judul.lower()}.")

    print()


def tampilkan_statistik(repo):
    """Menampilkan statistik transaksi"""
    print_header()

    data = repo.analisis()

    # Statistik umum transaksi valid
    if data["jumlah"] == 0:
        print("Tidak ada transaksi valid.\n")
    else:
        print("STATISTIK UMUM")
        print("=" * 30)
        print()
        print(f"Total Transaksi   : {data['jumlah']:,}")
        print(f"Total Nominal     : Rp{data['total']:,}".replace(",", "."))
        print(f"Rata-rata         : Rp{data['rata_rata']:,.0f}".replace(",", "."))
        print(f"Tertinggi         : Rp{data['tertinggi']:,}".replace(",", "."))
        print(f"Terendah          : Rp{data['terendah']:,}".replace(",", "."))
        print()

    # Statistik bulanan
    if data["bulanan"]:
        print("BREAKDOWN BULANAN")
        print("=" * 30)
        print()
        for bulan, total in sorted(data["bulanan"].items()):
            total_formatted = f"Rp{total:,}".replace(",", ".")
            print(f"  {bulan} : {total_formatted}")
        print()

    # Statistik transaksi tidak lengkap
    jumlah_tidak_lengkap = data.get("tidak_lengkap", {}).get("jumlah", 0)
    daftar_tidak_lengkap = data.get("tidak_lengkap", {}).get("daftar", [])

    if jumlah_tidak_lengkap > 0:
        print("TRANSAKSI TIDAK LENGKAP")
        print("=" * 30)
        print(f"Total Tidak Lengkap : {jumlah_tidak_lengkap}")
        print()
        print(f"{'No':<4} {'Nominal':<20} {'Tujuan':<20} {'Tanggal':<12}")
        print("-" * 60)

        for i, t in enumerate(daftar_tidak_lengkap, 1):
            nominal_str = f"Rp{t.nominal:,}".replace(",", ".") if t.nominal > 0 else "-"
            tujuan_str = (
                (t.tujuan[:17] + "...")
                if t.tujuan and len(t.tujuan) > 20
                else (t.tujuan or "-")
            )
            tanggal_str = t.tanggal or "-"
            print(f"{i:<4} {nominal_str:<20} {tujuan_str:<20} {tanggal_str:<12}")

        print()


def filter_per_bulan(repo):
    """Filter dan tampilkan transaksi per bulan"""
    try:
        print()
        print("FILTER TRANSAKSI PER BULAN")
        print("=" * 35)
        print()

        bulan = int(input("Masukkan bulan (1-12): "))
        tahun = int(input("Masukkan tahun (contoh: 2024): "))

        if bulan < 1 or bulan > 12:
            print("\nBulan harus antara 1-12.\n")
            return

        print("\nMencari data...")

        hasil = repo.filter_per_bulan(bulan, tahun)

        clear_screen()
        print_header()

        nama_bulan = [
            "",
            "Januari",
            "Februari",
            "Maret",
            "April",
            "Mei",
            "Juni",
            "Juli",
            "Agustus",
            "September",
            "Oktober",
            "November",
            "Desember",
        ][bulan]

        tampilkan_transaksi(hasil, f"Transaksi {nama_bulan} {tahun}")

    except ValueError:
        print("\nInput tidak valid. Harap masukkan angka.\n")


def print_goodbye():
    """Print goodbye message"""
    clear_screen()
    print()
    print("=" * 50)
    print("TERIMA KASIH".center(50))
    print("Sampai jumpa lagi!".center(50))
    print("=" * 50)
    print()


def run():
    print_header()
    print("Memulai aplikasi...")
    repo = TransaksiRepository()
    print("Memuat data transaksi...")
    repo.load_data()
    total_transaksi = len(repo.get_all())
    if total_transaksi > 0:
        print(f"Berhasil memuat {total_transaksi} transaksi")
    else:
        print("\nPERINGATAN")
        print("-" * 15)
        print("Tidak ada data transaksi.")
        print("Pastikan folder 'data' berisi file PDF atau gambar.\n")
        input("Tekan Enter untuk keluar...")
        return
    while True:
        try:
            pilihan = show_menu()
            if pilihan == "1":
                clear_screen()
                print_header()
                semua = repo.get_all()
                tampilkan_transaksi(semua, "Semua Transaksi")
            elif pilihan == "2":
                tampilkan_statistik(repo)
            elif pilihan == "3":
                clear_screen()
                print_header()
                filter_per_bulan(repo)
            elif pilihan == "4":
                print_goodbye()
                break
            else:
                print("\nPilihan tidak valid. Silakan coba lagi.\n")
            if pilihan in ["1", "2", "3"]:
                input("Tekan Enter untuk kembali ke menu...")
                clear_screen()
                print_header()

        except KeyboardInterrupt:
            clear_screen()
            print("\nAplikasi dihentikan oleh pengguna. Sampai jumpa!\n")
            break
        except Exception as e:
            print(f"\nTerjadi kesalahan: {str(e)}\n")
            input("Tekan Enter untuk melanjutkan...")


if __name__ == "__main__":
    run()
