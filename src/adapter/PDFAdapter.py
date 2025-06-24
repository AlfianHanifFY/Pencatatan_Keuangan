import fitz  # PyMuPDF


class PDFAdapter:

    @staticmethod
    def ToString(pdf_path):
        try:
            doc = fitz.open(pdf_path)
            all_text = ""
            for page in doc:
                all_text += page.get_text()
            return all_text
        except Exception as e:
            raise RuntimeError(f"Gagal membaca atau OCR PDF: {e}")
