import tkinter as tk

class App(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.hourstr = tk.StringVar(self, '10')
        self.hour = tk.Spinbox(self, from_=0, to=23, wrap=True,
                               textvariable=self.hourstr, width=2, state="readonly")
        self.minstr = tk.StringVar(self, '30')
        self.min = tk.Spinbox(self, from_=0, to=59, wrap=True,
                              textvariable=self.minstr, width=2, state="readonly")
        
        self.hour.grid(row=0, column=0)
        self.min.grid(row=0, column=1)
        
        # Example of how to retrieve the time
        self.submit_btn = tk.Button(self, text="Get Value", 
                                    command=lambda: print(f"Time selected: {self.hourstr.get()}:{self.minstr.get()}"))
        self.submit_btn.grid(row=1, columnspan=2)

root = tk.Tk()
App(root).pack()
root.mainloop()
