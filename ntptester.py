from utils.time_helper import get_sync_time
import time
ntplist = ["ca.pool.ntp.org", "time.nrc.ca", "0.ca.pool.ntp.org", "id.pool.ntp.org"]
while True:
    time.sleep(2)
    for ntp in ntplist:
        try:
            time_offset = get_sync_time(ntp)[1]
            if time_offset != 0:
                print(ntp, ": ", time_offset)
        except:
            print("time offset failed, try again")

