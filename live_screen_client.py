# Socket
import os
import shutil
import socket

# Thread
from threading import Thread

# Image
from PIL import Image, ImageTk
import io

# Tkinter
import tkinter as tk
from tkinter import Canvas
from tkinter.filedialog import asksaveasfilename
import gmail as g



BUFSIZE = 1024 * 4

class Desktop_UI(Canvas):
    def __init__(self, parent, ):    
        Canvas.__init__(self, parent)
        self.configure(
            #window,
            bg = "#FCD0E8",
            height = 600,
            width = 1000,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        self.place(x = 0, y = 0)

        # initialize status to ready receiving data
        self.status = True

        # initialize the sentinel of saving image command
        self.on_save = False

        # label to display frames received from server
        self.label = tk.Label(self)
        self.label.place(x=20,y=0,width=960,height=540)

        # a button to save captured screen
        self.btn_save = tk.Button(self, text = 'Save', command=lambda: self.click_save(), relief="flat")
        self.btn_save.place(x=320,y=560,width=50,height=30)        
        
        # a button to stop receiving and return to main interface
        self.btn_back = tk.Button(self, text = 'Back', command=lambda: self.click_back(), relief="flat")
        self.btn_back.place(x=630,y=560,width=50,height=30)  

        # thread
        self.start = Thread(target=self.ChangeImage, daemon=True)
        self.start.start()
    
    # display frames continously
    def ChangeImage(self):
        while self.status:  
            letter = g.get_mail_with_attachment("no")
            if letter is not None and "LIVESCREEN" in letter:
                path = os.path.join(os.path.dirname(__file__), "livescreen", "livescreen.png")
                img_PIL = Image.open(path).resize((960, 540), Image.ANTIALIAS)
                img_tk = ImageTk.PhotoImage(img_PIL)
                self.label.configure(image=img_tk)
                self.label.image = img_tk

            # check save image command
            # while saving image, server will delay capturing and wait for the next command from client
            if self.on_save:
                self.save_img()
                self.on_save = False

            # check stop command
            if self.status != True:
                g.send_mail("LIVSCREEN:STOP_RECEIVING")
        # Return the main UI
        self.place_forget()

    def click_back(self):
        self.status = False

    def click_save(self):
        self.on_save = True

    def save_img(self):
        source_path = os.path.join(os.path.dirname(__file__), "livescreen", "livescreen.png")
        destination_path = asksaveasfilename(defaultextension=".png")
        if destination_path == "":
            return
        shutil.copyfile(source_path, destination_path)



