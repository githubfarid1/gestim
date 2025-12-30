from utils.time_helper import get_sync_time, get_time_with_timezone_and_offset, \
    get_time_object_with_timezone_and_offset, get_current_day_with_timezone_and_offset, \
    run_by_time, get_request_time, get_time_from_params

from datetime import datetime, timedelta, date, time
from dateutil import tz
from pytz import timezone, utc
from pyautogui import click, displayMousePosition, typewrite, hotkey

est = timezone("US/Eastern")
clicktime = "07:43:59.461678"
315120
clickdate = "2025-12-16"
selected_timezone = 'US/Eastern'
clickme = datetime(int(clickdate.split("-")[0]), int(clickdate.split("-")[1]), int(clickdate.split("-")[2]), int(clicktime.split(":")[0]), int(clicktime.split(":")[1]), int(clicktime.split(":")[2].split(".")[0]), int(clicktime.split(":")[2].split(".")[1]), tzinfo = tz.gettz(selected_timezone))
# breakpoint()
starttocount = clickme - timedelta(seconds=2)

print("Sleep until", starttocount.strftime("%Y-%m-%d, %H:%M:%S"), "...", end="", flush=True)
while True:
    gt = datetime.now(est)
    # print(gt, starttocount)
    if gt.timestamp() > starttocount.timestamp():
        break
print("OK")

time_offset = 0
while True:
    try:
        time_offset = get_sync_time()[1]
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
        click(978, 815)
        break