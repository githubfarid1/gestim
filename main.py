from tkinter import *
from tkinter import ttk, messagebox
from functools import partial
from tkinter import filedialog
from tkinter import messagebox
import tkinter
from tkcalendar import Calendar, DateEntry
from pathlib import Path
import os
import sys
from sys import platform
from subprocess import Popen, check_call
# import git
import warnings
import shutil
from dotenv import load_dotenv, dotenv_values
from datetime import datetime, timedelta, date, time
from pathlib import Path
from time import strftime, sleep
from pytz import timezone, utc
from gspread import Worksheet, authorize
from google.oauth2.service_account import Credentials

warnings.filterwarnings("ignore", category=UserWarning)
if platform == "linux" or platform == "linux2":
    pass
elif platform == "win32":
	from subprocess import CREATE_NEW_CONSOLE
import json
load_dotenv()
VERSION = "1.0"
OWNER = ""

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)

client = authorize(creds)

sheet = client.open_by_key(os.environ.get("WORKSHEETID")).sheet1

def run_module(comlist):
	if platform == "linux" or platform == "linux2":
		comlist[:0] = ["--"]
		comlist[:0] = ["gnome-terminal"]
		# print(comlist)
		Popen(comlist)
	elif platform == "win32":
		Popen(comlist, creationflags=CREATE_NEW_CONSOLE)
	
	comall = ''
	for idx, com in enumerate(comlist):
		# breakpoint()
		if idx < 2:
			comall += com + " "
			continue
		if com[0] != '-':
			comall += f'"{com}" '
		else:
			comall += com + " "
	print(comall)

def main():
	window = Window()
	window.mainloop()

def remove_files(files=[]):
	for file in files:
		if os.path.exists(file):
			os.remove(file)

class Window(Tk):
	def update_time(self):
		est = timezone("US/Eastern")
		now = datetime.now(tz=est)
		string_time = now.strftime('%H:%M:%S %p -- %Y-%m-%d ')
		self.digital_clock.config(text=string_time)
		self.digital_clock.after(1000, self.update_time)
    
	def __init__(self) -> None:
		super().__init__()
		
		self.title(f'{OWNER} {VERSION}')
		# self.resizable(0, 0)
		self.grid_propagate(False)
		width = 750
		height = 550
		swidth = self.winfo_screenwidth()
		sheight = self.winfo_screenheight()
		newx = int((swidth/2) - (width/2))
		newy = int((sheight/2) - (height/2))
		self.geometry(f"{width}x{height}+{newx}+{newy}")
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, weight=1)
		# self.columnconfigure(3, weight=1)

		self.rowconfigure(0, weight=1)
		
		exitButton = ttk.Button(self, text="Exit", command=lambda:self.procexit())
		self.digital_clock = Label(self, font=('calibri', 16, 'bold'))
		
		exitButton.grid(row=2, column=3, sticky=(W), padx=20, pady=5)
		self.digital_clock.grid(row=2, column=0, sticky=(W), padx=20, pady=5)


		mainFrame = MainFrame(self)
		mainFrame.grid(column=0, row=0, sticky=(N, E, W, S), columnspan=4)
		self.update_time()

	def procexit(self):
		try:
			for p in Path(".").glob("__tmp*"):
				p.unlink()
		except:
			pass
		sys.exit()

