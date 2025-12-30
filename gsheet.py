# import gspread
from gspread import Worksheet, authorize
from google.oauth2.service_account import Credentials

# 1. Tentukan scope (izin akses)
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# 2. Load credentials dari file JSON (service account)
creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)

# 3. Autentikasi dengan gspread
client = authorize(creds)

# 4. Buka Google Sheet berdasarkan nama atau ID
# Gunakan ID sheet dari URL: https://docs.google.com/spreadsheets/d/<SHEET_ID>/edit
sheet = client.open_by_key("1uwl_RQN2h80QINlnpyNUjJFaFXvpnQ0qNVR4TGZi3OE").sheet1
cell_list = sheet.findall("Abicus")
rowlist = []
for cell in cell_list:
    rowlist.append(sheet.row_values(cell.row))
rowlist = rowlist[-5:]
totadjust = 0
for idx, row in enumerate(rowlist):
    submit1= str(row[3])[6:].replace('00.', '60.')
    submit2 = str(row[5])[6:].replace('00.', '60.')
    adjust = round(float(submit1) + round(60-float(submit2),6)-60,6)
    totadjust += adjust
    # list(rowlist[idx]).append(adjust)
    # print(float(submit2)-60)
result = round(totadjust/len(rowlist),6)
# breakpoint()
# 5. Insert data (contoh: append row)
# data = ["2025-12-20", "Mohamad", "Backend Automation", "Success"]
# sheet.append_row(data)

print("Data berhasil ditambahkan ke Google Sheet!")