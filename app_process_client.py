import tkinter as tk
from tkinter import  ttk
import pickle, struct
from tkinter import Canvas, Button, PhotoImage
import gmail as g
BUFSIZE = 1024 * 4
import os
import sys
def abs_path(file_name):
    file_name = 'assets\\' + file_name
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, file_name)

def switch(btn, tab):
    if btn['text'] == 'PROCESS':
        btn.configure(text = 'APPLICATION')
        tab.heading("Name", text = "Name Process")
        tab.heading("ID", text = "ID Process")
        tab.heading("Count", text = "Count Threads")
    else:
        btn.configure(text = 'PROCESS')
        tab.heading("Name", text = "Name Application")
        tab.heading("ID", text = "ID Application")
        tab.heading("Count", text = "Count Threads")
    return

def send_kill():
    global pid
    g.send_mail("KILL:"+str(pid.get()))
    while True:
        letter = g.read_mail()
        if "SUCCESS" in letter:
            tk.messagebox.showinfo(message = "Đã diệt!")
            kill.destroy()
            break
        elif "UN" in letter:
            tk.messagebox.showerror(message = "Lỗi!")
            return

def _list(tab, s):
    g.send_mail(s)
    count = 0
    while True:
        letter = g.read_mail()
        if letter != "no":
            cmd, data = g.split_messages(letter)
            if cmd == "ls1":
                ls1 = eval(data)
                count += 1
            elif cmd == "ls2":
                ls2 = eval(data)
                count += 1
            elif cmd == "ls3":
                ls3 = eval(data)
                count += 1
            if count == 3:
                break
    for i in tab.get_children():
        tab.delete(i)
    for i in range(len(ls1)):
        tab.insert(parent = '', index = 'end', text = '', values = (ls1[i], ls2[i], ls3[i]))
    return

def clear(tab):
    for i in tab.get_children():
        tab.delete(i)
    return

def send_start():
    global pname
    g.send_mail("START:" + str(pname.get()))
    while True:
        letter = g.read_mail()
        if "UN" in letter:
            tk.messagebox.showerror(message = "Lỗi!")
            return
        elif "SUCCESS" in letter:
            return        
def start(root):
    global pname
    pstart = tk.Toplevel(root)
    pstart['bg'] = '#adeff2'
    pstart.geometry("410x40")
    pname = tk.StringVar(pstart)
    tk.Entry(pstart, textvariable = pname, width = 38, borderwidth = 5).grid(row = 0, column = 0)
    tk.Button(pstart, text = "Start", width = 14, height = 1, fg = 'white', bg = '#ad4b50', borderwidth=0,
            highlightthickness=0, command = lambda: send_start(), relief="flat").grid(row = 0, column = 1)
    return
    
def kill(root):
    global pid
    kill = tk.Toplevel(root)
    kill['bg'] = '#adeff2'
    kill.geometry("410x40")
    pid = tk.StringVar(kill)
    tk.Entry(kill, textvariable = pid, width = 38, borderwidth = 5).grid(row = 0, column = 0)
    tk.Button(kill, text = "Kill", width = 14, height = 1, fg = 'white', bg = '#ad4b50', borderwidth=0,
            highlightthickness=0, command = lambda: send_kill(), relief="flat").grid(row = 0, column = 1)
    return
        
class App_Process_UI(Canvas):
     def __init__(self, parent):    
        Canvas.__init__(self, parent)
        self.configure(
            #window,
            bg = "#adeff2",
            height = 600,
            width = 1000,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.place(x = 0, y = 0)
        self.image_image_1 = PhotoImage(
            file=abs_path("bg.png"))
        self.image_1 = self.create_image(
            519.0,
            327.0,
            image=self.image_image_1
        )

        self.tab = ttk.Treeview(self, height = 18, selectmode='browse')
        self.scroll = tk.Scrollbar(self, orient = "vertical", command = self.tab.yview)
        self.scroll.place(x=766.0,
            y=162.0,
            height=404.0
            )
        self.tab.configure(yscrollcommand = self.scroll.set)
        self.tab['columns'] = ("Name", "ID", "Count")
        self.tab.column('#0', width=0)
        self.tab.column("Name", anchor="center", width = 150, minwidth = 10, stretch = True)
        self.tab.column("ID", anchor="center", width = 150, minwidth = 10, stretch = True)
        self.tab.column("Count", anchor="center", width = 150, minwidth = 10, stretch = True)
        self.tab.heading('#0', text='')
        self.tab.heading("Name", text = "Name Application")
        self.tab.heading("ID", text = "ID Application")
        self.tab.heading("Count", text = "Count Threads")
        self.tab.place(x=53.0,
            y=162.0,
            width=713.0,
            height=404.0
            )
        self.button_1 = Button(self, text = 'PROCESS', width = 20, height = 5, fg = 'white', bg = '#ad4b50',
            # image=button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: switch(self.button_1, self.tab),
            relief="flat"
        )
        self.button_1.place(
            x=838.0,
            y=66.0,
            width=135.0,
            height=53.0
        )
        self.button_2 = Button(self, text = 'KILL', width = 20, height = 5, fg = 'white', bg = '#ad4b50',
            #image=button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: kill(parent),
            relief="flat"
        )
        self.button_2.place(
            x=838.0,
            y=152.0,
            width=135.0,
            height=53.0
        )
        self.button_3 = Button(self, text = 'LIST', width = 20, height = 5, fg = 'white', bg = '#ad4b50',
            #image=button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: _list(self.tab, self.button_1['text']),
            relief="flat"
        )
        self.button_3.place(
            x=838.0,
            y=238.0,
            width=135.0,
            height=53.0
        )
        self.button_4 = Button(self, text = 'CLEAR', width = 20, height = 5, fg = 'white', bg = '#ad4b50',
            #image=button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: clear(self.tab),
            relief="flat"
        )
        self.button_4.place(
            x=838.0,
            y=317.0,
            width=135.0,
            height=53.0
        )
        self.button_5 = Button(self, text = 'START', width = 20, height = 5, fg = 'white', bg = '#ad4b50',
            #image=button_image_5,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: start(parent),
            relief="flat"
        )
        self.button_5.place(
            x=839.0,
            y=396.0,
            width=135.0,
            height=53.0
        )
        self.button_6 = Button(self, text = 'BACK', width = 20, height = 5, fg = 'white', bg = '#ad4b50',
            #image=button_image_6,
            borderwidth=0,
            highlightthickness=0,
            #command=lambda: back(),
            relief="flat"
        )
        self.button_6.place(
            x=838.0,
            y=473.0,
            width=135.0,
            height=53.0
        )