class MainFrame(ttk.Frame):

	def __init__(self, window) -> None:
		super().__init__(window)
		
		framestyle = ttk.Style()
		framestyle.configure('TFrame', background='#C1C1CD')
		self.config(padding="20 20 20 20", borderwidth=1, relief='groove', style='TFrame')
		
		# self.place(anchor=CENTER)
		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.rowconfigure(3, weight=1)
		self.rowconfigure(4, weight=1)
		self.rowconfigure(5, weight=1)
		self.rowconfigure(6, weight=1)
		self.rowconfigure(7, weight=1)
		self.rowconfigure(8, weight=1)
		self.rowconfigure(9, weight=1)
		self.rowconfigure(10, weight=1)
		
		titleLabel = TitleLabel(self, 'Main Menu')
		gestim1Button = FrameButton(self, window, text="Gestim Mines Submit", class_frame=Gestim1Frame)
		gestim2Button = FrameButton(self, window, text="Gestim Mines Submit (Remote)", class_frame=Gestim2Frame)

		# layout
		titleLabel.grid(column = 0, row = 0, sticky=(W, E, N, S), padx=15, pady=5, columnspan=4)
		gestim1Button.grid(column = 0, row = 1, sticky=(W, E, N, S), padx=15, pady=5)
		gestim2Button.grid(column = 0, row = 2, sticky=(W, E, N, S), padx=15, pady=5)
  
class TitleLabel(ttk.Label):
	def __init__(self, parent, text):
		super().__init__(parent)
		font_tuple = ("Comic Sans MS", 20, "bold")
		self.config(text=text, font=font_tuple, anchor="center")

class FrameButton(ttk.Button):
	def __init__(self, parent, window, **kwargs):
		super().__init__(parent)
		# object attributes
		self.text = kwargs['text']
		# configure
		self.config(text = self.text, command = lambda : kwargs['class_frame'](window))

