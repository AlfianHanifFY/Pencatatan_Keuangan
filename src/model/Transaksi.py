class Transaksi:
    def __init__(
        self, bukti: str, nominal: int = 0, tujuan: str = "", tanggal: str = ""
    ):
        self._bukti = bukti
        self._nominal = nominal
        self._tujuan = tujuan
        self._tanggal = tanggal

    # Getter dan Setter untuk bukti
    @property
    def bukti(self):
        return self._bukti

    @bukti.setter
    def bukti(self, value):
        self._bukti = value

    # Getter dan Setter untuk nominal
    @property
    def nominal(self):
        return self._nominal

    @nominal.setter
    def nominal(self, value):
        if not isinstance(value, int):
            raise ValueError("Nominal harus bertipe int")
        self._nominal = value

    # Getter dan Setter untuk tujuan
    @property
    def tujuan(self):
        return self._tujuan

    @tujuan.setter
    def tujuan(self, value):
        self._tujuan = value

    # Getter dan Setter untuk tanggal
    @property
    def tanggal(self):
        return self._tanggal

    @tanggal.setter
    def tanggal(self, value):
        self._tanggal = value

    def format_rupiah(self):
        return f"Rp{self.nominal:,.0f}".replace(",", ".")

    def __str__(self):
        return (
            "Transaksi:\n"
            f"Nominal : {self.format_rupiah() if self.nominal > 0 else 'Belum ditentukan'}\n"
            f"Tujuan  : {self.tujuan or 'Belum ditentukan'}\n"
            f"Tanggal : {self.tanggal or 'Belum ditentukan'}\n"
        )

    def to_dict(self):
        return {
            "bukti": self.bukti,
            "nominal": self.nominal,
            "tujuan": self.tujuan,
            "tanggal": self.tanggal,
        }
