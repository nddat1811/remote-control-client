import tkinter as tk
import gmail as g
BUFSIZE = 1024 * 4

def mac_address():
    while True:
        letter = g.read_mail()
        if letter != "no":
            tmp = letter.split(":")
            cmd = tmp[0]
            if cmd == "MAC":
                res = tmp[1]
                res = res[2:]
                res = res.upper()
                res = ':'.join(res[i:i + 2] for i in range(0, len(res), 2))
                print("join:", res)
                tk.messagebox.showinfo(title='MAC Address', message=res)
                return