class Gestim1Frame(ttk.Frame):
   
	def __init__(self, window) -> None:
		target_timezone = timezone('America/New_York')
		utc_now = datetime.now(utc)
		target_time = utc_now.astimezone(target_timezone)
		
		super().__init__(window)
		self.grid(column=0, row=0, sticky=(N, E, W, S), columnspan=4)
		self.config(padding="20 20 20 20", borderwidth=1, relief='groove')
		self.columnconfigure(0, weight=1)

		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.rowconfigure(3, weight=1)
		self.rowconfigure(4, weight=1)
		self.rowconfigure(5, weight=1)
		self.rowconfigure(6, weight=1)
		self.rowconfigure(7, weight=1)
		self.rowconfigure(8, weight=1)
		self.rowconfigure(9, weight=1)
		self.rowconfigure(10, weight=1)


		# populate
		titleLabel = TitleLabel(self, text="Gestim Mines Submit")
		self.digital_timer = Label(self, font=('calibri', 16, 'bold'))
		closeButton = CloseButton(self)
  
		labelappnumber = Label(self, text="App. Number:")
		textappnumber = Entry(self, width=80)
		labeldate = Label(self, text="Date:")
		textdate = DateEntry(self, width= 77, date_pattern='yyy-mm-dd')
		labeltime = Label(self, text="Submit Time:")
		texttime = Entry(self, width=80)
		labeluser = Label(self, text="Username:")
		textuser = Entry(self, width=80)
		labelpass = Label(self, text="Password:")
		textpass = Entry(self, width=80)
		labelcancel = Label(self, text="Auto Cancel:")
		options = ["Yes", "No"]
		combocancel = ttk.Combobox(self, values=options, state="readonly", width=78)
		combocancel.set("Yes")
		labeltarget = Label(self, text="Target Time:")
		texttarget = TimeEntry(self)
		labelestime = Label(self, text="Estimate Time:")
		textestime = Text(self, width=60, height=4)

		runButton = ttk.Button(self, text='Run Process', command = lambda:self.run_process(appnumber=textappnumber, date=textdate, time=texttime, user=textuser, password=textpass, autocancel=combocancel))
		titleLabel.grid(column = 0, row = 0, sticky = (W, E, N, S))
		estButton = ttk.Button(self, text='Estimate', command = lambda:self.estimation(target_time=texttarget, estime=textestime, submit_time=texttime))
		resButton = ttk.Button(self, text='Reset Gsheet', command = lambda:self.reset())
		
		labeluser.grid(column = 0, row = 1, sticky=(W))
		textuser.grid(column=0, row=1)
		labelpass.grid(column = 0, row = 2, sticky=(W))
		textpass.grid(column=0, row=2)

		labeldate.grid(column = 0, row = 3, sticky=(W))
		textdate.grid(column=0, row=3)
		labeltime.grid(column = 0, row = 5, sticky=(W))
		texttime.grid(column=0, row=5)
		# texttime.insert(0, os.environ.get("CLICKTIME"))
		textuser.insert(0, os.environ.get("USER"))
		textpass.insert(0, os.environ.get("PASSWORD"))
		textdate.set_date(target_time.date())
		
		# 
		labelappnumber.grid(column = 0, row = 6, sticky=(W))
		textappnumber.grid(column=0, row=6)
		runButton.grid(column = 0, row = 5, sticky = (E))
		estButton.grid(column = 0, row = 4, sticky = (E))
		resButton.grid(column = 0, row = 3, sticky = (E))
		closeButton.grid(column = 0, row = 11, sticky = (E))
		labelcancel.grid(column = 0, row = 7, sticky=(W))
		combocancel.grid(column = 0, row = 7)
		labelestime.grid(column = 0, row = 8, sticky=(W))
		textestime.grid(column=0, row=8)
		labeltarget.grid(column=0, row=4, sticky=(W))
		texttarget.grid(column=0, row=4)
		
	def run_process(self, **kwargs):
		try:
			date.fromisoformat(kwargs['date'].get())
		except ValueError:
			raise ValueError("Incorrect date format, should be YYYY-MM-DD")
		try:
			time.fromisoformat(kwargs['time'].get())
		except ValueError:
			raise ValueError("Incorrect time format, should be HH:MM:SS.MS")

		comlist = [PYLOC, "gestim.py", "-d", kwargs['date'].get(), "-t", kwargs['time'].get(), "-a", kwargs['appnumber'].get(), "-u", kwargs['user'].get(), "-p", kwargs['password'].get(), "-ac", kwargs['autocancel'].get()]
		if os.path.exists("gestim.exe"):
			comlist = [PYLOC, "-d", kwargs['date'].get(), "-t", kwargs['time'].get(), "-a", kwargs['appnumber'].get(), "-u", kwargs['user'].get(), "-p", kwargs['password'].get(), "-ac", kwargs['autocancel'].get()]
		run_module(comlist=comlist)

	def reset(self, **kwargs):
		data = sheet.findall(os.environ.get("PCNAME"))
		for dt in data:
			sheet.delete_rows(dt.row)
		messagebox.showinfo(title='Info', message=f'Data with PCNAME {os.environ.get("PCNAME")} deleted')
  
	def estimation(self, **kwargs):
		PCNAME = os.environ.get("PCNAME")
		cell_list = sheet.findall(PCNAME)
		# breakpoint()
		kwargs['submit_time'].delete(0, 30)
		target_time_str = f"{kwargs['target_time'].hourstr.get().zfill(2)}:{kwargs['target_time'].minstr.get().zfill(2)}:{kwargs['target_time'].secstr.get().zfill(2)}.000000"
		rowlist = []
		for cell in cell_list:
			rowlist.append(sheet.row_values(cell.row))

		if len(rowlist) >= 1:
			# target_time_str = kwargs['time'].get()
			actual_request_str = rowlist[-1][3]
			actual_execution_str = rowlist[-1][5]
			target_time = datetime.strptime(target_time_str, "%H:%M:%S.%f")
			actual_request = datetime.strptime(actual_request_str, "%H:%M:%S.%f")
			actual_execution = datetime.strptime(actual_execution_str, "%H:%M:%S.%f")      
			offset = (actual_execution - actual_request).total_seconds()
			request_time = target_time - timedelta(seconds=offset)
			request_time_str = request_time.strftime("%H:%M:%S.%f")
			kwargs['estime'].delete("1.0", END)
			kwargs['estime'].insert("1.0", request_time_str+"\n")


			rowlist = rowlist[-5:]
			totaloffset = 0
			for idx, row in enumerate(rowlist):
				actual_request_str = row[3]
				actual_execution_str = row[5]
				actual_request = datetime.strptime(actual_request_str, "%H:%M:%S.%f")
				actual_execution = datetime.strptime(actual_execution_str, "%H:%M:%S.%f")      
				offset = (actual_execution - actual_request).total_seconds()
				totaloffset += offset
			avoffset = round(totaloffset/len(rowlist),6)
			target_time = datetime.strptime(target_time_str, "%H:%M:%S.%f")
			request_time = target_time - timedelta(seconds=avoffset)
			request_time_str = request_time.strftime("%H:%M:%S.%f")
			# est1_time = request_time - timedelta(seconds=avoffset)
			kwargs['estime'].insert("2.0", request_time_str + "\n" )
			messagebox.showinfo(title='Info', message=f'Estimate process Finished..')
			# kwargs['estime'].insert("3.0", est1_time.strftime("%H:%M:%S.%f") + "\n" )
		else:
			# target_time_str = kwargs['time'].get()
			target_time = datetime.strptime(target_time_str, "%H:%M:%S.%f")
			request_time = target_time - timedelta(seconds=0.5)
			kwargs['estime'].delete("1.0", END)
			kwargs['estime'].insert("1.0", request_time.strftime("%H:%M:%S.%f") + "\n")

