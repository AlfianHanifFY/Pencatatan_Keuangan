from collections import defaultdict
from datetime import datetime
import os
from model.Transaksi import Transaksi
from adapter.ImageAdapter import ImageAdapter
from adapter.PDFAdapter import PDFAdapter
from extractor.extractor import Extractor


class TransaksiRepository:
    _instance = None

    def __new__(cls, data_folder="data"):
        if cls._instance is None:
            cls._instance = super(TransaksiRepository, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, data_folder="data"):
        if self._initialized:
            return
        self.data_folder = data_folder
        self.list_transaksi = []
        self._initialized = True

    def load_data(self):
        self.list_transaksi.clear()
        if not os.path.exists(self.data_folder):
            print(f"📁 Folder '{self.data_folder}' tidak ditemukan.")
            return

        for filename in os.listdir(self.data_folder):
            filepath = os.path.join(self.data_folder, filename)
            transaksi = None

            if filename.lower().endswith(".pdf"):
                try:
                    adapter = PDFAdapter(filepath)
                    text = adapter.to_string()
                    transaksi = Transaksi(bukti=text)
                    print(f"✅ PDF dimuat: {filename}")
                except Exception as e:
                    print(f"⚠️ Gagal memproses PDF {filename}: {e}")

            elif filename.lower().endswith((".png", ".jpg", ".jpeg")):
                try:
                    text = ImageAdapter.ToString(filepath)
                    transaksi = Transaksi(bukti=text)
                    print(f"✅ Gambar dimuat: {filename}")
                except Exception as e:
                    print(f"⚠️ Gagal memproses gambar {filename}: {e}")

            if transaksi:
                transaksi = Extractor.ekstrak(transaksi)
                self.list_transaksi.append(transaksi)

    def get_all(self):
        return self.list_transaksi

    def filter_per_bulan(self, bulan: int, tahun: int):
        hasil = []
        for transaksi in self.list_transaksi:
            if transaksi.tanggal:
                try:
                    dt = datetime.strptime(transaksi.tanggal, "%d-%m-%Y")
                    if dt.month == bulan and dt.year == tahun:
                        hasil.append(transaksi)
                except ValueError:
                    pass
        return hasil

    def analisis(self):
        total_semua = 0
        jumlah_transaksi = 0
        nominal_tertinggi = None
        nominal_terendah = None
        bulanan = defaultdict(int)
        jumlah_tidak_lengkap = 0
        list_tidak_lengkap = []
        for t in self.list_transaksi:
            incomplete = (
                t.nominal <= 0
                or not t.tujuan
                or not t.tanggal
                or not self._is_valid_date(t.tanggal)
            )
            if incomplete:
                jumlah_tidak_lengkap += 1
                list_tidak_lengkap.append(t)
                continue
            total_semua += t.nominal
            jumlah_transaksi += 1
            if nominal_tertinggi is None or t.nominal > nominal_tertinggi:
                nominal_tertinggi = t.nominal
            if nominal_terendah is None or t.nominal < nominal_terendah:
                nominal_terendah = t.nominal
            dt = datetime.strptime(t.tanggal, "%d-%m-%Y")
            key = dt.strftime("%Y-%m")
            bulanan[key] += t.nominal
        rata_rata = total_semua / jumlah_transaksi if jumlah_transaksi > 0 else 0
        bulanan = dict(bulanan)
        return {
            "total": total_semua,
            "jumlah": jumlah_transaksi,
            "rata_rata": rata_rata,
            "tertinggi": nominal_tertinggi or 0,
            "terendah": nominal_terendah or 0,
            "bulanan": bulanan,
            "tidak_lengkap": {
                "jumlah": jumlah_tidak_lengkap,
                "daftar": list_tidak_lengkap,
            },
        }

    @staticmethod
    def _is_valid_date(tanggal_str):
        try:
            datetime.strptime(tanggal_str, "%d-%m-%Y")
            return True
        except:
            return False
