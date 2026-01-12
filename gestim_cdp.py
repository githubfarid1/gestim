import re
from playwright.sync_api import Playwright, sync_playwright, expect
import requests
from PIL import Image
import pytesseract
import cv2
import sys
import argparse
from datetime import datetime, timedelta, date, time
from utils.rotation_logger import setup_logger
from pytz import timezone, utc
import os
from dateutil import tz
from dotenv import load_dotenv, dotenv_values
from utils.time_helper import get_sync_time, get_time_with_timezone_and_offset, \
    get_time_object_with_timezone_and_offset, get_current_day_with_timezone_and_offset, \
    run_by_time, get_request_time, get_time_from_params
import ntplib
import random
import gspread
from google.oauth2.service_account import Credentials
from gspread import Worksheet
from time import sleep as timesleep
from sys import platform
if platform == "win32":
    pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'

est = timezone("US/Eastern")
logger = setup_logger(__name__)
__version__ = '1.0'
logger.info(f'Gestim started at {datetime.now(est).strftime("%D %T")}. Version {__version__}')
load_dotenv()
UNTILSECOND = float(os.environ.get("UNTILSECOND"))
NTPSERVER = os.environ.get("NTPSERVER")
def read_captcha(filename):
    # Buka gambar CAPTCHA
    image = cv2.imread(filename)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresholded = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'
    
    text = pytesseract.image_to_string(thresholded, config=custom_config)

    # Bersihkan hasil
    captcha_number = text.strip()
    return captcha_number

def download_png(url, filename):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"OK")
    except requests.exceptions.RequestException as e:
        print(f"Failed: {e}")

def sleep_random_ms(min_ms, max_ms):
    # Convert milliseconds to seconds
    min_seconds = min_ms / 1000.0
    max_seconds = max_ms / 1000.0
    # Generate a random float between the min and max seconds
    sleep_time = random.uniform(min_seconds, max_seconds)
    timesleep(sleep_time)
    
def handle_dialog(dialog):
    timesleep(3)
    try:
        if dialog.type == "confirm":
            dialog.accept()   # klik OK
            # dialog.dismiss() # klik Cancel
        else:
            dialog.accept()
    except:
        breakpoint()

def run(playwright: Playwright, clickdate: str, clicktime: str, sheet: Worksheet, autocancel: bool = False, autoclose: bool = False, tabnumber: int = 1) -> None:
    selected_timezone = 'US/Eastern'
    PCNAME=os.environ.get("PCNAME")
    clickme = datetime(int(clickdate.split("-")[0]), int(clickdate.split("-")[1]), int(clickdate.split("-")[2]), int(clicktime.split(":")[0]), int(clicktime.split(":")[1]), int(clicktime.split(":")[2].split(".")[0]), int(clicktime.split(":")[2].split(".")[1]), tzinfo = tz.gettz(selected_timezone))
    starttocount = clickme - timedelta(seconds=UNTILSECOND)
    if os.environ.get("HEADLESS") == "yes":
        HEADLESS=True
    else:
        HEADLESS=False
        
    try:
        browser = playwright.chromium.connect_over_cdp(f"http://localhost:{tabnumber}")
        context = browser.contexts[0]
    except:
        input("Chrome has not opened yet")
        sys.exit()
    page = context.pages[0]
    clickmestr = " ".join([clickdate, clicktime])
    appnumber = page.locator("iframe[name=\"ifrPage1\"]").content_frame.locator("span#lblNoReqt").text_content()
    
    print("______GESTIM MINING_______")
    print(f"Tab Chrome : #{tabnumber}")
    print(f"Application Number: {appnumber}")
    print(f"Submit time execute: {clickmestr}")
    print()
        
    time_offset = 0
    while True:
        try:
            time_offset = get_sync_time(NTPSERVER)[1]
            if time_offset != 0:
                break
        except:
            print("time offset failed, try again")
            continue
    
    print("Sleep until", clickme.strftime("%Y-%m-%d, %H:%M:%S.%f"), "...", end="", flush=True)
    # breakpoint()
    buttonsubmit = page.locator("iframe[name=\"ifrPage1\"]").content_frame.locator("#btnImage")
    
    while True:
        gt = datetime.now(est)
        gt = gt + timedelta(seconds=time_offset)
        if gt.timestamp() >= clickme.timestamp():
            buttonsubmit.click()
            break

    result_time = page.locator("iframe[name=\"ifrPaiement1\"]").content_frame.locator("span#lblHeure").text_content().split(" ")[1]
    # breakpoint()
    if autocancel:
        page.on("dialog", handle_dialog)
        page.wait_for_timeout(2000)
        page.locator("iframe[name=\"ifrPaiement1\"]").content_frame.locator("input#imgAnnuler").click()
    print("END")
    print("Result time:", result_time)
    if not autoclose:
        if autocancel:
            input("Press Enter to save to Google Sheet and exit")
        else:
            input("Click  Checkout or Cancel and enter to save and exit")
        sheet.append_row([PCNAME, str(appnumber), clickdate, clicktime, str(time_offset), result_time])
    else:
        if autocancel:
            input("Press Enter to save to Google Sheet and exit")
        else:
            input("Press Enter to Exit from the Bot, then you can press Checkout or Cancel button")
        
        sleep_random_ms(100, 2000)
        sheet.append_row([PCNAME, str(appnumber), clickdate, clicktime, str(time_offset), result_time])
    # ---------------------
    context.close()
    browser.close()


def main():
    parser = argparse.ArgumentParser(description="Cells Swapper")
    parser.add_argument('-d', '--date', type=str,help="Date Click")
    parser.add_argument('-t', '--time', type=str,help="Time Click")
    parser.add_argument('-ac', '--autocancel', type=str,help="Autocancel")
    parser.add_argument('-ae', '--autoclose', type=str,help="Autoclose")
    parser.add_argument('-tb', '--tabnumber', type=str,help="Tab Number")



    args = parser.parse_args()
    try:
        date.fromisoformat(args.date)
    except ValueError:
        message = "Incorrect date format, should be YYYY-MM-DD"
        logger.exception(message)
        raise ValueError(message)
        
    try:
        time.fromisoformat(args.time)
    except ValueError:
        message = "Incorrect time format, should be HH:MM:SS.MS"
        logger.exception(message)
        raise ValueError(message)


    clear = lambda: os.system('cls')
    clear()
    # breakpoint()
    selected_timezone = 'US/Eastern'
    clickdate = args.date
    clicktime = args.time
    autocancel = args.autocancel
    autoclose = args.autoclose
    tabnumber = args.tabnumber    
    # 1. Tentukan scope (izin akses)
    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    WORKSHEETID=os.environ.get("WORKSHEETID")
    creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(WORKSHEETID).sheet1
    if autocancel == "Yes":
        autocancel = True
    else:
        autocancel = False
        
    if autoclose == "Yes":
        autoclose = True
    else:
        autoclose = False

    # print("START")
    with sync_playwright() as playwright:
        run(playwright=playwright, clickdate=clickdate, clicktime=clicktime,  sheet=sheet, autocancel=autocancel, autoclose=autoclose, tabnumber=tabnumber)

if __name__ == '__main__':
    main()