class Gestim2Frame(ttk.Frame):
   
	def __init__(self, window) -> None:
		target_timezone = timezone('America/New_York')
		utc_now = datetime.now(utc)
		target_time = utc_now.astimezone(target_timezone)
		
		super().__init__(window)
		self.grid(column=0, row=0, sticky=(N, E, W, S), columnspan=4)
		self.config(padding="20 20 20 20", borderwidth=1, relief='groove')
		self.columnconfigure(0, weight=1)

		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.rowconfigure(3, weight=1)
		self.rowconfigure(4, weight=1)
		self.rowconfigure(5, weight=1)
		self.rowconfigure(6, weight=1)
		self.rowconfigure(7, weight=1)
		self.rowconfigure(8, weight=1)
		self.rowconfigure(9, weight=1)
		self.rowconfigure(10, weight=1)


		# populate
		titleLabel = TitleLabel(self, text="Gestim Mines Submit (Remote)")
		self.digital_timer = Label(self, font=('calibri', 16, 'bold'))
		closeButton = CloseButton(self)
		labelport = Label(self, text="Chrome Port:")
		spinport = ttk.Spinbox(self, from_=9001, to=9010, wrap=True, textvariable=IntVar(self, 9001), width=78, state="readonly")
		labeldate = Label(self, text="Date:")
		textdate = DateEntry(self, width= 77, date_pattern='yyy-mm-dd')
		labeltime = Label(self, text="Submit Time:")
		texttime = Entry(self, width=80)
		labelcancel = Label(self, text="Auto Cancel:")
		options1 = ["Yes", "No"]
		combocancel = ttk.Combobox(self, values=options1, state="readonly", width=78)
		combocancel.set("Yes")
		labelclose = Label(self, text="Auto Close:")
		options2 = ["Yes", "No"]
		comboclose = ttk.Combobox(self, values=options2, state="readonly", width=78)
		comboclose.set("No")
  
		labeltarget = Label(self, text="Target Time:")
		texttarget = TimeEntry(self)
		labelestime = Label(self, text="Estimate Time:")
		textestime = Text(self, width=60, height=4)
		labeltab = Label(self, text="Chrome Port:")
		spintab = ttk.Spinbox(self, from_=9001, to=9010, wrap=True, textvariable=IntVar(self, 9001), width=78, state="readonly")
		runButton = ttk.Button(self, text='Run Process', command = lambda:self.run_process(date=textdate, time=texttime, autocancel=combocancel, tab=spintab, autoclose=comboclose))
		titleLabel.grid(column = 0, row = 0, sticky = (W, E, N, S))
		estButton = ttk.Button(self, text='Estimate', command = lambda:self.estimation(target_time=texttarget, estime=textestime, submit_time=texttime))
		resButton = ttk.Button(self, text='Reset Gsheet', command = lambda:self.reset())
		chromeButton = ttk.Button(self, text='Open Chrome', command = lambda:self.chrome(port=spinport))
		separator = ttk.Separator(self, orient=HORIZONTAL)
  
		labelport.grid(column = 0, row = 1, sticky=(W))
		spinport.grid(column = 0, row = 1)
		separator.grid(column=0, row=2, columnspan=2, sticky=(E, W))
		labeldate.grid(column = 0, row = 3, sticky=(W))
		textdate.grid(column=0, row=3)
		labeltime.grid(column = 0, row = 4, sticky=(W))
		texttime.grid(column=0, row=4)
		textdate.set_date(target_time.date())
		
		runButton.grid(column = 0, row = 7, sticky = (E))
		estButton.grid(column = 0, row = 3, sticky = (E))
		resButton.grid(column = 0, row = 5, sticky = (E))
		chromeButton.grid(column = 0, row = 1, sticky = (E))
		closeButton.grid(column = 0, row = 11, sticky = (E))

		labelcancel.grid(column = 0, row = 8, sticky=(W))
		combocancel.grid(column = 0, row = 8)
		labelestime.grid(column = 0, row = 6, sticky=(W))
		textestime.grid(column=0, row=6)
		labeltarget.grid(column=0, row=5, sticky=(W))
		texttarget.grid(column=0, row=5)
		labelclose.grid(column = 0, row = 9, sticky=(W))
		comboclose.grid(column = 0, row = 9)
		labeltab.grid(column = 0, row = 7, sticky=(W))
		spintab.grid(column = 0, row = 7)
		
	def run_process(self, **kwargs):
		try:
			date.fromisoformat(kwargs['date'].get())
		except ValueError:
			raise ValueError("Incorrect date format, should be YYYY-MM-DD")
		try:
			time.fromisoformat(kwargs['time'].get())
		except ValueError:
			raise ValueError("Incorrect time format, should be HH:MM:SS.MS")

		comlist = [PYLOC_CDP, "gestim_cdp.py", "-d", kwargs['date'].get(), "-t", kwargs['time'].get(), "-ac", kwargs['autocancel'].get(), "-ae", kwargs['autoclose'].get(), "-tb", kwargs['tab'].get()]
		if os.path.exists("gestim_cdp.exe"):
			comlist = [PYLOC_CDP, "-d", kwargs['date'].get(), "-t", kwargs['time'].get(), "-ac", kwargs['autocancel'].get(), "-ae", kwargs['autoclose'].get(), "-tb", kwargs['tab'].get()]
		run_module(comlist=comlist)

	def reset(self, **kwargs):
		data = sheet.findall(os.environ.get("PCNAME"))
		for dt in data:
			sheet.delete_rows(dt.row)
		messagebox.showinfo(title='Info', message=f'Data with PCNAME {os.environ.get("PCNAME")} deleted')
  
	def estimation(self, **kwargs):
		PCNAME = os.environ.get("PCNAME")
		cell_list = sheet.findall(PCNAME)
		# breakpoint()
		kwargs['submit_time'].delete(0, 30)
		target_time_str = f"{kwargs['target_time'].hourstr.get().zfill(2)}:{kwargs['target_time'].minstr.get().zfill(2)}:{kwargs['target_time'].secstr.get().zfill(2)}.000000"
		rowlist = []
		for cell in cell_list:
			rowlist.append(sheet.row_values(cell.row))

		if len(rowlist) >= 1:
			# target_time_str = kwargs['time'].get()
			actual_request_str = rowlist[-1][3]
			actual_execution_str = rowlist[-1][5]
			target_time = datetime.strptime(target_time_str, "%H:%M:%S.%f")
			actual_request = datetime.strptime(actual_request_str, "%H:%M:%S.%f")
			actual_execution = datetime.strptime(actual_execution_str, "%H:%M:%S.%f")      
			offset = (actual_execution - actual_request).total_seconds()
			request_time = target_time - timedelta(seconds=offset)
			request_time_str = request_time.strftime("%H:%M:%S.%f")
			kwargs['estime'].delete("1.0", END)
			kwargs['estime'].insert("1.0", request_time_str+"\n")


			rowlist = rowlist[-5:]
			totaloffset = 0
			for idx, row in enumerate(rowlist):
				actual_request_str = row[3]
				actual_execution_str = row[5]
				actual_request = datetime.strptime(actual_request_str, "%H:%M:%S.%f")
				actual_execution = datetime.strptime(actual_execution_str, "%H:%M:%S.%f")      
				offset = (actual_execution - actual_request).total_seconds()
				totaloffset += offset
			avoffset = round(totaloffset/len(rowlist),6)
			target_time = datetime.strptime(target_time_str, "%H:%M:%S.%f")
			request_time = target_time - timedelta(seconds=avoffset)
			request_time_str = request_time.strftime("%H:%M:%S.%f")
			# est1_time = request_time - timedelta(seconds=avoffset)
			kwargs['estime'].insert("2.0", request_time_str + "\n" )
			messagebox.showinfo(title='Info', message=f'Estimate process Finished..')
			# kwargs['estime'].insert("3.0", est1_time.strftime("%H:%M:%S.%f") + "\n" )
		else:
			# target_time_str = kwargs['time'].get()
			target_time = datetime.strptime(target_time_str, "%H:%M:%S.%f")
			request_time = target_time - timedelta(seconds=0.5)
			kwargs['estime'].delete("1.0", END)
			kwargs['estime'].insert("1.0", request_time.strftime("%H:%M:%S.%f") + "\n")

	def chrome(self, **kwargs):
		user_data = f"{os.getcwd()}\\{kwargs['port'].get()}"
		comlist = [os.environ.get("CHROME_PATH"), f"--remote-debugging-port={kwargs["port"].get()}", f"--user-data-dir={user_data}", "https://gestim.mines.gouv.qc.ca/MRN_GestimP_Presentation/ODM02101_login.aspx"]
		Popen(comlist, creationflags=CREATE_NEW_CONSOLE)	
 
