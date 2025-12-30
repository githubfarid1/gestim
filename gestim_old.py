import re
from playwright.sync_api import Playwright, sync_playwright, expect
import requests
from PIL import Image
import pytesseract
import cv2
# import time
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
import gspread
from google.oauth2.service_account import Credentials
from gspread import Worksheet
from time import sleep as timesleep

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

# def get_ntp_time(server="pool.ntp.org"):
#     client = ntplib.NTPClient()
#     response = client.request(server, version=3)
#     return datetime.fromtimestamp(response.tx_time, tz=utc)

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

def run(playwright: Playwright, clickdate: str, clicktime: str, username: str, password: str, appnumber: int, sheet: Worksheet, autocancel: bool = False) -> None:
    selected_timezone = 'US/Eastern'
    PCNAME=os.environ.get("PCNAME")
    clickme = datetime(int(clickdate.split("-")[0]), int(clickdate.split("-")[1]), int(clickdate.split("-")[2]), int(clicktime.split(":")[0]), int(clicktime.split(":")[1]), int(clicktime.split(":")[2].split(".")[0]), int(clicktime.split(":")[2].split(".")[1]), tzinfo = tz.gettz(selected_timezone))
    starttocount = clickme - timedelta(seconds=UNTILSECOND)
    browser = playwright.chromium.launch(headless=False, slow_mo=1000)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://gestim.mines.gouv.qc.ca/MRN_GestimP_Presentation/ODM02101_login.aspx")
    # breakpoint()
    page.wait_for_selector("a#A1")
    page.get_by_role("link", name="English").click()
    # breakpoint()
    page.wait_for_timeout(2000)
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.locator("#tbCodeUtilisateur").click()
    print("Input username and password...", end="", flush=True)
    page.locator("#tbCodeUtilisateur").type(username, delay=100)
    page.locator("#tbMotPasse").click()
    page.locator("#tbMotPasse").type(password, delay=100)
    print("OK")
    captchaurl = f'https://gestim.mines.gouv.qc.ca/MRN_GestimP_Presentation/{page.locator("img#imgImageSecure").get_attribute("src")}'
    print("Downloading Captcha image...", end="", flush=True)
    download_png(url=captchaurl, filename="captcha.png")
    print("Guessing Captcha number...", end="", flush=True)
    captchanumber = read_captcha("captcha.png")
    page.wait_for_timeout(1000)
    # breakpoint()
    print(captchanumber)
    page.locator("#tbCodeSecurite").click()
    page.locator("#tbCodeSecurite").type(captchanumber, delay=100)
    print("Trying to login...", end="", flush=True)
    page.locator("#imgBoutonSoumettre").click()
    print("OK")
    # breakpoint()
    print("Accepting End User Licence Agreement...", end="", flush=True)
    page.locator("#imgBoutonAccepter").click()
    print("OK")
    page.get_by_role("link").filter(has_text=re.compile(r"^$")).nth(3).click()
    page.get_by_role("link", name="Requests").click()
    print("Trying to Input Application number...", end="", flush=True)
    page.locator("iframe[name=\"ifrPage1\"]").content_frame.locator("input[name=\"tbNoReq\"]").type(str(appnumber), delay=100)
    # page.locator("iframe[name=\"ifrPage1\"]").content_frame.locator("#imgRechercher").click()
    page.wait_for_timeout(2000)
    page.locator("iframe[name=\"ifrPage1\"]").content_frame.locator("input[name=\"tbNoReq\"]").press("Enter")
    page.locator("iframe[name=\"ifrPage1\"]").content_frame.get_by_role("link", name=str(appnumber)).click()
    print("OK")
    print("Validating form...", end="", flush=True)
    page.wait_for_timeout(2000)
    ischecked = page.locator("iframe[name=\"ifrPage1\"]").content_frame.locator("#cbDeclaration").get_attribute("checked")
    if ischecked != "checked":
        page.locator("iframe[name=\"ifrPage1\"]").content_frame.locator("#cbDeclaration").click()
            
    page.locator("iframe[name=\"ifrPage1\"]").content_frame.locator("#imgValider").click()
    print("OK")
    page.wait_for_timeout(3000)
    # frame = page.locator("iframe[name=\"ifrPage1\"]").content_frame
    # breakpoint()
    #d39d6a66-12ac-42b0-8d1c-a0ad6f77b08b
    print("Sleep until", starttocount.strftime("%m/%d/%Y, %H:%M:%S"), "...", end="", flush=True)
    buttonsubmit = page.locator("iframe[name=\"ifrPage1\"]").content_frame.locator("#btnImage")
    while True:
        gt = datetime.now(est)
        if gt.timestamp() > starttocount.timestamp():
            break
    print("OK")
    
    time_offset = 0
    
    while True:
        try:
            time_offset = get_sync_time(NTPSERVER)[1]
            if time_offset != 0:
                break
        except:
            print("time offset failed, try again")
            continue
    
    while True:
        gt = datetime.now(est)
        gt = gt + timedelta(seconds=time_offset)
        # print("Now:", gt.strftime("%H:%M:%S.%f"))
        if gt.timestamp() >= clickme.timestamp():
            break
        
        
        # current_time = get_ntp_time(server="time.nrc.ca")
        # if current_time >= clickme:
        #     break
    
    
    # print("Trying to click Submit button...", end="", flush=True)
    # print(time_offset)
    gt = datetime.now(est) + timedelta(seconds=time_offset)
    strtime = gt.strftime('%Y-%m-%d %H:%M:%S.%f')
    print("start click at", strtime)    

    buttonsubmit.click()
    gt = datetime.now(est) + timedelta(seconds=time_offset)
    strtime = gt.strftime('%Y-%m-%d %H:%M:%S.%f')
    result_time = page.locator("iframe[name=\"ifrPaiement1\"]").content_frame.locator("span#lblHeure").text_content().split(" ")[1]
    if autocancel:
        page.on("dialog", handle_dialog)
        page.locator("iframe[name=\"ifrPaiement1\"]").content_frame.locator("input#imgAnnuler").click()
    
    sheet.append_row([PCNAME, str(appnumber), clickdate, clicktime, str(time_offset), result_time])
    print("end click at", strtime)   
    print("OK")
    print("END")
    if autocancel:
        input("Press Enter to exit")
    else:
        input("Click  Checkout or Cancel")
        
        
    # ---------------------
    context.close()
    browser.close()


def main():
    parser = argparse.ArgumentParser(description="Cells Swapper")
    parser.add_argument('-u', '--username', type=str,help="Username")
    parser.add_argument('-p', '--password', type=str,help="Password")
    parser.add_argument('-d', '--date', type=str,help="Date Click")
    parser.add_argument('-t', '--time', type=str,help="Time Click")
    parser.add_argument('-a', '--appnumber', type=str,help="Application Number")
    parser.add_argument('-ac', '--autocancel', type=str,help="Autocancel")



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
    username = args.username
    password = args.password
    appnumber = args.appnumber
    autocancel = args.autocancel
    
    clickmestr = " ".join([clickdate, clicktime])
    print("______GESTIM MINING_______")
    # print("PASSED")
    # print(f"Script Instance: {args.name}")
    print(f"Username: {username}")
    print(f"Application Number: {appnumber}")
    print(f"Submit time execute: {clickmestr}")
    print()
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
        
    print("START")
    with sync_playwright() as playwright:
        run(playwright=playwright, clickdate=clickdate, clicktime=clicktime, username=username, password=password, appnumber=appnumber, sheet=sheet, autocancel=autocancel)

if __name__ == '__main__':
    main()