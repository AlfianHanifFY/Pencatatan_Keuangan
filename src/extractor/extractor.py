import re
from model.Transaksi import Transaksi


class Extractor:
    @staticmethod
    def ekstrak(transaksi: Transaksi) -> Transaksi:
        text = transaksi.bukti

        # === 1. Ekstrak Nominal ===
        nominal_match = re.search(
            r"(?:Rp\.?|IDR)[\s]*([0-9a-zA-Z.,]+)", text, re.IGNORECASE
        )
        if nominal_match:
            raw = nominal_match.group(1).strip()

            # Ganti karakter OCR salah seperti 'd' → '0'
            cleaned = re.sub(r"[^0-9.,]", "0", raw)

            # Hapus akhiran desimal .xx atau ,xx (jika tepat 2 digit)
            cleaned = re.sub(r"[.,](\d{2})$", "", cleaned)

            # Hapus semua titik dan koma pemisah ribuan
            cleaned_int = re.sub(r"[.,]", "", cleaned)

            try:
                transaksi.nominal = int(cleaned_int)
            except ValueError:
                pass

        # === 2. Ekstrak dan Normalisasi Tanggal ===
        bulan_map = {
            # Bahasa Indonesia (lengkap)
            "januari": 1,
            "februari": 2,
            "maret": 3,
            "april": 4,
            "mei": 5,
            "juni": 6,
            "juli": 7,
            "agustus": 8,
            "september": 9,
            "oktober": 10,
            "november": 11,
            "desember": 12,
            # Bahasa Indonesia (singkatan)
            "jan": 1,
            "feb": 2,
            "mar": 3,
            "apr": 4,
            "mei": 5,
            "jun": 6,
            "jul": 7,
            "agu": 8,
            "sep": 9,
            "okt": 10,
            "nov": 11,
            "des": 12,
            # Bahasa Inggris (singkatan)
            "may": 5,
            "aug": 8,
            "oct": 10,
            "dec": 12,
        }

        # Format: 20 Mei 2024
        date_match = re.search(r"\b(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})", text)
        if date_match:
            day, month_str, year = date_match.groups()
            month_str = month_str.lower()
            if month_str in bulan_map:
                day_int = int(day)
                month_int = bulan_map[month_str]
                year_int = int(year)
                transaksi.tanggal = f"{day_int}-{month_int}-{year_int}"
        else:
            # Fallback: 20/05/2024 atau 20-05-2024
            fallback = re.search(r"\b(\d{1,2})[/-](\d{1,2})[/-](\d{4})", text)
            if fallback:
                d, m, y = fallback.groups()
                transaksi.tanggal = f"{int(d)}-{int(m)}-{int(y)}"

        # === 3. Ekstrak Tujuan ===
        tujuan = ""
        tujuan_patterns = [
            r"(?:Penerima|Ke|Pembayaran Ke|Merchant(?: Name)?)[\s:\-]+([A-Z][A-Za-z0-9 .,&'-]+)",
            r"(?<=\n)([A-Z][A-Z ]{3,})\n(?:Citibank|Bank|Rekening|[A-Z])",
        ]
        for pattern in tujuan_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                tujuan = match.group(1).strip()
                break
        if tujuan:
            transaksi.tujuan = tujuan

        return transaksi
