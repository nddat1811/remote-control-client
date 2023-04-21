import tkinter as tk
import gmail as g
BUFSIZE = 1024 * 4

def mac_address():
    letter = g.read_mail()
    res = letter.split(":")[1]
    res = res[2:].upper()
    res = ':'.join(res[i:i + 2] for i in range(0, len(res), 2))
    
    tk.messagebox.showinfo(title='MAC Address', message=res)