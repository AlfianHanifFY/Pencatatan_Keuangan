from PIL import Image, ImageEnhance
import pytesseract


class ImageAdapter:

    @staticmethod
    def ToString(path):
        try:
            image = Image.open(path)

            # === PREPROCESSING ===
            image = image.convert("L")  # Grayscale
            image = ImageEnhance.Contrast(image).enhance(2.0)  # Tingkatkan kontras
            image = image.point(lambda x: 0 if x < 160 else 255, "1")  # Thresholding
            image = image.resize((image.width * 2, image.height * 2))  # Perbesar gambar

            return pytesseract.image_to_string(image, config="--psm 6")
        except Exception as e:
            raise RuntimeError(f"Gagal membaca atau OCR gambar: {e}")
