from pyautogui import click, displayMousePosition, typewrite, hotkey, screenshot
from PIL import Image
import time
import requests
import sys

time.sleep(5)
CHAT_ID = "-1002473045324"
TOKEN = "7653970386:AAGNMh14sHuptG2fIaQQKqWlvZf49QiThfg"
url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"

# Kirim gambar

while True:
    click(67, 74)
    time.sleep(5)
    ss = screenshot(region=(1674, 110, 60, 53))
    ss.save("bell.png")

    img = Image.open("bell.png")

    # Konversi ke RGB
    pixels = img.convert("RGB").getdata()

    # Flag untuk cek apakah ada merah
    contains_red = False

    for r, g, b in pixels:
        # Syarat sederhana: nilai R lebih dominan dibanding G dan B
        if r > 150 and r > g + 50 and r > b + 50:
            contains_red = True
            break
    if contains_red:
        click( 1704, 137)
        time.sleep(0.5)
        IMAGE_PATH = "notification.png"
        ss = screenshot(imageFilename=IMAGE_PATH, region=(1340, 169, 402, 293))
        
        with open(IMAGE_PATH, "rb") as img:
            payload = {"chat_id": CHAT_ID}
            files = {"photo": img}
            response = requests.post(url, data=payload, files=files)
        
        print("Ada pesan baru")
    else:
        print("Kosong")
    time.sleep(120)