class CloseButton(ttk.Button):
	def __init__(self, parent):
		super().__init__(parent)
		self.config(text = '< Back', command=lambda : parent.destroy())

class TimeEntry(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        target_timezone = timezone('America/New_York')
        utc_now = datetime.now(utc)
        target_time = utc_now.astimezone(target_timezone)
        
        self.hourstr = StringVar(self, str(target_time.hour))
        self.hour = ttk.Spinbox(self, from_=0, to=23, wrap=True,
                               textvariable=self.hourstr, width=24, state="readonly")
        self.minstr = StringVar(self, str(target_time.minute))
        self.min = ttk.Spinbox(self, from_=0, to=59, wrap=True,
                              textvariable=self.minstr, width=24, state="readonly")
        self.secstr = StringVar(self, '00')							  
        self.sec = ttk.Spinbox(self, from_=0, to=59, wrap=True,
                              textvariable=self.secstr, width=24, state="readonly")
        
        self.hour.grid(row=0, column=0)
        self.min.grid(row=0, column=1)
        self.sec.grid(row=0, column=2)

    
if __name__ == "__main__":
	
	if platform == "linux" or platform == "linux2":
		PYLOC = "python"
		PYLOC_CDP = "python"
	elif platform == "win32":
		PYLOC = os.environ.get("PYLOC")
		PYLOC_CDP = os.environ.get("PYLOC_CDP")

	main()