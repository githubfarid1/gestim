from PIL import Image
import pytesseract

# Jika kamu pakai Windows, pastikan path ke tesseract.exe benar
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Buka gambar CAPTCHA
image = Image.open("captcha.png")  # Ganti dengan path ke file gambar kamu

# Konversi ke angka
text = pytesseract.image_to_string(image, config='--psm 8 -c tessedit_char_whitelist=0123456789')

# Bersihkan hasil
captcha_number = text.strip()
print("Angka dari CAPTCHA:", captcha_number)